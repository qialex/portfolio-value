import pandas as pd
import requests
import time 

from lib.Config import Config
from lib.storage.StorageSQL import StorageSQL

class PriceDataParser():

    config: None
    storage: None
    
    def __init__(self, config_path): 
        self.config = Config(config_path)
        self.storage = StorageSQL(self.config.get('storage'))

    def run(self):
        while True:
            df = self.get_all_data()
            self.storage.store(df)
            time.sleep(self.config.get('interval_to_check_prices_sec'))

    def get_data_api(self, symbol):

        try:
            api_key = self.config.get('alphavantage_api_key')
            url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=%s&apikey=%s' % (symbol, api_key)
            data = requests.get(url).json()
            return float(data['Global Quote']['05. price'])
        except:
            print('error during getting data for %s' % (symbol))
            return float(0)
            
    def get_all_data(self):
        from datetime import datetime, timedelta
        import functools
        symbols = self.config.portfolio_df['Stock'].tolist()
        data = functools.reduce(
            lambda a, b: a[0].append(b) or a[1].append(self.get_data_api(b)) or a,
            symbols,
            ([], [])
        )
        
        df = pd.DataFrame({
                'date': pd.Series([datetime.now().replace(second=0, microsecond=0)] * len(symbols)),
                'ticker': data[0],
                'price': data[1],
            }).set_index('date')
            
        return df