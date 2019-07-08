# ji

This is an example monorepo consisting of tools named
- **ji** written in bash to deploy/manage application on kubernetes cluster (look in [ji folder](./ji)) and
- **consul_pyconfig** written in python to allow python application to manange config using Consul key-value pairs (look in [consul_pyconfig folder](./consul_pyconfig))

And example applications in python (`example-app`) and javascript (`react-example-app`) to show how to integrate with these tools.

[![asciicast](https://asciinema.org/a/255857.svg)](https://asciinema.org/a/255857)

## Local Setup
Run command to setup: `./ji/libexec/ji-setup`
#### Then enable kubernetes cluster on docker:
```
Open Docker menu
-> Preferences
```
Enable Kubernetes on Docker's preferences menu.
```
Preferences
-> Kubernetes tab
-> Enable Kubernetes
-> Click "Apply"
```
Wait for it to start and then install helm tiller in this cluster
```sh
# verify that kubernetes cluster is ready
kubectl get pods -n kube-system
# Install tiller
helm init
```

### Trying Out

- deploying
```sh
# first start consul and make sure that it is accessible at default port 8500
# for example-app
# first generate database
export CONDUIT_SECRET='something-really-secret' \
  FLASK_DEBUG=1 \
  FLASK_APP=app-pyconfig.py
flask db init
flask db migrate
flask db upgrade
# then deploy it, it will use same above generated dev.db as mounting of codebase has been done while deploying to local kubernetes cluster
ji up local react-example-app dev
# for react-example-app
ji up local example-app dev

# OR both ji up command can be combined as (here application name is passed from .ji-all-component file's content)
ji up local all dev
# OR both ji up command can be combined as (here application name passed as comma separated)
ji up local react-example-app,example-app dev
```
- checking status
```sh
ji info local react-example-app dev
ji info local example-app dev
# OR combined into one
ji info local all dev
ji info local react-example-app,example-app dev
```
- try out by connecting to shown url
- tailing logs
```sh
ji logs local react-example-app dev
ji logs local example-app dev --since 1h
```
- restarting/reload
```sh
ji restart local react-example-app,example-app dev
ji reload local example-app,react-example-app dev
```
- connecting to bash terminal inside application container
```sh
ji attach local react-example-app dev
ji attach local example-app dev
```
- delete deployed application
```sh
ji down local example-app,react-example-app dev
# OR combined into one
ji down local all dev
```
- etc.
