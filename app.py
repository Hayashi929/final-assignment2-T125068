import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

st.title('タバコ・アルコールの物価と癌罹患数の関係（複数表示）')

with st.expander("アプリの概要・目的・使い方"):
    st.markdown("""
    **概要**  
    本アプリは、e-Statの統計データを用いて、たばこ・アルコール品の物価推移と
    がん罹患数の推移を同時に可視化するWebアプリです。

    **目的**
    - タバコ・アルコールの価格変化とがん罹患数の長期的推移を比較する
    - がん部位ごとの傾向を把握する

    **使い方**
    1. サイドバーから商品を選択
    2. がんの部位を1つ選択
    3. 表示する罹患数（男・女・総数）を選択
    4. 凡例をクリックすると表示のON/OFFが可能
    """)


price_df = pd.read_csv('maindata.csv')
cancer_df = pd.read_csv('cancer.csv')

price_df.columns = price_df.columns.str.strip()
cancer_df.columns = cancer_df.columns.str.strip()
cancer_df = cancer_df.rename(columns={"年": "year"})

product = st.sidebar.multiselect(
    "商品を選択してください",
    price_df["product"].unique()
)

site = st.sidebar.selectbox(
    "がんの部位を選択してください",
    cancer_df["部位"].unique()
)

gender = st.sidebar.selectbox(
    "表示する罹患数",
    ["罹患数(男)", "罹患数(女)", "罹患数(総数)"]
)

if len(product) == 0:
    st.warning("商品を選択してください")
    st.stop()

price_df = price_df[price_df["product"].isin(product)]
cancer_df = cancer_df[cancer_df["部位"]==site]

df = pd.merge(price_df, cancer_df, on="year")
df = df.sort_values("year")

st.markdown("## データ概要")
st.write(f"対象年：{df['year'].min()}年 ～ {df['year'].max()}年")
st.write(f"データ件数：{len(df)} 件")
st.write(f"がん部位：{site}")
st.write(f"商品：{', '.join(product)}")

fig = make_subplots(specs=[[{"secondary_y": True}]])

for s in df["部位"].unique():
    temp = df[df["部位"] == s]

fig.add_trace(
    go.Scatter(
        x=df["year"],
        y=df[gender],
        name=f"{site} がん罹患数",
        mode="lines+markers",
        line=dict(width=4)
    ),
    secondary_y=False,
)

for p in df["product"].unique():
    temp = df[df["product"] == p]

    fig.add_trace(
        go.Scatter(
            x=temp["year"],
            y=temp["price"],
            name=f"{p} 物価",
            mode="lines+markers",
            line=dict(dash="dot")
        ),
        secondary_y=True,
    )

fig.update_layout(
    title=f"{site} がん罹患数と {'・'.join(product)} の物価推移",
    xaxis_title="年",
    legend_title="凡例（クリックで表示切替）"
)

fig.update_yaxes(title_text="罹患数（人）", secondary_y=False)
fig.update_yaxes(title_text="価格（円）", secondary_y=True)

st.markdown("## 年ごとのがん罹患数（棒グラフ）")

bar_df = df.groupby("year")[gender].sum().reset_index()

fig_bar = go.Figure()
fig_bar.add_trace(
    go.Bar(
        x=bar_df["year"],
        y=bar_df[gender],
        name="罹患数"
    )
)

fig_bar.update_layout(
    xaxis_title="年",
    yaxis_title="罹患数（人）"
)

st.markdown("## 可視化結果の考察")

latest_year = df["year"].max()
latest_value = int(df[df["year"] == latest_year][gender].sum())

st.metric(
    label=f"{latest_year}年 {site}の罹患数",
    value=f"{latest_value:,} 人"
)

price_trend = df.groupby("year")["price"].mean().diff().mean()
cancer_trend = df.groupby("year")[gender].sum().diff().mean()

if price_trend > 0 and cancer_trend > 0:
    st.write("物価とがん罹患数はいずれも増加傾向にあります。")
elif price_trend > 0 and cancer_trend < 0:
    st.write("物価は上昇している一方で、がん罹患数は減少傾向が見られます。")
else:
    st.write("明確な増減傾向は確認できませんでした。")

st.plotly_chart(fig)
st.caption(
    "※ 左軸はがん罹患数（人）、右軸は価格（円）を示します。"
    "数値の大小を直接比較するものではありません。"
)
st.plotly_chart(fig_bar)


