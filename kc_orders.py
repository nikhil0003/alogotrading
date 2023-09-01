

from kiteconnect import KiteConnect

import pandas as pd
import datetime 




#generate trading session
access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)



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







instrument_dump = kite.instruments()
instrument_df = pd.DataFrame(instrument_dump)
expiryDate = next_Thrusdayweekday(datetime.date.today(),3)
listofStrickprices = createListOfStrickPrices(roundOffvalue(niftyCurrentPrice,50),10,50)
print(listofStrickprices)
dataframeofOptions = instrument_df[(instrument_df['name'] =='NIFTY') & (instrument_df['expiry'] == expiryDate) & (instrument_df['strike'].isin(listofStrickprices))]


#nifty50TokenDF = instrument_df[instrument_df['name'] =='NIFTY 50']

#nifty50Token = nifty50TokenDF['instrument_token'].loc[nifty50TokenDF.index[0]]



