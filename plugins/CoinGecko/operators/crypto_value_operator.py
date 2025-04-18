"""Module to move information from mysql instances."""
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.models import Variable
import requests
from datetime import datetime
from airflow.providers.mysql.hooks.mysql import MySqlHook
from include.src.airflow.jinga2 import get_search_path, render_template
import logging

log = logging.getLogger(__name__)

def store_crypto_data(data):
    log.info(f"Inserting data into the database")
    mysql_hook = MySqlHook(mysql_conn_id='mysql_write')
    sql_insert = render_template("crypto_data/insert_crypto_data.sql",
                                 base = data)
    mysql_hook.run(sql_insert, autocommit=False)
    log.info(f"Data loaded in the database")
    return 0

def get_crypto_data(date, coin_id):
    headers = {
        "accept": "application/json",
        "x_cg_demo_api_key": f"{Variable.get('coin_gecko_api_key_secret')}"
    }

    formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")

    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/history"
    params = {'date': formatted_date}
    result = {'id':None, 'name':None, 'symbol': None, 'price':None, 'date' : date}
    try:
        log.info(f"Attemping to get data for {coin_id} date: {date}")
        response = requests.get(url, params=params, headers= headers)
        if response.status_code == 200:
            data = response.json()
            result['name'] = data['name']
            result['symbol'] = data['symbol']
            result['id'] = data['id']
            result['price']  = data['market_data']['current_price']['usd']
        else:
            log.error(f"Failed to fetch data for {formatted_date} due response error")
            log.info(f"Error {response.json()}")

    except Exception as e:
        log.error(f"Error on {formatted_date}: {e}")
    return result


class CryptoValueOperator(BaseOperator):
    """Get and insert cryptocurrencies prices"""
    template_fields = []
    template_ext = ('.sql',)
    ui_color = '#ededed'

    @apply_defaults
    def __init__(self,
                 coins_id,
                 destiny_conn_id='mysql_default',
                 autocommit=False,
                 *args,
                 **kwargs):

        super().__init__(*args, **kwargs)
        self.coins_id = coins_id
        self.autocommit = autocommit


    def execute(self, context):
        """
        Makes a call to the CoinGecko API to get the crypto currencies value

        :param context: Airflow context
        :return: http response
        """
        ds = context['ds']
        crypto_data = []
        for coin_id in self.coins_id:
            current_coin_data = get_crypto_data(ds,coin_id)
            crypto_data.append(current_coin_data)
        store_crypto_data(crypto_data)
