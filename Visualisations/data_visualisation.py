import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#make functions better

strava_activities1 = pd.read_csv('../Webscraping/strava_activities.csv')

def scatter(df, x_ax,y_ax):
    plt.scatter(x=df[x_ax], y=df[y_ax])
    plt.show()

def bar(df, column, column_and_df, labels, bins):
    '''
    standard bar chart with value counts for column divided between relevant bins
    labels and bins corresponding like:
    labels = [f'{i} < {column} <= {i+20}' for i in range(100,220,20)]
    bins=[100, 120, 140, 160, 180, 200, 220]
    '''
    '''
    df[column] = pd.cut(df[column], bins=bins, labels=labels)
    column_and_df.value_counts().plot(kind='bar')
    plt.show()

labels1 = [f'{i} < max_heartrate <= {i + 20}' for i in range(100, 220, 20)]
bins1=[100, 120, 140, 160, 180, 200, 220]
print(bins1)
bar(strava_activities1, 'max_heartrate', strava_activities1.max_heartrate, labels1, bins1)

#-----average elapsed time for each max heartrate bar chart------
#ax = strava_activities1.groupby(['max_heartrate']).mean(numeric_only=True)['elapsed_time'].plot(kind='bar', title='average elapsed time by maxheartrate', xlabel='max_heartrate', ylabel='average elapsed time')
#for p in ax.patches:
#    ax.annotate(str(round(p.get_height())), (p.get_x()*1.005,p.get_height()*1.005))
#plt.show()
'''
def histplot_features(data, features):
    df = data.copy()
    cols = 3
    rows = len(features) // cols + 1
    figsize = (20, 30)
    def trim_axs(axs, N) :
        '''Reduce *axs* to *N* Axes. All further Axes are removed from the figure.'''
        axs = axs.flat
        for ax in axs[N:]:
            ax.remove()
        return axs[:N]
    axs = plt.figure(figsize=figsize, constrained_layout=True).subplots(rows, cols)
    axs = trim_axs(axs, len(features))
    for ax, feature in zip(axs, features):
        data = df[feature].dropna()
        str_title ='\n{}\n'.format(feature)
        ax.set_title(str_title, fontsize=25)
        ax.hist(data, bins = 25, color = 'orange', alpha = 0.6, edgecolor='black', linewidth=1.2)
    plt.savefig('Histogram 1.png')

def find_column_types(df):
    #identifies categorical, boolean and numerical values
    all_cols = list(df.columns)
    numerical_cols_temp = df._get_numeric_data().columns
    categorical_cols = list(set(all_cols) - set(numerical_cols_temp))
    bool_cols = [col for col in all_cols if np.isin(df[col].dropna().unique(), [0, 1,0.0,1.0]).all()]
    numerical_cols = list(set(numerical_cols_temp)-set(bool_cols))
    return categorical_cols, bool_cols, numerical_cols

#cat_cols, bool_cols, num_cols = find_column_types(strava_activities1)
#histplot_features(strava_activities1, num_cols)

#2 in one graph
#histogram_1 = plt.hist([strava_activities1[strava_activities1['type'] == 'Rowing']['average_heartrate'], strava_activities1[strava_activities1['type'] == 'Run']['average_heartrate']], bins=10)
#plt.legend(['Rowing', 'Run'])
#for this to be more effective,specify bins. Not necessarily all equal in size

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

def pie(df, column):
    df[column].value_counts().plot(kind='pie', ylabel='')
    plt.legend(loc = 'upper right')
    plt.show()
    #adjust legend size, add numerical values
    plt.savefig('Pie 1.png')

def heatmap_plotter(df, activity_type, column):
    ch2 = sns.cubehelix_palette(rot=0.2, as_cmap=True)
    mask = np.triu(np.ones_like(df[df[column] == activity_type].corr(), dtype=bool)) #removes upper triangle
    plt.figure(figsize=(16,6))
    heatmap = sns.heatmap(df[df[column] == activity_type].corr(), mask=mask, vmin=-1, vmax=1, cmap=ch2, annot=True)
    heatmap.set_title(f'Correlation Heatmap for type: {activity_type}', fontdict={'fontsize':12}, pad=12)
    plt.savefig(f'Heatmap_{activity_type}.png', bbox_inches='tight', dpi=150)
    plt.show()

#activity_type1 = 'Rowing'
#heatmap_plotter(strava_activities1, activity_type1, 'type')

def box_plotter(df,column):
    df[column].plot(kind='box')
    plt.show()

def line_plotter(df, x_val, y_val):
    '''want to plot a line graph of all rows with name = UT2, date against average hr max hr line on same graph'''
    plt.plot(df[df['name'] == 'UT2'][x_val], df[df['name'] == 'UT2']['average_heartrate'])
    plt.xlabel(x_val)
    plt.ylabel(y_val)
    plt.show()