import pandas as pd
import sqlite3
from lib.storage.Storage import Storage


class StorageSQL(Storage):
    
    config: None

    def __init__(self, config):
        self.config = config
        self.table, self.path = (self.config['table'], self.config['path'])
    
    def store(self, df):
        if super().store(df) == False:
            return False

        try:
            con = sqlite3.connect(self.path)
            # we can check for dupicates here
            # or we tune our db to have date as index and update exising lines instead of inserting duplicating
            df.to_sql(self.table, con, if_exists='append')
            con.close()       
        except:
            print('error storing data in SQL')
            
    def get(self):
        try:
            con = sqlite3.connect(self.path)
            df = pd.read_sql_query("SELECT * FROM %s " % (self.table), con)
            con.close()
            return df \
                .drop_duplicates(['date', 'ticker']) \
                .set_index('date')
        except:
            print('error getting data in SQL')