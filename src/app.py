import dash
import plotly.graph_objects as go
from dash import dcc, html, callback
from dash.dependencies import Output, Input
import plotly.express as px 
import dash_bootstrap_components as dbc
import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import dash_player as dp
from dash_bootstrap_templates import load_figure_template
import plotly.io as pio

# Create a Plotly layout with the desired dbc template
load_figure_template(["minty", "minty_dark","solar"])
layout = go.Layout(template= pio.templates["solar"])

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

#"""
#Defining a data range
start  = dt.datetime(2023,1,1)
end    = dt.datetime(2023,12,31)

#Defining wich stocks we want, and from which web are we getting them from (Stooq)
stocks = web.DataReader(
    ["BABA","ETSY","SWK","APPN","W","SNAP"],
    "stooq",
    start=start,
    end=end)

#Reshape Dataframe
stocks = stocks.stack().reset_index()

#The next lines will download the Df as a CSV file in a local environment. 
#This approach prevents overloading the API with requests every time we run the script, which could potentially lead to getting banned from the API
# -----------> Unhash the line 38 and 40 to enable saving the csv to a local environment, and reading it from it <-------------
#stocks.to_csv("mystocks.csv", index=False)
#Reading the local file 
#stocks = pd.read_csv(r"Dash_apps\Stocks_reader\mystocks.csv")
#"""

title= dbc.Col(
    html.H1("Market Watch: Dynamic Stock Tracker",
            style=  {'textAlign': 'center',
               '    color': '#457B9D',
                    #'font-family': 'Trebuchet MS, sans-serif'
                    }
            ),
            width = 12
            )

Cd_dpdw = dcc.Dropdown(     id = "candle-dpdn",
                    multi   = False,
                    value   = sorted(stocks["Symbols"].unique())[1], 
                    options = [{"label": x,"value": x} for x in sorted(stocks["Symbols"].unique())]
                    )
Candlestick = dcc.Graph(    id = "candle-stck",
                         figure = {}
                        )
    
lines_dpdn = dcc.Dropdown(  id = "lines-dpdn",
                    multi   = True,
                    value   = sorted(stocks["Symbols"].unique())[:4], 
                    options = [{"label": x,"value": x} for x in sorted(stocks["Symbols"].unique())]
                    )
Lineschart = dcc.Graph(     id = "lines-stck",
                            figure = {}
                )

line_dpdn = dcc.Dropdown(   id = "line-dpdn",
                    multi   = False,
                    value   = sorted(stocks["Symbols"].unique())[1], 
                    options = [{"label": x,"value": x} for x in sorted(stocks["Symbols"].unique())]
                    )
Linechart = dcc.Graph(      id = "line-stck",
                            figure = {}
                )

dates_histogram = dcc.DatePickerSingle( id ='histo-date',
                                min_date_allowed= dt.datetime(2023,1,1),
                                initial_visible_month=dt.date(2023, 8, 5),
                                max_date_allowed= dt.datetime(2023,12,31),
                                #date= dt.datetime(2023, 3, 2)
                        )
chklst_histogram = dcc.Checklist(       id ='histo-chklst', 
                        value     = stocks["Symbols"].unique()[0:5],
                        options   = [{"label": x,"value": x} for x in sorted(stocks["Symbols"].unique())],
                        inline    = True,
                        inputStyle={"margin-left":"6px", "margin-right": "2px"}
                        )
Histogram = dcc.Graph(      id = "histogram-stk",
                            figure = {}
                      )
def weekend_tracker(stock_date):
    date_obj = dt.datetime.strptime(stock_date, "%Y-%m-%d")
    # Check if the day of the week is either Saturday (5) or Sunday (6)
    if date_obj.weekday() >= 5:
        return True
    else:
        return False

sources = html.Div(
    [
        html.P("By Eduardo Salvador Rocha"),
        html.Label(
            [
                "Links: ",
                html.A(
                    "Eduardo's GitHub|  ",
                    href="https://github.com/Salvatore-Rocha",
                    target="_blank",
                ),
                html.A(
                    "Code (.py file) |   ",
                    href="https://github.com/Salvatore-Rocha/My-Dash-Apps/blob/f22f6ab40598472d71012e9a2e9111d7b7dfb508/Dash_apps/Styling/Styling_stocks_plots.py",
                    target="_blank",
                ),
            ]
        ),
    ]
)

app =  dash.Dash(__name__, 
                 external_stylesheets= [dbc.themes.SOLAR, dbc.icons.FONT_AWESOME, dbc_css],)
