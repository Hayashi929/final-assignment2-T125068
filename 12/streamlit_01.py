import streamlit as st
import pandas as pd
import numpy as np

st.title('streamlitの基本')

st.write('streamlitの基本的な機能を試します')

df=pd.DataFrame(data=np.random.randint(0,100,(3,6)),
             index=['支店A','支店B','支店C'],
             columns=['1月','2月','3月','4月','5月','6月'])

st.header('1.DataFrameの表示')
st.dataframe(df,width=600,height=200)

st.header('2.テーブルの表示')
st.table(df)

st.header('3.折れ線グラフの表示')
st.line_chart(df)
