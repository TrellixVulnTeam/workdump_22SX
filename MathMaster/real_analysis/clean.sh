#!/usr/bin/env bash
DIR_DEFAULT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
DIR=${1:-${DIR_DEFAULT}}
cd "${DIR}"
ls | grep analysis. | grep -Ev "\.pdf|\.tex" | xargs rm
ls | grep format_analysis. | grep -Ev "\.pdf|\.tex" | xargs rm
