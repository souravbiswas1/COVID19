import pandas as pd
import plotly
# import plotly_express as px
import plotly.express as px
import chart_studio.plotly as py
import chart_studio as cs
from urllib.parse import unquote
from datetime import date
from datetime import datetime
from datetime import timedelta

df = pd.read_csv(unquote('https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2Fnytimes%2Fcovid-19-data%2Fmaster%2Fus-states.csv&filename=us-states.csv'))
df['fips'] = df['fips'].astype(str)
df['date'] = pd.to_datetime(df['date'])

df_state = df.groupby(['state','fips','date'])['cases','deaths'].sum().reset_index().sort_values('date')

df_state = df_state.rename(columns = {'state': 'State'})
df_state = df_state.rename(columns = {'fips': 'FIPS'})
df_state = df_state.rename(columns = {'date': 'Date'})
df_state = df_state.rename(columns = {'cases': 'Confirmed cases'})
df_state = df_state.rename(columns = {'deaths': 'No of deaths'})

dateTimeObj = datetime.now() - timedelta(days = 2)
timestampStr = dateTimeObj.strftime("%Y-%m-%d")

group_state = df_state[(df_state['Date'].between('2020-03-28',timestampStr))]
group_state['Date'] = group_state['Date'].astype(str)

x_high_range = group_state['Confirmed cases'].max()
y_high_range = group_state['No of deaths'].max()

fig = px.scatter(group_state,
           x="Confirmed cases",
           y="No of deaths",
           size="No of deaths",
           size_max=60,
           color="State",
           hover_name="FIPS",
           animation_frame="Date",
           animation_group="State",
           log_x=True,
           range_x=[800, x_high_range + 100000],
           range_y=[0, y_high_range + 2000])

# fig.update_layout(title='Corona Spread Analysis across different states of US as on ' + timestampStr)
# fig.show()
fig.update_layout(title='Corona Spread Analysis across US states as on ' + timestampStr,xaxis_showgrid=False, yaxis_showgrid=False)
plotly.offline.plot(fig, filename='Covid-19_Spread_US.html')
