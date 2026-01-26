import streamlit as st
import pandas as pd
import plotly.express as px

st.title('広告費と売り上げ')

df=pd.read_csv('ad_expense_sales.csv')

selected_cats=st.sidebar.multiselect(
    "商品カテゴリ",
    df["prod_category"].unique(),
    default=df["prod_category"].unique()
)

selected_media=st.sidebar.selectbox(
    "広告媒体",
    df["media"].unique()
    )

color_option=st.sidebar.selectbox(
    "色分け",
    ["性別","年齢層","季節"]
)

if color_option=="性別":
    color_col="sex"
elif color_option=="年齢層":
    color_col="age"
else:
    color_col="age"

df=df[df["prod_category"].isin(selected_cats)]
df=df[df["media"]==selected_media]

st.dataframe(df)

fig=px.scatter(
df,
x="ad_expense",
y="sales",
color=color_col,
title="広告費と売り上げの関係"
)

st.plotly_chart(fig)