import subprocess
import netCDF4 as nc
import numpy as np

def compare_netcdf_files(file1, file2):
    """
    Compara os arquivos NetCDF listados em dois arquivos de texto usando 'diff -uq'.
    Se houver diferença, faz uma análise estatística das variáveis.
    """
    try:
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            netcdf_files1 = [line.strip() for line in f1.readlines()]
            netcdf_files2 = [line.strip() for line in f2.readlines()]
        
        if len(netcdf_files1) != len(netcdf_files2):
            print("O número de arquivos NetCDF em cada lista é diferente!")
        
        for orig_file, new_file in zip(netcdf_files1, netcdf_files2):
            result = subprocess.run(["diff", "-uq", orig_file, new_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            if result.returncode == 0:
                print(f"Arquivos {orig_file} e {new_file} são idênticos.")
            else:
                print(f"Arquivos {orig_file} e {new_file} diferem:")
                print(result.stdout)
                analyze_netcdf_differences(orig_file, new_file)
    except FileNotFoundError as e:
        print(f"Erro: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

def analyze_netcdf_differences(file1, file2):
    """
    Compara as variáveis dos arquivos NetCDF e exibe estatísticas das diferenças.
    """
    try:
        ds1 = nc.Dataset(file1)
        ds2 = nc.Dataset(file2)
        
        common_vars = set(ds1.variables.keys()).intersection(set(ds2.variables.keys()))
        
        for var in common_vars:
            data1 = ds1.variables[var][:]
            data2 = ds2.variables[var][:]
            
            if data1.shape != data2.shape:
                print(f"  -> Variável '{var}' tem tamanhos diferentes: {data1.shape} vs {data2.shape}")
                continue
            
            diff = data1 - data2
            mean_diff = np.mean(diff)
            std_diff = np.std(diff)
            mae_diff = np.mean(np.abs(diff))
            rmse_diff = np.sqrt(np.mean(diff ** 2))
            
            mean_data1 = np.mean(np.abs(data1))
            mae_percent = (mae_diff / mean_data1) * 100 if mean_data1 != 0 else 0
            rmse_percent = (rmse_diff / mean_data1) * 100 if mean_data1 != 0 else 0
            
            if rmse_percent > 0.1:
                print(f"  -> Estatísticas para variável '{var}':")
                print(f"     Média da diferença: {mean_diff:.6f}")
                print(f"     Desvio padrão da diferença: {std_diff:.6f}")
                print(f"     Erro absoluto médio (MAE): {mae_diff:.6f} ({mae_percent:.2f}%)")
                print(f"     Raiz do erro quadrático médio (RMSE): {rmse_diff:.6f} ({rmse_percent:.2f}%)")
        
        ds1.close()
        ds2.close()
    except Exception as e:
        print(f"Erro ao processar arquivos NetCDF: {e}")

if __name__ == "__main__":
    compare_netcdf_files("netcdfs_orig1080.txt", "netcdfs_new1080.txt")
