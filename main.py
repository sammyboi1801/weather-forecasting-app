import streamlit as st
import pandas as pd
import numpy as np
import requests
import pickle


API_KEY = "18eb2b6cdfea429e963142138230704"
loaded_model=pickle.load(open('RFC.pkl', 'rb'))



label_encoder_states={'andhra pradesh':0, 'arunachal pradesh':1, 'assam':2, 'bihar':3, 'chhattisgarh':4, 'goa':5, 'gujarat':6,
               'haryana':7, 'himachal pradesh':8, 'jharkhand':9, 'karnataka':10, 'kerala':11, 'madhya pradesh':12,
               'maharashtra':13, 'manipur':14, 'meghalaya':15, 'mizoram':16, 'nagaland':17, 'odisha':18, 'punjab':19,
               'rajasthan':20, 'sikkim':21, 'tamil nadu':22, 'telangana':23, 'tripura':24, 'uttar pradesh':25,
               'uttarakhand':26, 'west bengal':27}

label_encoder_condition={'Clear':0,'Sunny':1,'Patchy rain possible':2, 'Light rain shower':3, 'Partly cloudy':4,
                      'Cloudy':5, 'Moderate rain':6, 'Moderate or heavy rain shower':7,'Patchy light rain':8,
                      'Patchy light drizzle':9, 'Mist':10, 'Overcast':11, 'Thundery outbreaks possible':12,
                      'Moderate or heavy snow with thunder':13, 'Light snow showers':14, 'Patchy light snow with thunder':15,
                      'Light drizzle':16, 'Light rain':17, 'Fog':18, 'Moderate rain at times':19, 'Heavy rain':20,
                      'Patchy light rain with thunder':21, 'Torrential rain shower':22}

temp_c=wind_kph=wind_degree=pressure_mb=precip_mm=humidity=cloud=dewpoint_c=vis_km=state=0
tempapi=windsapi=winddapi=pressureapi=precipapi=humidityapi=cloudapi=visapi=dewpointapi=0


def get_live_results(location='Maharashtra'):
    # Calling API get live informatioin
    URL = f"http://api.weatherapi.com/v1/forecast.json?key=18eb2b6cdfea429e963142138230704&q={location}&days=1&aqi=no&alerts=no"
    r = requests.get(url=URL)
    data = r.json()

    URL2=f"https://geocode.maps.co/search?q={location}"
    r2=requests.get(url=URL2)
    data2 = r2.json()



    lat = float(data2[0]['lat'])
    lon = float(data2[0]['lon'])
    tempapi = data['current']['temp_c']
    windsapi = data['current']['wind_kph']
    winddapi = data['current']['wind_degree']
    pressureapi = data['current']['pressure_mb']
    precipapi = data['current']['precip_mm']
    humidityapi = data['current']['humidity']
    cloudapi = data['current']['cloud']
    visapi = data['current']['vis_km']
    dewpointapi = data['forecast']['forecastday'][0]['hour'][0]['dewpoint_c']
    df = pd.DataFrame([[lat, lon]], columns=['LAT', 'LON'])

    return lat,lon,tempapi,windsapi,winddapi,pressureapi,precipapi,humidityapi,cloudapi,visapi,dewpointapi,df

def predict_live(tempapi,windsapi,winddapi,pressureapi,precipapi,humidityapi,cloudapi,visapi,dewpointapi,location):
    if (([tempapi,windsapi,winddapi,pressureapi,precipapi,humidityapi,cloudapi,dewpointapi,visapi] == [0, 0, 0, 0, 0,
                                                                                                          0, 0, 0,
                                                                                                          0]) or location == ""):
        return "Select location from sidebar"
    else:

        try:
            state=label_encoder_states[location.lower()]
            value=loaded_model.predict(np.array([tempapi,windsapi,winddapi,pressureapi,precipapi,humidityapi,cloudapi,dewpointapi,visapi,state]).reshape(1, -1))
            result_live = {i for i in label_encoder_condition if label_encoder_condition[i]==value[0]}
            result_live=list(result_live)[0]
            print("Results: ",result_live)

            return result_live
        except:
            return "Wrong input"

