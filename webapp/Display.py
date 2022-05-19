import pandas as pd
import plotly.express as px

class Display():
    
    def portfolio(portfolio_df):
        df = portfolio_df.copy()
        df['to_display'] = df['Stock'] + df['Weight'].apply(lambda x: ': %s' % (str(round(x * 100, 2))+'%') )
        df['w_abs'] = df['Weight'].abs()
        fig = px.pie(df, values='w_abs', names='to_display', title='Portfolio')
        fig.update_traces(textposition='inside', textinfo='label')
        return fig
        
    def chart(portfolio_df, data_df, show_mode='only_total'):
        df = data_df.reset_index()
        tickers = list(portfolio_df['Stock'].values)
        
        if show_mode == 'only_total':
            columns = ['total']
            
        if show_mode == 'all_relative':
            columns = ['total']
            for column in tickers:
                df['%s_show' % column] = df['%s_change_relative' % column] + 1
                columns.append('%s_show' % column)
            
        if show_mode == 'abs_prices':
            columns = []
            for column in tickers:
                columns.append(column)
            

        fig = px.line(df, x='date', y=columns)
        fig.update_layout(hovermode="x unified")
        fig.update_xaxes(rangeslider_visible=True)
        return fig        