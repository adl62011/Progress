from Main_1 import data_manipulation
import numpy as np

def data_filtering():
    
    #Import past data
    df = data_manipulation()

    #Filtering
    mean_temp = np.mean(df['Temperature'])
    std_temp = np.std(df['Temperature'])
    outlier_limit = mean_temp + (3 * std_temp) # 3-Sigma Rule

    print(f"\nBatas Anomali Suhu: {outlier_limit:.2f}")
    print(f"Jumlah Data Anomali: {np.sum(df['Temperature'] > outlier_limit)}")

    return df, mean_temp, outlier_limit




