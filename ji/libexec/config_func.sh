#!/usr/bin/env bash

# Trapping ctrl+c and immediatly exiting
trap ctrl_c INT
ctrl_c() {
    echo "$(echored '*** Exiting, Recieved CTRL+C ***')"
    exit 1
}


slacking() {
    if [[ ! -z "$SLACK_WEBHOOK_URL" ]]; then
        slacking="$1"
    else
        slacking=false
    fi
}

# Reading from file $1 and returns an array containing uncommented component names with validating from defined components list
gather_name_of_components_from_file() {
    local all_components_file=$1
    if [ ! -e $all_components_file ]; then
        echo "$(echopurple $(basename $all_components_file)) $(echored 'file does not exist')"
        exit 1
    else
        readarray sanitized <<< $(tr -d ' \t\r\f' <$all_components_file)
        readarray common <<< $(comm -12 <(printf '%s\n' "${sanitized[@]}" | LC_ALL=C sort) <(printf '%s\n' "${components[@]}" | LC_ALL=C sort))
        for i in "${common[@]}"; do
            defined_output_array+=($i)
        done
        echo "${defined_output_array[@]}"
    fi
}

validate_components_name() {
    local input_component_name=$1
    if [[ ! " ${components[@]} " =~ " $input_component_name " ]]; then
        echo "$(echopurple $input_component_name) $(echored 'input is not a valid component name')"
        exit 1
    fi
}

# Converting comma separated string containing components names $1 to a array $2 with validating from defined components list
comma_separated_component_names_to_array() {
    local comma_separated_component_names=$1
    local defined_output_array=$2
    for i in $(echo $"$comma_separated_component_names" | sed "s/,/ /g"); do
        validate_components_name $i
        defined_output_array+=($i)
    done
}
