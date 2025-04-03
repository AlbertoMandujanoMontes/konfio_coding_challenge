import yfinance as yf
import pandas as pd
import mysql.connector

def create_insert_from_df(df, table_name):
    columns = list(df.columns)
    df = df.astype(str)
    df = df.replace('"', '\\"', regex=True)

    def enclose_in_quotes(cell_value):
        return f'"{cell_value}"'

    df = df.applymap(enclose_in_quotes)

    for column in columns:
        df[column] = "" + df[column] + ""

    values = pd.Series(
        '(' + pd.Series(df.fillna('').values.tolist()).str.join(',') + ')').str.cat(sep=',')
    template = f"insert into {table_name} " \
               f"{tuple(columns)} " \
               f"values {values}"

    update_string = ','.join([f"{column} = values({column}) " for column in columns])

    template = template + 'ON DUPLICATE KEY UPDATE ' + update_string
    return template.replace("\'", "")

ticker = 'BTC-USD'

start_date = '2022-01-01'
end_date = '2022-04-01'

btc_data_full = yf.download(ticker, start=start_date, end=end_date)

btc_data = btc_data_full[['Close']].reset_index()

btc_data.columns = ['Date', 'Close']

btc_data.rename(columns = {'Date':'date', 'Close':'price'}, inplace=True)
btc_data['id_crypto'] = 'bitcoin'
btc_data['crypto_name'] = 'Bitcoin'
btc_data['crypto_symbol'] = 'btc'


host = '127.0.0.1'
user = 'dev_user'
password = 'dev_pass'
database = 'konfio_coding_challenge'

cnx = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
)



sql_insert = create_insert_from_df(btc_data, 'crypto_currency_value')

cursor = cnx.cursor()

cursor.execute(sql_insert)
cnx.commit()

cursor.close()
cnx.close()