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
from dash import Dash
from callback_graph import register_graph
from callback_price import register_price
from prime_api import prime_calls
from layout import layout

app = Dash(__name__)
app.title = "Insto trading app"

app.layout = layout
register_graph(app)
register_price(app)
prime_calls(app)

if __name__ == "__main__":
    app.run_server(debug=True)
