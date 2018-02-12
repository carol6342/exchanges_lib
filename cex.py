import time
import requests
import hashlib
import json
import hmac
import datetime

class CexAPI(object):
  def __init__(self, user_id, api_key, api_secret):
    self.user_id = user_id
    self.api_key = api_key
    self.api_secret = api_secret

  def set_nonce(self):
    self.nonce = '{:.10f}'.format(time.time() * 1000).split('.')[0]

  def get_curr_timestamp(self):
      return int(datetime.datetime.now().timestamp() * 1000)

  def get_signature(self):
    self.set_nonce()
    #message = self.nonce + self.user_id + self.api_key
    #key_bytes = bytes(self.api_secret, 'latin-1')
    timestamp = self.get_curr_timestamp()
    message = "{}{}{}".format(timestamp, self.user_id, self.api_key)
    return hmac.new(self.api_secret.encode(), msg=message.encode(), digestmod=hashlib.sha256).hexdigest().upper()

  def request_url(self, url, params):
    r = requests.post(url=url, data=params)
    data = json.loads(r.text)
    return data

  def api_call(self, api_function, params={}, private=0, pair=''):
    url = 'https://cex.io/api/' + api_function + '/' + pair

    if private == 1:
      params = dict(
          key=self.api_key,
          signature=self.get_signature(),
          nonce=self.nonce
      )

    return self.request_url(url, params)

  def balance(self):
    return self.api_call('balance', {}, 1)

  def archived_orders(self, pair):
    return self.api_call('archived_orders', True, pair)

  def open_orders(self):
    return self.api_call('open_orders', True)

  def last_price(self, pair):
    return self.api_call('last_price', False, pair)

  def current_orders(self, couple='GHS/BTC'):
    return self.api_call('open_orders', {}, 1, couple)

  def cancel_order(self, order_id):
    return self.api_call('cancel_order', {"id": order_id}, 1)
  
  def cancel_orders(self, couple=''):
    return self.api_call('cancel_orders',{},1, couple)
  
  def place_order(self, ptype='buy', amount=0, price=0, couple=''):
    return self.api_call('place_order', {"type": ptype, "amount": str(amount), "price": str(price)}, 1,  couple)

  def price_stats(self, last_hours, max_resp_arr_size, couple='GHS/BTC'):
    return self.api_call(
      'price_stats',
      {"lastHours": last_hours, "maxRespArrSize": max_resp_arr_size},
      0, couple)
