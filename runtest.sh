#!/bin/bash
EXE=/home/xwangiit/tools/codes/install/bin/model-net-mpi-replay
NET_CONFIG='-- /home/xwangiit/workspace/script/runtime_conf/8r_dragonfly.conf'
FLAG='--sync=1 --disable_compute=1 --enable_sampling=0 --workload_type=dumpi'
APP=( amg mg cr )
APP_PATH=( "/home/xwangiit/workspace/traces/AMG/n1728_dumpi/dumpi-2014.03.03.14.55.50-" \
           "/home/xwangiit/workspace/traces/MG/n1000_dumpi/dumpi-2014.03.07.00.25.12-" \
           "/home/xwangiit/workspace/traces/CR/n100_dumpi/dumpi--2014.04.23.12.12.05-")
RANK=( 1728 1000 100 )
SEED=1
MAX=10
INTERVAL_MAX=1
MAX_NODE=3456
payload=( 1000 1000 1000 )
interval=( 10000 10000 10000)
bcknodes=( 0 3456 )
allocation=( "rand_node" )

declare -a nametag
declare -A matrix_payload
declare -A matrix_interval
declare -A matrix_bcksize

#prepare parameters
for (( i=0; i<${#APP[@]}; i++ ))
do
    nametag[i]="${APP[i]}${RANK[i]}"
    for (( j=0; j<$MAX; j++ ))
    do
        # matrix_payload[$i,$j]=$((${payload[$i]}*($j+1)))
        if (( $J != 0 )); then
            matrix_payload[$i,$j]=$((${payload[$i]}*$j*10))
        else
            matrix_payload[$i,$j]=${payload[$i]}
        fi
    done
    for (( j=0; j<$INTERVAL_MAX; j++ ))
    do
    #    if [ ${APP[i]} != "cr" ]; then
    #        matrix_interval[$i,$j]=${interval[j]}
    #    else
    #        matrix_interval[$i,$j]=$((${interval[j]}*100))
    #    fi
        matrix_interval[$i,$j]=${interval[i]}
    done
    for (( j=0; j<${#bcknodes[@]}; j++ ))
    do
        if [ ${bcknodes[j]} == 0 ]; then
            matrix_bcksize[$i,$j]=${bcknodes[j]}
        else
            matrix_bcksize[$i,$j]=$((${bcknodes[j]}-${RANK[i]}))
        fi
    done    
done

function get_ready(){
    # generate workload file  
    cd ~/workspace/script/runtime_conf/wk_conf/
    for (( i=0; i<${#APP[@]}; i++ ))
    do
        for (( j=0; j<${#bcknodes[@]}; j++ ))
        do        
            if [ ${matrix_bcksize[$i,$j]} == 0 ] ; then
                filename="trace_${nametag[i]}.conf"
                echo $filename
            else
                filename="trace_${nametag[i]}_bck${matrix_bcksize[$i,$j]}.conf"
                echo $filename
            fi
            line="${RANK[$i]} ${APP_PATH[i]}"
            printf "$line\n" > $filename
            if [ ${matrix_bcksize[$i,$j]} != 0 ] ; then
                line="${matrix_bcksize[$i,$j]} synthetic-tr"
                printf "$line\n" >> $filename
            fi
        done
    done

    # generate allocation file    
   cd ~/workspace/alloclistgen/
   for (( i=0; i<${#APP[@]}; i++ ))
   do
       for (( j=0; j<${#bcknodes[@]}; j++ ))
       do    
           if [ ${matrix_bcksize[$i,$j]} == 0 ] ; then
               ./my_test.py ${RANK[$i]} 0
           else
               ./my_test.py ${RANK[$i]} ${matrix_bcksize[$i,$j]} 1
           fi
       done
   done
}

function prepare_all_test(){
    # prepare parameter
    BCK_NODES=( 0 $MAX_NODE )
    for (( j=0; j<${#APP[@]}; j++ ))
    do
        BCK_NODES[1]=$((${BCK_NODES[1]}-${RANK[j]}))
    done
    echo "${BCK_NODES[0]} ${BCK_NODES[1]}"

    # generate workload file  
    cd ~/workspace/script/runtime_conf/wk_conf/
    for (( j=0; j<${#BCK_NODES[@]}; j++ ))
    do       
        if [ ${BCK_NODES[$j]} == 0 ] ; then
            filename="trace_3apps.conf"
            echo $filename
        else
            filename="trace_3apps_bck${BCK_NODES[$j]}.conf"
            echo $filename
        fi

        for (( i=0; i<${#APP[@]}; i++ ))
        do 
            line="${RANK[$i]} ${APP_PATH[i]}"
            if (( $i == 0 )); then
                printf "$line\n" > $filename
            else
                printf "$line\n" >> $filename
            fi
        done

        if [ ${BCK_NODES[$j]} != 0 ] ; then
            line="${BCK_NODES[$j]} synthetic-tr"
            printf "$line\n" >> $filename
        fi
    done

    # generate allocation file    
    cd ~/workspace/script/alloclistgen/
    for (( j=0; j<${#BCK_NODES[@]}; j++ ))
    do    
        if (( ${BCK_NODES[$j]} == 0 )) ; then
            ./my_test.py ${RANK[0]} ${RANK[1]} ${RANK[2]} 0
        else
            ./my_test.py ${RANK[0]} ${RANK[1]} ${RANK[2]} ${BCK_NODES[$j]} 1
        fi
    done

}

function execute_test(){
    ####   Get APP id ####
    echo "app id is $1"
    for (( q=0; q<${#allocation[@]}; q++ ))
    do
        for (( i=0; i<${#bcknodes[@]}; i++ ))
        do
            if (( ${matrix_bcksize[$1,$i]} == 0 )) ; then        
                WK_FILE=/home/xwangiit/workspace/script/runtime_conf/wk_conf/trace_${nametag[$1]}.conf
                if [ ${allocation[$q]} == "cont-cons" ]; then
                    LPIO_CONF="--lp-io-dir=${allocation[$q]}-${nametag[$1]}-bck0-l0-i0 --lp-io-use-suffix=1"
                    ALLOC_FILE=/home/xwangiit/workspace/script/alloclistgen/${allocation[$q]}-alloc-$MAX_NODE-${RANK[$1]}.conf
                else
                    LPIO_CONF="--lp-io-dir=${allocation[$q]}0-${nametag[$1]}-bck0-l0-i0 --lp-io-use-suffix=1"
                    ALLOC_FILE=/home/xwangiit/workspace/script/alloclistgen/${allocation[$q]}0-alloc-$MAX_NODE-${RANK[$1]}.conf                    
                fi
                echo "run ${allocation[$q]} test with bcksize=0 payload=0 interval=0"
                mpirun -f $COBALT_NODEFILE -n $PROCS $EXE $FLAG $LPIO_CONF $BCK_CONF --workload_conf_file=$WK_FILE --alloc_file=$ALLOC_FILE $NET_CONFIG
                wait
                sleep 10
            else
                for (( k=0; k<$MAX; k++ ))
                do
                    for (( p=0; p<$INTERVAL_MAX; p++ ))
                    do
                        if [ ${allocation[$q]} == "cont-cons" ]; then
                            DSEED=1
                        else
                            DSEED=$SEED
                        fi
                        for (( j=0; j<$DSEED; j++ ))
                        do
                            BCK_CONF="--mean_interval=${matrix_interval[$1,$p]} --payload_size=${matrix_payload[$1,$k]}"
                            WK_FILE=/home/xwangiit/workspace/script/runtime_conf/wk_conf/trace_${nametag[$1]}_bck${matrix_bcksize[$1,$i]}.conf
                            if [ ${allocation[$q]} == "cont-cons" ]; then
                                LPIO_CONF="--lp-io-dir=${allocation[$q]}-${nametag[$1]}-bck${matrix_bcksize[$1,$i]}-l${matrix_payload[$1,$k]}-i${matrix_interval[$1,$p]} --lp-io-use-suffix=1"
                                ALLOC_FILE=/home/xwangiit/workspace/script/alloclistgen/${allocation[$q]}-alloc-$MAX_NODE-${RANK[$1]}_${matrix_bcksize[$1,$i]}.conf
                            else
                                LPIO_CONF="--lp-io-dir=${allocation[$q]}$j-${nametag[$1]}-bck${matrix_bcksize[$1,$i]}-l${matrix_payload[$1,$k]}-i${matrix_interval[$1,$p]} --lp-io-use-suffix=1"
                                ALLOC_FILE=/home/xwangiit/workspace/script/alloclistgen/${allocation[$q]}$j-alloc-$MAX_NODE-${RANK[$1]}_${matrix_bcksize[$1,$i]}.conf
                            fi
                            echo "run ${allocation[$q]} test with bcksize=bck${matrix_bcksize[$1,$i]} payload=${matrix_payload[$1,$k]} interval=${matrix_interval[$1,$p]} seed=$j"
                            mpirun -f $COBALT_NODEFILE -n $PROCS $EXE $FLAG $LPIO_CONF $BCK_CONF --workload_conf_file=$WK_FILE --alloc_file=$ALLOC_FILE $NET_CONFIG
                            wait
                            sleep 10
                        done
                    done
                done
            fi
        done
        echo "Test is done! APP = ${allocation[$q]}-${nametag[$1]}" | mail -s "codes test" xwang925@gmail.com
    done

}

function execute_all_test(){
    # prepare parameter
    BCK_NODES=( 0 $MAX_NODE )
    for (( j=0; j<${#APP[@]}; j++ ))
    do
        BCK_NODES[1]=$((${BCK_NODES[1]}-${RANK[j]}))
    done
    echo "${BCK_NODES[0]} ${BCK_NODES[1]}"

    declare -a PAYLOADS
    for (( i=0; i<$MAX; i++ ))
    do
        if (( $i != 0 )); then
            PAYLOADS[$i]=$((${payload[0]}*$i*10))
        else
            PAYLOADS[$i]=${payload[0]}
        fi
    done

    for (( q=0; q<${#allocation[@]}; q++ ))
    do
        for (( i=0; i<${#BCK_NODES[@]}; i++ ))
        do
            if (( ${matrix_bcksize[$1,$i]} == 0 )) ; then        
                WK_FILE=/home/xwangiit/workspace/script/runtime_conf/wk_conf/trace_3apps.conf
                if [ ${allocation[$q]} == "cont-cons" ]; then
                    LPIO_CONF="--lp-io-dir=${allocation[$q]}-3apps-bck0-l0-i0 --lp-io-use-suffix=1"
                    ALLOC_FILE=/home/xwangiit/workspace/script/alloclistgen/${allocation[$q]}-alloc-$MAX_NODE-${RANK[0]}_${RANK[1]}_${RANK[2]}.conf
                else
                    LPIO_CONF="--lp-io-dir=${allocation[$q]}0-3apps-bck0-l0-i0 --lp-io-use-suffix=1"
                    ALLOC_FILE=/home/xwangiit/workspace/script/alloclistgen/${allocation[$q]}0-alloc-$MAX_NODE-${RANK[0]}_${RANK[1]}_${RANK[2]}.conf                    
                fi
                echo "run ${allocation[$q]} test with bcksize=0 payload=0 interval=0"
                mpirun -f $COBALT_NODEFILE -n $PROCS $EXE $FLAG $LPIO_CONF $BCK_CONF --workload_conf_file=$WK_FILE --alloc_file=$ALLOC_FILE $NET_CONFIG
                wait
                sleep 10
            else
                for (( k=0; k<$MAX; k++ ))
                do
                    for (( p=0; p<$INTERVAL_MAX; p++ ))
                    do
                        if [ ${allocation[$q]} == "cont-cons" ]; then
                            DSEED=1
                        else
                            DSEED=$SEED
                        fi
                        for (( j=0; j<$DSEED; j++ ))
                        do
                            BCK_CONF="--mean_interval=${interval[0]} --payload_size=${PAYLOADS[$k]}"
                            WK_FILE=/home/xwangiit/workspace/script/runtime_conf/wk_conf/trace_3apps_bck${BCK_NODES[$i]}.conf
                            if [ ${allocation[$q]} == "cont-cons" ]; then
                                LPIO_CONF="--lp-io-dir=${allocation[$q]}-${nametag[$1]}-bck${BCK_NODES[$i]}-l${PAYLOADS[$k]}-i${interval[0]} --lp-io-use-suffix=1"
                                ALLOC_FILE=/home/xwangiit/workspace/script/alloclistgen/${allocation[$q]}-alloc-$MAX_NODE-${RANK[$1]}_${BCK_NODES[$i]}.conf
                            else
                                LPIO_CONF="--lp-io-dir=${allocation[$q]}$j-${nametag[$1]}-bck${BCK_NODES[$i]}-l${PAYLOADS[$k]}-i${interval[0]} --lp-io-use-suffix=1"
                                ALLOC_FILE=/home/xwangiit/workspace/script/alloclistgen/${allocation[$q]}$j-alloc-$MAX_NODE-${RANK[$1]}_${BCK_NODES[$i]}.conf
                            fi
                            echo "run ${allocation[$q]} test with bcksize=bck${BCK_NODES[$i]} payload=${PAYLOADS[$k]} interval=${interval[0]} seed=$j"
                            mpirun -f $COBALT_NODEFILE -n $PROCS $EXE $FLAG $LPIO_CONF $BCK_CONF --workload_conf_file=$WK_FILE --alloc_file=$ALLOC_FILE $NET_CONFIG
                            wait
                            sleep 10
                        done
                    done
                done
            fi
        done
        echo "Test is done! APP = ${allocation[$q]}-3apps" | mail -s "codes test" xwang925@gmail.com
    done

}

function assemble_all(){
    for (( q=0; q<${#allocation[@]}; q++ ))
    do
        for (( p=0; p<$INTERVAL_MAX; p++ ))
        do
            # move directories
            fig_dir=${allocation[$q]}-3apps-i${interval[$p]}
            mkdir ~/workspace/$fig_dir
            if [ ${allocation[$q]} == "cont-cons" ] ; then
                mv ~/workspace/${allocation[$q]}-3apps-bck*-l*-i${interval[$p]}-*/ ~/workspace/$fig_dir/
            else
                mv ~/workspace/${allocation[$q]}0-3apps-bck*-l*-i${interval[$p]}-*/ ~/workspace/$fig_dir/
            fi
        done
    done
}

function draw_all(){
    for (( q=0; q<${#allocation[@]}; q++ ))
    do
        for (( p=0; p<$INTERVAL_MAX; p++ ))
        do
            fig_dir=${allocation[$q]}-3apps-i${interval[$p]}
            cp -r ~/workspace/$fig_dir/* ~/workspace/drawscripts/
            cd ~/workspace/drawscripts/
            echo "draw ${allocation[$q]}-3apps-i${interval[$p]} figures"

            for (( a=0; a<${#APP[@]}; a++ ))
            do
                ./draw.py ${APP[$a]} 1 2>/dev/null
                waite
            done
            # ./draw.py syn 1 2>/dev/null
            # wait      

            # mv figures
            echo "copy and clean"
            for (( a=0; a<${#APP[@]}; a++ ))
            do
                mv ${APP[$a]}-* ${APP[$a]}_* ~/workspace/$fig_dir/
                mv syn-* syn_* ~/workspace/$fig_dir/ 2>/dev/null
                rm -rf ~/workspace/drawscripts/${allocation[$q]}*-3apps-bck*-l*-i${interval[$p]}-*/       
            done
            sleep 60
        done
    done    
}

function post_assemble(){
    echo "app id is $1"
    #assemble same allocation with diff bck load
    for (( q=0; q<${#allocation[@]}; q++ ))
    do
        for (( p=0; p<$INTERVAL_MAX; p++ ))
        do
            fig_dir=${allocation[$q]}-${nametag[$1]}-i${matrix_interval[$1,$p]}-varies-bck
            mkdir ~/workspace/$fig_dir
            cp -r ~/workspace/${allocation[$q]}*-${nametag[$1]}-bck*-l*-i*-*/ ~/workspace/$fig_dir/
        done
    done

    #assmeble different allocation with same payload
    for (( i=0; i<${#bcknodes[@]}; i++ ))
    do
        if (( ${bcknodes[$i]} == 0 )) ; then
            fig_dir=varies-alloc-${nametag[$1]}-bck0-l0-i0
            mkdir ~/workspace/$fig_dir 
            mv ~/workspace/*-${nametag[$1]}-bck0-l0-i0-*/ ~/workspace/$fig_dir/
        else
            for (( k=0; k<$MAX; k++ ))
            do
                for (( p=0; p<$INTERVAL_MAX; p++ ))
                do
        	    fig_dir=varies-alloc-${nametag[$1]}-bck${matrix_bcksize[$1,$i]}-l${matrix_payload[$1,$k]}-i${matrix_interval[$1,$p]}
        	    mkdir ~/workspace/$fig_dir
                    mv ~/workspace/*-${nametag[$1]}-bck${matrix_bcksize[$1,$i]}-l${matrix_payload[$1,$k]}-i${matrix_interval[$1,$p]}-*/ ~/workspace/$fig_dir/
	        done
            done
	fi
    done
}

function draw_fig(){
    echo "app id is $1"
    #draw fig for varies bck load
    for (( q=0; q<${#allocation[@]}; q++ ))
    do
        for (( p=0; p<$INTERVAL_MAX; p++ ))
        do
            fig_dir=${allocation[$q]}-${nametag[$1]}-i${matrix_interval[$1,$p]}-varies-bck
            cp -r ~/workspace/$fig_dir/* ~/workspace/drawscripts/
            echo "draw ${allocation[$q]}-${nametag[$1]}-i${matrix_interval[$1,$p]} figures"
            ./draw.py ${APP[$1]} 1
            wait
            ./draw.py syn 1 2>/dev/null
            wait
            # mv figures
            echo "copy and clean"
            mv ${APP[$1]}-* ${APP[$1]}_* ~/workspace/$fig_dir/
            mv syn-* syn_* ~/workspace/$fig_dir/ 2>/dev/null
            rm -rf ~/workspace/drawscripts/{allocation[$q]}*-${nametag[$1]}-bck*-l*-i${matrix_interval[$1,$p]}-*/       
            sleep 10
        done
    done

    #draw fig for varies allocation
    for (( i=0; i<${#bcknodes[@]}; i++ ))
    do
        for (( k=0; k<$MAX; k++ ))
        do
            for (( p=0; p<$INTERVAL_MAX; p++ ))
            do
                fig_dir=varies-alloc-${nametag[$1]}-bck${matrix_bcksize[$1,$i]}-l${matrix_payload[$1,$k]}-i${matrix_interval[$1,$p]}
                cp -r ~/workspace/$fig_dir/* ~/workspace/drawscripts/
                cd ~/workspace/drawscripts/
                echo "draw varies-alloc-${nametag[$1]}-bck${matrix_bcksize[$1,$i]}-l${matrix_payload[$1,$k]}-i${matrix_interval[$1,$p]} figures"
                if (( ${matrix_bcksize[$1,$i]} == 0 )) ; then
                    ./draw.py ${APP[$1]} 0
                    wait
                else
                    ./draw.py ${APP[$1]} 1
                    wait
                    .d:/draw.py syn 1
                    wait
                fi        
                # mv figures
                echo "copy and clean"
                mv ${APP[$1]}-* ${APP[$1]}_* ~/workspace/$fig_dir/
                mv syn-* syn_* ~/workspace/$fig_dir/ 2>/dev/null
                rm -rf ~/workspace/drawscripts/*-${nametag[$1]}-bck${matrix_bcksize[$1,$i]}-l${matrix_payload[$1,$k]}-i${matrix_interval[$1,$p]}-*/       
                sleep 10
            done
        done
    done
}

get_ready
#execute_test 0  # amg
#execute_test 1  # multigrid
#execute_test 2  # crystal router
# post_assemble 0  # amg
#post_assemble 1  # multigrid
#post_assemble 2  # crystal router
# draw_fig 0  # amg
# draw_fig 1  # multigrid
# draw_fig 2  # crystal router

# prepare_all_test
# execute_all_test
# assemble_all
# draw_all
