#!/bin/bash
app=$1
syn=$2
for d in ./*/;
do
    cd "$d"
    # echo "$app $d"
    if [ $app != "syn" ]; then
    	grep " 0" mpi-replay-stats > $app.csv
    fi
    if (( $syn==1 )); then
    	grep " 1" mpi-replay-stats > syn.csv
    fi
   # grep "APP 0" mpi-replay-stats > amg.csv
   # grep "APP 1" mpi-replay-stats > cr.csv
   # grep "APP 2" mpi-replay-stats > cr.csv

    cd ../
    
done
