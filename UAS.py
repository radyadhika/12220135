'''
Nama: Radya Evandhika Novaldi
NIM: 12220135
Topik: UAS Pemrograman Komputer
'''

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
listsampah = []

for i in list(df['kode_negara']):
    if i not in listkodecsv:
        listkodecsv.append(i)

namajson = "kode_negara_lengkap.json"
openjson = open(namajson)
loadjson = json.load(openjson)
df_json = pd.read_json(namajson)

list_kode_bersih = []

for i in listkodecsv:
    if i not in list(df_json['alpha-3']):
        listsampah.append(i)

for i in listsampah:
    df = df[df.kode_negara != i]
    if i in listkodecsv:
        listkodecsv.remove(i)

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
st.title("Informasi Seputar Data Produksi Minyak Mentah dari Berbagai Negara di Seluruh Dunia")
st.markdown("*Aplikasi ini dibuat oleh Radya Evandhika Novaldi/12220135/Teknik Perminyakan Institut Teknologi Bandung*")
############### title ###############)

############### sidebar ###############
st.sidebar.title("Pengaturan")
st.sidebar.subheader("Konfigurasi Grafik")
width = st.sidebar.slider("Lebar Grafik", 1, 25, 13)
height = st.sidebar.slider("Tinggi Grafik", 1, 25, 5)
############### sidebar ###############

col1a, col1b = st.columns(2)

############### first column ###############
col1a.subheader("Tabel Representasi Data Mentah")
n_tampil = col1b.number_input("Jumlah Baris dalam Tabel yang Ingin Ditampilkan", min_value=1, max_value=None, value=10)
col1b.write("\n")
col1b.write("\n")
col1b.write("\n")
S = col1b.selectbox("Filter", list(df_csv_clean.columns))
col1a.dataframe((df_csv_clean.head(n_tampil)).sort_values(by=S, ascending=False))
############### first column ###############

############### second column ###############
st.subheader("Grafik Negara")
N = st.selectbox("Pilih Negara", listnama)

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


fig, ax = plt.subplots(figsize=(width, height))
plt.plot(grafik1_tahun, grafik1_produksi)
plt.title('Grafik Produksi Negara ' + N, fontsize = 14)
plt.legend([N])
plt.xlabel('Tahun', fontsize = 12)
plt.ylabel('Produksi', fontsize = 12)
plt.grid(axis='y')

st.pyplot(fig)
############### second column ###############

st.write("\n")
col3opt1, col3opt2 = st.columns(2)

############### third column ###############
st.subheader("Grafik Jumlah Produksi Minyak Terbesar Pada Tahun Tertentu")

T = col3opt1.number_input("Pilih Tahun", min_value=1970, max_value=2015, value=1990)
B1 = col3opt2.number_input("Pilih Banyaknya Negara", min_value=1, max_value=None, value=10)

dftahun = df_csv_clean.loc[df_csv_clean['tahun'] == T].sort_values(by=['produksi'], ascending=False)
dftahunbanyak = dftahun[:B1]

negara2 = dftahunbanyak['kode_negara']
produksi2 = dftahunbanyak['produksi']

fig, ax = plt.subplots(figsize=(width, height))
plt.bar(negara2, produksi2)
plt.title('Grafik ' + str(B1) + ' Negara Produksi Terbesar pada Tahun ' + str(T), fontsize = 13)
plt.xlabel('Negara', fontsize = 12)
plt.xticks(rotation=90)
plt.ylabel('Produksi', fontsize = 12)
plt.grid(axis='y')

st.pyplot(fig)
############### third column ###############

st.write("\n")

############### fourth column ###############
st.subheader("Grafik Jumlah Produksi Minyak Terbesar Secara Kumulatif Keseluruhan Tahun")

B2 = st.number_input("Banyak Negara", min_value=1, max_value=None, value=10, key=int)

