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
from st_pages import Page, show_pages

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

st.write(Page("home.py", "FIFA23 Dataset", "⚽️"))

show_pages(
    [
        Page("home.py", "FIFA23 Dataset", "⚽️"),
        Page("pages/0_players.py", "Jogadores", "👨"),
        Page("pages/1_teams.py", "Clubes", "❎"),
    ]
)
