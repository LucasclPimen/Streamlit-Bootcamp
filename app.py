import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import webbrowser

# Importando as funções

from functions import *

# Configurações básicas

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide")

st.markdown("<h1 style='text-align: center;'>📊Sales Report - Adidas</h1>", unsafe_allow_html=True)

# Sidebar

# Centralizando os botões horizontalmente
st.markdown(
    """
    <style>
    .stButton > button {
        display: block;
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .stDownloadButton > button {
        display: block;
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.sidebar.markdown("<h1 style='text-align: center;'>👾Bootcamp - Streamlit </h1>", unsafe_allow_html=True)

st.sidebar.write('')

btn = st.sidebar.link_button('Liga de Data Science', 'https://linktr.ee/ligadsunicamp?utm_source=linktree_profile_share&ltsid=bcdbacaf-d0b6-48f7-9aa3-897fac981740')

st.sidebar.write("")

@st.cache_data # Previne que a operação seja executada sempre que o programa for re-executado
def convert_df(df):
    return df.to_csv().encode('utf-8')
download = st.sidebar.download_button('Download data as CSV', data = convert_df(df), file_name='Adidas.csv', mime = 'text/csv')

st.sidebar.divider()

region = st.sidebar.selectbox('Region', df['Region'].unique())
state = st.sidebar.selectbox('State', df['State'].unique())
product = st.sidebar.selectbox('Product', df['Product'].unique())
retailer = st.sidebar.selectbox('Retailer', df['Retailer'].unique())

st.divider()



# Dashboard
with st.container():

    col1, col2 = st.columns([5,5])
    with col1.container(border=True):

        st.markdown("<h3 style='text-align: center;'>Consolidated Data </h3>", unsafe_allow_html=True)
        st.write("")
        st.write("")
        st.markdown("###### All products, regions and retailers", unsafe_allow_html=True)
        subcol1, subcol2 = st.columns([1,1])
        #col1.plotly_chart(state_sales(df),config={'displayModeBar': False}, use_container_width=True)

        subcol1.metric(label = 'Profit', value=f"$ {round(df['Operating Profit'].sum()/1000000,2)} M")
        subcol2.metric(label = 'Sales', value = f"{round(df['Total Sales'].sum()/1000000,2)} M")

        #st.markdown("<br><br>", unsafe_allow_html=True)
        
        st.write("")

        st.markdown("###### By product, region and retailer", unsafe_allow_html=True)
        subcol3, subcol4 = st.columns([1,1])
        subcol3.metric(label = 'Profit', value=f'$ {round(total_profit(df, retailer, product, region)/1000000,3)} M', 
                    delta = f"{round(total_profit(df, retailer, product, region) / df['Operating Profit'].sum() * 100, 2)}%")
        subcol4.metric(label = 'Sales', value = f'{round(total_sales(df, retailer, product, region)/1000,2)} K',
                    delta = f"{round(total_sales(df, retailer, product, region)/df['Total Sales'].sum()*100, 4)}%")    
        
        st.write("")

        st.markdown("""*Note: the green arrow does not represent a positive variation. It just points to the data directly above, meaning that 
                    the the filtered data is equivalent to the percentage (next to the arrow) of the total amount.*""")
        
        st.write("")

        
    with col2.container(border= True):
        st.markdown("<h3 style='text-align: center;'>Sales Over Time </h3>", unsafe_allow_html=True)
        st.plotly_chart(sales_timeseries(df, retailer, product, region), config={'displayModeBar': False}, use_container_width=True)


with st.container(border = True):
    st.markdown("<h3 style='text-align: center;'>Product Sales by State </h3>", unsafe_allow_html= True)
    st.plotly_chart(state_sales_distribution(df, product, retailer), config = {"displayModeBar":False}, use_container_width=True)

col3, col4 = st.columns([1,1])

with col3.container(border = True):
    st.markdown("<h3 style='text-align: center;'>Sales Method </h3 ", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center;'>By State, product and retailer </h6", unsafe_allow_html=True)

    st.plotly_chart(sales_method_distribution(df, product, state, retailer), config = {'displayModeBar': False}, use_container_width= True)

with col4.container(border = True):
    st.markdown("<h3 style='text-align: center;'>Total sales per state", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center;'> No filters </h6", unsafe_allow_html=True)
    st.plotly_chart(state_sales(df), config={'displayModeBar': False}, use_container_width= True) 

with st.container(border=True):
    st.markdown("<h3 style='text-align: center;'>Pareto: Units Sold </h3 ", unsafe_allow_html=True)
    st.plotly_chart(pareto(df), use_container_width=True)