jumlah_produksi_kumulatif = []
# Menjumlahkan produksi minyak tiap negara dan memasukkannya ke list_sum
for i in listkodecsv:
    a = df_csv_clean.loc[df_csv_clean['kode_negara'] == i, 'produksi'].sum()
    jumlah_produksi_kumulatif.append(a)

# Membuat dataframe baru dan diurutkan berdasarkan produksi kumulatif
# minyak terbesar
df3 = pd.DataFrame(list(zip(listkodecsv, jumlah_produksi_kumulatif)), columns=['kode_negara', 'produksi_kumulatif']).sort_values(by=['produksi_kumulatif'], ascending=False)
df3 = df3 [:B2]

negara3 = df3['kode_negara']
produksikumul3 = df3['produksi_kumulatif']

fig, ax = plt.subplots(figsize=(width, height))
plt.bar(negara3, produksikumul3)
plt.title('Grafik ' + str(B2) + ' Negara Produksi Kumulatif Terbesar', fontsize = 13)
plt.xlabel('Negara', fontsize = 12)
plt.xticks(rotation=90)
plt.ylabel('Produksi', fontsize = 12)
plt.grid(axis='y')

st.pyplot(fig)
############### fourth column ###############

st.write("\n")
col5a, col5b = st.columns(2)

############### fifth column ###############
col5a.subheader("Summary Kumulatif")
dfsummary = pd.DataFrame(list(zip(listkodecsv, jumlah_produksi_kumulatif)), columns=['kode_negara', 'produksi_kumulatif'])

dfsummary['NamaNegara'] = list(df_json_clean['NamaNegara'])
dfsummary['Region'] = list(df_json_clean['Region'])
dfsummary['Sub-region'] = list(df_json_clean['SubRegion'])
dfsummary['KodeNegara'] = list(df_json_clean['ISO3'])

dfsummary = dfsummary[['NamaNegara', 'KodeNegara', 'Region', 'Sub-region', 'produksi_kumulatif']].sort_values(by=['produksi_kumulatif'], ascending=False)

df_summary_clean = dfsummary.set_index("produksi_kumulatif")
df_summary_clean.head()
df_summary_clean = df_summary_clean.drop([0])
df_summary_clean.reset_index(drop=False, inplace=True)

print("Negara dengan Produksi Kumulatif Terbesar:")
col5a.markdown("**Negara dengan Produksi Kumulatif Terbesar:**")
print(df_summary_clean.iloc[0]['NamaNegara'])
col5a.markdown("Nama Negara: " + df_summary_clean.iloc[0]['NamaNegara'])
print(df_summary_clean.iloc[0]['KodeNegara'])
col5a.markdown("Kode Negara: " + df_summary_clean.iloc[0]['KodeNegara'])
print(df_summary_clean.iloc[0]['Region'])
col5a.markdown("Region: " + df_summary_clean.iloc[0]['Region'])
print(df_summary_clean.iloc[0]['Sub-region'])
col5a.markdown("Sub-region: " + df_summary_clean.iloc[0]['Sub-region'])
print(df_summary_clean.iloc[0]['produksi_kumulatif'])
col5a.markdown("Produksi Kumulatif: " + str(df_summary_clean.iloc[0]['produksi_kumulatif']) + " TMT")

print("\nNegara dengan Produksi Kumulatif Terkecil:")
col5a.markdown("**Negara dengan Produksi Kumulatif Terkecil:**")
print(df_summary_clean.iloc[len(df_summary_clean)-1]['NamaNegara'])
col5a.markdown("Nama Negara: " + df_summary_clean.iloc[len(df_summary_clean)-1]['NamaNegara'])
print(df_summary_clean.iloc[len(df_summary_clean)-1]['KodeNegara'])
col5a.markdown("Kode Negara: " + df_summary_clean.iloc[len(df_summary_clean)-1]['KodeNegara'])
print(df_summary_clean.iloc[len(df_summary_clean)-1]['Region'])
col5a.markdown("Region: " + df_summary_clean.iloc[len(df_summary_clean)-1]['Region'])
print(df_summary_clean.iloc[len(df_summary_clean)-1]['Sub-region'])
col5a.markdown("Sub-region: " + df_summary_clean.iloc[len(df_summary_clean)-1]['Sub-region'])
print(df_summary_clean.iloc[len(df_summary_clean)-1]['produksi_kumulatif'])
col5a.markdown(str(df_summary_clean.iloc[len(df_summary_clean)-1]['produksi_kumulatif']) + " TMT")

