import glob
import os

import pandas as pd


files = glob.glob('./analysis/fine-results/*.csv')

for file in files:
    save_path = file.replace('fine-results', 'dataview')
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    with open(save_path, mode='w') as f:
        df = pd.read_csv(file)
        unique_variants = df.drop(columns=['Accuracy']).nunique()
        f.write(f"Parameter numbers:\n")
        f.write(str(unique_variants) + '\n')

        param_stats = {}

        for column in df.columns:
            if column != 'ExampleType':
                df_temp = df[df['ExampleType'] == 'ZeroShot']
            if column != 'Accuracy' and unique_variants[column] > 1:
                stats = df.groupby(column)['Accuracy'].agg(['mean', 'std'])
                stats.columns = ['mean', 'std']
                param_stats[column] = stats

        for param, stats_df in param_stats.items():
            f.write(f"\nStatistics for parameter '{param}':\n")
            f.write(str(stats_df) + '\n')