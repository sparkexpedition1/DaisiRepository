import streamlit as st
import pydaisi as pyd
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
# def hello(name="Daisi"):
#   return f"Hello {name}!"
def execution():
    df_amazon = pd.read_csv("https://storage.googleapis.com/t-systems-hackathon-webapp/AmazonCombined.csv")
    df_amazon.dropna(axis=0, subset=['name', 'reviews.rating', 'reviews.text', 'reviews.date','primaryCategories'],inplace=True)
    req_columns = ['name', 'asins', 'brand','primaryCategories', 'manufacturer',
       'reviews.date', 'reviews.doRecommend','reviews.numHelpful', 'reviews.rating',
       'reviews.text', 'reviews.title', 'reviews.username',]
    df_amazon = df_amazon[req_columns].copy()
    for idx in df_amazon.index:
        df_amazon.at[idx,'date'] = df_amazon.loc[idx,'reviews.date'][:10]
    df_amazon.drop(['reviews.date'],axis=1, inplace=True)
    analyzer = SentimentIntensityAnalyzer()
    for idx in df_amazon.index:
        sentence = df_amazon.loc[idx,'reviews.text']
        value = analyzer.polarity_scores(sentence)['compound']
        # Converting Rating from -1 to 1 into 1 to 5
        newValue = ((((value) - (-1)) * (5 - 1)) / (1 - (-1))) + 1
        df_amazon.at[idx,'textSentimentRating'] = newValue
    for idx in df_amazon.index:
        df_amazon.at[idx,'averageRating'] = (df_amazon.loc[idx,'reviews.rating'] + df_amazon.loc[idx,'textSentimentRating'])/2
    df_group1 = df_amazon.groupby(['name'])
    df_temp = df_group1[['reviews.rating', 'textSentimentRating','averageRating']].mean()
    df_temp.reset_index(inplace=True)
    df_text_rating = df_temp.sort_values(by='textSentimentRating',ascending=False)
    df_text_rating.reset_index(drop=True, inplace=True)
    df_top = df_text_rating.head(10)
    df_bot = df_text_rating.tail(10).sort_values(by='textSentimentRating',ascending=True).reset_index(drop=True)
    #%matplotlib inline
    fig=plt.figure(figsize=(15,5))
    for idx in df_top.index:
        df_top.at[idx,'short.name'] = df_top.loc[idx,'name'][:16]
    df_top = df_top.sort_values(by='averageRating',ascending=True).reset_index(drop=True)
    plt.plot(df_top['short.name'],df_top['reviews.rating'],color="green",marker='o',linewidth=7,markersize=15)
    plt.plot(df_top['short.name'],df_top['textSentimentRating'],color="blue",marker='o',linewidth=7,markersize=15)
    plt.plot(df_top['short.name'],df_top['averageRating'],color="red",marker='o',linewidth=7,markersize=15)
    plt.xlabel('name',size=15)
    plt.ylabel('Rating',size=15)
    plt.grid(True)
    plt.xticks(fontstretch='ultra-condensed',rotation=90,size=12)
    plt.yticks([3,4,5],size=15)
    plt.ylim([3,6])
    plt.legend(('reviews.rating','textSentimentRating','averageRating'))
    st.image(plt.show())
    #%matplotlib inline
    fig=plt.figure(figsize=(15,5))
    for idx in df_bot.index:
        df_bot.at[idx,'short_name'] = df_bot.loc[idx,'name'][:16]
    df_bot = df_bot.sort_values(by='averageRating',ascending=True).reset_index(drop=True)
    plt.plot(df_bot['short_name'],df_bot['reviews.rating'],color="green",marker='o',linewidth=7,markersize=15)
    plt.plot(df_bot['short_name'],df_bot['textSentimentRating'],color="blue",marker='o',linewidth=7,markersize=15)
    plt.plot(df_bot['short_name'],df_bot['averageRating'],color="red",marker='o',linewidth=7,markersize=15)
    plt.xlabel('name',size=15)
    plt.ylabel('Rating',size=15)
    plt.grid(True)
    plt.xticks(fontstretch='ultra-condensed',rotation=90,size=12)
    plt.yticks(size=12)
    plt.ylim([0,6])
    plt.legend(('reviews.rating','textSentimentRating','averageRating'))
    st.image(plt.show())
    #return [img1,img2]
def uiExample():
    st.set_page_config(layout = "wide")
    algorithm = st.sidebar.text_input("Algoritm", "Algo")
    st.title("The Algorithm being implemented is " + str(algorithm)+"\nfor rating write Sentiment Rating")
    if algorithm == "Sentiment Rating":
        execution()
        st.markdown("Complete")
        
if __name__ == "__main__":
    uiExample()