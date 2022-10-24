import streamlit as st
import plotly.express as px
import pandas as pd
import base64

@st.cache
def get_data(url):
	return pd.read_csv(url)
@st.cache
def get_co2_data(): 
	# OWID Data on CO2 and Greenhouse Gas Emissions
	# Creative Commons BY license
	url = 'https://github.com/owid/co2-data/raw/master/owid-co2-data.csv'
	return get_data(url)
@st.cache
def get_warming_data():
	# OWID Climate Change impacts
	# Creative Commons BY license
	url = 'https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Climate%20change%20impacts/Climate%20change%20impacts.csv'
	return get_data(url).query("Entity == 'World' and Year <=2021")


st.set_page_config(layout = "wide")
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

#background_img_code
img = get_img_as_base64("image.jpg")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT380qS4XZICYe1DaFATXDIF_Wpg4LgFpbBVw&usqp=CAU");
background-size: 180%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}
[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

df_co2= get_co2_data()

st.markdown("""
# World CO2 emissions
__The graphs below show the CO2 emissions per capita for the entire 
world and individual countries over time.
Select a year with the slider in the left-hand graph and countries 
from the drop down menu in the other one.__
__Hover over any of the charts to see more detail__
---
""")


col2, space2, col3 = st.columns((10,1,10))

with col2:
	st.markdown("""
		<style>
		.big-font {
		    font-size:20px !important;
		}
		</style>
		""", unsafe_allow_html=True)
	st.markdown('<p class="big-font">Select year</p>', unsafe_allow_html=True)
	year = st.slider('',1750,2020)
	st.markdown("""
		<style>
		.big-font {
		    font-size:40px !important;
		}
		</style>
		""", unsafe_allow_html=True)
	st.markdown('<p class="big-font">Co2 emissions per capita</p>', unsafe_allow_html=True)
	fig = px.choropleth(df_co2[df_co2['year']==year], locations="iso_code",
						color="co2_per_capita",
						hover_name="country",
						range_color=(0,25),
						color_continuous_scale=px.colors.sequential.Reds)
	st.plotly_chart(fig, use_container_width=True)

with col3: 

	default_countries = ['World','United States','United Kingdom','EU-27','China', 'Australia']
	countries = df_co2['country'].unique()
	st.markdown("""
		<style>
		.big-font {
		    font-size:20px !important;
		}
		</style>
		""", unsafe_allow_html=True)
	st.markdown('<p class="big-font">Select country or group</p>', unsafe_allow_html=True)
	selected_countries = st.multiselect('',['World','United States','United Kingdom','EU-27','China', 'Australia'],default=["World"])

	st.markdown("""
		<style>
		.big-font {
		    font-size:30px !important;
		}
		</style>
		""", unsafe_allow_html=True)
	st.markdown('<p class="big-font">Co2 emissions per capita according to country</p>', unsafe_allow_html=True)
	df3 = df_co2.query('country in @selected_countries' )

	fig2 = px.line(df3,"year","co2_per_capita",color="country")

	st.plotly_chart(fig2, use_container_width=True)


st.markdown('__Data Source:__ _Our World in Data CC BY_')