
import requests
import configparser
import pandas as pd
import numpy as np
import json
import time as systime
import ast

class API():
    def __init__(self):
        self.token = 'feda87f1f9a79663042fcd5ee82ab17c-22f342d828f6cfd14b6004a04fdb6283'
        self.account = '101-011-11815575-001'
        self.username = 'kgua0311'
        self.header = {"Content-Type": "application/json", "Authorization": "Bearer " + self.token}

        self.pricing_url = 'https://api-fxpractice.oanda.com/v3/accounts/' +self.account+"/pricing"
        self.order_url = 'https://api-fxpractice.oanda.com/v3/accounts/' + self.account + "/orders"
        self.pricing_stream = 'https://stream-fxpractice.oanda.com/v3/accounts/' + self.account+"/pricing/stream"
        self.instruments_url = "https://api-fxpractice.oanda.com/v3/accounts/" + self.account + "/instruments"
#        self.set_instruments()
        self.Tickers = ['USD_CNH',
                        
                        'MBTC_USD',
                        'XAU_CAD',
                        'SGD_HKD',
                        'SPX500_USD',
                        'EUR_HUF',
                        'AUD_NZD',
                        'CAD_JPY',
                        'EU50_EUR',
                        'USB10Y_USD',
                        'ZAR_JPY',
                        'EUR_AUD',
                        'DE30_EUR',
                        'XCU_USD',
                        'XAG_GBP',
                        'HKD_JPY',
                        'XAG_JPY',
                        'XAG_USD',
                        'USD_NOK',
                        'CAD_SGD',
                        'USD_CZK',
                        'GBP_NZD',
                        'XAG_NZD',
                        'FR40_EUR',
                        'EUR_DKK',
                        'USD_CAD',
                        'AUD_JPY',
                        'USD_HUF',
                        'EUR_CZK',
                        'AUD_HKD',
                        'CHF_ZAR',
                        'SUGAR_USD',
                        'EUR_HKD',
                        'AU200_AUD',
                        'NZD_USD',
                        'AUD_USD',
                        'SGD_JPY',
                        'AUD_CAD',
                        'WTICO_USD',
                        'DE10YB_EUR',
                        'CORN_USD',
                        'AUD_CHF',
                        'CN50_USD',
                        'NL25_EUR',
                        'BTC_USD',
                        'TWIX_USD',
                        'EUR_CHF',
                        'USB02Y_USD',
                        'SG30_SGD',
                        'EUR_NOK',
                        'AUD_SGD',
                        'USD_CHF',
                        'TRY_JPY',
                        'USD_THB',
                        'GBP_CHF',
                        'USD_PLN',
                        'GBP_AUD',
                        'EUR_SGD',
                        'CHF_JPY',
                        'USD_INR',
                        'EUR_SEK',
                        'USD_SGD',
                        'XAU_NZD',
                        'XAU_GBP',
                        'USD_DKK',
                        'XPT_USD',
                        'XAG_CHF',
                        'NZD_SGD',
                        'XAU_XAG',
                        'XAG_EUR',
                        'UK10YB_GBP',
                        'SOYBN_USD',
                        'GBP_ZAR',
                        'USD_HKD',
                        'XAU_USD',
                        'GBP_PLN',
                        'USD_JPY',
                        'EUR_TRY',
                        'NAS100_USD',
                        'EUR_ZAR',
                        'XAU_HKD',
                        'NZD_HKD',
                        'NZD_CHF',
                        'XAU_CHF',
                        'GBP_CAD',
                        'USD_SAR',
                        'XAU_JPY',
                        'NZD_CAD',
                        'EUR_JPY',
                        'NZD_JPY',
                        'EUR_NZD',
                        'WHEAT_USD',
                        'XAU_AUD',
                        'US30_USD',
                        'XAU_EUR',
                        'UK100_GBP',
                        'EUR_GBP',
                        'USD_SEK',
                        'GBP_SGD',
                        'US2000_USD',
                        'USB05Y_USD',
                        'USD_ZAR',
                        'NATGAS_USD',
                        'CHF_HKD',
                        'XPD_USD',
                        'GBP_HKD',
                        'EUR_PLN',
                        'BCO_USD',
                        'XAG_AUD',
                        'JP225_USD',
                        'XAG_HKD',
                        'EUR_USD',
                        'XAG_SGD',
                        'XAU_SGD',
                        'IN50_USD',
                        'USD_TRY',
                        'GBP_JPY',
                        'EUR_CAD',
                        'HK33_HKD',
                        'XAG_CAD',
                        'USD_MXN',
                        'GBP_USD',
                        'SGD_CHF',
                        'CAD_CHF',
                        'CAD_HKD',
                        'USB30Y_USD']
    
        
    def set_instruments(self):
        headers = {'Authorization':"Bearer "+ self.token}
        s = requests.Session()
        req = requests.Request("GET", self.instruments_url, headers = headers)#, params = params)
        pre = req.prepare()
        resp = s.send(pre)
        s.close()
        self.instruments = resp.json()
        self.tickers = [instruments ['instruments'][i]['name'] for i in range(len(instruments ['instruments']))]
        
        
    def get_AIBD_signal(self, Hist_Data, power = 0.75, Threshold_ranges = [-0.2, 0.5]):
        time_window = Hist_Data.shape[0] # It identifies the time window for past data you're using
        n = time_window**power # this is one of the parameters of the algoritm
        
        High_shift = Hist_Data['High'].shift(1) # For the current candel, I consider the last 9 candels for calculations in the High
        Low_shift = Hist_Data['Low'].shift(1) # Same for the Low
        TR1 = High_shift-Low_shift # Calculate the first value of reference as an array
        TR2 = np.abs(High_shift - Hist_Data['Close']) # Calculate the second value of reference as an array
        TR3 = np.abs(Low_shift-Hist_Data['Close']) # Calculate the third value of reference as an array
        TR = pd.concat([TR1,TR2,TR3], axis = 1) # join them into a dataframe
        TR = [max(TR.iloc[i,:]) for i in range(TR.shape[0])] # For each row, take the maximum value
        Avr_TR = np.nanmean(TR) # calculate the mean of TR
        High_Range = Hist_Data['High'] - Hist_Data['Low'].min() # Get the difference between the current High and the past min Low
        Low_Range = Hist_Data['Low'] - Hist_Data['High'].max() # Get the difference between the current Low and the past max High
        NHR = High_Range/n/Avr_TR
        NHR = NHR.values[-1] # Extracts the current value of the indicator for the High
        NLR = Low_Range/n/Avr_TR
        NLR = NLR.values[-1] # Extracts the current value of the indicator for the Low
        
        # Defines the value of the signal according to the trading rule
        if (NHR > Threshold_ranges[1] and NLR < Threshold_ranges[0]):
            signal = 1
        elif (NLR > Threshold_ranges[0] and NHR < Threshold_ranges[1]):
            signal = -1
        else:
            signal = 0
    
        return(signal)

    def fetch_hist_prices(self, epic_id, quantity, granularity, price_type):
        """
        This will pull historical prices for certain instrument epic_id.
        epic_id: instrument Ticker
        quantity: number of candles you want to get
        granularity: The frequency of the candle sampling. A string formed by one letter
                S: Seconds
                M: minutes
                H: hours
                D: day
                W: week
                M: month
            followed by the number of the frequency of the sample. Entering M5 as a parameter, will give a 5 minute
             candle as return. More info https://developer.oanda.com/rest-live-v20/instrument-df/#CandlestickGranularity
        price_type: M for mid price, B for bid prices and A for ask prices
        """

        pars = {"instruments": epic_id, "price": price_type, "granularity": granularity, "count": quantity}
        url = 'https://api-fxpractice.oanda.com/v3/instruments/' + epic_id + "/candles"
        session = requests.Session()

        ob_req = requests.Request("GET", url, headers=self.header, params=pars)
        ob_pre = ob_req.prepare()
        resp = session.send(ob_pre)
        session.close()

        if resp.ok:
            dict_response = resp.json()

            df = pd.DataFrame(columns=["o", "h", "l", "c", "volume"])
            for i in dict_response["candles"]:
                if price_type == "M":
                    i['mid']['volume'] = i['volume']
                    df = df.append(pd.DataFrame(i["mid"], index=[i["time"]]))
                if price_type == "B":
                    i['bid']['volume'] = i['volume']
                    df = df.append(pd.DataFrame(i["bid"], index=[i["time"]]))
                if price_type == "A":
                    i['ask']['volume'] = i['volume']
                    df = df.append(pd.DataFrame(i["ask"], index=[i["time"]]))
            df = df.astype(float)
            df.index = pd.to_datetime(df.index)
            return df
        else:
            print(resp.reason)


    def fetch_current_price(self, epic_id):
        pars = {"instruments": epic_id}
        session = requests.Session()  # create a session
        ob_req = requests.Request("GET", self.pricing_url, headers=self.header, params=pars)
        ob_pre = ob_req.prepare()
        resp = session.send(ob_pre)
        session.close()
        if resp.ok:  # If this is "OK" means that the sending and receiving was succesful
            # Extracting information from the json output
            dict_response = resp.json()
            res = {'Instrument': epic_id}
            res['values'] = {}
            res['values']['BID'] = dict_response["prices"][0]["bids"][0]["price"]
            res['values']['OFFER'] = dict_response["prices"][0]["asks"][0]["price"]
        return res
    
    def stream_price(self, epics, multiple = False):
        """
        takes an string of tickers for oanda to stream. For multiple, set parameter
        multiple as True
        """
        
        if multiple:
            epics = ','.join(epics)
        
        url = "https://stream-fxpractice.oanda.com/v3/accounts/" + self.account + "/pricing/stream"
        headers = {'Authorization':"Bearer " + self.token}
        params = {"instruments":epics}
        s = requests.Session()
        req = requests.Request("GET",url, headers = headers, params = params)
        pre = req.prepare()
        resp = s.send(pre, stream = True)
        print(resp.reason)        
        for i in resp.iter_lines(1):
          j = i.decode()
          k = json.loads(j)
          if (k['type'] != 'HEARTBEAT'):
            print(k['instrument'])
            print(str(k['bids']) + ' / ' + str(k['asks']))
            print('\n')
            return k
          else:
              print(j)          

    def placeOrder(self, epic_id, order_type = None, units = None, price = None):
        """
        Function to place orders in OANDA.
        :param epic_id: Ticker of the instrument
        :param order_type: one of the following as strings
                    - MARKET
                    - LIMIT
        :param units: integer of the number of units to buy, negative if selling
        :param price: target price, only for LIMIT, STOP_LOSS, TAKE_PROFIT orders
        """

        if order_type is None:
            print('No type order given. Please specify the order type.')
            return None

        if units > 0:
            stop_price = price * (1 - 0.003)
        else:
            stop_price = price * (1 + 0.003)

        if order_type == "MARKET":
            params = {"order": {"timeInForce": "GTC",
                                "instrument": epic_id,
                                "units": str(units),
                                "type": order_type,
                                # "stopLossOnFill": {
                                #     "price": str(stop_price)
                                # },
                                "positionFill": "DEFAULT"}}

        if order_type == "LIMIT":
            params = {"order": {"price": str(price),
                                "timeInForce": "GTC",
                                "instrument": epic_id,
                                "units": str(units),
                                "type": order_type,
                                # "stopLossOnFill": {
                                #     "price": str(stop_price)
                                # },
                                "positionFill": "DEFAULT"}}

        params = json.dumps(params)
        session = requests.Session()
        req = requests.Request("POST", self.order_url, headers=self.header, data=params)
        pre = req.prepare()
        resp = session.send(pre)
        session.close()
        print(resp.reason)
        ins = resp.json()
        print(ins)

