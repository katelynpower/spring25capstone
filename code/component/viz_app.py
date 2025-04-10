from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

file_path = 'C:/Users/power/Desktop/Classes/DATS4001/25-spring-KPower/data/cleaned_vaccine_sentiment_data.csv'
df= pd.read_csv(file_path)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

page_title = html.H2(f"Vaccination Sentiment Visualization", className="bg-secondary text-white p-2 mb-4") 

info = dbc.Accordion([
    dbc.AccordionItem(dcc.Markdown("info"), title="About" ),
    dbc.AccordionItem(dcc.Markdown("info"), title="Data Source")
],  start_collapsed=True)

vaccine_dropdown = dcc.Dropdown(
    id='vaccinedrop',
    options=[{'label': vaccine, 'value': vaccine} for vaccine in df['vaccine'].unique()],
    clearable=False,
    value='COVID-19',
    className='m-2'
)
demo_dropdown = dcc.Dropdown(
    id='demodrop',
    options=[{'label': demo, 'value': demo} for demo in df['demo_group'].unique()],
    clearable=False,
    value='Age',
    className='m-2'
)
month_dropdown = dcc.Dropdown(
    id='monthdrop',
    options=[{'label': month, 'value': month} for month in df['month_label'].unique()],
    clearable=True,
    className='m-2'
)

selects = dbc.Card(dbc.CardBody([html.Div("Select Vaccine, Demographic Type, and Time Period"),vaccine_dropdown, demo_dropdown, month_dropdown], className='bg-light',), className='mb-4')


bargraph_motivators = dcc.Graph(id='bargraph_motivators', style={'height': '350px'})
bargraph_concerns = dcc.Graph(id='bargraph_concerns', style={'height': '350px'})
treemap = dcc.Graph(id='treemap')
heatmap = dcc.Graph(id='heatmap')

'''
app.layout = html.Div([
                       dbc.Row([page_title,
                           dbc.Col([selects, info], width=3),
                           dbc.Col([dbc.Card(dbc.CardBody([bargraph_motivators, bargraph_concerns, heatmap]))], width=9)]),
                        dbc.Row([treemap])
                       ], style={'padding': '10px 20px 20px 20px'})'''

app.layout = html.Div([
    dbc.Row([page_title,selects,
        dbc.Row([dbc.Col([bargraph_motivators, bargraph_concerns], width=8), dbc.Col([heatmap], width=4)], style={'height': '700px'}),
        dbc.Row([treemap])
    ])])


@app.callback(
    Output('bargraph_motivators', 'figure'),
    Input('vaccinedrop', 'value'),
    Input('demodrop', 'value'),
    Input('monthdrop', 'value')
)
def update_graph(selected_vaccine, selected_demo, selected_month): 
    filtered_df = df[df['vaccine'] == selected_vaccine]
    filtered_df = filtered_df[~filtered_df['indicator_category'].isin(['Other', 'Nothing'])]
    filtered_df = filtered_df[filtered_df['demo_group'] == selected_demo]
    filtered_df= filtered_df[filtered_df['dashboard_type']=='motivators']
    if selected_month:
        filtered_df = filtered_df[filtered_df['month_label'] == selected_month]
    fig = px.bar(filtered_df, x='indicator_category', y='estimate', color='demo_category', barmode='group',
                 labels={'demo_category':'Demographic'},custom_data=['month_label'])
    fig.update_traces(hovertemplate='%{customdata[0]}<br>%{x}: %{y:.2f}%')
    fig.update_layout(title='Motivators for Vaccination', xaxis_title=None, yaxis_title='Percent', xaxis={'categoryorder':'total ascending'}, template='plotly_white',legend={'yanchor': 'top', 'y': 1.2},
        margin={'b': 40, 't': 80})
    return fig

@app.callback(
    Output('bargraph_concerns', 'figure'),
    Input('vaccinedrop', 'value'),
    Input('demodrop', 'value'),
    Input('monthdrop', 'value')
)
def update_graph(selected_vaccine, selected_demo, selected_month): 
    filtered_df = df[df['vaccine'] == selected_vaccine]
    filtered_df = filtered_df[~filtered_df['indicator_category'].isin(['Other', 'No concerns or issues'])]
    filtered_df = filtered_df[filtered_df['demo_group'] == selected_demo]
    filtered_df= filtered_df[filtered_df['dashboard_type']=='concerns/issues']
    if selected_month:
        filtered_df = filtered_df[filtered_df['month_label'] == selected_month]
    fig = px.bar(filtered_df, x='indicator_category', y='estimate', color='demo_category', barmode='group',
                 labels={'demo_category':'Demographic'},custom_data=['month_label'])
    fig.update_traces(hovertemplate='%{customdata[0]}<br>%{x}: %{y:.2f}%')
    fig.update_layout(title='Concerns about Vaccination', xaxis_title=None,yaxis_title='Percent', xaxis={'categoryorder':'total ascending'}, template='plotly_white',legend={'yanchor': 'top', 'y': 1.2},
        margin={'b': 40, 't': 80})
    return fig

@app.callback(
    Output('heatmap', 'figure'),
    Input('vaccinedrop', 'value'),
    Input('demodrop', 'value'),
    Input('monthdrop', 'value')
)
def update_graph(selected_vaccine, selected_demo, selected_month):
    filtered_df = df[df['vaccine'] == selected_vaccine]
    filtered_df = filtered_df[~filtered_df['indicator_category'].isin(['Other', 'No concerns or issues'])]
    filtered_df = filtered_df[filtered_df['demo_group'] == selected_demo]
    if selected_month:
        filtered_df = filtered_df[filtered_df['month_label'] == selected_month]
    fig = px.density_heatmap(filtered_df, x='indicator_category', y='demo_category', z='estimate',labels={'estimate':'Estimate (%)'}, color_continuous_scale=[(0, "#636EFA"), (1, "#EF553B")])
    fig.update_layout(title='Demographic vs. Sentiment Heatmap', xaxis_title=None, yaxis_title=None, template='plotly_white', height=600)
    return fig

@app.callback(
    Output('treemap', 'figure'),
    Input('vaccinedrop', 'value'),
    Input('demodrop', 'value'),
    Input('monthdrop', 'value')
)
def update_graph(selected_vaccine, selected_demo, selected_month):
    filtered_df = df[~df['indicator_category'].isin(['Other', 'No concerns or issues', 'Nothing'])]
    fig = px.treemap(filtered_df, path=[px.Constant('Vaccine Sentiment Estimates'),'demo_group','demo_category','indicator_category','vaccine','month_label'], values='estimate',custom_data=['month_label', 'indicator_category', 'estimate'], 
                     color='dashboard_type', color_discrete_map={'motivators':'#636EFA','concerns/issues':'#EF553B'})
    fig.update_traces(root_color="lightgrey", hovertemplate="<b>%{label}</b><br>%{parent}<br>Estimate: %{value:.2f}%<extra></extra>")
    return fig



if __name__ == '__main__':
    app.run(debug=True)