import pandas as pd

def merge_data():
    # reading csv files
    data1 = pd.read_csv('dstat/monitor_dstat_data.csv')
    data2 = pd.read_csv('powertop/monitor_powertop_data.csv')
    
    # using merge function by setting how='left'
    output = pd.merge(data1, data2, 
                    on=['date', 'time'], 
                    how='left').fillna('')

    # displaying result
    print(output)
    # save result
    output.to_csv('output/output.csv', index=False)