print("\nNegara dengan Produksi Kumulatif Sama Dengan Nol:")
col5a.markdown("**Negara dengan Produksi Kumulatif Sama Dengan Nol:**")
namanol = dfsummary.iloc[len(df_summary_clean):len(dfsummary)]['NamaNegara']
negaranol = dfsummary.iloc[len(df_summary_clean):len(dfsummary)]['KodeNegara']
regionnol = dfsummary.iloc[len(df_summary_clean):len(dfsummary)]['Region']
subregionnol = dfsummary.iloc[len(df_summary_clean):len(dfsummary)]['Sub-region']
produksinol = dfsummary.iloc[len(df_summary_clean):len(dfsummary)]['produksi_kumulatif']
dfnol = pd.DataFrame(list(zip(namanol, negaranol, regionnol, subregionnol, produksinol)), columns=['Nama_Negara', 'Kode_Negara', 'Region', 'Sub-Region', 'Produksi_Kumulatif'])
col5a.dataframe(dfnol)

col5b.subheader("Summary Tahun Tertentu")
T2 = col5b.number_input("Tahun Berapa", min_value=1970, max_value=2015, value=1990, key=int)
dftahun2 = df_csv_clean.loc[df_csv_clean['tahun'] == T2].sort_values(by=['produksi'], ascending=False)
df_tahun_clean = dftahun2.set_index("produksi")
df_tahun_clean.head()
df_tahun_clean = df_tahun_clean.drop([0])
df_tahun_clean.reset_index(drop=False, inplace=True)
print("Negara dengan Produksi Minyak Terbesar pada Tahun " + str(T2) + ":")
col5b.markdown("**Negara dengan Produksi Minyak Terbesar pada Tahun** " + str(T2) + "**:**")
print(dftahun2.iloc[0]['kode_negara'])
col5b.markdown(dftahun2.iloc[0]['kode_negara'])
print(dftahun2.iloc[0]['produksi'])
col5b.markdown(dftahun2.iloc[0]['produksi'])
print("\nNegara dengan Produksi Minyak Terkecil pada Tahun " + str(T2) + ":")
col5b.markdown("\n**Negara dengan Produksi Minyak Terkecil pada Tahun** " + str(T2) + "**:**")
print(dftahun2.iloc[len(df_tahun_clean)-1]['kode_negara'])
col5b.markdown(dftahun2.iloc[len(df_tahun_clean)-1]['kode_negara'])
print(dftahun2.iloc[len(df_tahun_clean)-1]['produksi'])
col5b.markdown(dftahun2.iloc[len(df_tahun_clean)-1]['produksi'])
print("\nNegara dengan Produksi Minyak Sama Dengan Nol pada Tahun " + str(T2) + ":")
col5b.markdown("\n**Negara dengan Produksi Minyak Sama Dengan Nol pada Tahun** " + str(T2) + "**:**")
negaranol2 = dftahun2.iloc[len(df_tahun_clean):len(dftahun2)]['kode_negara']
produksinol2 = dftahun2.iloc[len(df_tahun_clean):len(dftahun2)]['produksi']
dfnol2 = pd.DataFrame(list(zip(negaranol2, produksinol2)), columns=['kode_negara', 'produksi'])
col5b.dataframe(dfnol2)
############### fifth column ###############
