#!/bin/bash

NAME=$1
DOMAIN=$2

WI_OCCURRENCES="s/blogalessionardineu*"/"${NAME}"/"g"
INTEXT_OCCURRENCES="s/blogalessionardineu"/"${NAME}"/"g"
DOMAIN_OCCURRENCES="s/blog.alessionardin.eu"/"${DOMAIN}"/"g"

# Renaming project variables so that they match the new project name
find . -iname "blogalessionardineu" | rename $WI_OCCURRENCES
find . -iname "blogalessionardineu*" | rename $WI_OCCURRENCES
find . -iname "blogalessionardineu*" | rename $WI_OCCURRENCES

find . -iname "blog.alessionardin.eu" | rename $DOMAIN_OCCURRENCES
grep -RiIl "blogalessionardineu" | xargs sed -i $INTEXT_OCCURRENCES
grep -RiIl "blog.alessionardin.eu" | xargs sed -i $DOMAIN_OCCURRENCES

exit 0

