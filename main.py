import streamlit as st
import pydaisi as pyd
import pandas as pd
import yfinance as yf
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

def GlobalStockTracker():
    st.set_page_config(layout = "wide")
    stock_name = st.sidebar.text_input("Stock", "Apple")
    st.text("Checking " + stock_name + " across all Global markets ..")
    nifty = yf.Ticker("^NSEI")
    nifty_cur = nifty.info['regularMarketPrice']
    nifty_change = (nifty_cur - nifty.info['previousClose'])/nifty.info['previousClose']*100
    #st.markdown('Nifty 50 :  ' + str(nifty_cur) + ' Change: ' + str(nifty_change) + '%')
    
    sensex = yf.Ticker("^BSESN")
    sensex_cur = sensex.info['regularMarketPrice']
    sensex_change = (sensex_cur - sensex.info['previousClose'])/sensex.info['previousClose']*100
    #st.markdown('Sensex 50 :  ' + str(sensex_cur) + ' Change: ' + str(sensex_change) + '%')
    
    snp = yf.Ticker("^GSPC")
    snp_cur = snp.info['regularMarketPrice']
    snp_change = (snp_cur - snp.info['previousClose'])/snp.info['previousClose']*100
    #st.markdown('S&P :  ' + str(snp_cur) + ' Change: ' + str(snp_change) + '%')
    
    russel = yf.Ticker("^RUT")
    russel_cur = russel.info['regularMarketPrice']
    russel_change = (russel_cur - russel.info['previousClose'])/russel.info['previousClose']*100
    #st.markdown('Russel :  ' + str(russel_cur) + ' Change: ' + str(russel_change) + '%')
    
    dj = yf.Ticker("^DJI")
    dj_cur = dj.info['regularMarketPrice']
    dj_change = (dj_cur - dj.info['previousClose'])/dj.info['previousClose']*100
    #st.markdown('DOW Jones :  ' + str(dj_cur) + ' Change: ' + str(dj_change) + '%')
    
    fig = plt.figure()
    l1 = [["Nifty",nifty_change,nifty_cur],["Sensex", sensex_change,sensex_cur], ["SNP",snp_change,snp_cur], ["Russel",russel_change,russel_cur], ["DOW Jones",dj_change,dj_cur],["sample",-0.25,100]]
    lp =[]
    ln = []
    for lst in l1:
        lst[1] = round(lst[1],2)
        lst[2]= round(lst[2],0)
        if lst[1] >= 0 :
            lp.append([lst[0],lst[1],lst[2]])
        else:
            ln.append([lst[0],lst[1]*(-1),lst[2]])
    df_lp  =  pd.DataFrame(lp,columns=["Index","Change","Current"])
    df_ln  =  pd.DataFrame(ln,columns=["Index","Change","Current"])
    fig = plt.figure(figsize = (10, 5))
    plt.bar(df_lp['Index'],df_lp['Change'],color="green",width = 0.4)
    plt.bar(df_ln['Index'],df_ln['Change'],color="red",width = 0.4)
    z = list(df_lp['Change']) + list(df_ln['Change'])
    y =[]
    for i in lp:
        y.append(str(i[2]) + "(+" + str(i[1]) + ")")
    for i in ln:
        y.append(str(i[2]) + "(-" + str(i[1]) + ")")
    for i in range(0, len(y)):
        plt.text(i-0.04,z[i]+0.025,y[i])
    
    #plt.tick_params(top='off', bottom='off', left='off', right='off')
    #plt.plot(df_lp['Index'],df_lp['Change'],color="green")
    #plt.plot(df_ln['Index'],df_ln['Change'],color="red")
    
    st.pyplot(fig=plt)

    #st.text("For ratings type Product Rating")
    #st.text("For Text Sentiment type Text Sentiment")
    #algorithm = st.text_input("Please enter the Algorithm",value="")
    #if algorithm == "Product Rating":
    #    execution()
    #elif algorithm == 'Text Sentiment':
    #    textSentiment()
    #     else:
    #         st.text("No such Algorithm defined in this daisi")
        
if __name__ == "__main__":
    GlobalStockTracker()
