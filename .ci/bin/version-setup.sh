#!/usr/bin/env bash
raw_version="$(cat klippy/.version)"
declare -a versontags
IFS="-" read -r -a versiontags <<<"$raw_version"
# TODO: Handle a single tag, for actual release tags
py_version="${versiontags[0]}-dev${versiontags[1]}+git.${versiontags[2]}"
echo "$py_version" > ".py_version"
