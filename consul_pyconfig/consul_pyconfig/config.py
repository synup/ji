import requests
import os
import logging
import sys
import json
import base64

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def get_consul_svc(svc_endpoint, request_params, service):
    """
    Since consul does not have concept of prefix for service, so we are using tags for this purpose.
    """
    consul_data = requests.get(svc_endpoint, params=request_params)
    body = json.loads(consul_data.text)
    return {
        "address": body[0]["Service"]["Address"],
        "port": body[0]["Service"]["Port"]
    }

def key_missing_error(key_endpoint, status_code):
    log_msg = "Unable to get key endpoint: '{}' having status_code: '{}'".format(
        key_endpoint,
        status_code
    )
    logger.error(log_msg)

def get_consul_kv(key_endpoint, params=None):
    data = {}
    r = requests.get(key_endpoint, params=params)
    if not r.ok:
        key_missing_error(key_endpoint, r.status_code)
        return None
    body = json.loads(r.text)
    for val in body:
        if val.get("Value"):
            data[val["Key"]] = base64.b64decode(val["Value"]).decode()
    return data

def del_consul_kv(key_endpoint, params=None):
    r = requests.delete(key_endpoint, params=params)
    if r.text.strip() != "true":
        logger.error("unable to delete key endpoint: '{}' having status_code: '{}'".format(
            key_endpoint, r.status_code))
    logger.info("successfully deleted key endpoint: '{}' with params: '{}'".format(
        key_endpoint, params))

def put_consul_kv(key_endpoint, key, value):
    if type(key_endpoint) != str or type(key) != str or type(value) != str:
        logger.error("send string type only in {}".format(__class__))
    r = requests.put(key_endpoint, value)
    if r.text.strip() != "true":
        logger.error("unable to put key endpoint: '{}' having status_code: '{}'".format(
            key_endpoint, r.status_code))
    logger.info("successfully put key endpoint: '{}'".format(key_endpoint))

