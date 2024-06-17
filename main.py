import pandas as pd
from dash import Dash,dcc,html
# import numpy as np
import dash_table
import plotly.express as px

sales_df = pd.read_csv('./retail_sales_dataset.csv', parse_dates=['Date'])
sales_df['Month'] = sales_df['Date'].dt.strftime('%B')
product_cat = sales_df.groupby(by='Product Category')['Total Amount'].sum()
by_month = sales_df.groupby(by='Month')['Total Amount'].sum()
print()
slices_color= {
    'Electronics' : 'lightcyan', 
    'Clothing' : 'cyan',
    'Beauty' : 'royalblue'
}
pie_fig = px.pie(sales_df,names='Product Category', values='Total Amount', title="Product sales per category", color_discrete_map={'Electronics':'darkblue','Clothing':'cyan','Beauty':'royalblue'}, color = 'Product Category')

pie_fig.update_layout(
    paper_bgcolor='rgba(0, 0, 0, 0)',
    height=400,
    title_font_color = 'white', 
    legend=dict(
        title_font_color='white'
    )
)

pie_fig.update_traces(
    textfont_color = 'white'
)

bar = px.line(y=by_month.values,x=by_month.index,labels=['Month','Total sales($)'])
grouped_bar = px.his.ventogram(sales_df,x='Month',y='Quantity',color='Product Category',barmode='group')
bar.update_xaxes(title_text='Month', tickangle=45)
bar.update_yaxes(title_text='Total sales($)')
total_sales = sales_df['Total Amount'].sum()
max_sale = sales_df['Total Amount'].max()
sales_count = sales_df['Transaction ID'].count()
top_sales = sales_df[['Customer ID','Product Category','Total Amount','Quantity']].sort_values(by='Total Amount', ascending=False).head(10)
app = Dash(__name__)
app.css.append_css({'external_url': '/assets/styles.css'})
app.layout = html.Main(
    children=[
        html.H3(
            children="Sales Overview", 
            id='title'
            ),
        html.Section(
            id = 'sectionOne',
            children=[
                html.Div(
                    id='secDiv1',
                    children=[
                        html.H3(
                            children="Total Sales"),
                        html.H1(f'${total_sales}')
                    ]
                    ),
                html.Div(
                    id='secDiv2',
                    children=[
                        html.H3(
                            children="Maximum Sale"),
                        html.H2(f'${max_sale}')
                    ]),
                html.Div(
                    id='secDiv3',
                    children=[
                        html.H3(
                            children="Total Number Sales"),
                        html.H1(f'{sales_count}')
                    ]),
                html.Div(
                    id='secDiv4',
                    children=[
                        html.H3(
                            children="Highest Sales(Month)"),
                        html.H1(f'{by_month.idxmax()}:{by_month.max()}')
                    ]),
            ]
        ), 
        html.Section(
            id='sectionTwo', 
            children=[
                html.Div(
                    id='topTable', 
                    children=[
                        dash_table.DataTable(
                            columns= [{'name': i, 'id': i} for i in top_sales.columns],
                            data = top_sales.to_dict('records'),
                            style_header= {'backgroundColor':'#fff','color': '#1A2238','textAlign':'left','padding': '10px'}, 
                            style_cell={'padding':'10px','backgroundColor':'#F0EFEF'},
                            page_size=7
                        )
                    ]
                ),
                html.Div(
                    id='pieChart',
                    children=[
                        dcc.Graph(
                            figure=pie_fig, 
                            style={'height': '100%'},                            
                        )
                    ]
                )
            ]
        ),
        html.Section(
            children=[
                html.Div(
                    dcc.Graph(
                        figure=grouped_bar
                    )
                )
            ]
        )
    ]
)
if __name__ == '__main__':
    app.run_server(debug=True)