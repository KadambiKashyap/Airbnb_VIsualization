import pandas as pd
import pymongo
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image
import streamlit as st
import folium
from streamlit_folium import st_folium 
from streamlit_option_menu import option_menu
import urllib.parse



username = "kashyap"
password = "Abdevillers@17"
cluster_url = "kash.1gzj0jw.mongodb.net/sample_airbnb"

escaped_username = urllib.parse.quote_plus(username)
escaped_password = urllib.parse.quote_plus(password)

uri = f"mongodb+srv://{escaped_username}:{escaped_password}@{cluster_url}"

client = pymongo.MongoClient(uri)
db = client["sample_airbnb"]
col= db["listingsAndReviews"]


df = pd.read_csv('Airbnb_data.csv') # Importing your dataframe

################################# STREAMLIT PAGE  ###########################################
icon = Image.open("air.png")

st.set_page_config(page_title= "AIRBNB DATA VISUALIZATION",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This interactive dashboard app offers a dynamic visualization tool for exploring Airbnb data, allowing users to analyze trends, compare prices, and discover popular destinations.
                                It provides an interactive experience to help users make informed decisions and plan their travel experiences effectively"""}
                  )

st.title("**AIRBNB DATA VISUALIZATION**", anchor = False)
with st.sidebar:
    
    selected = option_menu(menu_title = None,
                          options=["HOME", "EXPLORATION","INSIGHTS"],
                          icons=["house-fill","database-fill","bar-chart-fill" ],
                          default_index = 0,
                          menu_icon="cast",
                          key="navigation_menu",
                          styles={
                                    "font_color": "#DC143C",   
                                    "border": "2px solid #DC143C", 
                                    "padding": "10px 25px"   
                          })

if selected == 'HOME':  
    st.image("airbnb.jpeg",width= 300)

    st.subheader("Unlocking Insights with Data Visualization")

    st.markdown("---")  

    st.markdown(
        """Airbnb, a revolutionary platform, has transformed the way we travel. Connecting people with unique accommodations worldwide, it has redefined the concept of hospitality.    
    This interactive dashboard empowers you to delve into the fascinating world of Airbnb data. Our mission is to unlock valuable insights hidden within this data, providing you with a deeper understanding of the global landscape of Airbnb listings."""
    )

    st.divider() 


    st.subheader("Embark on a Journey of Discovery")
    st.markdown("""
    - :red[**Global Distribution:**] Explore a captivating world map showcasing the distribution of Airbnb listings across different regions.
                            This interactive visualization allows you to pinpoint areas with high listing density and uncover potential travel hotspots.
    - :red[**Data-Driven Exploration:**] We'll equip you with the tools to filter and analyze listings based on a variety of criteria. 
                               This empowers you to tailor your exploration to your specific interests, whether you're curious about trends in specific locations, price ranges, or reviews given.
    - :red[**Interactive Insights (Optional):**] Depending on the scope of your project, you might encounter sections dedicated to uncovering deeper insights through interactive visualizations.
                                       These visualizations could reveal trends in pricing, popularity, or other relevant factors.
    - :red[**Predictions (Optional):**] If your project incorporates historical data analysis, you might encounter a section exploring potential future trends and pricing predictions for Airbnb listings."""
    )



    st.markdown("---") 


    st.markdown("Through this Streamlit application, you'll gain a comprehensive understanding of Airbnb's global presence, identify valuable patterns within the data, and potentially predict future trends in this dynamic market.  Let's dive in and unlock the hidden stories within the world of Airbnb!")

#####################################  EXPLORATION PAGE  ############################################

if selected == 'EXPLORATION':
    tab1, tab2 = st.tabs(["**PRICE ANALYSIS**","**GEOSPATIAL VISUALIZATION**"])
    
    with tab1:
        st.subheader("PRICE ANALYSIS W.R.T. COUNTRIES & ROOM TYPE")

        countries = st.multiselect("Select the Countries", df['country'].unique())

        df_country = df[df['country'].isin(countries)]
        df_country.reset_index(inplace = True)

        rt = st.selectbox("Select the Room Type", df_country['room_type'].unique())
        df_rt = df_country[df_country['room_type'] == rt]
        df_rt.reset_index(inplace= True)


        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            df1 = pd.DataFrame(df_rt.groupby("property_type")[["price","no_of_reviews"]].sum())
            df1.reset_index(inplace=True)
            fig = px.bar(df1, x='property_type', y="price", title="TOTAL PRICE FOR PROPERTY TYPES",
                        hover_data=["no_of_reviews"],
                        color_discrete_sequence=px.colors.sequential.Sunsetdark,
                        width=700, height=600)
            st.plotly_chart(fig)

        with col2:
            total_price_selected_countries = df[df['country'].isin(countries)]['price'].sum()
            st.metric(label="**:red[TOTAL PRICE FOR SELECTED COUNTRIES]**", value=total_price_selected_countries, delta=None)

        with col3:
            min_price_country = df[df['country'].isin(countries)]['price'].min()
            # Display metric showing min price for selected countries
            st.metric(label="**:red[MINIMUM PRICE FOR SELECTED COUNTRIES]**", value=min_price_country, delta=None)

            max_price_country = df[df['country'].isin(countries)]['price'].max()
            st.metric(label="**:red[MAXIMUM PRICE FOR SELECTED COUNTRIES]**", value=max_price_country, delta=None)

            Avg_bedroom = df[df['country'].isin(countries)]['total_bedrooms'].mean()
            rounded_avg_bedrooms = round(Avg_bedroom, 2)
            st.metric(label="**:red[AVERAGE BEDROOMS FOR SELECTED COUNTRIES]**", value=rounded_avg_bedrooms , delta=None)

            avg_review_score = df[df['country'].isin(countries)]['review_score'].mean()
            rounded_avg_review_score =  round(avg_review_score,0)
            st.metric(label="**:red[AVERAGE REVIEW SCORE FOR SELECTED COUNTRIES]**", value=rounded_avg_review_score, delta=None)


        with col4:
           total_prices_by_country_roomtype = df_rt.groupby(['country', 'room_type'])['price'].sum().reset_index()

           total_price_all_countries_roomtype = total_prices_by_country_roomtype['price'].sum()


           total_prices_by_country_roomtype['percentage'] = (total_prices_by_country_roomtype['price'] / total_price_all_countries_roomtype) * 100

           fig_pie_roomtype = px.pie(total_prices_by_country_roomtype, 
                                        values='percentage', 
                                        names='country', 
                                        title='PERCENTAGE OF TOTAL PRICE  BY COUNTRY AND ROOM TYPE',
                                        labels={'percentage': 'Percentage', 'country': 'Country'},
                                        color_discrete_sequence=px.colors.qualitative.Vivid)

           st.plotly_chart(fig_pie_roomtype)

           avg_price_country = df_country.groupby('country')['price'].mean().reset_index()
           avg_price_country = avg_price_country.sort_values(by='price', ascending=False)

           fig = px.bar(avg_price_country,x='price',y='country',orientation='h',title="AVERAGE PRICE OF AIRBNB LISTINGS BY COUNTRY",
                labels={'price': 'Average Price', 'country': 'Country'},width=550, height=450)

           fig.update_layout(
                margin=dict(l=100, r=20, t=70, b=70), 
            )

           for i, row in avg_price_country.iterrows(): #iterate through avg price of country 
                fig.add_annotation(
                    x=row['price'],
                    y=row['country'],
                    text=f"{row['price']:.0f}", 
                    showarrow=False,
                    xanchor='left',
                    yanchor='middle'
                )

           st.plotly_chart(fig)

    with tab2:
        st.subheader("GEO-SPATIAL VISUALISATION")

        selected_countries = st.selectbox('Select Countries', df['country'].unique())

        # Filter hotels based on selected countries
        filtered_hotels = df[df['country']==selected_countries]

        if filtered_hotels.shape[0] > 0:
            map = folium.Map(location=[filtered_hotels['Latitude'].mean(), filtered_hotels['Longitude'].mean()], zoom_start=3)

            # Add markers for each hotel
            for id, row in filtered_hotels.iterrows():
                folium.Marker(
                    location=[row['Latitude'], row['Longitude']],
                    popup=f"Name- {row['name']}: Price-{row['price']}",
                    icon=folium.Icon(color='blue', icon='map-pin')
                ).add_to(map)

            # Render map
            st.markdown(f"### Map of {selected_countries}")
            st_data = st_folium(map, width = 1200)
        else:
            st.warning('No hotels found for the selected countries.')
        


        city_counts = df.groupby('street')['id'].count().reset_index()
        city_counts.rename(columns={'id': 'count'}, inplace=True)

        df_city = pd.merge(df, city_counts, on='street', how='left')

        df_city['hover_info'] = df_city['name'] + ', ' + df_city['country'] # displaying hover_data


        fig = px.scatter_mapbox(
            df_city,
            lat = "Latitude",
            lon = "Longitude",
            color = "count",
            size = "count", 
            mapbox_style = "open-street-map",
            zoom = 1,
            hover_name = 'hover_info', 
            labels = {"count": "Airbnb Listings"},
            title = "AIRBNB LISTINGS BY COUNTRY",
            template = 'plotly_dark',
            width=1200, height=700,
            color_continuous_scale='bluered'
        )

        fig.update_layout(
            geo=dict(showcoastlines=False, projection=dict(type='mercator')),
            coloraxis_colorbar=dict(title="Listing Count"),
            margin=dict(l=50, r=0, t=50, b=0)
        )

        st.plotly_chart(fig)


        fig2 = px.scatter_geo(df, 
                     lat='Latitude', 
                     lon='Longitude', 
                     color='country',
                     hover_name='name', 
                     size='Host_total_listings',
                     title='PROPERTY LISTING AROUND THE WORLD',
                     projection="natural earth",  
                     locationmode='country names', 
                     width=1500,  
                     height=800)  

        fig2.update_traces(marker=dict(size=8, opacity=0.8))

        st.plotly_chart(fig2)

############################################# INSIGHTS PAGE  ###############################################

if selected == 'INSIGHTS':
    question = st.selectbox("Select a question:", [
    "What are the counts of different room types in the listings?",
    "Which are the top 15 hosts with the most number of listings?",
    "What is the average number of listings per host?",
    "What is the average price per night for each cancellation policy?",
    "What is the Range of the number of guests included?",
    "What is the relationship between review scores and price?",
    "What is the most common property type?",
    "What is the average price per night for each bed type?",
    "What is the average price per night for Top 10 hosts?",
    "What is the distribution of listings across different countries?"
])
        # Visualizations based on the selected question

    if question == "What are the counts of different room types in the listings?":
        fig = px.histogram(df, x='room_type', title="Different Room Types in the Listings",
                   labels={'room_type': 'Room Type', 'count': 'Count'},
                   color='room_type')
        fig.update_layout(barmode='group', xaxis_tickangle=-45, height=700, width=1000)

    elif question == "Which are the top 15 hosts with the most number of listings?":
        top_hosts = df['host_name'].value_counts().sort_values(ascending = False).index[:15]
        df_top_hosts = df[df['host_name'].isin(top_hosts)]
        fig = px.histogram(df_top_hosts, x='host_name', title="Top 15 Hosts with Most Number of Listings",
                        labels={'host_name': 'Host Name', 'count': 'Count'})
        fig.update_layout(barmode='group', xaxis_tickangle=-45)
        
    elif question == "What is the average number of listings per host?":
        average_listings_per_host = df.groupby('host_name')['Host_total_listings'].mean().reset_index().sort_values(by='Host_total_listings', ascending=False)[:10]
        fig = px.bar(average_listings_per_host, x='host_name', y='Host_total_listings', color='Host_total_listings')
        fig.update_layout(title="Average Number of Listings per Host", xaxis_title="Host Name", yaxis_title="Average Number of Listings", height=700, width=1000)

    elif question == "What is the average price per night for each cancellation policy?":
        avg_price_by_cancel_policy = df.groupby('cancellation_policy')['price'].mean().reset_index()
        fig = px.bar(avg_price_by_cancel_policy, x='cancellation_policy', y='price', color='price')
        fig.update_layout(title="Average Price per Night for Each Cancellation Policy", xaxis_title="Cancellation Policy", yaxis_title="Average Price", height=700, width=1000)

    elif question == "What is the Range of the number of guests included?":
        x = df['guests_included'].value_counts().sort_index().reset_index()
        fig = px.bar(x, x='index', y='guests_included', color='guests_included')
        fig.update_layout(title="Distribution of the Number of Guests Included", xaxis_title="No. of Guests", yaxis_title="Count", height=700, width=1000)

    elif question == "What is the relationship between review scores and price?":
        fig = px.scatter(df, x='review_score', y='price')
        fig.update_layout(title="Relationship between Review Scores and Price", xaxis_title="Review Score", yaxis_title="Price", height=700, width=1000)

    elif question == "What is the most common property type?":
        property_type_counts = df['property_type'].value_counts().reset_index()
        fig = px.bar(property_type_counts, x='index', y='property_type', color='property_type')
        fig.update_layout(title="Most Common Property Type", xaxis_title="Property Type", yaxis_title="Frequency", height=700, width=1000)

    elif question == "What is the average price per night for each bed type?":
        avg_price_by_bed_type = df.groupby('bed_type')['price'].mean().reset_index()
        fig = px.bar(avg_price_by_bed_type, x='bed_type', y='price')
        fig.update_layout(title="Average Price per Night for Each Bed Type", xaxis_title="Bed Type", yaxis_title="Average Price", height=700, width=1000)

    elif question == "What is the average price per night for Top 10 hosts?":
        avg_price_by_host = df.groupby('host_name')['price'].mean().sort_values(ascending=False)[:15].reset_index()
        fig = px.bar(avg_price_by_host, x='host_name', y='price', color='price')
        fig.update_layout(title="Average Price per Night for Each Host", xaxis_title="Host Name", yaxis_title="Average Price", height=700, width=1000)

    elif question == "What is the distribution of listings across different countries?":
        country_counts = df['country'].value_counts().reset_index()
        fig = px.bar(country_counts, x='index', y='country')
        fig.update_layout(title="Distribution of Listings Across Different Countries", xaxis_title="Country", yaxis_title="Frequency", height=700, width=1000)

    st.plotly_chart(fig)




                
