# BSUB -P 0575                              # Project name
# BSUB -J "assm${ENSEMBLE_SIZE}"            # Job name                     
# BSUB -W 00:20                             # Tempo máximo de execução (20 minutos)
# BSUB -o ${LOGFILE}                        # Single output file for all jobs
# BSUB -e ${LOGFILE}                        # Single output file for all jobs
# BSUB -R "rusage[mem=1GB]"                 # Memory per process (default MB)
# BSUB -n ${ENSEMBLE_SIZE}                  # Request cores (total processes)
# BSUB -R "span[ptile=${TASKS_PER_NODE}]"   # Distribute  processes per node

echo "Running assimilation executor with params"
#_${ENSEMBLE_SIZE}_${TOTALPES}_${TASKS_PER_NODE}.log"
echo "CASE: ${CASE}, ENSEMBLE_SIZE: ${ENSEMBLE_SIZE}, TOTALPES: ${TOTALPES}, TASKS_PER_NODE: ${TASKS_PER_NODE}"


exit 0

