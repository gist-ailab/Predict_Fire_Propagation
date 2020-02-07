import numpy as np
import pandas as pd
import shapefile as shp
import os
from glob import glob
from data_preprocessing.utils import util
from datetime import datetime
import pickle
import matplotlib.pyplot as plt

# shp statistics
def save_stats(shp_list, year_list):
    data_list = []
    index_list = []

    data_dict = {}
    for ix, shp_path in enumerate(shp_list):
        year = year_list[ix]
        # Load shape file as DataFrame
        sf = shp.Reader(shp_path)
        df = util.read_shp(sf)
        # Delete NaN
        df.replace([b'', '', None], np.nan, inplace=True)
        df = df.dropna(subset=['uniquefire', 'perimeterd', 'gisacres', 'incidentna'])
        # Delete duplicate
        fire_name = df.uniquefire,
        fire_unique = np.unique(fire_name)

        # Check the statistics
        for fire in fire_unique:
            data_fire = df[df.uniquefire == fire]
            place_unique = np.unique(df[df.uniquefire == fire].incidentna.to_numpy())
            for place in place_unique:
                date = data_fire[data_fire.incidentna == place]
                # Instance is separated by 'unique fire name', 'place(incidentna)'
                date_peri = data_fire[data_fire.incidentna == place].perimeterd
                date_peri = date_peri.apply(lambda x: str2date(x, year))
                days = int((max(date_peri)-min(date_peri)).days)+1
                # Duplicated object is selected by acre size
                index = remove_duple(date)
                count = len(index)
                # Fire perimeter acre
                area = date.loc[index, 'gisacres'].mean()

                data_list.append([[fire], [place], [days], [count], [area], [year]])
                index_list.append(index)

        data_dict['%d' %year] = df

    data_list = np.asarray(data_list)
    data_stats = pd.DataFrame({'fire':data_list[:,0].astype('str').reshape(-1),
                               'place': data_list[:,1].astype('str').reshape(-1),
                               'days':data_list[:,2].astype('int').reshape(-1),
                               'count':data_list[:,3].astype('int').reshape(-1),
                               'area':data_list[:,4].astype('float').reshape(-1),
                               'year':data_list[:,5].astype('int').reshape(-1),
                               'index':index_list})

    return data_dict, data_stats

# change string to datatime format
def str2date(string, year):
    if type(string) == str:
        split = string.split(' ')[0]
        date = datetime.strptime(split, '%m/%d/%Y')
    else:
        date = string
    date = datetime.strptime('%d-%s' %(year, date.strftime('%m-%d')), '%Y-%m-%d')
    return date

# Remove duplication of perimated time
def remove_duple(date):
    time_unique = np.unique(date.perimeterd.to_numpy())

    df_time = date.perimeterd
    df_acre = date.gisacres

    index_list = []
    for time in time_unique:
        imp_time = df_time[df_time == time]
        if len(imp_time) > 1:
            df_acre_new = df_acre[imp_time.index.to_numpy()].sort_values(ascending=False)
            index = df_acre_new.index.to_numpy()[0]
        else:
            index = imp_time.index.to_numpy()[0]
        index_list.append(index)
    return index_list

if __name__ == "__main__":
    # Option
    save = True
    folder_path = 'E:/Dropbox/dataset/Satellite_Dataset/fire_perimeter'

    # Path
    fire_folder = sorted(os.listdir(folder_path), key=lambda x: int(x.split('_')[0]))
    year_list = [int(f.split('_')[0]) for f in fire_folder]

    # shp files path
    shp_list = []
    for fire in fire_folder:
        fire_path = os.path.join(folder_path, fire)
        shp_path = glob(os.path.join(fire_path, '*.shp'))[0]
        shp_list.append(shp_path)

    # Extract and Save the statistics
    if save == True:
        data_dict, data_stats = save_stats(shp_list, year_list)
        data_save = {'original':data_dict, 'stats':data_stats}
        with open('data_perimeter.pkl', 'wb') as f:
            pickle.dump(data_save, f)
    else:
        with open('data_perimeter.pkl', 'rb') as f:
            data_save = pickle.load(f)

    # Visualize Stats
    data_stats = data_save['stats']
    data_stats = data_stats.sort_values(by=['days', 'count'], ascending=False)
    plt.figure()


    # TODO: plot the statistics of perimeter data(days, count)


    plt.show()

    # Export stats to Excel
    data_stats.to_csv('stats_perimeter.csv', index=False)

    # Select Data
    original = data_save['original']


    # TODO: select the appropriate data by referencing above statistics


    select = None

    with open('select_perimeter.pkl', 'wb') as f:
        pickle.dump(select, f)