class Config:
    """
    Wrapper on top of consul api to facilitates configuration for Application.
    Get Consul Server hostname and port from the environment variable `CONSUL_HOSTNAME` and `CONSUL_PORT`
    Puts all application configuration on Consul. Allow overwriting of any configuration with the environment variable.
    Priority of configuration will be:
        1: Environment Variable
        2: Consul key’s value
    Key Naming:
        - Use underscores to separate words inside the key name.
        - Use lower case letters.
        -  Key name for environment variable must be capitalised.
    So if key name is `redis_hostname` on the application then corresponding
    consul key name will be `component/environment/URL/redis_hostname` (like `example-app/production/v2.pyconfig.com/redis_hostname`)
    Environment variable name will be `REDIS_HOSTNAME`.
    """

    def __init__(self, consulhost=None, consulport=None, keyprefix=None, component=None, env=None, prefix=None):
        self.consul_host = consulhost or os.environ.get(
            'CONSUL_HOSTNAME') or 'localhost'
        self.consul_port = int(
            consulport or os.environ.get('CONSUL_PORT') or '8500')
        self.app = component or os.environ.get('COMPONENT_NAME') or 'DUMMY'
        self.env = env or os.environ.get('APP_ENV') or 'development'
        self.prefix = prefix or os.environ.get('COMPONENT_PREFIX') or 'dev'
        self.keyprefix = keyprefix or '{}/{}/{}'.format(
            self.app, self.env, self.prefix)
        self.consul_url = "http://{}:{}".format(
            self.consul_host, self.consul_port)
        self.consul_kv_endpoint = "{}/v1/kv".format(self.consul_url)
        self.consul_svc_endpoint = "{}/v1/health/service".format(
            self.consul_url)
        logger.info("consul url is '{}'".format(self.consul_url))
        logger.info("keyprefix is '{}'".format(self.keyprefix))

    def put(self, key, value):
        """
        It will write to Consul with prefix/key key name.
        `keyprefix`, `key`, `value` are string data-type.
        example:
        Config.keyprefix = "app/staging/main"
        Config.put(key", "value")
        """
        key_endpoint = "{}/{}/{}".format(self.consul_kv_endpoint,
                                         self.keyprefix, key)
        put_consul_kv(key_endpoint, key, value)

    def reset(self, data):
        """
        It will delete existing prefix namespace on consul, if already present and will create mentioned key-value pairs on Consul.
        `data` is dictionary data-type with string data-type as key and value.
        `keyprefix` is string data-type.
        example:
        Config.keyprefix = "app/staging/main"
        d = { "key1": "value1", "key2": "value2" }
        Config.reset(d)
        """
        key_endpoint = "{}/{}".format(self.consul_kv_endpoint, self.keyprefix)
        del_consul_kv(key_endpoint, params={"recurse": True})
        for k, v in data.items():
            self.put(k, v)

    def get(self, key):
        """
        It will read from Consul and environment variable then return the value of higher priority.
        `keyprefix`, `key` are string data-type. return data-type is dictionary.
        example:
        Config.keyprefix = "app/staging/main"
        Config.get("key")
        """
        env_key = key.upper()
        if env_key in os.environ:
            try:
                value = json.loads(os.environ[env_key])
            except ValueError:
                value = os.environ[env_key]
            return value
        key_endpoint = "{}/{}/{}".format(self.consul_kv_endpoint,
                                         self.keyprefix, key)
        consul_data = get_consul_kv(key_endpoint)
        if consul_data:
            return json.loads(consul_data["{}/{}".format(self.keyprefix, key)])
        logger.error("Invalid prefix -> {} or Invalid key -> {}".format(
            self.keyprefix, key))
        return None

    def get_multi(self, keyprefix):
        """
        It will read from Consul and returns a dictionary.
        `keyprefix` are string data-type. return data-type is dictionary.
        example:
        Config.get_multi("jwt_keys")
        """
        key_endpoint = "{}/{}".format(self.consul_kv_endpoint,
                                      keyprefix)
        consul_data = get_consul_kv(key_endpoint, {"recurse": True})
        data = {}
        if consul_data:
            for k, v in consul_data.items():
                data[k.split('/')[-1]] = json.loads(v)
            return data
        return {
            "Invalid prefix -> {}".format(
                self.keyprefix)
        }

    def get_all(self):
        """
        It will read from Consul and environment variable then return the dictionary containing all with below format:
            {
                environment: {'key': 'value', ... },
                consul: {'key': 'value', ... }
            }
        `keyprefix` is string data-type and return data-type is dictionary.
        example:
        Config.keyprefix = "app/staging/main"
        Config.get_all()
        """
        data = {'environment': {}, 'consul': {}}
        for k, v in os.environ.items():
            if k.startswith("pyconfig_"):
                data['environment'][k] = v
        key_endpoint = "{}/{}".format(self.consul_kv_endpoint, self.keyprefix)
        consul_data = get_consul_kv(key_endpoint, params={"recurse": True})
        if consul_data:
            for k, v in consul_data.items():
                data['consul'][k] = v
        return data

    def delete(self, key):
        """
        It will delete `key` from Consul.
        `keyprefix`, `key` are string data-type.
        example:
        Config.keyprefix = "app/staging/main"
        Config.delete("key")
        """
        key_endpoint = "{}/{}/{}".format(self.consul_kv_endpoint, self.keyprefix, key)
        del_consul_kv(key_endpoint)

    def delete_all(self):
        """
        It will delete `prefix` from Consul.
        `prefix` is string data-type.
        example:
        Config.keyprefix = "app/staging/main"
        Config.delete_all()
        """
        key_endpoint = "{}/{}".format(self.consul_kv_endpoint, self.keyprefix)
        del_consul_kv(key_endpoint, params={"recurse": True})

    def get_service(self, service):
        """
        It will get service from Consul using HTTP API request.
        This will be used for geting services like RabbitMQ, Redis, Kafka, ElasticSearch hostname.
        So basically anything that needs status-checking/load-balancing, can be used through this.
        `keyprefix` and `service` are string data-type. return type will be dictionary data-type.
        example:
        Config.keyprefix = "app/staging/main"
        Config.get_service("rmq-stg-internal")
        """
        svc_endpoint = "{}/{}".format(self.consul_svc_endpoint, service)
        request_params = {"tag": self.keyprefix, "passing": True}
        return get_consul_svc(svc_endpoint, request_params, service)
