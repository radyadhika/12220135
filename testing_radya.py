"""
Aplikasi Streamlit untuk menggambarkan statistik penumpang TransJakarta

Sumber data berasal dari Jakarta Open Data
Referensi API Streamlit: https://docs.streamlit.io/library/api-reference
"""

# import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import json
import streamlit as st

# read dataset
filepath = "produksi_minyak_mentah.csv"
df = pd.read_csv(filepath)

df_csv_clean = df.set_index("kode_negara")
df_csv_clean.head()

df_csv_clean = df_csv_clean.drop(["WLD","G20","OECD","OEU","EU28"])
df_csv_clean.reset_index(drop=False, inplace=True)

listkodecsv = []

for i in list(df['kode_negara']):
    if i not in listkodecsv:
        listkodecsv.append(i)

namajson = "kode_negara_lengkap.json"
openjson = open(namajson)
loadjson = json.load(openjson)

list_kode_bersih = []
for i in loadjson :
    A = i.get('alpha-3')
    list_kode_bersih.append(A)
    if A not in listkodecsv:
        list_kode_bersih.remove(A)

df_json = pd.read_json(namajson)

listnama = []
listkodenegara = []
listregion = []
listsubregion = []

for i in range(len(listkodecsv)):
    for j in range(len(list(df_json['alpha-3']))):
        if list(df_json['alpha-3'])[j] == listkodecsv[i] and list(df_json['name'])[j] not in listnama:
            listnama.append(list(df_json['name'])[j])
            listkodenegara.append(list(df_json['country-code'])[j])
            listregion.append(list(df_json['region'])[j])
            listsubregion.append(list(df_json['sub-region'])[j])

df_json_clean = pd.DataFrame(list(zip(listnama, listkodecsv, listkodenegara, listregion, listsubregion)), columns=['NamaNegara', 'ISO3', 'KodeNegara', 'Region', 'SubRegion'])
############### title ###############
st.set_page_config(layout="wide")  # this needs to be the first Streamlit command called
st.title("UAS 12220135")
st.markdown("*Sumber data berasal dari [Jakarta Open Data](https://data.jakarta.go.id/dataset/data-jumlah-penumpang-trans-jakarta-tahun-2019-kpi)*")
############### title ###############)

############### sidebar ###############
st.sidebar.title("Pengaturan")
left_col, mid_col, right_col = st.columns(3)

## User inputs on the control panel
st.sidebar.subheader("Pengaturan konfigurasi tampilan")
N = st.selectbox("Pilih Negara", listnama)
T = st.sidebar.number_input("Tahun Berapa", min_value=1970, max_value=2015, value=1990)
B1 = st.sidebar.number_input("Banyak Negara", min_value=1, max_value=None, value=10)

n_tampil = st.sidebar.number_input("Jumlah baris dalam tabel yang ditampilkan", min_value=1, max_value=None, value=10)
############### sidebar ###############

############### upper left column ###############
left_col.subheader("Tabel representasi data")
left_col.dataframe(df.head(n_tampil))
############### upper left column ###############

############### upper middle column ###############
mid_col.subheader("Jenis transportasi")

for i in range(len(listnama)):
    if listnama[i] == N:
        kodenegarahuruf = listkodecsv[i]
        kodenegaraangka = listkodenegara[i]
        region = listregion[i]
        subregion = listsubregion[i]

# Membuat list baru untuk menampung data produksi negara dan tahunnya
grafik1_tahun = []
grafik1_produksi = []

# Mengambil data produksi dan tahun berdasarkan negara yang dipilih pada
# option dan memasukkannya ke list yang telah dibuat
for i in range(len(list(df_csv_clean['kode_negara']))):
    if kodenegarahuruf == list(df_csv_clean['kode_negara'])[i]:
        grafik1_tahun.append(list(df_csv_clean['tahun'])[i])
        grafik1_produksi.append(list(df_csv_clean['produksi'])[i])

fig, ax = plt.subplots(figsize=(20,10))
plt.plot(grafik1_tahun, grafik1_produksi)
plt.title('Grafik Produksi Negara ' + N, fontsize = 14)
plt.legend([N])
plt.xlabel('Tahun', fontsize = 12)
plt.ylabel('Produksi', fontsize = 12)
plt.grid(axis='y')

mid_col.pyplot(fig)
############### upper middle column ###############

############### upper right column ###############
right_col.subheader("Total penumpang perbulan")

dftahun = df_csv_clean.loc[df_csv_clean['tahun'] == T].sort_values(by=['produksi'], ascending=False)
dftahunbanyak = dftahun[:B1]

negara2 = dftahunbanyak['kode_negara']
produksi2 = dftahunbanyak['produksi']

fig, ax = plt.subplots(figsize=(8,5))
plt.bar(negara2, produksi2)
plt.title('Grafik ' + str(B1) + ' Negara Produksi Terbesar pada Tahun ' + str(T), fontsize = 13)
plt.xlabel('Negara', fontsize = 12)
plt.ylabel('Produksi', fontsize = 12)
plt.grid(axis='y')

right_col.pyplot(fig)
############### upper right column ###############
