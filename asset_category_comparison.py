import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, dash_table, Input, Output
from preprocessing import get_assets

assets = get_assets()

aggregate = {
    'Last Sale Total Price': 'mean',
    'Asset Favorites': 'sum',
    'Num Sales': 'sum'
}

category_comparison = assets.groupby('Asset Category')[['Last Sale Total Price', 'Asset Favorites', 'Num Sales']]\
    .agg(aggregate).sort_values('Num Sales', ascending=False).reset_index()
category_comparison['Asset Category'] = category_comparison['Asset Category'].str.replace('&', ' & ')
category_comparison['Asset Category'] = category_comparison['Asset Category'].str.replace('-', ' ')
category_comparison['Asset Category'] = category_comparison['Asset Category'].str.title()
category_comparison['Last Sale Total Price'] = category_comparison['Last Sale Total Price']//10e15

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    children=[
        html.H1('NFT Asset Category Comparison'),
        dcc.Dropdown(
            options = ['Last Sale Total Price', 'Asset Favorites', 'Num Sales'],
            value = 'Last Sale Total Price',
            id='asset-category-compare-choice'
        ),
        dcc.Graph(id='asset-category-compare-graph')
    ]
)

@app.callback(
    Output(component_id='asset-category-compare-graph', component_property='figure'),
    Input(component_id='asset-category-compare-choice', component_property='value'),
)
def update_graph(choice):
    fig = px.bar(
        data_frame = category_comparison.sort_values(choice, ascending=False), 
        x='Asset Category', 
        y=choice,
        color='Asset Category'
    )
    fig.update_layout(
        yaxis_title= f"Sum of {choice}" if choice!='Last Sale Total Price' else f"Mean of {choice} (Quadrillion)", 
        showlegend=False
    )
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)