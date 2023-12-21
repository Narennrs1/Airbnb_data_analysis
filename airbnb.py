#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#:Important package to be import:
import pandas as pd 
import pymongo
import csv
import numpy as np
import plotly_express as px
import matplotlib.pyplot as plt
import collections
from collections import Counter
import plotly.graph_objects as go
import seaborn as sns
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import warnings
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#:PAGE STEPUP:
warnings.filterwarnings('ignore')

st.set_page_config(page_title="AIRBNB.Inc DATA ANALYSIS",
                   layout="wide",
                   page_icon="🧊",
                   initial_sidebar_state='auto'
                   )
image1=Image.open("D:\DTM9\CAP-4\Airbnb_data_analysis\icons\Airbnb_icon .png")
st.image(image1)

if st.session_state.get('switch_button', False):
    st.session_state['menu_option'] = (st.session_state.get('menu_option',0) + 1) % 3
    manual_select = st.session_state['menu_option']
else:
    manual_select = None

with st.sidebar:    
    selected = option_menu("Main menu", ["Home", "Data Exploration", 'About'], 
        icons=['app-indicator', 'file-bar-graph-fill', 'person-lines-fill'],
        manual_select=manual_select, key='menu_4')
st.button(f":red[Switch Tab] {st.session_state.get('menu_option',1)}", key='switch_button')
selected
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#:HOME:
df=pd.read_csv("D:\DTM9\CAP-4\Airbnb_data_analysis\AirBnB01.csv")
if selected=="Home":
    st.subheader(":red[AIRBNB.Inc Data Analysis]")

    df=df.rename(columns={"lati":"lat","longi":"lon"})
    st.map(df)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#:Data Exploration:
if selected=="Data Exploration":
    st.write("#### Kindly choose your preferred output parameter from the list of option below")
    cl1,cl2,cl3=st.columns([1,2,1])
    with cl1:
        country=st.multiselect("Select The Desire Country",sorted(df['Country'].unique()))
        if not country:
            df1=df.copy()
        else:
            df1=df[df['Country'].isin(country)]
    with cl2:
        pro_type=st.multiselect("Select The Desire Property_type",sorted(df['Property_type'].unique()))
        if not pro_type:
            df2=df1.copy()
        else:
            df2=df1[df1['Property_type'].isin(pro_type)]
    with cl3:
        room_ty=st.multiselect("Select The Desire Room_type",sorted(df['Room_type'].unique()))
        if not room_ty:
            df3=df2.copy()
        else:
            df3=df2[df2['Room_type'].isin(room_ty)]

    cl1,cl2=st.columns([1,1])
    with cl1:
        country_df=df3.groupby("Country").Id.count()
        country_df=country_df.reset_index()
        country_df=country_df.rename(columns={'Id':'Total_listed'})

        fig=px.bar(country_df,x='Total_listed',y='Country',title='Countries with high Airbnb Listing',
                color_discrete_sequence=px.colors.sequential.Blackbody_r)
        st.plotly_chart(fig)
    with cl2:
        Roomdf=df3.groupby('Room_type').Id.count()
        Roomdf=Roomdf.reset_index()
        Roomdf=Roomdf.rename(columns={'Id':'Total_listed'})
        label=Roomdf['Room_type']
        values=Roomdf['Total_listed']
        fig=go.Figure(data=[go.Pie(labels=label,values=values,hole=.5,title="Room Type Distribution")])
        fig.update_layout(width=500,height=450)
        st.plotly_chart(fig)

    price_Df=df3.groupby(['Country','Property_type','Room_type']).price.mean()
    price_Df=price_Df.reset_index()
    price_Df=price_Df.sort_values('price',ascending=False)
    p=price_Df.sort_values(by='price')
    fig=px.bar(p,x='price',y='Country',title='Average Price distribution in Room type and Corresponding Countries',
            color='Room_type')
    st.plotly_chart(fig)

    on=st.toggle("Average Price for Room_type and Property_type & Corresponding Countries")
    if on:
        price_Df=df3.groupby(['Country','Property_type','Room_type']).price.mean()
        price_Df=price_Df.reset_index()
        price_Df=price_Df.sort_values('price',ascending=False)
        fig=px.bar(price_Df,x='price',y='Country',title='Average Price distribution in Room type and Corresponding Countries',
            color='Room_type')
        st.plotly_chart(fig)
        
        fig=px.bar(price_Df,x='Property_type',y='price',title='Average Price distribution in Property type and Corresponding Countries',
            color='Country')
        fig.update_layout(width=900,height=600)
        st.plotly_chart(fig)
        
    st.write("#### Geo-Visualization")
    fig = px.scatter_mapbox(df3, lat='lati', lon='longi', color='price', size='accommodates',
                            color_continuous_scale=px.colors.cyclical.Edge_r,hover_name='Name', mapbox_style="carto-positron", zoom=0)
    fig.update_layout(width=1150,height=800,title='Geospatial Distribution of Listings')
    st.plotly_chart(fig)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#:About:
if selected=="About":
    st.subheader(":gray[My Contact]")
    st.image(Image.open("D:\\DTM9\\CS-3\\flyer.png"))
    st.subheader(":black[Project - Airbnb Data Anlysis]")
    st.link_button(":blue[LinkedIn]","https://www.linkedin.com/in/narayana-ram-sekar-b689a9201/")
    st.link_button(":black[GitHub]","https://github.com/Narennrs1")
