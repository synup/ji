# ji

A simple bash script to make life easier for managing services on Kubernetes. It contain commands for doing basic tasks like for doing deployment, checking logs, restarting the services etc.

This project is organised using [sub](https://github.com/basecamp/sub). For main config and starting point look at [config.sh](./libexec/config.sh) and then specific scripts for each subcommands in [libexec folder](./libexec/).

General command structure looks like: `ji <action> <environment> <services> <prefix_string>`.


### Configure Deployement Setup on Local

Run command to setup: `./ji/libexec/ji-setup`

## Start/Stop/Deploy/Manage the components

Follow these commands for deployment and other tasks:

```
# prints help
ji help [up/down/restart/reload/logs/log/attach/info/port]

# prints all commands
ji commands

# Deploys to local/remote Kubernetes Cluster
ji up <local/staging/production> <all/component1,component2> <component-prefix>

# Uninstalls componenets from local/remote Kubernetes Clusters
ji down <local/staging> <all/component1,component2> <component-prefix>

# Display info about deployed components on local/remote Kubernetes cluster
ji info <local/staging/production> <all/component1,component2> <component-prefix>

# Restart components on local/remote Kubernetes Cluster (killing the pods without making new one up)
ji restart <local/staging/production> <all/component1,component2> <component-prefix>

# Soft Reload components on local/remote Kubernetes Cluster (making up new pod then killing the old ones)
ji reload <local/staging/production> <all/component1,component2> <component-prefix>

# Tail the logs for deployed components on local/remote Kubernetes cluster
ji logs <local/staging/production> <all/component1,component2> <component-prefix>

# Tail logs of a deployed component's pod on local/remote Kubernetes cluster
ji log <local/staging/production> <component> <component-prefix>

# Attaches to Container's bash terminal
ji attach <local/staging/production> <component> <component-prefix>

# Forward a local port to a Kubernetes Service
ji port <SEARCH_TERM>
```

#### Required configuration
Look into [config.sh](./libexec/config.sh) and fill/correct needed values. If you want to add support for configuration of accessing remote kubernetes cluster on new client machine using [ji-setup](./libexec/setup), please add a function for it in same (example is provided for aws EKS cluster, `setup_kubeconfig_for_remote_cluster` function).

### How it does?

General command looks like:
```
ji <action> <environment> <services> <prefix_string>
```
where *action* can be up/down/log/logs/restart/reload, *enviornment* can be production/staging/local and *prefix_string* can be any string.
Now let’s talk about what basic tasks it supports and how.
```sh
ji up staging foo main
```
which is going to deploy `foo` service on staging with a (helm package) name `main-foo` and *prefix_string* easily allows us to deploy second instance of same application on staging as `ji up staging foo other`. `ji up` is for deploying the application. It `cd` into service’s charts directory (it knows the path of it because of monorepo) and runs `skaffold-<environments>.yaml` file with some validation and exports `COMPONENT_PREFIX` with value of `<prefix_string>` needed by helm chart to decide which key-value folder on Consul to connect to get config for this service. So [config directory on Consul](../consul_pyconfig/README.md#consul_pyconfig-module) `/SERVICE_NAME/ENVIRONMENT/<SOME_RANDOM_STRING>`'s `SOME_RANDOM_STRING` becomes `prefix_string` on ji deployment. For more info look into [ji-up](./libexec/ji-up).
```sh
ji attach staging foo main
```
attaches to container's terminal running though dialog selection for `main-foo` application. For more info look into [ji-attach](./libexec/ji-attach).
```sh
ji logs staging foo main
```
tails the logs of all pods for all k8s deployments with `main-foo` name prefix. For more info look into [ji-logs](./libexec/ji-logs).
```sh
ji log staging foo main
```
tails the logs of all pods for a particular k8s deployment through a selection menu for `main-foo` name prefix. For more info look into [ji-log](./libexec/ji-log).
```sh
ji restart staging foo main
```
is going to kill all pods with name prefix `main-foo` and Kubernetes will spawn new ones in-place of these, like restart. It’s hard restart. For more info look into [ji-restart](./libexec/ji-restart).
```sh
ji reload staging foo main
```
is going to update all k8s deployment objects with a random environment variable and it will trigger rolling deployment of existing deployment. It’s a soft restart in the sense that application will not be down at any particular point of time. For more info look into [ji-reload](./libexec/ji-reload).
```sh
ji info staging foo main
```
will print the current status of deployed foo application with main prefix (`main-foo` helm chart). For more info look into [ji-info](./libexec/ji-info).
```sh
ji down staging foo main
```
will uninstall `main-foo` application. For more info look into [ji-down](./libexec/ji-down).

---
Big Thanks for below projects:
- [sub](https://github.com/basecamp/sub) for a delicious way to organize it
- [kubetail](https://github.com/johanhaleby/kubetail/) for kubectl logs enhancement using bash

