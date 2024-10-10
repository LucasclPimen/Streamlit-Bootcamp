import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go


# Importando e preparando a base de dados

df = pd.read_excel('Adidas.xlsx')
df.drop(columns = ['RetailerID'], inplace = True)
df.rename(columns = {'InvoiceDate': 'Invoice Date', 'PriceperUnit': 'Unit Price', 'UnitsSold': 'Units Sold', 'TotalSales': 'Total Sales',
                     'OperatingProfit':'Operating Profit','OperatingMargin':'Operating Margin', 'SalesMethod': 'Sales Method'},
                     inplace= True)

# 1. Funções de dados consolidados: (indicadores)

## Lucro total por Retailer, Produto e Região
def total_profit(df, retailer, product, region):
    df_filtered = df[df['Region'] == region]
    df_filtered_aux = df_filtered[df_filtered['Product'] == product]
    df_filtered_aux_final = df_filtered_aux[df_filtered_aux['Retailer'] == retailer]

    return round(df_filtered_aux_final['Operating Profit'].sum(),3)


## Vendas por Retailer, Produto e Região
def total_sales(df, retailer, product, region):
    df_filtered = df[df['Region'] == region]
    df_filtered_aux = df_filtered[df_filtered['Product'] == product]
    df_filtered_aux_final = df_filtered_aux[df_filtered_aux['Retailer'] == retailer]

    return df_filtered_aux_final['Units Sold'].sum()

# 2. Vendas ao longo do tempo

def sales_timeseries(df, retailer, product, region):
    df_filtered = df[df['Region'] == region]
    df_filtered_aux = df_filtered[df_filtered['Product'] == product]
    df_filtered_aux_final = df_filtered_aux[df_filtered_aux['Retailer'] == retailer]
    df_filtered_aux_final = df_filtered_aux_final.groupby('Invoice Date')['Units Sold'].sum().reset_index()
    
    # Criando o gráfico:

 
    fig = px.line(
        df_filtered_aux_final,
        x="Invoice Date",
        y="Units Sold",
        template = 'plotly_dark',
        hover_data = ['Units Sold'],
        title=f'{product} by {retailer} in {region}',
        #labels = 
    )



    return fig

# 3. Vendas de um produto e Retailer distribuídas por estados
def state_sales_distribution(df, product, retailer):
    df_filtered= df[df['Product'] == product]
    df_filtered_aux = df_filtered[df_filtered['Retailer'] == retailer]

    df_filtered_aux = df_filtered_aux.groupby('State')[['Units Sold', 'Total Sales']].sum().reset_index()

    # Gerando o gráfico:

    fig = go.Figure()
    fig.add_trace(go.Bar(x = df_filtered_aux["State"], y = df_filtered_aux["Total Sales"], name = "Total Sales"))
    fig.add_trace(go.Scatter(x=df_filtered_aux["State"], y = df_filtered_aux["Units Sold"], mode = "lines",
                            name ="Units Sold", yaxis="y2"))
    fig.update_layout(
        title = "Total Sales and Units Sold by State",
        xaxis = dict(title="State"),
        yaxis = dict(title="Total Sales", showgrid = False),
        yaxis2 = dict(title="Units Sold", overlaying = "y", side = "right"),
        template = "plotly_dark",
        legend = dict(x=1,y=1.1)
    )

    return fig


# 4. Pizza de sales method estratificado por produto, estado e retailer

def sales_method_distribution(df, product, state, retailer):
    df_filtered = df[df['State'] == state]
    df_filtered_aux = df_filtered[df_filtered['Product'] == product]
    df_filtered_aux_final = df_filtered_aux[df_filtered_aux['Retailer'] == retailer]

    pie = df_filtered_aux_final['Sales Method'].value_counts()

    # Gerando a Figura
    fig = px.pie(
        pie,
        values='count',
        names=list(pie.index),
        labels= {'Sales Method': 'Sales Method'},
        title=f'{product} by {retailer} in {state}',
        template = 'plotly_dark'
    )

    fig.update_traces(hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percent: %{percent}')

    return fig


# 5. Gráfico de barras com as vendas totais por estado (sem filtros)

def state_sales(df):
    df_filtered = df.groupby('Region')['Total Sales'].sum().reset_index()

    fig = px.bar(
        df_filtered,
        x="Region",
        y="Total Sales",
        title="State Sales",
        template = 'plotly_dark'
    )
    return fig


# 6. Gráfico de Pareto (sem filtros)

def pareto(df):
    df_pareto = pd.DataFrame(df.groupby('Product')['Units Sold'].sum())
    df_pareto.reset_index(inplace = True)
    df_pareto.sort_values('Units Sold', ascending= False, inplace= True)
    df_pareto['Cumulative Sales'] = df_pareto['Units Sold'].cumsum()
    df_pareto['Relative Cumulative Sales'] = df_pareto['Cumulative Sales']/(df_pareto['Units Sold'].sum())


    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_pareto['Product'],
        y=df_pareto['Units Sold'],
        name='Units Sold',

    ))
    fig.add_trace(
        go.Scatter(
            x=df_pareto['Product'],
            y=df_pareto['Relative Cumulative Sales'],
            name = 'Relative Cumulative Sales',
            mode = 'lines',
            line=dict(),
            yaxis='y2' 
        )

    )

    fig.update_layout(
        title = "Pareto: Product versus unit sold",
        xaxis = dict(title="State"),
        yaxis = dict(title="Total Sales", showgrid = False),
        yaxis2 = dict(title="Units Sold", overlaying = "y", side = "right"),
        template = "plotly_dark",
        legend = dict(x=1,y=1.1)
    )

    return fig




