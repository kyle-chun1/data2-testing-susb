import pandas as pd
from .models import ddo_hourly


def import_records():
    df = pd.read_csv('test_data.csv')
    print(df.shape == df.isna().shape and df.shape == df.isnull().shape)
    df['hDate'] = pd.to_datetime(df['hDate'])
    temp_columns = list(df.columns)
    for i in range(0,df.shape[0]):
        temp_dict = {}
        for n,j in enumerate(df.iloc[i]):
            temp_dict[temp_columns[n]] = j
        ddo_hourly.objects.create(**temp_dict).save()
