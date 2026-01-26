import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

st.title('streamlitのグラフ表示')

df=pd.DataFrame(data=np.random.randint(0,1000,(3,6)),
             index=['支店A','支店B','支店C'],
             columns=['1月','2月','3月','4月','5月','6月'])

st.header('1.折れ線グラフの表示')
st.line_chart(df.T)

st.header('2.棒グラフの表示')
st.bar_chart(df.T)

st.header('3.面グラフの表示')
st.area_chart(df.T)

st.header('4 散布図の表示')
df_sales_2023=pd.read_csv('air_conditioner_sales_2023.csv',
                          index_col='date')
st.scatter_chart(df_sales_2023,x='temp',y='sales')

st.header('5.散布図の表示')

plt.scatter(df_sales_2023['temp'],
            df_sales_2023['sales'],
            s=50,
            color='b',
            marker='D',
            alpha=0.3
            )
plt.xlim(15.0,40.0)
plt.ylim(300,750)
plt.title('AirConditioner Sales vs Temparature 2023',fontsize=16)
plt.xlabel('Temparature(℃)',fontsize=16)
plt.ylabel('sales (thousand $)',fontsize=16)
plt.grid(True)
plt.tick_params(labelsize=12)
st.pyplot(plt.gcf())

st.header('6.散布図の表示(plotly)')
fig=px.scatter(df_sales_2023,
               x='temp',
               y='sales',
               labels={'temp':'Temparature(C)','sales':'Sales(thousand $)'},
               title='Temp vs Sales')
st.plotly_chart(fig)
