#!/usr/bin/bash

bash dataroutine.sh
dr=$?

if [ $dr == 0 ]; then 
    echo 'Dataset Routine has been finished'
    echo 'Continue to perform some Magic'
    python3 seasonep.py
    se=$?
    if [ $se == 0 ]; then 
        echo 'Please check results in CSV file'
    else
        echo "ERROR - return code: $se"
    fi
else
    echo "ERROR - return code: $dr"
fi
