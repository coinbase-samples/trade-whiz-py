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
from dash import html, dcc

layout = html.Div(
    children=[
        html.H1(children="Coinbase Prime trading application"),
        html.Div(id="price-ref", style={"padding-top": 10, "font-size": "22px"}),
        html.Div(
            id="portfolio-bal",
            style={"padding-top": 10, "padding-bottom": 30, "font-size": "22px"},
        ),
        html.Div(
            [
                dcc.Dropdown(
                    [
                        "ETH-USD",
                        "BTC-USD",
                        "CRV-USD",
                        "SOL-USD",
                        "CBETH-USD",
                        "CBETH-ETH",
                    ],
                    "ETH-USD",
                    id="product-switcher",
                    clearable=False,
                    style={"width": "150px"},
                ),
                dcc.Dropdown(
                    options={
                        "60": "1m",
                        "300": "5m",
                        "900": "15m",
                        "3600": "1h",
                        "21600": "6h",
                        "86400": "1d",
                    },
                    value="3600",
                    id="gran-switcher",
                    clearable=False,
                    style={"width": "150px"},
                ),
            ]
        ),
        dcc.Graph(id="product-chart", style={"width": "90%"}),
        html.H1(children="Buy/Sell"),
        html.Div(dcc.Input(id="amount-box", placeholder="quantity", type="text")),
        dcc.Dropdown(
            ["BUY", "SELL"],
            "BUY",
            id="buy-sell-toggle",
            clearable=False,
            style={"width": "150px"},
        ),
        html.Button("Submit", id="submit-button", n_clicks=0),
        html.Div(id="buy-sell-response", style={"padding-top": 10}),
    ],
    style={"padding": 30, "flex": 1, "font-family": "Inter"},
)
