import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import dash_table



df = pd.read_csv('owid-covid-data.csv')

#Data cleanning
df.dropna(inplace=True)
df['total_deaths'] = df['total_deaths'].fillna(0)
df['new_deaths'] = df['new_deaths'].fillna(0)
df["date"] = pd.to_datetime(df["date"])


#Dân số
popu = df.groupby(['location','population']).max()
popu.reset_index(inplace=True)
popu = popu.iloc[:,[0,1]]
popu.head()


#Số ca nhiễm và chết theo khu vực
region = df.groupby(['location']).max()
region2 = region.groupby('continent').sum()
region2.reset_index(inplace=True)

reg_case = region2.iloc[:,[0,1]].sort_values('total_cases', ascending=False)
reg_death = region2.iloc[:,[0,3]].sort_values('total_deaths', ascending=False)


#Số ca nhiễm và chết toàn cầu
global_case = reg_case['total_cases'].sum()
global_death = reg_death['total_deaths'].sum()

glo_case = []
glo_case.append(global_case)
glo_case2 = pd.DataFrame(glo_case,columns=['Global_case'])
glo_case2['Global_case'] = glo_case2['Global_case'].map('{:,.0f}'.format)

glo_death = []
glo_death.append(global_death)
glo_death2 = pd.DataFrame(glo_death,columns=['Global_death'])
glo_death2['Global_death'] = glo_death2['Global_death'].map('{:,.0f}'.format)


#Số ca nhiễm và chết 7 ngày gần đây 
df_day = df.loc[(df['date'] >= '2021-02-10') & (df['date'] <= '2021-02-16')]
day_case = df_day['new_cases'].sum()
day_death = df_day['new_deaths'].sum()
day_death2 = pd.DataFrame([day_death],columns=['day_death'])
day_death2['day_death'] = day_death2['day_death'].map('{:,.0f}'.format)
day_case2 = pd.DataFrame([day_case],columns=['day_case'])
day_case2['day_case'] = day_case2['day_case'].map('{:,.0f}'.format)


#Map
region = df.groupby('location').max().sort_values('total_cases',ascending=False)
region.reset_index(inplace=True)


#Table
rank1 = region.sort_values('total_cases',ascending=False)
rank2 = rank1.iloc[0:13,[0,4,6]]

rank = []
for i in range(1,14):
    rank.append(i)

rank2['Rank'] = rank
rank3 = rank2.iloc[:,[3,0,1,2]]
rank3['total_cases'] = rank3['total_cases'].map('{:,.0f}'.format)
rank3['total_deaths'] = rank3['total_deaths'].map('{:,.0f}'.format)


#df3
df2 = df.groupby('date').sum()
df2.reset_index(inplace=True)
df3 = df2

df4 = df3[(df3['date'] >= '2021-02-09') & (df3['date'] <= '2021-02-16')]

