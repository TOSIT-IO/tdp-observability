#!/bin/bash
hooks_dir=$(git rev-parse --git-dir)/hooks
pre_push_file=$(dirname $0)/pre-push

function read_yn {
    while true; do
        read -p "$1 " yn
        case $yn in
            [YyOo]* ) echo "Y"; break;;
            [Nn]* ) echo "N"; break;;
            * ) echo "Please answer yes or no.";;
        esac
    done
}
if [[ ! -d $hooks_dir ]]; then
    echo "ERROR: Can't find hooks dir !!"
    exit 1
fi

if [[ "$1" == "--uninstall"  || "$1" == "-u" ]]; then
    if [ -f "$hooks_dir/pre-push" ]; then
        if [ $(read_yn 'Uninstall pre-push hook. Are you sure ? ') == 'N' ]; then
            exit 0 
	else
	    rm $hooks_dir/pre-push
	fi
    else
        echo "Can't find pre-push file in hooks dir : Nothing to do"
    fi
elif [[ "$1" == "--help" || "$1" == "-h" ]]; then
    echo "$(basename $0) :"
    echo "Installs or uninstall git pre-push hook"
    echo "Options : "
    echo "  -u, --unsinstall : uninstall hook"
    echo "  -h, --help       : display this help message"
    echo
else
    if [ -f "$hooks_dir/pre-push" ]; then
        echo "pre-push already exists in $hooks_dir"
        if [ $(read_yn 'Overwrite ?') == 'N' ]; then
            exit 0 
        fi
    fi
    cp $pre_push_file $hooks_dir
fi

