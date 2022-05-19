import json
from flask import Flask,render_template
import plotly
import plotly.express as px


from Data import Data
from Display import Display

app=Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    portfolio_df, df = Data('./config.json').get_all_data()
    print(df.head(10))
    data = {
        'portfolio_fig_JSON': json.dumps(Display.portfolio(portfolio_df), cls=plotly.utils.PlotlyJSONEncoder),
        'chart_fig_JSON': json.dumps(Display.chart(portfolio_df, df), cls=plotly.utils.PlotlyJSONEncoder),
        'chart_abs_prices_fig_JSON': json.dumps(Display.chart(portfolio_df, df, show_mode='abs_prices'), cls=plotly.utils.PlotlyJSONEncoder),
    }

    return render_template("index.html", data=data)
	
if __name__=='__main__':
    app.run(debug=True)