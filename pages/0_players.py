# Copyright (c) InforServ (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import pandas as pd
from datetime import datetime
import requests

st.set_page_config(
    page_title="FIFA23 JOGADORES! ⚽️",
    page_icon="👨",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.inforserv.pt/contact/',
        'Report a bug': "https://www.inforserv.pt/contact/",
        'About': "# InforServ. This is an *extremely* cool app!"
    }
)

class RealTimeCurrencyConverter():
    def __init__(self,url):
        self.data= requests.get(url).json()
        self.currencies = self.data['rates']

    def convert(self, from_currency, to_currency, amount): 
        initial_amount = amount 
        #first convert it into USD if it is not in USD.
        # because our base currency is USD
        if from_currency != 'USD' : 
            amount = amount / self.currencies[from_currency] 
    
        # limiting the precision to 4 decimal places 
        amount = round(amount * self.currencies[to_currency], 4) 
        return amount

if "data" not in st.session_state:
    df_data = pd.read_csv("CLEAN_FIFA23_official_data.csv", index_col=0)
    df_data = df_data[df_data["Contract Valid Until"] >= datetime.today().year]
    df_data = df_data[df_data["Value(£)"] > 0]
    df_data = df_data.sort_values(by="Value(£)", ascending=False)
    st.session_state["data"] = df_data
else:
    df_data = st.session_state["data"]

clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)

df_players = df_data[df_data["Club"] == club]
players = df_players["Name"].value_counts().index
player = st.sidebar.selectbox("Jogador", players)

st.sidebar.markdown("""---""")
st.sidebar.markdown("Desenvolvido por [InforServ](https://www.inforserv.pt)")

player_stats = df_data[df_data["Name"] == player].iloc[0]

st.image(player_stats["Photo"])
st.title(f"{player_stats['Name']}")

ccol1, ccol2, ccol3, ccol4, ccol5 = st.columns(5)
ccol1.markdown(f"**País:** {player_stats['Nationality']}")
ccol2.image(player_stats['Flag'])

col_1, col0, col00, col000, col0000 = st.columns(5)
col_1.markdown(f"**Club:** {player_stats['Club']}")
col0.image(player_stats['Club Logo'])
st.markdown(f"**Posição:** {player_stats['Position']}")

col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"**Idade:** {player_stats['Age']}")
col2.markdown(f"**Altura:** {player_stats['Height(cm.)'] / 100} mt")
col3.markdown(f"**Peso:** {player_stats['Weight(lbs.)'] * 0.453:.2f} kg")

st.divider()
st.subheader(f"Overall {player_stats['Overall']}")
st.progress(int(player_stats['Overall']))

st.divider()

col5, col6, col7 = st.columns(3)
url = 'https://api.exchangerate-api.com/v4/latest/USD'
converter = RealTimeCurrencyConverter(url)
col5.metric(label="Valor de mercado", value=f"€ {converter.convert('GBP','EUR', player_stats['Value(£)']):,.1f}")
col5.metric(label="Valor de mercado (£)", value=f"£ {player_stats['Value(£)']:,}")

col6.metric(label="Remuneração Semanal", value=f"€ {converter.convert('GBP','EUR', player_stats['Wage(£)']):,.1f}")
col6.metric(label="Remuneração Semanal (£)", value=f"£ {player_stats['Wage(£)']:,}")

col7.metric(label="Cláusula de rescisão", value=f"€ {converter.convert('GBP','EUR', player_stats['Release Clause(£)']):,.1f}")
col7.metric(label="Cláusula de rescisão (£)", value=f"£ {player_stats['Release Clause(£)']:,}")

st.divider()