def predict(temp_c,wind_kph,wind_degree,pressure_mb,precip_mm,humidity,cloud,dewpoint_c,vis_km,location1):
    if(([temp_c,wind_kph,wind_degree,pressure_mb,precip_mm,humidity,cloud,dewpoint_c,vis_km]==[0,0,0,0,0,0,0,0,0]) or location1==""):
        return "Please enter values"
    else:

        try:
            URL2 = f"https://geocode.maps.co/search?q={location1}"
            r2 = requests.get(url=URL2)
            data2 = r2.json()

            lat = data2[0]['lat']
            lon = data2[0]['lon']

            state = label_encoder_states[location1.lower()]
            value = loaded_model.predict(np.array([temp_c, wind_kph, wind_degree, pressure_mb, precip_mm, humidity, cloud, dewpoint_c, vis_km,state]).reshape(1, -1))
            result = {i for i in label_encoder_condition if label_encoder_condition[i] == value[0]}
            result = list(result)[0]
            df = pd.DataFrame([[float(lat), float(lon)]], columns=['LAT', 'LON'])
            return df,result
        except:
            return "Wrong input"



st.title(':rainbow: Weather Forecasting :sunny:')

text="123"

with st.sidebar:

    st.title('Live weather :cloud: : ')
    location=st.text_input('Location: ')
    df = pd.DataFrame([[19.115790280537365, 72.88187586540101]], columns=['LAT', 'LON'])
    try:
        lat, lon, tempapi, windsapi, winddapi, pressureapi, precipapi, humidityapi, cloudapi, visapi, dewpointapi,df = get_live_results(
            location)
        st.text(f"Temperature: {tempapi}")
        st.text(f"Wind Speed: {windsapi}")
        st.text(f"Wind Degree: {winddapi}")
        st.text(f"Pressure in mb: {pressureapi}")
        st.text(f"Precipitation in mm: {precipapi}")
        st.text(f"Humidity: {humidityapi}")
        st.text(f"Cloud cover: {cloudapi}")
        st.text(f"Dewpoint in C: {dewpointapi}")
        st.text(f"Visibility in km: {visapi}")
    except:
        pass


results=""

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    temp_c=st.text_input("&emsp;&emsp;Temperature")
    humidity=st.text_input("&emsp;&emsp;Humidity")

with col2:
    wind_kph=st.text_input("&emsp;&emsp;Wind Speed")
    cloud=st.text_input("&emsp;&emsp;Cloud")

with col3:
    wind_degree=st.text_input("&emsp;&nbsp;&nbsp;&nbsp;Wind Direction")
    dewpoint_c=st.text_input("&emsp;&nbsp;&nbsp;&nbsp;Dewpoint")

with col4:
    pressure_mb=st.text_input("&emsp;&emsp;Pressure")
    vis_km=st.text_input("&emsp;&emsp;Visibility")

with col5:
    precip_mm=st.text_input("&emsp;&emsp;Precipitation")
    location1=st.text_input("&emsp;&emsp;State")

col1,col2=st.columns(2)
with col1:
    if st.button('Predict using live weather'):
        results=predict_live(tempapi,windsapi,winddapi,pressureapi,precipapi,humidityapi,cloudapi,visapi,dewpointapi,location)

with col2:
    if st.button('Predict'):
        try:
            df,results=predict(temp_c,wind_kph,wind_degree,pressure_mb,precip_mm,humidity,cloud,dewpoint_c,vis_km,location1)
        except:
            results=predict(temp_c,wind_kph,wind_degree,pressure_mb,precip_mm,humidity,cloud,dewpoint_c,vis_km,location1)
st.markdown(f"### Prediction: {results}")

st.map(df,zoom=5)