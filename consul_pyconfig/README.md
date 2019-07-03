## `consul_pyconfig` Module:

Wrapper on top of consul api to facilitates configuration for Application.

Get Consul Server hostname and port from the environment variable `CONSUL_HOSTNAME` and `CONSUL_PORT` but can be overwritten with class `Config` attributes.

We decided to use following directory for a service configuration home:
```
/SERVICE_NAME/ENVIRONMENT/SOME_RANDOM_STRING
```
like:
```
/app/production/main
```

Puts all application configuration on Consul. Allow overwriting of any configuration with the environment variable.
Priority of configuration will be:
```
1: Environment Variable
2: Consul key’s value
```

Key Naming:
```
Use underscores to separate words inside the key name.
     - Use lower case letters.
     - Key name for environment variable must be capitalised.
```

So if key name is `redis_hostname` on the application then corresponding
consul key name will be `service/environment/RANDOM_STRING/redis_hostname` (like `v2app/production/v2.pyconfig.com/redis_hostname`)
Environment variable name will be `REDIS_HOSTNAME`.

## Using it

It Can be used as pip package.

```sh
# you can use it directory from github
pip install 'git+https://github.com/rahulwa/ji#subdirectory=consul_pyconfig'
# Or copy/clone this repo and install using directory path
pip install -e PATH_TO_/consul_pyconfig
```

## Allowed methods:
 
### get(key)
```
It will read from Consul and environment variable then return the value of higher priority.
`keyprefix`, `key` are string data-type. return data-type is dictionary or string depending on whether value is json encoded.
example:
Config.keyprefix = "app/staging/main"
Config.get("key")
```
 
### get_multi(keyprefix)
```
It reads all keys from Consul recursively and returns a dictionary with flattening of directories so beware if it overwrites same key name.
`keyprefix` are string data-type. return data-type is dictionary.
example:
Config.get_multi("jwt_keys")
Config.get_multi()
```
 
### get_all()
```
It will read from Consul and environment variable then return the dictionary containing all with below format:
        {
        environment: {'key': 'value', ... },
        consul: {'key': 'value', ... }
        }
`keyprefix` is string data-type and return data-type is dictionary.
example:
Config.keyprefix = "app/staging/main"
Config.get_all()
```
 
### put(key, value)
```
It will write to Consul with prefix/key key name.
`keyprefix`, `key`, `value` string data-type.
`value` is going to json encoded so most of data structures are supported.
example:
Config.keyprefix = "app/staging/main"
Config.put(key", "value")
```
 
### delete(key)
 ```
It will delete `key` from Consul.
`keyprefix`, `key` are string data-type.
example:
Config.keyprefix = "app/staging/main"
Config.delete("key")
```
 
### delete_all()
```
It will delete `prefix` from Consul.
`prefix` is string data-type.
example:
Config.keyprefix = "app/staging/main"
Config.delete_all()
```
 
### get_service(service)
```
It will get service from Consul using HTTP API request.
This will be used for geting services like RabbitMQ, Redis, Kafka, ElasticSearch hostname.
So basically anything that needs status-checking/load-balancing, can be used through this.
`keyprefix` and `service` are string data-type. return type will be dictionary data-type.
example:
Config.keyprefix = "app/staging/main"
Config.get_service("rmq-stg-internal")
```
 
### reset(data)
```
It will delete existing prefix namespace on consul, if already present and will create mentioned key-value pairs on Consul.
`data` is dictionary data-type with string data-type as key and value.
`keyprefix` is string data-type.
example:
Config.keyprefix = "app/staging/main"
d = { "key1": "value1", "key2": "value2" }
Config.reset(d)
```
 
### get_service(service)
```
It will get service from Consul using HTTP API request.
This will be used for geting services like RabbitMQ, Redis, Kafka, ElasticSearch hostname.
So basically anything that needs status-checking/load-balancing, can be used through this.
`keyprefix` and `service` are string data-type. return type will be dictionary data-type.
example:
Config.keyprefix = "app/staging/main"
Config.get_service("rmq-stg-internal")
```