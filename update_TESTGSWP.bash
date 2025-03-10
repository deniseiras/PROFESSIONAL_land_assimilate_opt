#!/bin/bash
set -x
# switch_user spreads-lnd

W='/work/cmcc/spreads-lnd/work_d4o/TEST_GSWP'
S='/work/cmcc/de34824/work/PROFESSIONAL_land_assimilate_opt'


cd $W
rm -f assimilate.csh 
ln -sf $S/assimilate.csh 

cd $W/run
runfiles='run_dart_to_clm.bash run_filter.bash run_clm_to_dart_par.bash run_dart_to_clm_snow.bash run_inflation.bash'
rm -f $runfiles

for f in $runfiles; do
  ln -sf $S/run/$f .
done

