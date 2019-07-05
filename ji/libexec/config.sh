#!/usr/bin/env bash

# list of components defined in this file to be used as source for all (`ji __ all`) arguement
all_components_file="$_JI_ROOT/../.ji-all-components"
component_path="$_JI_ROOT/.."

# Declaring all component names so that they can be used for validating input
declare -a components=(example-app react-example-app)

# kubectl contexts to be used for local and remote
local_context=docker-for-desktop
remote_context=aws

# if provided, it will enable posting to slack on configured channel for ji events
# like SLACK_WEBHOOK_URL='https://hooks.slack.com/services/XXXX/XXX/XXX'
SLACK_WEBHOOK_URL=''

declare -a entered_components=()
current_context=$(kubectl config current-context)

# bringing functions into scope
source config_func.sh

# Parsing the arguements and passing config values to subsequent sub-command (almost all subcommand imports this file).
# Note that very first arguement is subcommand is it getting taken care by https://github.com/basecamp/sub and ji bootstraped from this library.
# Basic idea of arguments is that
#   first one select the environment (like prod/staging/dev)
#   second one select which project (the project folder in this monorepo)
#   and third one select the prefix where this command going to operate on.
#       prefix is a random string that allows to have multiple instances of same project and environment running simultaneously.

# Using first argument and making condition using it
# This is used for selecting environment
case "$1" in
    "local" )
        use_context=$local_context
        use_namespace=default
        slacking "false"
        deploy_command_string=""
        ;;
    "staging")
        use_context=$remote_context
        use_namespace=staging
        slacking "true"
        deploy_command_string="-staging"
        ;;
    "production")
        if [[ $PRODUCTION_SUPPORT == true ]]; then
            use_context=$remote_context
            use_namespace=production
            ALL_SUPPORTfalse
            MULTI_INPUT=false
            slacking "true"
            prod_slacking=true
            deploy_command_string="-production"
        else
            echo "$(echopurple $1) $(echored 'is not supported for this command')"
            exit 1
        fi
        ;;
    * )
        echo "$(echopurple $1) $(echored 'input is not a valid environment')"
        echo "Running $(echogreen 'ji help '"$ACTION"'')"
        ji help $ACTION
        exit 1
        ;;
esac

# Using second argument
# This is used for selecting components
case "$2" in
    "all" )
        # Reading from file $all_components_file and appending uncommented component names to a array (entered_components),
        # so that ji command can be run for all components in that file
        if [[ $ALL_SUPPORT == true ]]; then
            entered_components=($(gather_name_of_components_from_file ${all_components_file}))
        else
            echo "$(echopurple all) $(echored 'is not supported here')"
            exit 1
        fi
        ;;
    * )
    # supporting multiple components name at a time using comma separated input
        if echo $2 | grep ',' 2>&1 > /dev/null; then
            if [[ $MULTI_INPUT == true ]]; then
                comma_separated_component_names_to_array $2 entered_components
            else
                echo "$(echopurple ,) $(echored 'is not supported here')"
                exit 1
            fi
        else
            validate_components_name $2
            # `$2` can be used safely here
            entered_components+=($2)
        fi
        ;;
esac

# Using third argument
# Component Prefix
case "$3" in
    "" )
        echo "$(echored 'Also pass COMPONENT_PREFIX as arguement')"
        exit 1
        ;;
    * )
        component_prefix=$3
        ;;
esac
