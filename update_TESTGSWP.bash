#!/bin/bash
set -x
# switch_user spreads-lnd

WORK_DIR=$1
SOURCE_DIR=$PWD


cd $WORK_DIR
rm -f assimilate.csh assimilate_executor.csh
cp -f $SOURCE_DIR/assimilate.csh $SOURCE_DIR/assimilate_executor.csh .

cd $WORK_DIR/run
runfiles='run_dart_to_clm.bash run_filter.bash run_clm_to_dart_par.bash run_dart_to_clm_snow.bash run_inflation.bash'
rm -f $runfiles

for f in $runfiles; do
  cp -f $SOURCE_DIR/run/$f .
done





