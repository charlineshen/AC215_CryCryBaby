#!/bin/bash

echo "Model2 Container is running!"

args="$@"
echo $args

if [[ -z ${args} ]]; 
then
    echo "Starting shell"
    pipenv shell
else
    echo "Running python script"
    pipenv run python $args
fi