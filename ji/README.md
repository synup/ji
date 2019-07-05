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

---
Big Thanks for below projects:
- [sub](https://github.com/basecamp/sub) for a delicious way to organize it
- [kubetail](https://github.com/johanhaleby/kubetail/) for kubectl logs enhancement using bash

