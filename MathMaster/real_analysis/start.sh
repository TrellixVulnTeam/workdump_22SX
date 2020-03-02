#!/usr/bin/env bash

set -x
git pull
if [ -x "$(command -v evince)" ]; then
    viewer="evince"
else
    viewer="qpdfview"
fi

"${viewer}" __analysis.pdf &
#"${viewer}" rudin/RudinW.PrinciplesOfMathematicalAnalysis3e1976600Dpi.pdf &
"${viewer}" dlsu/linear_algebra/smallpdf.com_la.pdf &
"${viewer}" dlsu/linear_algebra/LINEALGLEC1.pdf
