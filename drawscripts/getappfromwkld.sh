#!/bin/bash
app=$1
syn=$2
for d in ./*/;
do
    cd "$d"
    # echo "$app $d"
    if [ $app != "syn" ]; then
    	grep " 0$" mpi-replay-stats > $app.csv
    fi
    if (( $syn==1 )); then
    	grep " 1$" mpi-replay-stats > syn.csv
    fi
   # grep "0.000000 0" mpi-replay-stats > alltoallv.csv
   # grep "0.000000 1" mpi-replay-stats > allreduce.csv
   # grep "0.000000 2" mpi-replay-stats > cr.csv

    cd ../
    
done
