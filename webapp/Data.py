import pandas as pd

import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from lib.Config import Config
from lib.storage.StorageSQL import StorageSQL

class Data():
    
    config: None
    storage: None
    
    def __init__(self, config_path): 
        self.config = Config(config_path)
        self.storage = StorageSQL(self.config.get('storage'))
        

    def data_to_portfolio(self, df):
        def transform_groupby(x):
            return pd.DataFrame(columns=list(x.ticker.values), data=[list(x.price.values)])
        
        def transform_calc(df_init):
            df = df_init.copy()
            col_list = []
            for column in df.columns:
                df = df[df[column] > 0]

            for column in df.columns:
                w = self.config.portfolio_df[self.config.portfolio_df['Stock'] == column].reset_index().at[0, 'Weight']
                m = 1 if w > 0 else -1
                df['%s_weigth' % column] = w
                df['%s_change_abs' % column] = (df[column] - df[column][0]) * m
                df['%s_change_relative' % column] = (df[column] / df[column][0] - 1) * m
                df['%s_change_relative_w' % column] = (1 + df['%s_change_relative' % column]) * abs(w)
                col_list.append('%s_change_relative_w' % column)
            df.insert(0, "total", df[col_list].sum(axis=1), True)
            return df
        
        temp_df = df.groupby('date')[['ticker', 'price']] \
            .apply(transform_groupby) \
            .reset_index() \
            .set_index('date') \
            .drop('level_1', axis=1)
        
        return transform_calc(temp_df)
    
    def get_all_data(self):
        return (self.config.portfolio_df, self.data_to_portfolio(self.storage.get()))