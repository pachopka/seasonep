#!/usr/bin/bash

bash dataroutine.sh
dr=$?

if [ $dr == 0 ]; then
    echo "$(tput setaf 7)$(tput setab 5)Step 3:$(tput sgr 0)$(tput setaf 7)$(tput setab 4) Continue to perform some Magic$(tput sgr 0)"
    python3 seasonep.py
    se=$?
    if [ $se == 0 ]; then
        echo "$(tput setaf 7)$(tput setab 4)Please check results in $(tput sgr 0)$(tput setaf 7)$(tput setab 5)CSV file$(tput sgr 0)"
    else
        echo "$(tput setaf 7)$(tput setab 1)ERROR - return code: $se$(tput sgr 0)"
    fi
else
    echo "$(tput setaf 7)$(tput setab 1)ERROR - return code: $dr$(tput sgr 0)"
fi
