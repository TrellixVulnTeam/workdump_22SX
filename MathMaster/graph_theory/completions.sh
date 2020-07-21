#!/usr/bin/env bash

set -x
sublime_user_path = "$1"
if [ -z "$sublime_user_path" ]; then
	echo "Enter sublime user path: "
	read sublime_user_path
fi

cp math.sublime-completions "$sublime_user_path"
echo "Copied math.sublime-completions to $sublime_user_path"
