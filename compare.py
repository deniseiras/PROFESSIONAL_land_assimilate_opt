import subprocess
import netCDF4 as nc
import numpy as np
import os
import re
import sys

def compare_netcdf_files(dir1, dir2, exp1_name, exp2_name, datehour_suffix_pattern):
    """
    Compare netcdf restart files in two directories
    """
    try:
        files1 = sorted([f for f in os.listdir(dir1) if f.startswith(f'{exp1_name}.clm2_') and f.endswith(f'.r.{datehour_suffix_pattern}.nc')])
        files2 = sorted([f for f in os.listdir(dir2) if f.startswith(f'{exp2_name}.clm2_') and f.endswith(f'.r.{datehour_suffix_pattern}.nc')])
        
        print(files1)
        print('\n\n---')
        print(files2)
        
       
        if len(files1) != len(files2):
            print("The number of files in the two directories is different.")
            print(f"\n\nFiles in dir1: {files1}")
            print(f"\n\nFiles in dir2: {files2}")
            # print(f"Files in dir1: {len(files1)}")
            # print(f"Files in dir2: {len(files2)}")
            sys.exit(1)
        
        for file1, file2 in zip(files1, files2):
            path1 = os.path.join(dir1, file1)
            path2 = os.path.join(dir2, file2)
            
            result = subprocess.run(["diff", "-uq", path1, path2], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            print('\n\n---')
            if result.returncode == 0:
                print(f"Files {file1} e {file2} are equal.")
            else:
                print(f"Files {file1} e {file2} differs:")
                print(result.stdout)
                analyze_netcdf_differences(path1, path2)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}") 

def analyze_netcdf_differences(file1, file2):
    """
    Compare variables in two netcdf files and print statistics
    """
    try:
        ds1 = nc.Dataset(file1)
        ds2 = nc.Dataset(file2)
        
        common_vars = set(ds1.variables.keys()).intersection(set(ds2.variables.keys()))
        
        for var in common_vars:
            data1 = ds1.variables[var][:]
            data2 = ds2.variables[var][:]
            
            if data1.shape != data2.shape:
                print(f"  -> Variable'{var}' has different sizes: {data1.shape} vs {data2.shape}") 
                continue
            
            diff = data1 - data2
            mean_diff = np.mean(diff)
            std_diff = np.std(diff)
            mae_diff = np.mean(np.abs(diff))
            rmse_diff = np.sqrt(np.mean(diff ** 2))
            
            mean_data1 = np.mean(np.abs(data1))
            mae_percent = (mae_diff / mean_data1) * 100 if mean_data1 != 0 else 0
            rmse_percent = (rmse_diff / mean_data1) * 100 if mean_data1 != 0 else 0
            

            if rmse_percent > 0.00001:
                print(f"  -> Statistics for variable '{var}':")
                print(f"     Mean difference: {mean_diff:.6f}")
                print(f"     Difference standard deviation: {std_diff:.6f}")
                print(f"     Mean absolute error (MAE): {mae_diff:.6f} ({mae_percent:.2f}%)")
                print(f"     Root mean square error (RMSE): {rmse_diff:.6f} ({rmse_percent:.2f}%)")
        
        ds1.close()
        ds2.close()
    except Exception as e:
        print(f"Error processing file {file1} or {file2}: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Use: python script.py <directory1> <directory2> <exp_name1> <exp2_name> <date_hour_suffix_pattern>")
        sys.exit(1)
    
    dir1 = sys.argv[1]
    dir2 = sys.argv[2]
    exp_name1 = sys.argv[3]
    exp2_name = sys.argv[4]
    date_hour_suffix_pattern = sys.argv[5]
    
    compare_netcdf_files(dir1, dir2, exp_name1, exp2_name, date_hour_suffix_pattern)
