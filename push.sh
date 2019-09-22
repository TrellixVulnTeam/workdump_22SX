#!/usr/bin/env bash

git add .
git commit --fixup=HEAD
git pull
git push
