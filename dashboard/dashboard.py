import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style="dark")


def create_most_genre_release_df(df):
    exp_genre_yang_paling_banyak_dirilis = df.groupby(["Genre"])["Film Dirilis"].sum().reset_index().sort_values(ascending=False,by="Film Dirilis")
    exp_genre_yang_paling_banyak_dirilis["Film Dirilis"] = exp_genre_yang_paling_banyak_dirilis["Film Dirilis"].astype(int)
    return exp_genre_yang_paling_banyak_dirilis

def create_year_with_most_gross_df(df):
    exp_tahun_pendapatan_kotor_terbanyak = df.groupby("Tahun").agg({
    "Pendapatan Kotor": "max"
    }).sort_values(ascending = False, by = "Pendapatan Kotor").reset_index()
    return exp_tahun_pendapatan_kotor_terbanyak

def create_top_film_with_most_gross_df(df):
    exp_film_dengan_pendapatan_kotor_terbanyak = df.groupby(by="Film Teratas").agg({
        "Pendapatan Kotor Film Teratas": "sum"
    }).sort_values(ascending=False,by="Pendapatan Kotor Film Teratas").reset_index()
    return exp_film_dengan_pendapatan_kotor_terbanyak

df = pd.read_csv("dashboard/all_data.csv")
year_min = df["Tahun"].min()
year_max = df["Tahun"].max()
start_year_current = year_min
end_year_current = year_max

with st.sidebar:
    st.image("th.jpg")
    values = st.slider(
        label= "Pilih jangkauan tahun",
        min_value= year_min,
        max_value=year_max,
        value=(year_min,year_max)
    )
    start_year_current,end_year_current = values

main_df = df[(df["Tahun"] >= start_year_current) & (df["Tahun"] <= end_year_current)]
df_most_genre_release = create_most_genre_release_df(main_df)
df_year_with_most_gross = create_year_with_most_gross_df(main_df)
df_top_film_with_most_gross_ = create_top_film_with_most_gross_df(main_df)

st.header("Analisa Industri Film Amerika")
st.header("Dengan rentang tahun " + str(start_year_current) + " - " + str(end_year_current),divider="rainbow",)
st.write("")
st.subheader("Genre Yang Paling Banyak Dirilis")
col1,col2 = st.columns(2)
with col1:
    total_genre = str(df_most_genre_release["Genre"].count()) + " Genre"
    st.metric("Total Genre",value=total_genre)
with col2:
    total_rilis = str(df_most_genre_release["Film Dirilis"].sum()) + " Film"
    st.metric("Total Rilis",value=total_rilis)    
fig,ax = plt.subplots()
flavor = df_most_genre_release["Genre"].head(5)
votes = df_most_genre_release["Film Dirilis"].head(5)
colors = ('#8B4513', '#FFF8DC', '#93C572', '#E67F0D','#93C')
explode = (0.1,0,0,0,0)
ax.pie(
    x=votes,
    labels=flavor,
    colors=colors,
    wedgeprops={'width':0.4},
    explode=explode,
    autopct='%1.1f%%'
)
st.pyplot(fig)

st.subheader("Tahun Dengan Pendapatan Kotor Terbanyak")
fig,ax = plt.subplots(figsize = (16,10))
sns.barplot(data=df_year_with_most_gross,x=df_year_with_most_gross["Tahun"],y=df_year_with_most_gross["Pendapatan Kotor"],label ="Pendapatan Kotor",palette="viridis")
st.pyplot(fig)

st.subheader("Film Dengan Pendapatan Kotor Terbanyak")
fig,ax = plt.subplots(figsize = (16,10))
sns.set(style="whitegrid")
sns.barplot(x=df_top_film_with_most_gross_["Film Teratas"], y=df_top_film_with_most_gross_["Pendapatan Kotor Film Teratas"], data=df_top_film_with_most_gross_, palette='viridis')
# ax.title('Box Office Film Teratas')
# ax.xlabel('Film')
# ax.ylabel('Box Office (in millions)')
# ax.xticks(rotation=45, ha='right')
st.pyplot(fig)
