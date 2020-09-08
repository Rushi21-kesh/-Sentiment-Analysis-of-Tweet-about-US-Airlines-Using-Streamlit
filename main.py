import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.title("Sentiment Analysis of Tweet about US Airlines")
st.markdown("This application is a streamlit dashboard to Analys the sentiment of Tweets 🐦 ")

st.sidebar.title("Sentiment Analysis of Tweet about US Airlines")
st.sidebar.markdown("This application is a streamlit dashboard to Analys the sentiment of Tweets 🐦 ")

DATA_URL=('Tweets.csv') #path of dataset

@st.cache(persist=True)#check dada load single time 

def load_data():
    data=pd.read_csv(DATA_URL) #load Dataset
    data['tweet_created']=pd.to_datetime(data['tweet_created']) #convert data of tweet_created to datatime formate
    return data

data=load_data() #call function

#st.write(data)#write data into the main frame

st.sidebar.subheader("Show Randam Tweet")
random_tweet=st.sidebar.radio('Sentiment',('positive','negative','neutral')) #create radio button

st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[['text']].sample(n=1).iat[0,0])

st.sidebar.markdown("### number of Tweets by sentiments" )
select=st.sidebar.selectbox('Visulization Type',['Histogram','Pie Chart'],key='1')

sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index,'Tweets':sentiment_count.values})
if not st.sidebar.checkbox("Hide",True):
    st.markdown("### Number of Tweets by Sentiments")
    if('Histogram'==select):
        fig=px.histogram(sentiment_count,x='Sentiment',y='Tweets',color='Tweets',height=400)
        st.plotly_chart(fig)

    elif('Pie Chart'==select):
        fig=px.pie(sentiment_count,names='Sentiment',values='Tweets')
        st.plotly_chart(fig)