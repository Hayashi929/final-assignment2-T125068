import streamlit as st
import pandas as pd
import numpy as np

st.title("streamlitのレイアウト")

st.header('1.カラム')
col=st.columns(3)
col[0].write('カラム1')
col[1].write('カラム2')
col[2].write('カラム3')

st.subheader('検索条件をカラムに分ける')
col=st.columns(2)
col[0].multiselect('支店を選択してください',
                   ['支店A','支店B','支店C','支店D','支店E'],
                   key='ml')
col[1].number_input('年を入力して下さい',
                    min_value=2020,
                    max_value=2026,
                    value=2020,
                    step=1,
                    key='n1')
