#!/bin/bash
BLUE='\033[0;34m'
GREEN='\033[0;32m'
CYAN='\033[0;35m'
RED='\033[0;31m'
YELLOW='\033[0;36m'
NC='\033[0m'
cd Docker;
docker -v  1>/dev/null 2>&1  && printf "$BLUE[+] $GREEN check docker$NC\n";
tar -czf spide.tar.gz spide && printf "$BLUE[+] $GREEN tar web project i$NC\n";
docker build -t social-solder . &&  printf "$BLUE[+]$GREEN build images ok  'docker images ' to see .... $NC\n";

if [ $? -eq 0 ];then
    rm spide.tar.gz
    printf "$BLUE[+] $RED build ok then rm tmp file$NC"
fi
