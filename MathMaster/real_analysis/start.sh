#! /bin/bash
default_bookmark="OrderR"
bookmark=${1:-${default_bookmark}}
firefox analysis.pdf#${bookmark} &
qpdfview rudin/RudinW.PrinciplesOfMathematicalAnalysis3e1976600Dpi.pdf &
