import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import model_algo as m
#selected bank names with its value
bank=[]
bankname=pd.read_excel(r"Data/BankName.csv.xlsx")
for i in range(0,19):
    b={'label':bankname['name'][i],'value':bankname['csv'][i]}
    bank.append(b)

#initialize
app = dash.Dash(__name__)

#createing web page with dash
app.layout = html.Div([

#logo and banner of app         
    html.Div([
        html.H2("Stock Prediction App"),
        
        html.Img(src="/assets/stock-icon6.png")
    ], className="banner"),
# bank name dropdown container
    html.Div([
        dcc.Dropdown(
        id='demo-dropdown',
        style={'width': '300px'},
        
        options=bank,
        value='BANKINDIA'
    ),
    html.Div(id='dd-output-container')
    ]),
#div for disply the ghraph     
    html.Div([
            dcc.Loading([
        html.Div([
            dcc.Graph(
                id="graph_close",
                figure={
            'data': [ 
                
            ],
            'layout': {
                'plot_bgcolor': 'rgb(26, 47, 66)',
                'paper_bgcolor': 'rgb(26, 47, 66)',
                'font': {
                    'color': 'white'
                    
                },
                
            }
        },
    
            style={'height': '600px'},
 
            )
        ]),

    ],type='graph',style={'padding-top': '250px'})
    ])
],className="background1")
#callback values from web page
@app.callback(dash.dependencies.Output('graph_close', 'figure'),
              
              [dash.dependencies.Input('demo-dropdown', 'value')])
#updating figure function                                      
def update_f(value):

#calling model
    m.model_lstm(value) 
    
#graph    
    data=[]#store the actual and predicted line ghraph
    #acutal value graph
    trace_close=go.Scatter(x=list(m.actual.index),
                       y=list(m.actual['CLOSE']),
                       name="actual close",                       
                       line = dict(
                                   color = 'green',
                                   width = 3,
                                   ))     
    #predicted ghraph                               
    trace_actual=go.Scatter(x=list(m.pred_date.index),
                           y=list(m.pred_date['Predictions']),                                                     
                           name="prdicted close",                           
                           line = dict(
                                   color = 'red',
                                   width = 3,
                                   ))                         
                             
    data.append(trace_close)
    data.append(trace_actual)

    #layout of graph
    layout = dict(
        title=value,
        paper_bgcolor='rgba(26, 47, 66,27)',
        plot_bgcolor='rgba(0, 0, 0,0)',       
        font =dict(family='Sherif',
                               size=16,
                               color = 'white'),
        xaxis=dict(
            title='Date',
            titlefont=dict(               
                size=18,              
            ),
            showline=True, linewidth=2, linecolor='black',
            rangeslider=dict(
            visible=True,
            paper_bgcolor='rgba(26, 47, 66,27)',
            plot_bgcolor='rgba(0, 0, 0,0)',
        ),type='date'
        ),
        yaxis=dict(
            title='Closing Price',
            titlefont=dict(               
                size=18,                
            ),
            gridcolor='#D3D3D3',
            showline=True, linewidth=2, linecolor='black'                        
        )
    )
                    
    return {
        "data": data,
        "layout": layout
        
    }
#running app at http://localhost:8050/     
if __name__== "__main__":
    app.run_server(debug=True,use_reloader=False)
   

     
