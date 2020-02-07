import numpy as np
import pandas as pd
import shapefile as shp
import matplotlib.pyplot as plt
import seaborn as sns
import os
from glob import glob

# Graphic Option
sns.set(style='whitegrid', palette='pastel', color_codes=True)
# sns.mpl.rc('figure', figsize=(10,6))

# Fire perimeter .shp path
folder_path = 'E:/Dropbox/dataset/Satellite_Dataset/fire_perimeter'
fire_folder = os.listdir(folder_path)

fire_path = os.path.join(folder_path, fire_folder[0])
shp_path = glob(os.path.join(fire_path, '*.shp'))[0]

# Function for shp to pandas
def read_shp(sf):
    fields = [x[0] for x in sf.fields][1:]
    records = sf.records()
    shps = [s.points for s in sf.shapes()]

    df = pd.DataFrame(columns=fields, data=records)
    df = df.assign(coords=shps)

    return df

# Load shp file
sf = shp.Reader(shp_path)
print('first shape has %d points' %len(sf.shape(0).points))
print('first shape has %d points' %len(sf.shapes()[0].points))
print('first point of first shape-x:%f, y:%f' %(sf.shape(0).points[0][0], sf.shape(0).points[0][1]))
print('first shape-bbox-xlim:[%f, %f] ylim:[%f, %f]' %(sf.shape(0).bbox[0], sf.shape(0).bbox[2], sf.shape(0).bbox[1], sf.shape(0).bbox[3]))
df = read_shp(sf)

# Plot single shp files
def plot_shape(sf, id, s=None):
    """ PLOTS A SINGLE SHAPE """
    plt.figure()
    ax = plt.axes()
    ax.set_aspect('equal')
    shape_ex = sf.shape(id)
    x_lon = np.zeros((len(shape_ex.points),1))
    y_lat = np.zeros((len(shape_ex.points),1))
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]
    plt.plot(x_lon,y_lat)
    x0 = np.mean(x_lon)
    y0 = np.mean(y_lat)
    plt.text(x0, y0, s, fontsize=10)
    # use bbox (bounding box) to set plot limits
    plt.xlim(shape_ex.bbox[0],shape_ex.bbox[2])
    plt.show()
    return x0, y0

# Plot all shp files
def plot_map(sf, id=None, x_lim=None, y_lim=None, figsize=(11, 9)):
    '''
    Plot map with lim coordinates
    '''
    plt.figure(figsize=figsize)
    ax = plt.axes()
    ax.set_aspect('equal')
    id = 0
    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        plt.plot(x, y, 'k')

        if (x_lim == None) & (y_lim == None):
            x0 = np.mean(x)
            y0 = np.mean(y)
            plt.text(x0, y0, id, fontsize=10)
        id = id + 1

    if (x_lim != None) & (y_lim != None):
        plt.xlim(x_lim)
        plt.ylim(y_lim)

    plt.show()

comuna = df.loc[:,'uniquefire'].to_numpy()


com_id = df[df.uniquefire == comuna].index.to_numpy()[0]

x_lim = (-105, -110)
y_lim = (42, 44)
plot_map(sf, x_lim=x_lim, y_lim=y_lim)

print(sf.shape(1))