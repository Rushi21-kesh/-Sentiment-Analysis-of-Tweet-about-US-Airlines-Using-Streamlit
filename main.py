import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt
st.title("Sentiment Analysis of Tweet about US Airlines")
st.markdown("This application is a streamlit dashboard to Analys the sentiment of Tweets 🐦 ")

st.sidebar.title("Sentiment Analysis of Tweet about US Airlines")
st.sidebar.markdown("This application is a streamlit dashboard to Analys the sentiment of Tweets 🐦 ")

#load US airline sentiment data
DATA_URL=('Tweets.csv') #path of dataset

@st.cache(persist=True)#check dada load single time 

def load_data():
    data=pd.read_csv(DATA_URL) #load Dataset
    data['tweet_created']=pd.to_datetime(data['tweet_created']) #convert data of tweet_created to datatime formate
    return data

data=load_data() #call function

#st.write(data)#write data into the main frame

#disply tweet  into sidebar
st.sidebar.subheader("Show Randam Tweet")
random_tweet=st.sidebar.radio('Sentiment',('positive','negative','neutral')) #create radio button

st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[['text']].sample(n=1).iat[0,0])

st.sidebar.markdown("### number of Tweets by sentiments" )
select=st.sidebar.selectbox('Visulization Type',['Histogram','Pie Chart'],key='1')

#plot map 
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

#plot location data
st.sidebar.subheader("When and Where are users tweeting from ?")
hour=st.sidebar.slider("Hour of Day",0,23)
modified_data=data[data['tweet_created'].dt.hour==hour]
if not st.sidebar.checkbox("Close",False,key='1'):
    st.markdown("## Tweet location base on the time of day ")
    st.markdown("%i tweets between %i:00 and %i:00 " %(len(modified_data),hour,(hour+1)%24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data",False):
        st.write(modified_data)

#plot number of sentiment for each airlines
st.sidebar.subheader("Breakdown airlines by sentiments")
choice=st.sidebar.multiselect("Pickup Airline",('US Airways','Virgin America','United','American','Delta','Southwest'),key='0')
if len(choice) > 0:
    choice_data=data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data,x='airline',y='airline_sentiment',histfunc='count',color='airline_sentiment',
    facet_col='airline_sentiment',labels={'airline_sentiment':'Tweets'},height=600,width=800)
    st.plotly_chart(fig_choice)

#word colud ]

st.sidebar.header("Word Cloud")
word_sentiments = st.sidebar.radio("Select sentiment for display Word Cloud",("positive",'negative','neutral'))
if not st.sidebar.checkbox("Close",True,key='3'):
    st.header('Word Cloud for %s sentiment'%(word_sentiments))
    df=data[data['airline_sentiment']==word_sentiments]
    word=' '.join(df['text'])
    process_word=' '.join([word for word in  word.split() if 'http' not in word and not word.startswith('@') and word != 'RT' ])
    wordcloud=WordCloud(stopwords=STOPWORDS,background_color='White',height=400,width=800).generate(process_word)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()









