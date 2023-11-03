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
    page_title="FIFA23 TEAMS! ⚽️",
    page_icon="❎",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.inforserv.pt/contact/',
        'Report a bug': "https://www.inforserv.pt/contact/",
        'About': "# This is a header. This is an *extremely* cool app!"
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

df_filtered = df_data[df_data["Club"] == club].set_index("Name") 

st.sidebar.markdown("""---""")
st.sidebar.markdown("Desenvolvido por [InforServ](https://www.inforserv.pt)")

st.image(df_filtered.iloc[0]["Club Logo"])
st.markdown(f"## {club}")

url = 'https://api.exchangerate-api.com/v4/latest/USD'
converter = RealTimeCurrencyConverter(url)
df_filtered["Value(€)"] = converter.convert('GBP','EUR', df_filtered['Value(£)'])
df_filtered["Wage(€)"] = converter.convert('GBP','EUR', df_filtered['Wage(£)'])
df_filtered["Release Clause(€)"] = converter.convert('GBP','EUR', df_filtered['Release Clause(£)'])

columns = ["Age", "Photo", "Flag", "Overall", "Value(€)", "Wage(€)", "Release Clause(€)",
           "Joined", "Contract Valid Until", "Height(cm.)", "Weight(lbs.)"
           ]

df_filtered = df_filtered[columns]

value_total = '{:,.0f} €'.format(df_filtered["Value(€)"].sum())
wage_total = '{:,.0f} €'.format(df_filtered["Wage(€)"].sum())

df_filtered = df_filtered.style.format(
    {
        "Value(€)": lambda x : '{:,.0f} €'.format(x),
        "Wage(€)": lambda x : '{:,.0f} €'.format(x),
        "Release Clause(€)": lambda x : '{:,.0f} €'.format(x),
        "Contract Valid Until": lambda x : '{:.0f}'.format(x),
        "Height(cm.)": lambda x : '{:.2f} mt'.format(x / 100),
        "Weight(lbs.)": lambda x : '{:.2f} kg'.format(x * 0.453),  
    }
)

st.markdown(f"### Valor de Mercado da Equipa: **{value_total}**")
st.markdown(f"#### Custo Semanal com Jogadores: **{wage_total}**")

st.dataframe(df_filtered,
             column_config={
                 "Name": st.column_config.TextColumn(label="Nome", width=180),
                 "Age": st.column_config.TextColumn(label="Idade", width="small"),
                 "Overall": st.column_config.ProgressColumn("Overall", format="%d", min_value=0, max_value=100, width="medium"),
                 "Photo": st.column_config.ImageColumn("Foto", width="small"),
                 "Flag": st.column_config.ImageColumn("País", width="small"),
                 "Joined": st.column_config.DateColumn("Entrou a", width="small"),
                 "Contract Valid Until": st.column_config.TextColumn(label="Contrato até", width="small"),
                 "Value(€)": st.column_config.TextColumn(label="Valor Mercado (€)", width=120),
                 "Wage(€)": st.column_config.TextColumn(label="Salário Semanal (€)", width=120),
                 "Release Clause(€)": st.column_config.TextColumn(label="Cláusula Rescisão (€)", width=140),
                 "Height(cm.)": st.column_config.TextColumn(label="Altura (mt)", width="small"),
                 "Weight(lbs.)": st.column_config.TextColumn(label="Peso (Kg)", width="small"),
             },
             height=600,
             use_container_width=True,
             hide_index=False
             )