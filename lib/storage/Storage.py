class Storage():

    config: None

    def __init__(self, config):
        self.config = config
  
    def store(self, df):
        df = df[df['price'] != 0]
        if df.shape[0] == 0:
            print ('no prices to store. all 0')
            return False
        return True

    def get(self):
        pass