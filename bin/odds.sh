#!/bin/bash

bin_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
root_dir=${bin_dir}/..

. ${root_dir}/ve/bin/activate && PYTHONPATH=. ${root_dir}/dice/odds.py "$@"