server = app.server
app.layout = dbc.Container([
    dbc.Row([ #Title
            title
            ]),
    html.Br(),
    dbc.Row([ #Subtitle + Histogram
        dbc.Col([ 
            html.H2("A dashboard to analyzse Stock Trends"),
            html.P("This dashboard was created using the Dash app and Python libraries to download and parse stock data into \
                    dataframes. It's designed to highlight the interactivity provided by the Dash app for plots. The stocks and dates \
                    were chosen arbitrarily and can be easily switched in the main code. You can find the link to the file at the bottom.")
                ],
                width = 3
                ),
        dbc.Col([ #Dropdown +  Date picker for Histogram
            html.H4("1️⃣ Select a Date", className="card-title"),
            html.H6("Dates are only availables for the year 2023 and should not fall on a weekend", className="card-subtitle1"),
            dates_histogram,
            html.H4("2️⃣ Select Stocks", className="card-title"),
            html.H6("Please choose the stocks for which you’d like to view the closing values in the histogram", className="card-subtitle"),
            html.Br(),
            chklst_histogram
            ]),
        dbc.Col([ #Histogram Plot
            Histogram
                ],
                width = 6
                )
            ]),
    html.Br(),
    dbc.Row([ #Videoplayer + Candlestick plot
        dbc.Col([
                html.H4("But what are stocks, anyway?🪬👅🪬"),
                dp.DashPlayer(id="player",
                            url="https://www.youtube.com/watch?v=p7HKvqRI_Bo",
                            controls=False,
                            width="100%",
                                 )
                ], 
                width= 5),
        dbc.Col([
                html.H4("Select a stock to see its behavior"),
                Cd_dpdw,
                Candlestick
                ], 
                width= 7),
            ]),
    dbc.Row([ #Text for line plots
        dbc.Col([html.H5("➡️ Comparing how different stocks perform helps investors decide which ones to buy or sell.\
                        It also helps them manage risks and make sure their investment portfolio is balanced and set up for success."),
                 html.H5("🟩 Below, you'll find plots comparing the behavior of a single stock versus multiple stocks throughout the entire year of 2023.")],
                width= 7)
            ]),
    dbc.Row([ #Single line + multiple lines plot
            dbc.Col([
                line_dpdn,
                Linechart,
                ], width= 6),
            dbc.Col([
                lines_dpdn,
                Lineschart,
                ], width= 6),
            ],
            className="g-0" #this is the new version of "no_gutters" which is deprecated
            ),
    dbc.Row([ #Links
            sources
            ])
], 
fluid = True,
className="dbc"
)

# Histogram chart - Multiple
@callback(
    Output("histogram-stk", "figure"),
    Input("histo-chklst", "value"),
    Input("histo-date","date")
        )
def histogram_plot(selected_stonks,date_set):
        dff = stocks[stocks["Symbols"].isin(selected_stonks)]
        if date_set == None:
            date_set = '2023-12-29'
        dff = dff[dff['Date']==date_set]      
        fig = px.histogram(dff, 
                           x='Symbols',
                           y='Close',
                           color= "Symbols",
                           text_auto= True,
                           template= "solar"
                           )
        if weekend_tracker(date_set) == True:
            fig.update_layout(title_text=f'Cannot show data, Date -> {date_set} <- falls on a weekend')
        else:
            fig.update_layout(title_text=f'Closing Values | Data shown is from the Date {date_set}')
        return fig

# Line chart - Single
@callback(
    Output("line-stck", "figure"),
    Input("line-dpdn", 'value')
        )
def single_line_plot(selected_stonk):
        dff = stocks[stocks["Symbols"] == selected_stonk]
        fig = px.line(dff, 
                    x="Date",
                    y="Close",
                    color= "Symbols",
                    hover_data=["Open","Close","High","Low"],
                    template= "solar"
                    )
        return fig

# Line chart - Multiple
@callback(
    Output("lines-stck", "figure"),
    Input("lines-dpdn", "value")
        )
def multiple_lines_plot(selected_stonks):
        dff = stocks[stocks["Symbols"].isin(selected_stonks)]
        fig = px.line(dff, 
                    x="Date",
                    y="Close",
                    color= "Symbols",
                    hover_data=["Open","Close","High","Low"],
                    template= "solar"
                    )
        return fig
    
# Candlestick chart - Single
@callback(
    Output("candle-stck", "figure"),
    Input("candle-dpdn", 'value')
        )
def candlestick_plot(selected_stock):
        dff = stocks[stocks["Symbols"] == selected_stock]      
        fig = go.Figure(data=[go.Candlestick(x=dff['Date'],
                open=dff['Open'],
                high=dff['High'],
                low=dff['Low'],
                close=dff['Close'],
                increasing_line_color= 'cyan', 
                decreasing_line_color= 'gray',)],
                layout= layout
                )
        fig.update_layout(title_text=f'Candlestick chart for Stock {selected_stock}')
        return fig

if __name__=='__main__':
    app.run_server(debug=True)