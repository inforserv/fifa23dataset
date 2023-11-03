# Copyright (c) InforServ (2023)
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
import webbrowser
from datetime import datetime

st.set_page_config(
    page_title="FIFA23 OFFICIAL DATASET! ⚽️",
    page_icon="⚽️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.inforserv.pt/contact/',
        'Report a bug': "https://www.inforserv.pt/contact/",
        'About': "# InforServ. This is an *extremely* cool app!"
    }
)

if "data" not in st.session_state:
    df_data = pd.read_csv("CLEAN_FIFA23_official_data.csv", index_col=0)
    df_data = df_data[df_data["Contract Valid Until"] >= datetime.today().year]
    df_data = df_data[df_data["Value(£)"] > 0]
    df_data = df_data.sort_values(by="Value(£)", ascending=False)
    st.session_state["data"] = df_data
else:
    df_data = st.session_state["data"]

st.sidebar.markdown("""---""")
st.sidebar.markdown("Desenvolvido por [InforServ](https://www.inforserv.pt)")
    
st.write("# FIFA23 OFFICIAL DATASET! ⚽️")

btn = st.button("Acesse os dados no Kaggle")
if btn:
    webbrowser.open_new_tab("https://www.kaggle.com/datasets/kevwesophia/fifa23-official-datasetclean-data/data")
    
st.markdown(
    """
    O conjunto de dados 
    de jogadores de futebol de 2017 a 2023 fornece informações 
    abrangentes sobre jogadores de futebol profissionais. 
    O conjunto de dados contém uma ampla gama de atributos, incluindo dados 
    demográficos dos jogadores, características físicas, estatísticas de jogo, 
    detalhes de contratos e afiliações de clubes. 
    
    Com **mais de 17.000 registros**, este conjunto de dados oferece um recurso valioso para 
    analistas de futebol, pesquisadores e entusiastas interessados em explorar vários 
    aspectos do mundo do futebol, pois permite estudar atributos de jogadores, métricas de 
    desempenho, avaliação de mercado, análise de clubes, posicionamento de 
    jogadores e desenvolvimento do jogador ao longo do tempo.
    """
    )        
