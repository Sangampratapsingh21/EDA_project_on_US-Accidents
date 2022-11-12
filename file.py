import streamlit as st
import pandas as pd
import seaborn as sns
import folium
from folium.plugins import HeatMap
import csv
from matplotlib import pyplot as plt
import io
from streamlit_folium import folium_static
import plotly.express as px

datafile = 'US_Accidents_Dec21_updated.csv'
df = pd.read_csv(datafile)

selected = st.sidebar.selectbox(
    "Which columns of the dataset you want to analyse?",
    ("1. Overview",
    "2. Data Preparation and Cleaning",
    "3. City", 
    "4. Start Time of the Accident", 
    "5. Starting Longitude and Starting Latitude & on Weather Condition during accident",
    "6. Statewise Accident Analysis (on per capita basis as well)"))

if selected == '1. Overview':
    st.title('Exploratory Data Analysis on Accidents in USA 2016-2021')
    st.subheader('Sources:')
    st.write('1. Accident Dataset : [Link](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents) \n2. Population Dataset : [Link](https://www.kaggle.com/datasets/peretzcohen/2019-census-us-population-data-by-state)')

    st.subheader('Modules Used:')
    st.write('1. Pandas \n2. Seaborn \n3. Folium \n4. Matplotlib \n5. io \n6. ploty.express \n7. csv \n8. Streamlit')

    st.subheader("Insights from Project: ")
    st.write('- It doesn\'t contain accident dataset of New York City \n- City with most of the accidents is Miami and state with most of the accidents is California \n- Around 95.75% of cities have less than 1000 accidents \n- Around 1110 cities have repeatedly 1 accident \n- High percentages of accidents occur around 2PM - 5PM (75.5%) \n- On Sundays of accidents occur around 12PM - 6PM (56.28%) \n- On Mondays most of the accidents occur around 2PM - 5PM (80.75%) \n- Density of accidents is more in Western Part of USA and coastlines \n- Most of the accidents occur around November-December (Start of winter season) \n- Most of the accidents occur during fair weather condition \n- State with maximum value of per capita accidents i.e. no. of accidents over total population is Florida(FL) around 0.186')



elif selected == '2. Data Preparation and Cleaning':
    
    st.title('Data Preparation and Cleaning:- \n1. Loading File in Pandas \n2. Look at the structure of dataset \n3. Selecting which columns to analyse')

    #Data Preparation and cleaning
    
    st.write(df[['Start_Time', 'End_Time', 'Start_Lat', 'Start_Lng', 'City', 'Weather_Condition', 'Zipcode', 'Wind_Direction']].head(10))


    st.markdown('### 1. List of the columns and their datatypes:-')

    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)

    st.markdown('### 2. Graph showing percentage of missing data in columns')
    missing_percentages = df.isna().sum().sort_values(ascending = False) / len(df)
    st.bar_chart(missing_percentages)


    st.text('From the above graph we can clearly see that there are around 18 columns in the \ndataset having missing values outof 47  total columns. \nLater in this program we will analyse about the following columns:- \n\ta. City \n\tb. Start_Time \n\tc. Start_Lat and Start_Lng \n\td. Weather_Condtion \n\te. State')



elif selected == "3. City":
    st.title('Analysis of City Column')
    cities = df.City.unique()
    st.write('There are around', len(cities), 'unique cities in USA out of which the first 30 are below listed:-')
    st.table(cities[:30])

    cities_by_accident = df.City.value_counts()

    st.markdown("#### Below is the graph of Accidents v/s City")

    st.text("\u2022 From the below illustration we can clearly see that Miami is accident hub in \nUSA having around 1 lakh accidents followed by Los Angeles, Olrando and Dallas")
    
    fig = plt.figure()
    cities_by_accident[:20].plot(kind = 'barh')
    st.pyplot(fig)
    
    # st = st.line_chart(cities_by_accident[:20])

    

    st.write("\u2022 From the below histogram we observe that around 1000 cities have recorded only 1 accident and around", (len(cities_by_accident[cities_by_accident<1000])/len(cities_by_accident))*100, "\u0025 cities have recodered less than 1000 accidents")

    fig1 = plt.figure()
    sns.histplot(cities_by_accident,log_scale=True, kde = True)
    st.pyplot(fig1)

    

