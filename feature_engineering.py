# Import key packages
import pandas as pd
import numpy as np
from utils import  get_seconds, sort_dt, get_td_mean, get_td_sd, rem_dups


def format_data(data):
    # convert d_time field to a numeric timestamp value
    data['d_time'] = pd.to_datetime(data['d_time']).values.astype(np.int64)

    # create feature mean_time_difference which shows the mean difference in time between two consecutive attacks from the same ip
    data_grouped_td = data[['src_ip','d_time']].groupby('src_ip',as_index = False).agg({'d_time':lambda x: x.tolist()})
    data_grouped_td['d_time'] = data_grouped_td['d_time'].apply(sort_dt)
    data_grouped_td['d_time'] = data_grouped_td['d_time'].apply(get_td_mean)
    data_grouped_td['d_time'] = pd.to_datetime(data_grouped_td['d_time'], unit='ns')
    data_grouped_td['d_time'] = data_grouped_td['d_time'].apply(get_seconds)
    data_grouped_td = data_grouped_td.rename({'d_time':'mean_time_difference'},axis = 1)

    # create feature sd_time_difference which shows the standard deviation in time difference between two consecutive attacks from the same ip
    data_grouped_sd = data[['src_ip','d_time']].groupby('src_ip',as_index = False).agg({'d_time':lambda x: x.tolist()})
    data_grouped_sd['d_time'] = data_grouped_sd['d_time'].apply(sort_dt)
    data_grouped_sd['d_time'] = data_grouped_sd['d_time'].apply(get_td_sd)
    data_grouped_sd['d_time'] = pd.to_datetime(data_grouped_sd['d_time'], unit='ns')
    data_grouped_sd['d_time'] = data_grouped_sd['d_time'].apply(get_seconds)
    data_grouped_sd = data_grouped_sd.rename({'d_time':'sd_time_difference'},axis = 1)

    data_grouped = data[['src_ip','d_time']].groupby('src_ip',as_index = False).agg({'d_time':np.mean})
    data_grouped['d_time'] = pd.to_datetime(data_grouped['d_time'], unit='ns')

    data_grouped1 = data[['src_ip','d_time']].groupby('src_ip',as_index = False).agg({'d_time':np.std})
    data_grouped1['d_time'] = pd.to_datetime(data_grouped1['d_time'], unit='ns')
    data_grouped1['d_time'] = data_grouped1['d_time'].apply(get_seconds)

    data_grouped2 = data[['sensor','src_ip']].groupby('src_ip',as_index = False).agg({'sensor':lambda x: x.tolist()})
    data_grouped2['sensor_number'] = data_grouped2['sensor'].apply(rem_dups)
    data_grouped2['sensor_number'].value_counts()


    data_final = data_grouped.merge(data_grouped1, left_on='src_ip', right_on='src_ip')
    data_final = data_final.merge(data_grouped_td,left_on='src_ip', right_on='src_ip')
    data_final = data_final.merge(data_grouped_sd,left_on='src_ip', right_on='src_ip')
    data_final = data_final.merge(data_grouped2,left_on='src_ip', right_on='src_ip')
    data_final = data_final.rename({'d_time_x':'mean_time_of_attack','d_time_y':'sd_time_of_attack','sensor':'all_sensors'},axis = 1)

    # drop to get rid of those columns, like you would in a spreadsheet
    data_final.drop(["mean_time_of_attack", "sd_time_of_attack", "all_sensors"], axis = 1, inplace= True)
    return data_final



def generate_features(data):
     # Getting rid of empty rows. dropna means to drop all rows with NaN in them
    # This is cleaning data
    new = data[["ssh_username", "src_ip"]].dropna()
    # apply is like a function that gets run for every row.
    # Generate a new row that has the length of each username on it
    new["length_username"] = new["ssh_username"].apply(len)

    user_length = new.groupby("src_ip").mean()

    current = pd.merge(user_length, data, how = "outer", on = "src_ip")

    current['length_username'].fillna(value = current['length_username'].mean(), inplace = True)

    new_command = data[['src_ip', 'command']]
    new_command.dropna(inplace = True)
    new_command['length_command'] = new_command['command'].apply(len)
    # generate new feature by getting average of data
    feature = new_command.groupby('src_ip').mean()
    features = pd.merge(current, feature, how = 'outer', on = "src_ip")
    return features

def generate_honeypot_features(data, features):
    counts = data['app'].value_counts()
    res = data[~data['app'].isin(counts[counts < 27].index)]
    res['app'].value_counts()
    honeypot = res[['app', 'src_ip']]
    honeypot['app'].value_counts()
    honeypot.groupby('src_ip')
    new_features = pd.merge(features, honeypot, how = 'inner', on = 'src_ip')
    return new_features


def generate_ip_features(data, features):
    dat = data.groupby('src_ip')[['src_ip', 'app']].head()
    temp = dat.drop_duplicates()
    let = pd.get_dummies(temp['app'])
    det = pd.concat([let,temp], axis = 1)
    det['app'].value_counts()
    counts = det['app'].value_counts()
    det = det[~det['app'].isin(counts[counts < 100].index)]
    det['app'].value_counts()
    head = data.groupby('src_ip').count()
    head.reset_index(inplace = True)
    val = head[['src_ip', 'app']]
    features = pd.merge(features, val, how = 'inner', on = 'src_ip')
    features.rename(columns={'app':'daily_frequency'}, inplace=True)

    dat_t = data.groupby('src_ip')['dest_port'].nunique()
    new_dat_t = dat_t.reset_index()
    features = pd.merge(new_dat_t, features, how = 'inner', on = 'src_ip')
    features.rename(columns={'dest_port':'dest_port_number'}, inplace=True)
    return features

def generate_password_features(data, features):
    new_data = data[['src_ip', 'ssh_password']]
    new_data.dropna(inplace = True)
    new_data['length_password'] = new_data['ssh_password'].apply(len)
    new_data.drop(['ssh_password'], axis = 1, inplace = True)
    new_data.drop_duplicates(inplace= True)
    features = pd.merge(features, new_data, how = 'outer', on = 'src_ip')
    features['length_password'].fillna(value = features['length_password'].mean(), inplace = True)
    features.drop_duplicates(inplace= True)
    features.drop_duplicates('src_ip', inplace= True)
    return features



