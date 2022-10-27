# Copyright 2022 Coinbase Global, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json, requests
from dash import Input, Output
from datetime import datetime


def register_price(app):
    """functionalizes price callbacks into app.py"""

    @app.callback(
        Output("price-ref", "children"),
        Input("product-switcher", "value"))
    def update_price(product_id_selection):
        """calls Exchange Get Product Ticker endpoint for price data"""
        denomination = product_id_selection.split("-")[1]

        now = datetime.now().strftime("%H:%M:%S")
        if "06:00:00" < now < "12:00:00":
            now = "Good morning"
        elif now < "18:00:00":
            now = "Good afternoon"
        else:
            now = "Good evening"

        url = f"https://api.exchange.coinbase.com/products/{product_id_selection}/ticker"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers)
        parse = json.loads(response.text)
        price_val = parse["price"]

        return f"{now}. The price of {product_id_selection} is {price_val} {denomination}."
