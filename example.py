import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

num_points = int(1e3)
ts = np.linspace(0,40*np.pi, num_points)
xs = np.sin(ts/(1+ts/250))
window_size = 3

data_matrix = np.zeros([num_points-window_size, window_size])
for i in range(num_points-window_size):
    data_matrix[i] =  xs[i:(i+window_size)]

model = PCA(n_components=2, whiten=True)
X = model.fit_transform(data_matrix)

from viz import TimeCluster
time_series = np.stack([ts,xs], axis=1)
tc = TimeCluster(time_series[window_size:], X)
tc.start_viz()
print(tc.label_mask)
