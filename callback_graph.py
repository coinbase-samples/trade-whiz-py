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
import plotly.graph_objects as go
import pandas as pd
from dash import Input, Output
from ta import momentum
from ta.trend import MACD
from plotly.subplots import make_subplots


def create_dataframe(parse):
    """called by register_graph to build a dataframe from Coinbase candlestick chart data"""
    df = pd.DataFrame(
        parse,
        columns=[
            "timestamp",
            "price_low",
            "price_high",
            "price_open",
            "price_close",
            "volume",
        ],
    )
    df = df.loc[::-1].reset_index(drop=True)
    df["diff"] = df["price_close"] - df["price_open"]
    df["rsi"] = momentum.rsi(df["price_close"], window=14, fillna=False)
    df.loc[df["diff"] >= 0, "color"] = "green"
    df.loc[df["diff"] < 0, "color"] = "red"
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
    df["rsi"] = momentum.rsi(df["price_close"], window=14, fillna=False)
    df["MA20"] = df["price_close"].rolling(window=20).mean()
    df["MA7"] = df["price_close"].rolling(window=7).mean()
    return df


def render_graph(df):
    max_volume = df["volume"].max()

    macd = MACD(
        close=df["price_close"], window_slow=26, window_fast=12, window_sign=9
    )

    fig1 = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.01,
        row_heights=[0.8, 0.2, 0.15],
        specs=[
            [{"secondary_y": True}],
            [{"secondary_y": True}],
            [{"secondary_y": True}],
        ],
    )
    fig1.add_trace(
        go.Candlestick(
            x=df["timestamp"],
            open=df["price_open"],
            high=df["price_high"],
            low=df["price_low"],
            close=df["price_close"],
            name="Price",
        )
    )
    fig1.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["MA20"],
            opacity=0.7,
            line=dict(color="blue", width=2),
            name="MA 20",
        )
    )
    fig1.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["MA7"],
            opacity=0.7,
            line=dict(color="orange", width=2),
            name="MA 7",
        )
    )
    fig1.add_trace(
        go.Bar(
            x=df["timestamp"],
            y=df["volume"],
            name="Volume",
            marker={"color": df["color"]},
        ),
        secondary_y=True,
    )
    fig1.add_trace(go.Bar(x=df["timestamp"], y=macd.macd_diff()), row=2, col=1)
    fig1.add_trace(
        go.Scatter(
            x=df["timestamp"], y=macd.macd(), line=dict(color="black", width=2)
        ),
        row=2,
        col=1,
    )
    fig1.add_trace(
        go.Scatter(
            x=df["timestamp"], y=macd.macd_signal(), line=dict(color="red", width=1)
        ),
        row=2,
        col=1,
    )
    fig1.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["rsi"],
            mode="lines",
            line=dict(color="purple", width=1),
        ),
        row=3,
        col=1,
    )

    fig1.update_layout(
        height=900, showlegend=False, xaxis_rangeslider_visible=False
    )

    fig1.update_yaxes(title_text="<b>Price</b>", row=1, col=1)
    fig1.update_yaxes(
        title_text="<b>Volume</b>",
        range=[0, max_volume * 5],
        row=1,
        col=1,
        secondary_y=True,
    )
    fig1.update_yaxes(title_text="<b>MACD</b>", showgrid=False, row=2, col=1)
    fig1.update_yaxes(title_text="<b>RSI</b>", row=3, col=1)
    return fig1


def register_graph(app):
    """functionalizes chart callbacks into app.py"""

    @app.callback(
        Output("product-chart", "figure"),
        Input("product-switcher", "value"),
        Input("gran-switcher", "value"),
    )
    def update_output(product_id_selection, granularity_selection):
        """updates Plotly candlestick chart on UI product and granularity inputs"""
        url = f"https://api.exchange.coinbase.com/products/{product_id_selection}/candles?granularity={str(granularity_selection)}"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)

        df = create_dataframe(data)
        return render_graph(df)
