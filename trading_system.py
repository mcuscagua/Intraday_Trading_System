
import requests
import configparser
import pandas as pd
import json
import time as systime

class API():
    def __init__(self):
        self.token = 'feda87f1f9a79663042fcd5ee82ab17c-22f342d828f6cfd14b6004a04fdb6283'
        self.account = '101-011-11815575-001'
        self.username = 'kgua0311'
        self.header = {"Content-Type": "application/json", "Authorization": "Bearer " + self.token}

        self.pricing_url = 'https://api-fxpractice.oanda.com/v3/accounts/' +self.account+"/pricing"
        self.order_url = 'https://api-fxpractice.oanda.com/v3/accounts/' + self.account + "/orders"
        self.pricing_stream = 'https://stream-fxpractice.oanda.com/v3/accounts/' + self.account+"/pricing/stream"
        
        self.Tickers = {'AUD_CAD': {'minspread':  4.0},
                        'AUD_CHF': {'minspread':  3.2},
                        'AUD_HKD': {'minspread': 22.2},
                        'AUD_JPY': {'minspread':  2.2},
                        'AUD_NZD': {'minspread':  4.5},
                        'AUD_SGD': {'minspread':  5.3},
                        'AUD_USD': {'minspread':  1.6},
                        'CAD_CHF': {'minspread':  3.6},
                        'CAD_HKD': {'minspread': 25.1},
                        'CAD_JPY': {'minspread':  3.5},
                        'CAD_SGD': {'minspread':  6.1},
                        'CHF_HKD': {'minspread': 34.4},
                        'CHF_JPY': {'minspread':  3.7},
                        'CHF_ZAR': {'minspread':501.8},
                        'EUR_AUD': {'minspread':  2.8},
                        'EUR_CAD': {'minspread':  3.7},
                        'EUR_CHF': {'minspread':  2.5},
                        'EUR_CZK': {'minspread':337.5},
                        'EUR_DKK': {'minspread': 23.8},
                        'EUR_GBP': {'minspread':  2.9},
                        'EUR_HKD': {'minspread': 30.7},
                        'EUR_HUF': {'minspread':121.4},
                        'EUR_JPY': {'minspread':  2.7},
                        'EUR_NOK': {'minspread':209.5},
                        'EUR_NZD': {'minspread':  7.0},
                        'EUR_PLN': {'minspread': 52.7},
                        'EUR_SEK': {'minspread':285.7},
                        'EUR_SGD': {'minspread':  7.8},
                        'EUR_TRY': {'minspread':220.0},
                        'EUR_USD': {'minspread':  1.9},
                        'EUR_ZAR': {'minspread':533.6},
                        'GBP_AUD': {'minspread':  9.8},
                        'GBP_CAD': {'minspread':  8.5},
                        'GBP_CHF': {'minspread':  7.3},
                        'GBP_HKD': {'minspread': 47.6},
                        'GBP_JPY': {'minspread':  4.5},
                        'GBP_NZD': {'minspread': 14.8},
                        'GBP_PLN': {'minspread': 71.1},
                        'GBP_SGD': {'minspread': 11.0},
                        'GBP_USD': {'minspread':  3.9},
                        'GBP_ZAR': {'minspread':601.5},
                        'HKD_JPY': {'minspread': 45.9},
                        'NZD_CAD': {'minspread':  5.1},
                        'NZD_CHF': {'minspread':  3.6},
                        'NZD_HKD': {'minspread': 25.6},
                        'NZD_JPY': {'minspread':  2.6},
                        'NZD_SGD': {'minspread':  5.9},
                        'NZD_USD': {'minspread':  2.1},
                        'SGD_CHF': {'minspread':  4.0},
                        'SGD_HKD': {'minspread': 29.0},
                        'SGD_JPY': {'minspread':  3.8},
                        'TRY_JPY': {'minspread':  7.4},
                        'USD_CAD': {'minspread':  3.2},
                        'USD_CHF': {'minspread':  2.4},
                        'USD_CNH': {'minspread': 35.0},
                        'USD_CZK': {'minspread':248.7},
                        'USD_DKK': {'minspread': 25.2},
                        'USD_HKD': {'minspread': 14.1},
                        'USD_HUF': {'minspread': 88.9},
                        'USD_INR': {'minspread': 25.0},
                        'USD_JPY': {'minspread':  1.7},
                        'USD_MXN': {'minspread':207.7},
                        'USD_NOK': {'minspread':202.3},
                        'USD_PLN': {'minspread': 46.8},
                        'USD_SAR': {'minspread': 57.2},
                        'USD_SEK': {'minspread':263.5},
                        'USD_SGD': {'minspread':  4.6},
                        'USD_THB': {'minspread': 12.1},
                        'USD_TRY': {'minspread':180.6},
                        'USD_ZAR': {'minspread':450.3},
                        'ZAR_JPY': {'minspread':  3.6}}
        
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
          print(i)

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

