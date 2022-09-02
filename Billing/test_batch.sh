#!/bin/bash
# all test to change
bold=$(tput bold)
normal=$(tput sgr0)
green='\e[1;32m'
red='\e[1;31m'
white='\e[0m'


pushd /app/git/Billing/tests > /dev/null
    command rm -f output.txt
    command ./get_health.sh >> output.txt
    command ./get_monitor.sh >> output.txt
    command ./get_rates.sh >> output.txt
    command ./post_provider.sh >> output.txt
    command ./put_provider_id.sh >> output.txt
    command ./post_get_truck.sh >> output.txt
    command ./post_rates.sh >> output.txt
    passed_count=$(grep -c "Passed" output.txt)
    if [ $passed_count -eq 0 ]; then
        echo -e "\n${bold}${red}Oh...$passed_count/9 tests passed.${white}${normal}\n"
    
    elif [ $passed_count -eq 9 ]; then
        echo -e "\n${bold}${green}$passed_count/9 tests passed! Great job!${white}${normal}\n"

    else echo -e "\n${bold}${red}Oh...$passed_count/9 tests passed.${white}${normal}\n"
    fi

    if [ $passed_count -eq 9 ]; then
        exit 100
    else
        exit $passed_count
    fi



popd > /dev/null
