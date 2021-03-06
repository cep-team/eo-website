import geemap.foliumap as geemap
import ee
import numpy
import streamlit as st
import datetime
import pandas as pd
from PIL import Image
import time
from streamlit_folium import st_folium
import folium
from earth_observation_v1 import Fire
from io import StringIO
import json
import numpy as np

st.set_page_config(
    page_title="Page 2 ",
    page_icon="👋",
    layout="wide"
)

# Remove whitespace from the top of the page and sidebar
st.markdown("""
        <style>
            .css-18e3th9 {
                    padding-top: 3rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
            .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

st.session_state["errors"] = []

df = pd.read_csv("Data/wildfire_boreal_forest.csv")
fires_choices = df["name"]
layers_choices = {"True Color": "true", "False Color": "false",
                  "SWIR": "swir", "NBR": "nbr", "BAI": "bai",
                  "EVI": "evi", "Air Quality (Nitrogen Dioxide)": "no2",
                  "Air Quality (Carbon Monoxide)": "co",
                  "LST": "lst"}


st.markdown(
    """<p style="color:#33ff33; font-size:50px; text-align:center">
            A Deeper Dive Into The Boreal Forrest</p>""",
    unsafe_allow_html=True,
)

with st.sidebar:
    fire = st.selectbox("Choose a fire", fires_choices)
    st.session_state['fire_name'] = fire

    st.write("____________________")
    start_date = str(st.date_input("Start Date",
                                value=datetime.datetime.strptime(df[df['name'] == fire]["date_start"].iloc[0], "%d/%m/%Y").date(),
                                min_value=datetime.date(2000, 1, 1),
                                max_value=datetime.date.today()))

    end_date=str(st.date_input("End Date",
                                value=datetime.datetime.strptime(df[df['name'] == fire]["date_end"].iloc[0], "%d/%m/%Y").date(),
                                min_value = datetime.date(2000, 1, 1),
                                max_value = datetime.date.today()))

    st.write("____________________")

    layer=st.selectbox("Choose a layer", layers_choices.keys())

    # if "Air Quality" in layer and pd.to_datetime(start_date) > pd.to_datetime('2017-11-13'):
    #     air_indice = st.selectbox("Choose an air quality indice", [
    #                               "Carbon Monoxide", "Nitrogen Dioxide"])
    if "Air Quality" in layer and pd.to_datetime(start_date) < pd.to_datetime('2017-11-13'):
            st.markdown(
                """<p class="small-font" style="color:red">
                    Air Quality layer unavailable before 2017-11-13.</p>""",
                unsafe_allow_html=True,
            )
            st.session_state["errors"].append(True)

    st.write("____________________")
        # with st.expander("Parameters"):

    pressed=st.button("Build Map")

if "fire_name" in st.session_state:
    description = str(df[df["name"]==st.session_state['fire_name']]["description"].iloc[0])
    if description != "nan":
        st.markdown(
                f"""<p class="small-font" style="text-align:center">
                    {description}</p>""",
                unsafe_allow_html=True,
            )

if (pressed) and (True not in st.session_state["errors"]):

        fire_object=Fire(df.iloc[df[df['name'] == fire].index[0]])
        st.session_state["fire_object"]=fire_object

        if layer == "True Color":
            st.session_state["fire_object"].true_color(start_date=start_date,
                                                       end_date=end_date)

        elif layer == "False Color":
            st.session_state["fire_object"].false_color(
                start_date=start_date, end_date=end_date)

        elif layer == "SWIR":
            st.session_state["fire_object"].swir(start_date=start_date,
                                                 end_date=end_date)

        elif layer == "NBR":
            st.session_state["fire_object"].nbr(
                start_date=start_date, end_date=end_date)

        elif layer == "BAI":
            st.session_state["fire_object"].bai(
                start_date=start_date, end_date=end_date)

        elif layer == "EVI":
            st.session_state["fire_object"].evi(
                start_date=start_date, end_date=end_date)

        elif "Air Quality" in layer:
            st.session_state["fire_object"].air_quality(
                start_date=start_date, end_date=end_date, air_indice=layers_choices[layer])

        elif layer == "LST":
            st.session_state["fire_object"].lst(
                start_date=start_date, end_date=end_date)

        st.session_state["start_date"]=start_date
        st.session_state["end_date"]=end_date

if "fire_object" not in st.session_state:
        Map=geemap.Map(plugin_Draw=False)
        # Add a basemap
        # Map.add_basemap("ROADMAP")
        Map.to_streamlit(
            width=1500, height=700)
else:
        st.session_state["fire_object"].Map.to_streamlit(
            width=1500,
            height=700)

        # print(st.session_state["fire_object"].Map.draw_features)
        # output = st_folium(st.session_state["fire_object"].Map, key="init",
        #                     width=st.session_state["width_slider"],
        #                     height=st.session_state["height_slider"])

        # if output["last_active_drawing"]:
        #     st.session_state["last_active_drawing"] = output["last_active_drawing"]["geometry"]["coordinates"][0]


# st_data = st_folium(m, width=725)
if st.button("Continue to Boreal_Exploration Data exploration"):
    st.markdown('<meta http-equiv="refresh" content="0;url=/Boreal_Exploration_Continued">',
                unsafe_allow_html=True)

    