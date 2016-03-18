#!/bin/sh

# fetch all gists, preserve timestamps

user="u0d7i"
url="https://api.github.com/users/${user}/gists"

wget -q -O - ${url} | grep raw_url | awk -F\" '{print $4}' | xargs -n1 wget -c  \
&& \
wget -q -O - ${url} | egrep "\"filename\":|\"created_at\"" | awk -F\" '{print $4}' | sed 'N;s/\n/ -d /' | while read line; do touch $line; done
