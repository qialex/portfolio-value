import json
import pandas as pd

class Config():
    
    config_path = None
    config = None
    portfolio_df = None

    def __init__(self, config_path):
        self.config_path = config_path
        self.init_config()
        self.init_portfolio()

    def init_config(self):
        file = open(self.config_path)
        self.config = json.load(file)
        file.close()

    def init_portfolio(self):
        self.portfolio_df = pd.read_csv(self.config['portfolio_path'])

    def get(self, property):
        return self.config[property]