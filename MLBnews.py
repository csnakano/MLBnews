# !pip install -U beautifulsoup4
# !pip install streamlit
# !pip install googletrans==3.1.0a0
# !pip install transformers
from bs4 import BeautifulSoup
import requests
import time
import streamlit as st
from googletrans import Translator
import torch
from transformers import pipeline

st.title(
"MLB日本人プレイヤーまとめ")
""
"MLBの日本人プレイヤーの記事を検索したり翻訳したりします"
""
#選手辞書
N_reage_playerlist = {
"ダルビッシュ  有":"yu darvish", "松井 祐樹":"yuki matsui", "鈴木 誠也":"seiya suzuki", 
"今永 昇太":"shota imanaga", "山本 由伸":"yoshinobu yamamoto", "大谷 翔平":"shohei ohtani", 
"千賀 滉大":"kodai senga","藤浪 晋太郎":"shintaro fujinami","ラーズ・ヌートバー":"lars nootbaar",
}
A_reage_playerlist = {
"菊池雄星":"yusei kikuchi","前田健太":"kenta maeda","吉田 正尚":"masataka yoshita"
}

st.subheader('☆☆最新ニュースを検索☆☆')
# リーグを選択
league = st.radio("リーグを選んでください", ("ナショナル・リーグ", "アメリカン・リーグ",))
if league == "ナショナル・リーグ":
    players = []
    # 選手を選択
    player = N_reage_playerlist[st.selectbox(
        "誰を検索しますか？",
        [players for players in N_reage_playerlist.keys()]
    )]
if league == "アメリカン・リーグ":
    players = []
    # 選手を選択
    player = A_reage_playerlist[st.selectbox(
        "誰を検索しますか？",
        [players for players in A_reage_playerlist.keys()]
    )]
""

# チェックボックス
if st.button("検索"):
  st.write("最新ニュース一覧")
  url = (f"https://www.mlb.com/search?q={player}")
  r = requests.get(url) 
  soup = BeautifulSoup(r.text, "html.parser") 

  # 検索結果のURLを抽出
  urls = []
  for i in range(1, 6):
     el = soup.select(f"#root > div.styles__AppContainer-sc-14vxo4n-0.jlcbYQ > div.styles__SearchContent-huywcz-0.hMYHyt > div.search-content__results > div > div> a:nth-child({i})")[0]
     urls.append(el.get('href'))
# 検索結果のURLを出力
  headings = soup.find_all("h3")
  for i in range(5):
    st.write("*",headings[i].text)
    st.write("└",urls[i])

trans = Translator()

st.subheader("記事翻訳&要約")

text = st.text_area("記事内容をさっくりと翻訳します", placeholder="ここに記事内容を貼り付け")

trans = Translator()

if st.button("翻訳"):
    with st.spinner("翻訳中・・・"):
        pipe = pipeline("summarization")
        result = pipe(text, max_length=100, min_length=50)
        text = result[0]["summary_text"]
        result = trans.translate(text, src='en', dest='ja')
        result.text


