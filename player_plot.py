from nfl_function_pool import *
import matplotlib.pyplot as plt
import matplotlib.colors as colors

csvfile = 'rushing_2017.csv'
r17data = data_from_csv(csvfile)

data = get_data_columns(r17data, ['player', 'rush_yds', 'rush_td'])

points = 0.1*np.asarray(data[:,1], dtype=float) + 6*np.asarray(data[:,2], dtype=float)

xroundval = 0
yroundval = 0


fig = plt.figure(figsize=[8,6])
ax = fig.add_subplot(111)
ax.plot(data[:,1], data[:,2], color='g', marker='.', markersize=4, linestyle='None')
annot = ax.annotate('Label', xy=(0,0), xytext=(5,10), textcoords='offset points',
    bbox=dict(boxstyle='round', fc='w'), arrowprops=dict(arrowstyle='-'))
annot.set_visible(False)
annot.set_text('Player')
ax.grid(color=(0.8*np.ones((1,3))).tolist()[0], linestyle='--', linewidth=1)
ax.set_xlabel('Rushing Yds')
ax.set_ylabel('Rushing TDs')
ax.set_yticks(range(14))
ax.set_xticks(np.arange(0,1400,100))

def update_annotation(row_ind):
    annot.set_text(data[row_ind, 0])
    annot.xy = (float(data[row_ind, 1]), float(data[row_ind, 2]))

def hover_fcn(event):
    if (event.inaxes == ax):
        xydata = np.asarray(ax.lines[0].get_xydata(), dtype=float)
        eventxy = np.array([event.xdata, event.ydata])
        sqdists = ((xydata[:,0]-eventxy[0])/np.diff(ax.get_xlim())[0])**2 + ((xydata[:,1]-eventxy[1])/np.diff(ax.get_ylim())[0])**2
        dists = np.sqrt(sqdists)
        min_ind = np.argmin(dists)
        if dists[min_ind] < 0.01:
            update_annotation(min_ind)
            annot.set_visible(True)
        else:
            annot.set_visible(False)
        fig.canvas.draw_idle()

fig.canvas.mpl_connect('motion_notify_event', hover_fcn) 

plt.show()
