"""Module to move information from mysql instances."""
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.models import Variable
import requests

from datetime import datetime
def get_crypto_data(date, coin_id):
    headers = {
        "accept": "application/json",
        "x_cg_demo_api_key": f"{Variable.get('coin_gecko_api_key_secret')}"
    }

    formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")

    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/history"
    params = {'date': formatted_date}
    result = {'id':None, 'name':None, 'symbol': None, 'price':None}
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            result['name'] = data['name']
            result['symbol'] = data['symbol']
            result['id'] = data['id']
            result['price']  = data['market_data']['current_price']['usd']
        else:
            print(f"Failed to fetch data for {formatted_date}")
            print(f"Error {response.json()}")

    except Exception as e:
        print(f"Error on {formatted_date}: {e}")
    return result


class CryptoValueOperator(BaseOperator):
    """Update attributes in Intercom"""
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
        print(f"el ds es {ds}")
        for coin_id in self.coins_id:
            data = get_crypto_data(ds,coin_id)
            print(f"the data es {data}")