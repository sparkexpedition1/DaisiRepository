import streamlit as st
import pydaisi as pyd
import pandas as pd
import yfinance as yf
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
    st.pyplot(fig=plt)
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
    st.pyplot(fig=plt)
def textSentiment():
    text = st.text_input("Please enter thex here",value="This is a sample Text")
    analyzer = SentimentIntensityAnalyzer()
    value = analyzer.polarity_scores(text)['compound']
    # Converting Rating from -1 to 1 into 1 to 5
    new_value = ((((value) - (-1)) * (5 - 1)) / (1 - (-1))) + 1
    if new_value < 2.5:
        st.text("Negative")
    elif new_value > 3.5:
        st.text("Positive")
    else:
        st.text("Neutral")
def uiExample():
    st.set_page_config(layout = "wide")
    user_name = st.sidebar.text_input("Name", "Jhon")
    st.text("Hi " + user_name)
    nifty = yf.Ticker("^NSEI")
    nifty_cur = nifty.info['regularMarketPrice']
    nifty_change = (nifty_cur - nifty.info['previousClose'])/nifty.info['previousClose']*100
    st.markdown('Nifty 50 :  ' + str(nifty_cur) + ' Change: ' + str(nifty_change) + '%')
    
    sensex = yf.Ticker("^BSESN")
    sensex_cur = sensex.info['regularMarketPrice']
    sensex_change = (sensex_cur - sensex.info['previousClose'])/sensex.info['previousClose']*100
    st.markdown('Sensex 50 :  ' + str(sensex_cur) + ' Change: ' + str(sensex_change) + '%')
    
    snp = yf.Ticker("^GSPC")
    snp_cur = snp.info['regularMarketPrice']
    snp_change = (snp_cur - snp.info['previousClose'])/snp.info['previousClose']*100
    st.markdown('S&P :  ' + str(snp_cur) + ' Change: ' + str(snp_change) + '%')
    
    russel = yf.Ticker("^RUT")
    russel_cur = russel.info['regularMarketPrice']
    russel_change = (russel_cur - russel.info['previousClose'])/russel.info['previousClose']*100
    st.markdown('Russel :  ' + str(russel_cur) + ' Change: ' + str(russel_change) + '%')
    
    dj = yf.Ticker("^DJI")
    dj_cur = dj.info['regularMarketPrice']
    dj_change = (dj_cur - dj.info['previousClose'])/dj.info['previousClose']*100
    st.markdown('DOW Jones :  ' + str(dj_cur) + ' Change: ' + str(dj_change) + '%')
    
    #fig = plt.figure()
    l1 = [["Nifty",nifty_change],["Sensex", sensex_change], ["SNP",snp_change], ["Russel",russel_change], ["DOW Jones",dj_change],["sample",-0.25]]
    lp =[]
    ln = []
    for lst in l1:
        if lst[1] >= 0 :
            lp.append(lst)
        else:
            ln.append(lst)
    df_lp  =  pd.DataFrame(lp,columns=["Index","Change"])
    df_ln  =  pd.DataFrame(ln,columns=["Index","Change"])
    df_lp.plot(kind="bar",color="green")
    df_ln.plot(kind="bar",color="red")
#     plt.plot(df_lp['Index'],df_lp['Change'],color="green")
#     plt.plot(df_ln['Index'],df_ln['Change'],color="red")
    st.pyplot(fig=plt)
#     plt.show()
#     nsei =yf.Ticker('NSEI')
#     st.text(nsei.info)
#     df_list = pd.read_html('https://finance.yahoo.com/world-indices/')
#     majorStockIdx = df_list[0]
#     st.dataframe(data=majorStockIdx)
    st.text("For ratings type Product Rating")
    st.text("For Text Sentiment type Text Sentiment")
    algorithm = st.text_input("Please enter the Algorithm",value="")
    if algorithm == "Product Rating":
        execution()
    elif algorithm == 'Text Sentiment':
        textSentiment()
#     else:
#         st.text("No such Algorithm defined in this daisi")
        
if __name__ == "__main__":
    uiExample()
