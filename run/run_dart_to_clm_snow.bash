#!/bin/bash
#
# Este script processa arquivos clm_to_dart em paralelo usando o sistema de jobs 'bsub'.
# Ele cria um job para cada membro do ensemble e espera que todos os jobs sejam concluídos
# antes de prosseguir para a próxima etapa.


# HISTORY
#
# author            version     comments
# Luis Gustavo      none        Improved paralelized version submitting many jobs in a for in any node available
# Denis Eiras       1.0.0       Improved paralelized version submitting many jobs in a job array in one node
# Denis Eiras       1.1.0       Improved paralelized version distributing jobs in some nodes
# Denis Eiras       1.1.1       Adapting to the spreads - firtst github version


# Argumentos do script (valores fornecidos na linha de comando)
#
export CASE=$1               # CASE é o nome do caso específico
export LND_DATE_EXT=$2       # LND_DATE_EXT é a extensão da data para identificar os arquivos


source /users_home/cmcc/lg07622/modules_juno.me

string_id=""

unlink clm_vector_history   

# Initialize ensemble count
enscount=1

# Iterate over RESTART files matching the pattern
for RESTART in "${CASE}.clm2_"*.r."${LND_DATE_EXT}".nc; do

    NDIR='dd_'$enscount
    
    if [ -d tmp/$NDIR ]; then
      rm -Rf tmp/$NDIR
      mkdir -p tmp/$NDIR
    else
      mkdir -p tmp/$NDIR
    fi
    
    # Extract POSTERIOR_RESTART
    #change from 2.2 to 2.3??
    #POSTERIOR_RESTART="${RESTART/${CASE}.}"
    POSTERIOR_RESTART="${RESTART}"

    # Create POSTERIOR_VECTOR and CLM_VECTOR
    #change from 2.2 to 2.3??

    #POSTERIOR_VECTOR="analysis_member_00$(printf "%02d" $enscount)_d03.nc"
    #CLM_VECTOR="${CASE}.clm2_00$(printf "%02d" $enscount).h2.${LND_DATE_EXT}.nc"

    POSTERIOR_VECTORA="clm_analysis_member_00$(printf "%02d" $enscount)_d03.${LND_DATE_EXT}.nc"
    POSTERIOR_VECTORB="analysis_member_00$(printf "%02d" $enscount)_d03.nc"
    CLM_VECTOR="${CASE}.clm2_00$(printf "%02d" $enscount).h2.${LND_DATE_EXT}.nc"

    if [ -e $POSTERIOR_VECTORA ]; then
        #echo "EXISTS: $POSTERIOR_VECTORA"
        POSTERIOR_VECTOR=$POSTERIOR_VECTORA
    fi
    if [ -e $POSTERIOR_VECTORB ]; then
        #echo "EXISTS: $POSTERIOR_VECTORB"
        POSTERIOR_VECTOR=$POSTERIOR_VECTORB
    fi


    # Confirm the existence of H2OSNO prior/posterior files
    if [[ ! -e $POSTERIOR_VECTOR || ! -e $CLM_VECTOR ]]; then
        echo "ERROR: assimilate.sh could not find $POSTERIOR_VECTOR or $CLM_VECTOR"
        echo "When SWE re-partitioning is enabled H2OSNO must be"
        echo "within vector history file (h2). Also, the analysis"
        echo "stage must be output in 'stages_to_write' within filter_nml"
        exit 7
    fi

    # Copy necessary files
    cp input.nml "tmp/$NDIR/"

    # Change directory
    cd "tmp/$NDIR"

    # Create symbolic links
    ln -sf "../../$POSTERIOR_RESTART" "dart_posterior.nc"
    ln -sf "../../$POSTERIOR_VECTOR" "dart_posterior_vector.nc"
    ln -sf "../../$RESTART" "clm_restart.nc"
    ln -sf "../../$CLM_VECTOR" "clm_vector_history.nc"
    ln -sf "../../clm_history.nc" "clm_history.nc"

cd "${dirwrk}"
../../dart_to_clm &

cd ../../

((enscount++))
done

wait

echo "ALL DART_TO_CLM JOBS FINISHED" 
exit

