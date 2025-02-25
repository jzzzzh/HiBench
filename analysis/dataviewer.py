import glob
import os
import pandas as pd

files = glob.glob('./analysis/format-results/*.csv')


example_llama_family = ['Meta-Llama-3.1-8B-Instruct', 'Llama-3.2-1B-Instruct', 'Llama-3.2-3B-Instruct']

for file in files:
    print(f'processing: {file}')
    save_path = file.replace('format-results', 'dataview').replace('.csv', '.xlsx')
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    with pd.ExcelWriter(save_path, engine='xlsxwriter') as writer:
        df = pd.read_csv(file)
        # get unique variants for each parameter
        unique_variants = df.drop(columns=['Accuracy']).nunique()
        unique_variants_df = pd.DataFrame(unique_variants, columns=['Unique Variants'])
        unique_variants_df.to_excel(writer, sheet_name='Unique Variants', index=True)
        
        param_stats = {}
        
        for column in df.columns:
            # skip bullshit in JSON analysis.
            df_temp = df
            if 'JSON' in file:
                if column == 'Mode':
                    continue
                df_temp = df[df['Mode'] != 'bullshit']
            # only static ZeroShot performance if the control parameter is not 'ExampleType'.
            if column != 'ExampleType':
                df_temp = df_temp[df_temp['ExampleType'] == 'ZeroShot']
            # only static performance of models who have zeroshot, oneshot, and fewshot results, if the control parameter is 'ExampleType'.
            else:
                if column != 'Accuracy' and unique_variants[column] > 1:
                    zero_shot_models = df['ModelName'][df['ExampleType'] == 'ZeroShot']
                    one_shot_models  = df['ModelName'][df['ExampleType'] == 'OneShot']
                    few_shot_models  = df['ModelName'][df['ExampleType'] == 'FewShot']
                    model_union = set(zero_shot_models) & set(one_shot_models) & set(few_shot_models) - set(['Yi-1.5-9B-Chat'] + example_llama_family)
                    df_temp     = df[df['ModelName'].isin(model_union)]
                    print(f'ExampleType model list: {model_union}')

            # skip accuracy.
            if column != 'Accuracy' and unique_variants[column] > 1:
                stats = df_temp.groupby(column)['Accuracy'].agg(['mean', 'std', 'count'])
                stats.columns = ['mean', 'std', 'count']
                param_stats[column] = stats
                # find maximum average accuracy per ModelFamily
                if column == 'ModelFamily':
                    avg_accuracy_per_model = df.groupby("ModelName")["Accuracy"].mean().reset_index()
                    avg_accuracy_per_model = avg_accuracy_per_model.merge(df[["ModelName", "ModelFamily"]].drop_duplicates(), on="ModelName")
                    avg_accuracy_per_model = avg_accuracy_per_model.groupby("ModelFamily")["Accuracy"].max().reset_index().rename(columns={'Accuracy': 'max'})
                    param_stats[column] = param_stats[column].merge(avg_accuracy_per_model, on="ModelFamily")
                    
        # Write each parameter's statistics to a separate sheet in the Excel file
        for param, stats_df in param_stats.items():
            stats_df.to_excel(writer, sheet_name=param, index=True)
