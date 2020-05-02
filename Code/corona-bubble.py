import pandas as pd
# import plotly_express as px
import plotly
import plotly.express as px
import chart_studio.plotly as py
import chart_studio as cs
from urllib.parse import unquote
from datetime import date
from datetime import datetime
from datetime import timedelta
import os
os.chdir(r'C:\\Users\\admin\\Documents\\Sourav\\Code\\RnD\\Corona')


confirmed_df = pd.read_csv(unquote('https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv'))
# confirmed_df = pd.read_csv('time_series_covid19_confirmed_global.csv')
del confirmed_df['Province/State']
confirmed_df.rename(columns={"Country/Region": "Country"},inplace=True)
confirmed_df = pd.melt(confirmed_df,id_vars=['Country','Lat','Long'], var_name='Day', value_name='ConfirmedCount')


recovered_df = pd.read_csv(unquote('https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_recovered_global.csv&filename=time_series_covid19_recovered_global.csv'))
# recovered_df = pd.read_csv('time_series_covid19_recovered_global.csv')
del recovered_df['Province/State']
recovered_df.rename(columns={"Country/Region": "Country"},inplace=True)
recovered_df = pd.melt(recovered_df,id_vars=['Country','Lat','Long'], var_name='Day', value_name='RecoveredCount')

death_df = pd.read_csv(unquote('https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_deaths_global.csv&filename=time_series_covid19_deaths_global.csv'))
# death_df = pd.read_csv('time_series_covid19_deaths_global.csv')
del death_df['Province/State']
death_df.rename(columns={"Country/Region": "Country"},inplace=True)
death_df = pd.melt(death_df,id_vars=['Country','Lat','Long'], var_name='Day', value_name='DeathCount')

finaldf = confirmed_df.merge(recovered_df,on=["Country",'Lat','Long','Day'],how='left').merge(death_df,on=["Country",'Lat','Long','Day'],how='left')
del finaldf['Lat']
del finaldf['Long']

finaldf['Day'] = pd.to_datetime(finaldf['Day'])
group = finaldf.groupby(['Country','Day'])['RecoveredCount','DeathCount','ConfirmedCount'].sum().reset_index().sort_values('Day')
group = group.rename(columns={'RecoveredCount': 'No of recovered'})
group = group.rename(columns={'ConfirmedCount': 'No of confirmed'})
group = group.rename(columns={'DeathCount': 'No of death'})
group['Day'] = group['Day'].astype(str)

dateTimeObj = datetime.now() - timedelta(days = 1)
timestampStr = dateTimeObj.strftime("%Y-%m-%d")

x_high_range = group['No of recovered'].max()
y_high_range = group['No of death'].max()

fig = px.scatter(group,
           x="No of recovered",
           y="No of death",
           size="No of confirmed",
           size_max=60,
           color="Country",
           hover_name="Country",
           animation_frame="Day",
           animation_group="Country",
           log_x=True,
           range_x=[10, x_high_range + 30000],
           range_y=[0, y_high_range + 5000])

# fig.update_layout(title='Corona Spread Analysis across different countries as on ' + timestampStr)
# fig.show()
fig.update_layout(title='Corona Spread Analysis across different countries as on ' + timestampStr,xaxis_showgrid=False, yaxis_showgrid=False)
plotly.offline.plot(fig, filename='Covid-19_Spread.html')
