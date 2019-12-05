import numpy as np
import pandas as pd
import datetime as dt
import os
import sys


def main():
    # Read each csv as a pandas dataframe
    activity_small = pd.read_csv("smallData/activity_small.csv")
    basal_small = pd.read_csv("smallData/basal_small.csv")
    bolus_small = pd.read_csv("smallData/bolus_small.csv")
    cgm_small = pd.read_csv("smallData/cgm_small.csv")
    hr_small = pd.read_csv("smallData/hr_small.csv")
    meal_small = pd.read_csv("smallData/meal_small.csv")
    smbg_small = pd.read_csv("smallData/smbg_small.csv")

    # This list will make it easier to iterate over each pandas
    # dataframe
    pandas_dfs = [cgm_small, basal_small, bolus_small,
                  activity_small, hr_small, meal_small, smbg_small]
    pandas_colnames = ['cgm', 'basal', 'bolus',
                       'activity', 'hr', 'meal', 'smbg']
    i = 0

    # For each data frame, coerce the values to float,
    # remove NaNs, rename columns
    for k in pandas_dfs:
        k['time'] = pd.to_datetime(k['time'])
        k.value = pd.to_numeric(k.value, errors='coerce')
        if k.value.dtype != 'float64':
            k.value = k.value.astype('float64')
        k.rename(columns={'value': pandas_colnames[i]}, inplace=True)
        k = k.dropna(subset=[pandas_colnames[i]])
        i += 1

    # Merge dataframes together, starting with cgm_small
    combined_df = cgm_small
    for df in pandas_dfs[1:]:
        combined_df = combined_df.merge(df, on='time', how='left')

    # Replace NaNs with 0
    combined_df = combined_df.fillna(value=0)
    # Create new columns of rounded time points
    combined_df['time5'] = combined_df['time'].dt.round('5min')
    combined_df['time15'] = combined_df['time'].dt.round('15min')
    # Generate sums or mean for each data frame. We'll group off these later
    combined_df_5_sum = pd.DataFrame(combined_df.groupby('time5').sum())
    combined_df_5_mean = pd.DataFrame(combined_df.groupby('time5').mean())
    combined_df_15_sum = pd.DataFrame(combined_df.groupby('time15').sum())
    combined_df_15_mean = pd.DataFrame(combined_df.groupby('time15').mean())

    # Start with the sum df, and then change the appropriate columns
    # to averages instead
    combined_df_5_final = combined_df_5_sum[['activity', 'basal', 'bolus',
                                             'cgm', 'hr', 'meal', 'smbg']]
    combined_df_5_final['smbg'] = combined_df_5_mean['smbg']
    combined_df_5_final['hr'] = combined_df_5_mean['hr']
    combined_df_5_final['cgm'] = combined_df_5_mean['cgm']
    combined_df_5_final['basal'] = combined_df_5_mean['basal']

    combined_df_15_final = combined_df_15_sum[['activity', 'basal', 'bolus',
                                               'cgm', 'hr', 'meal', 'smbg']]
    combined_df_15_final['smbg'] = combined_df_15_mean['smbg']
    combined_df_15_final['hr'] = combined_df_15_mean['hr']
    combined_df_15_final['cgm'] = combined_df_15_mean['cgm']
    combined_df_15_final['basal'] = combined_df_15_mean['basal']

    combined_df_5_final.to_csv('pandas_5min.csv')
    combined_df_15_final.to_csv('pandas_15min.csv')


if __name__ == '__main__':
    main()
