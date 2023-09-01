

from kiteconnect import KiteConnect

import pandas as pd
import datetime 
from kiteconnect import KiteTicker




#generate trading session
access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)

kws = KiteTicker(key_secret[0],kite.access_token)




niftyLtp = kite.quote("NSE:NIFTY 50")

niftyCurrentPrice= int(niftyLtp.get("NSE:NIFTY 50").get("last_price"))


def next_Thrusdayweekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def roundOffvalue(strickPrice,roundValue):
  
    # Smaller multiple
    a = (strickPrice // roundValue) * roundValue
      
    # Larger multiple
    b = a + roundValue
      
    # Return of closest of two
    return (b if strickPrice - a > b - strickPrice else a)


def createListOfStrickPrices(currentPrice,noofsrticks,strickdifference):
    strickprices = []
    
    StrickPrice = currentPrice
    for i in range(1,noofsrticks+1):
      StrickPrice = StrickPrice - strickdifference
      strickprices.append(StrickPrice)
      
    postiveStrickPrice = currentPrice
    for i in range(1,noofsrticks+1):
     postiveStrickPrice = postiveStrickPrice+strickdifference
     strickprices.append(postiveStrickPrice)
     strickprices.sort()
     
    return strickprices


instrument_df = pd.DataFrame(kite.instruments())
dataframeofOptions = instrument_df[(instrument_df['name'] =='NIFTY') & (instrument_df['expiry'] == next_Thrusdayweekday(datetime.date.today(),3)) & (instrument_df['strike'].isin(createListOfStrickPrices(roundOffvalue(niftyCurrentPrice,50),10,50)))]
instrumentsTokenList = dataframeofOptions['instrument_token'].tolist()



def on_ticks(ws,ticks):
    # Callback to receive ticks.
    #logging.debug("Ticks: {}".format(ticks))
    print(ticks)

def on_connect(ws,response):
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
    #logging.debug("on connect: {}".format(response))
    ws.subscribe(instrumentsTokenList)
    ws.set_mode(ws.MODE_FULL,instrumentsTokenList) # Set all token tick in `full` mode.
  
 

kws.on_ticks=on_ticks
kws.on_connect=on_connect
kws.connect()



#nifty50TokenDF = instrument_df[instrument_df['name'] =='NIFTY 50']

#nifty50Token = nifty50TokenDF['instrument_token'].loc[nifty50TokenDF.index[0]]