elif selected == '4. Start Time of the Accident':
    st.title('Analysis of Start_Time Column')
    st.table(df.Start_Time[:30])
    df.Start_Time = pd.to_datetime(df.Start_Time)

    st.write('\u2022 The below graph shows \u0025age of accidents in a day i.e. in each hour. From the graph we can observe that most of the accidents occur around 2PM - 5PM i.e. average of 75.5%')

    fig2 = plt.figure(figsize=(8,4))
    sns.distplot(df.Start_Time.dt.hour, bins = 24, kde = False, norm_hist = True)  
    st.pyplot(fig2)

    st.write('\u2022 The below graph show \u0025age distribution of accidents of a week i.e. in each day. From the graph we can observe that most of the accidents occur during working days i.e. Monday - Friday')
    
    fig3 = plt.figure()
    sns.distplot(df.Start_Time.dt.dayofweek, bins = 7, kde = False, norm_hist = True)
    st.pyplot(fig3)

    st.write('\u2022 Below is the accident distribution on Sundays. From this we can infer that around 56.28\u0025 accidents during 12PM - 6PM')
    sundays_starttime = df.Start_Time[df.Start_Time.dt.dayofweek == 6]
    mondays_starttime = df.Start_Time[df.Start_Time.dt.dayofweek == 0]
    
    fig4 = plt.figure(figsize=(8,3))    
    sns.distplot(sundays_starttime.dt.hour, bins = 24, kde = False, norm_hist = True)
    st.pyplot(fig4)

    st.write('\u2022 Below is the accident distribution on Monday. On mondays most of the accidents occur during 2PM-5PM around 80.75\u0025')
    fig5 = plt.figure(figsize=(8,3))
    sns.distplot(mondays_starttime.dt.hour, bins = 24, kde = False, norm_hist = True)
    st.pyplot(fig5)


    st.write('\u2022 Below graph shows accident distribution across the year i.e. among each month. From this we can observe that most of the accidents occur around November and December i.e. Start of winter season')
    fig6 = plt.figure(figsize=(9,4))
    sns.distplot(df.Start_Time.dt.month, bins = 12, kde = False, norm_hist = False)
    st.pyplot(fig6)



elif selected == "5. Starting Longitude and Starting Latitude & on Weather Condition during accident":
    st.title('Analysis of Start_Lat and Start_Lng Column')

    st.markdown('### This is the scatterplot of starting latitude and longitude of accidents')
    df_sample = df.sample(int(0.1*len(df)))
    fig7 = plt.figure()
    sns.scatterplot(x = df_sample.Start_Lng, y = df_sample.Start_Lat, size = 0.001)
    st.pyplot(fig7)

    st.markdown('### Below is the heatmap of the starting latitude and longitude')
    map = folium.Map(location = [38,-98], zoom_start = 4)
    sample_df = df.sample(int(0.01*len(df)))
    lat_lon_pairs = list(zip(list(df.Start_Lat), list(df.Start_Lng)))
    HeatMap(lat_lon_pairs).add_to(map)
    folium_static(map)
    st.write('Red Color more accident prone region and as the shade lightes down the rate of accident in that region decreases. Observation:-')
    st.write('1. As we zoom into the heat map and observe the scatterplot we can clearly say density of accidents is more in Western Region of USA and coastlines')

    st.markdown('### Weather Condition during accidents')
    st.write('From the below graph we can se that most of the accidents occur during fair weather condition(i.e. less than 3/8 opaque clouds, no precipitation, no extremes of visibility, temperature or winds.) around 11 lakh cases followed by cloudy weather around 7 lakh cases.')
    weather_con = df.Weather_Condition.value_counts()
    st.bar_chart(weather_con[:10])



elif selected == '6. Statewise Accident Analysis (on per capita basis as well)':
    st.title('Analysis of State Column')
    st.write('Given below is table containing postal codes of USA States to check what code refers to which state [click here](https://www.scouting.org/resources/los/states/)')
    state = df.State.unique()
    st.table(state)
    
    st.write("\u2022 Given graph shows the trend of accidents in states of USA, by the graph we can see that California has maximum of no. of accidents recorded around 8 lakhs followed by florida around 4 lakhs.")
    state_by_accident = df.State.value_counts()
    st.line_chart(state_by_accident)

    population = open('population.csv', 'r')
    filereader = csv.reader(population)
    pop = []
    for row in filereader:
        pop.append(row[1])


    # for percapita one
    per_capita = []
    for i in range(len(state_by_accident)):
        per_capita.append(int(state_by_accident[i])/int(pop[i]))

    x_axis = ['CA','FL','TX','OR','VA','NY','PA','MN','NC','SC','MD','AZ','NJ','TN','UT','LA','IL','MI','MI','WA','CT','MO','CO','OH','IN','AL','MT','AR','IA','DC','KS','OK','ID','WI','WV','KY','MA','NV','MS','DE','RI','NH','NE','NM','ND','ME','WY','VT','SD']
    st.write('\u2022 Below graph shows accidents per capita in different states. Maximum in Florida around 0.18 and minimum in South Dakota 0.0022')
    p = px.line(x = x_axis, y=per_capita, width= 1000, height = 500)
    st.write(p)