external_stylesheets = [
    {
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = 'Covid-19 Dashboard'

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children='Coronavirus COVID-19  Global Dashboard - Update 02/2021', className='header_title'),
                html.P(children='By: Huy Nguyen', className='header_sub'),
            ],
            className = 'header'
        ),
        html.Div(
            children=[
               dbc.Row(
            [
                dbc.Col(html.Div(
                    children=[
                    html.P('Total Case',className='P2'),
                    html.P(glo_case2['Global_case'], className='P1')
                    ]
                ), md=3,className='card'),
                dbc.Col(html.Div(
                    children=[
                    html.P('Recent case - 7day ',className='P2'),
                    html.P(day_case2['day_case'],className='P1')
                    ]
                ), md=3,className='card'),
                dbc.Col(html.Div(
                    children=[
                    html.P('Total Death',className='P2'),
                    html.P(glo_death2['Global_death'], className='P1')
                    ]
                ), md=3,className='card'),
                dbc.Col(html.Div(
                    children=[
                    html.P('Recent death - 7day',className='P2'),
                    html.P(day_death2['day_death'], className='P1')
                    ]
                ), md=3,className='card'),
            ],
            className='Row1',
        ),
            ]
        ),
    
     html.Div(
            children=[
               dbc.Row(
                        [
                dbc.Col(html.Div(
                        children=[
                        dash_table.DataTable(
                                    id='table',
                                    columns=[{"name": i, "id": i} 
                                            for i in rank3.columns],
                                    data=rank3.to_dict('records'),
                                    style_cell={'textAlign':'center', 'backgroundColor': '#12151F', 'font-family':'Arial, Helvetica, sans-serif'},
                                    style_header={'backgroundColor':'#181c27','fontWeight': 'bold','border':'0px','color':'#05F4B7','font-size':'12px'},
                                    style_data={'backgroundColor':"#12151F", 'color':'#E1E2E2', 'border':'0px','font-size':'12px'},
                                    style_data_conditional=[
                                                                {
                                                                'if': {'row_index': 'odd'},
                                                                'backgroundColor': '#181c27',
                                                                }
                                                            ],
                                            ),
    
                                ]
                            ),className='card2', md=4),
                            dbc.Col(html.Div(   
                                children=[
                                        dcc.Graph(
                                            figure={
                                                'data':[
    
                                                    {
                                                        'x':df3['date'],
                                                        'y':df3['new_cases'],
                                                        'label': 'new_cases',
                                                        'name': 'new_cases',
                                                        'type':'bar',
                                                        'marker':{'color':'#05F4B7'},
                                                        
                                                    },
                                                   ]
                                                ,
                                                'layout':
                                                {
                                                    "title": {"text": "New cases time series", "x": 0.055, "xanchor": "left"},
                                                    'plot_bgcolor': '12151F',
                                                    'paper_bgcolor' :'#12151F',
                                                    'font':{
                                                        'color':'#E1E2E2'
                                                    },
                                                    'margin':{
                                                        't':50,
                                                        'b':45,
                                                        # 'l':100,
                                                        # 'r':65
                                                    },
                                                }
                                            }
                                        ),
        
                                ]
                            ), className='card3')
                        ],
                    ),
                ]
            ),
        html.Div(
            children=[
                dbc.Row(
                    children=[dbc.Col( children=[html.Div(children=[
                             dcc.Graph(
                                            figure={
                                                'data':[
                                                    {
                                                        'x':df4['date'],
                                                        'y':df4['new_deaths'],
                                                        # 'label': 'total_cases',
                                                        'name': 'new_deaths',
                                                        'type':'line',
                                                        'marker':{'color':'#05F4B7'},
                                    
                                                    },
                                                   ]
                                                ,
                                                'layout':
                                                {
                                                    "title": {"text": "Number of deaths within the last 7 days", "x": 0.075, "xanchor": "left"},
                                                    'plot_bgcolor': '12151F',
                                                    'paper_bgcolor' :'#12151F',
                                                    'font':{
                                                        'color':'#E1E2E2'
                                                    },
                                                    'margin':{
                                                        't':60,
                                                        'b':45,
                                                        # 'l':30,
                                                        'r':0
                                                    },
                                                }
                                            }
                                        )
                    ])], className='card3', md=7),
                    dbc.Col(html.Div(children=[
                        dcc.Graph(
                                        figure={
                                                'data':[
                                                    {
                                                        'values':reg_case['total_cases'].head(),
                                                        'labels': reg_case['continent'].head(),
                                                        # 'names': reg_case['continent'].head(),
                                                        'type':'pie',
                                                        'marker':{'colors':['#277A66','#05F4B7','#50FBD0','#3FE0A6','#1CC794']},
                                                        'hole':0.7,
                                                        'textinfo':'value+label',
                                                        'textposition':'outside'

                                                    },
                                                   ]
                                                ,
                                                'layout':
                                                {
                                                    "title": {"text": "Total case by region", "x": 0.34, "xanchor": "left"},
                                                    'plot_bgcolor': '#12151F',
                                                    'paper_bgcolor' :'#12151F',
                                                    'font':{
                                                        'color':'#E1E2E2',
                                                        'font-size':'12px'
                                                    },
                                                    'margin':{
                                                        't':60,
                                                        'b':45,
                                                        'l':70,
                                                        # 'r':0,
                                                    },
                                                    'legend':
                                                    {
                                                    'orientation':'h',
                                                    'xanchor':'center', 'x':0.5, 'y': -0.07,
                                                    }
                                                }
                                            }      
                        )
                    ]),className='card4')
                    ])
            ]
        ),

    ]
)



if __name__ == "__main__":
    app.run_server(debug=True)
