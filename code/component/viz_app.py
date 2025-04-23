from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import os

file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'cleaned_vaccine_sentiment_data.csv')
df= pd.read_csv(file_path)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

page_title = html.Div(style={"backgroundColor": "#636EFA"},children=html.H2(f"Vaccination Sentiment Visualization", className="text-white p-2 mb-0", style={"padding":"10px 20px"}))

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
    value='December 2024/January 2025',
    className='m-2'
)

selects = dbc.Card(dbc.CardBody([html.P("Select Vaccine, Demographic Type, and Time Period", className='mb-0'),
                                 vaccine_dropdown, demo_dropdown, month_dropdown], className='bg-light'))

cite = dbc.Card(dbc.CardBody([
    html.P([
        "Data Source: ",
        html.A(
            "Vaccination Concerns, Issues, and Motivators",
            href="https://data.cdc.gov/Vaccinations/Vaccination-Concerns-Issues-and-Motivators-RespVax/94wp-9pid",
            target="_blank"
        ),
        " provided by the National Center for Immunization and Respiratory Diseases"],
        className='mb-0'),
    html.P("Created by: Katelyn Power", className='mb-0')
], className='bg-light'))

bargraph_motivators = dcc.Graph(id='bargraph_motivators', style={'height': '350px'})
bargraph_concerns = dcc.Graph(id='bargraph_concerns', style={'height': '350px'})
treemap = dcc.Graph(id='treemap')
heatmap = dcc.Graph(id='heatmap')

app.layout = html.Div([
    dbc.Row([page_title,selects,
        dbc.Row([dbc.Col([bargraph_motivators, bargraph_concerns], width=7), dbc.Col([heatmap], width=5)], style={'height': '700px'}),
        dbc.Row([treemap])]),cite], style={'transform': 'scale(0.75)','transformOrigin': 'top left',  'width': '133.33%', 'height': '133.33%'}
    )


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
        margin={'b': 40, 't': 80, 'l': 40, 'r': 0})
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
        margin={'b': 40, 't': 80, 'l': 40, 'r': 0})
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
    x_order = (
        filtered_df.groupby('indicator_category')['estimate']
        .mean()
        .sort_values()
        .index.tolist()
    )
    fig = px.density_heatmap(filtered_df, x='indicator_category', y='demo_category', z='estimate', category_orders={'indicator_category': x_order}, labels={'estimate':'Estimate (%)'}, color_continuous_scale=[(0, "#636EFA"), (1, "#EF553B")])
    fig.update_traces(hovertemplate='%{x}<br>Demographic: %{y}<br>Estimate: %{z}%<extra></extra>')
    fig.update_layout(title='Demographic vs. Sentiment Heatmap', xaxis_title=None, yaxis_title=None, xaxis=dict(tickfont=dict(size=11)), yaxis=dict(tickfont=dict(size=10)),
                      margin=dict(l=0, r=0, t=80, b=0),template='plotly_white', height=600, coloraxis_colorbar=dict(thickness=10,tickfont=dict(size=10)))
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
    fig.update_layout(margin={'b': 20, 't': 40, 'l': 20, 'r': 0})
    return fig



if __name__ == '__main__':
    app.run(debug=True)
