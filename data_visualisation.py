import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

strava_activities1 = pd.read_csv('strava_activities.csv')

#-----scatter graph of elapsed time against heart rate------
#scatter_fig = plt.scatter(x=strava_activities1['average_heartrate'], y=strava_activities1['elapsed_time'])
#scatter_fig = plt.show()

#------bar chart of value counts against max heart rate-----
#print(strava_activities1['max_heartrate'].describe())
#gives average values etc.
#labels = [f'{i} < max_heartrate <= {i+20}' for i in range(100,220,20)]
#strava_activities1['max_heartrate'] = pd.cut(strava_activities1['max_heartrate'], bins=[100, 120, 140, 160, 180, 200, 220], labels=labels)
#bar_fig1 = strava_activities1.max_heartrate.value_counts().plot(kind='bar')
#bar_fig1 = plt.show()

#-----average elapsed time for each max heartrate bar chart------
#ax = strava_activities1.groupby(['max_heartrate']).mean(numeric_only=True)['elapsed_time'].plot(kind='bar', title='average elapsed time by maxheartrate', xlabel='max_heartrate', ylabel='average elapsed time')
#for p in ax.patches:
#    ax.annotate(str(round(p.get_height())), (p.get_x()*1.005,p.get_height()*1.005))
#plt.show()

#------histograms--------

#use function on data visualisation notebook: histplot_features

#histogram_1 = plt.hist([strava_activities1[strava_activities1['type'] == 'Rowing']['average_heartrate'], strava_activities1[strava_activities1['type'] == 'Run']['average_heartrate']], bins=10)
#plt.legend(['Rowing', 'Run'])
#histogram_1 = plt.show()
#for this to be more effective,specify bins. Not necessarily all equal in size

#histogram of elapsed time
#histogram_2 = strava_activities1['elapsed_time'].plot(kind='hist', bins=50)
#histogram_2 = plt.show()

#2 histograms in subplots comparing elapsed time for rowing and running
#fig, axs = plt.subplots(1, 2, sharey=True)

#axs[0].hist(strava_activities1[strava_activities1['type'] == 'Rowing']['elapsed_time'])
#axs[0].set_title('Rowing')
#axs[1].hist(strava_activities1[strava_activities1['type'] == 'Run']['elapsed_time'])
#axs[1].set_title('Run')
#axs[0].set_xlabel('Elapsed Time')
#axs[1].set_xlabel('Elapsed Time')
#axs[0].set_ylabel('Frequency')
#plt.show()

#-----pie charts-----
#strava_activities1['type'].value_counts().plot(kind='pie', ylabel='')
#plt.legend(loc = 'upper right')
#plt.show()
#adjust legend size, add nuerical values

#----heat map----
#represents relationship between variables, strong positive: both increase etc. 0=no correlation
del strava_activities1['Unnamed: 0']
del strava_activities1['id']
#split into types, data is meaningless when all together
#activity_type = 'Run'
#ch2 = sns.cubehelix_palette(rot=0.2, as_cmap=True)
#mask = np.triu(np.ones_like(strava_activities1[strava_activities1['type'] == activity_type].corr(), dtype=bool)) #removes upper triangle
#plt.figure(figsize=(16,6))
#heatmap = sns.heatmap(strava_activities1[strava_activities1['type'] == activity_type].corr(), mask=mask, vmin=-1, vmax=1, cmap=ch2, annot=True)

#heatmap = sns.heatmap(strava_activities1.corr()['type'], mask=mask, vmin=-1, vmax=1, cmap=ch2, annot=True)
#heatmap.set_title(f'Correlation Heatmap for type: {activity_type}', fontdict={'fontsize':12}, pad=12)
#plt.savefig(f'Heatmap_{activity_type}.png', bbox_inches='tight', dpi=150)
#plt.show()
#significant correlation between heart rate and cadence because for pre-garmin runs, there was no HR or
#cadence picked up so many activities have (0, 0, 0) for these values

#----box plot----
#strava_activities1['distance'].plot(kind='box')
#plt.show()

#----line graphs----
#plt.plot(strava_activities1['distance'], strava_activities1['moving_time'])
#plt.show()