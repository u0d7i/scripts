#!/bin/bash
# update all github repos

CL="curl -sS"
GH="github.com"         # github host
GHA="https://api.${GH}" # github API URL

# redefine these in CFG below if needed
BD=$(pwd)                # basedir for gh repos
GU=""                    # github users,  space separated
GC="$HOME/github/gh.cfg" # github config for above

err(){
    echo "-err: $@"
    exit
}

# source local config if exists
[ -e ${GC} ] && . "${GC}"

# check if we have username
[ -z ${GU+x} ] && err "no github users set"

for U in $GU;
do
    [ -d "${BD}/${U}" ] || mkdir "${BD}/${U}"
    if [ -d "${BD}/${U}" ]; then
        cd "${BD}/${U}" || err "can't continue"
        ${CL} "${GHA}/users/${U}/repos?visibility=all" | grep '"name":' | awk -F\" '{print $4}' | while read R;
            do
                echo "+ ${U}/${R} ..."
                if [ -d "${BD}/${U}/${R}" ]; then
                    # we have a repo, update it
                    cd "${BD}/${U}/${R}"
                    git fetch && git checkout && git pull origin && git reset --hard && git clean -fd
                    cd "${BD}/${U}"
                else
                    # we don't have a repo, clone it
                    git clone git@${GH}:/${U}/${R}
                fi
            done
    else
        err "can't continue"
    fi
done

