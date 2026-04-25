from Main_2 import data_filtering
import matplotlib.pyplot as plt

def main():
    # --- VISUAL MATPLOTLIB ---

    df, mean_temp, outlier_limit = data_filtering()
    
    plt.figure(figsize=(12, 5))

    # Plot Histogram Temperature for distribution visual
    plt.hist(df['Temperature'], bins=50, color='skyblue', edgecolor='black', alpha=0.7)
    plt.axvline(mean_temp, color='red', linestyle='dashed', linewidth=2, label='Mean')
    plt.axvline(outlier_limit, color='orange', linestyle='dashed', linewidth=2, label='Anomaly Limit')

    plt.title('Distribution of Engine Temperature (100k Data Points)', fontsize=14)
    plt.xlabel('Temperature (C)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig('Grafik_data_test.png')
    
    print("Membuka jendela grafik...") 
    plt.show()

if __name__ == '__main__':
    main()
