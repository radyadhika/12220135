'''
Nama: Radya Evandhika Novaldi
NIM: 12220135
Topik: UAS Pemrograman Komputer
'''

#Library
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import json
import streamlit as st

#Read CSV
filepath = "produksi_minyak_mentah.csv"
df = pd.read_csv(filepath)

#Membersihkan CSV
df_csv_clean = df.set_index("kode_negara")
df_csv_clean.head()

df_csv_clean = df_csv_clean.drop(["WLD","G20","OECD","OEU","EU28"])
df_csv_clean.reset_index(drop=False, inplace=True)

#Membuat List Organisasi/Non-Negara dan Menghilangkannya dari List Kode Negara
listkodecsv = []
listkodecsvbanyak = []
listorganisasi = []

for i in list(df['kode_negara']):
    if i not in listkodecsv:
        listkodecsv.append(i)

namajson = "kode_negara_lengkap.json"
openjson = open(namajson)
loadjson = json.load(openjson)
df_json = pd.read_json(namajson)

for i in list(df_csv_clean['kode_negara']) :
    if i in list(df_json['alpha-3']) :
        listkodecsvbanyak.append(i)

list_kode_bersih = []

for i in listkodecsv:
    if i not in list(df_json['alpha-3']):
        listorganisasi.append(i)

for i in listorganisasi:
    df = df[df.kode_negara != i]
    if i in listkodecsv:
        listkodecsv.remove(i)

#Mengekstrak Data yang Unik dari file json dan Menyimpannya pada List Kosong
listnamajson = []
listkodenegarajson = []
listregionjson = []
listsubregionjson = []

for i in range(len(listkodecsv)):
    for j in range(len(list(df_json['alpha-3']))):
        if list(df_json['alpha-3'])[j] == listkodecsv[i] and list(df_json['name'])[j] not in listnamajson:
            listnamajson.append(list(df_json['name'])[j])
            listkodenegarajson.append(list(df_json['country-code'])[j])
            listregionjson.append(list(df_json['region'])[j])
            listsubregionjson.append(list(df_json['sub-region'])[j])

#Membuat DataFrame dari Data yang Sudah Diekstrak ke List tadi
df_json_clean = pd.DataFrame(list(zip(listnamajson, listkodecsv, listkodenegarajson, listregionjson, listsubregionjson)), columns=['NamaNegara', 'ISO3', 'KodeNegara', 'Region', 'SubRegion'])

#Menampung nama negara, region negara, dan sub region negara milik keseluruhan data
namanegara = []
regionnegara = []
subregionnegara = []

for i in listkodecsvbanyak:
    for j in range(len(df_json)) :
        if i == df_json['alpha-3'][j] :
            namanegara.append(df_json['name'][j])
            regionnegara.append(df_json['region'][j])
            subregionnegara.append(df_json['sub-region'][j])

#Menambahkan column pada dataframe dari excel dengan informasi nama negara, region negara, dan sub region negara
df_csv_clean['Nama_Negara'] = namanegara
df_csv_clean['Region'] = regionnegara
df_csv_clean['Sub-Region'] = subregionnegara

############### title ###############
st.set_page_config(layout="wide")  # this needs to be the first Streamlit command called
st.title("Informasi Seputar Data Produksi Minyak Mentah dari Berbagai Negara di Seluruh Dunia")
st.markdown("*Aplikasi ini dibuat oleh Radya Evandhika Novaldi/12220135/Teknik Perminyakan/Institut Teknologi Bandung*")
############### title ###############)

############### sidebar ###############
st.sidebar.title("Pengaturan")
st.sidebar.subheader("Konfigurasi Grafik")
width = st.sidebar.slider("Lebar Grafik", 1, 25, 16)
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
st.subheader("Informasi Produksi Minyak pada Suatu Negara")
N = st.selectbox("Pilih Negara", listnamajson)

# Mensinkronisasi data excel dan data json
for i in range(len(listnamajson)):
    if listnamajson[i] == N:
        kodenegarahuruf = listkodecsv[i]
        kodenegaraangka = listkodenegarajson[i]
        region = listregionjson[i]
        subregion = listsubregionjson[i]

#Menampung data-data produksi minyak dan tahun milik suatu negara pada list
tahun1 = []
produksi1 = []

for i in range(len(list(df_csv_clean['kode_negara']))):
    if kodenegarahuruf == list(df_csv_clean['kode_negara'])[i]:
        tahun1.append(list(df_csv_clean['tahun'])[i])
        produksi1.append(list(df_csv_clean['produksi'])[i])

#Membuat grafik produksi minyak terhadap tahun milik suatu negara
fig, ax = plt.subplots(figsize=(width, height))
plt.plot(tahun1, produksi1)
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
st.subheader("Informasi Jumlah Produksi Minyak Terbesar pada Tahun Tertentu")

T = col3opt1.number_input("Pilih Tahun", min_value=1971, max_value=2015, value=1990)
B1 = col3opt2.number_input("Pilih Banyaknya Negara", min_value=1, max_value=None, value=10)

#Membuat DataFrame baru berdasarkan Tahun yang dipilih
dftahun = df_csv_clean.loc[df_csv_clean['tahun'] == T].sort_values(by=['produksi'], ascending=False)

#Membuat DataFrame baru berdasarkan Banyaknya Negara yang dipilih
dftahunbanyak = dftahun[:B1]

#Menampung data-data kode negara dan produksi minyak milik (B1)-Negara pada tahun tertentu
negara2 = dftahunbanyak['kode_negara']
produksi2 = dftahunbanyak['produksi']

#Membuat grafik produksi minyak milik (B1)-Negara pada tahun tertentu
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
st.subheader("Informasi Produksi Minyak Terbesar Secara Kumulatif Keseluruhan Tahun")

B2 = st.number_input("Banyak Negara", min_value=1, max_value=None, value=10, key=int)

#Menampung Nilai Produksi Minyak secara Kumulatif pada list kosong
jumlah_produksi_kumulatif = []

for i in listkodecsv:
    a = df_csv_clean.loc[df_csv_clean['kode_negara'] == i, 'produksi'].sum()
    jumlah_produksi_kumulatif.append(a)

#Membuat DataFrame baru yang sudah disesuaikan produksinya menjadi produksi minyak kumulatif
df3 = pd.DataFrame(list(zip(listkodecsv, jumlah_produksi_kumulatif)), columns=['kode_negara', 'produksi_kumulatif']).sort_values(by=['produksi_kumulatif'], ascending=False)
df3 = df3 [:B2]

#Menampung data-data kode negara dan produksi minyak secara kumulatif milik (B2)-Negara
negara3 = df3['kode_negara']
produksikumul3 = df3['produksi_kumulatif']

#Membuat grafik produksi minyak milik (B2)-Negara pada tahun tertentu
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

col5a.markdown("**Negara dengan Produksi Kumulatif Terbesar:**")
col5a.markdown("Nama Negara: " + df_summary_clean.iloc[0]['NamaNegara'])
col5a.markdown("Kode Negara: " + df_summary_clean.iloc[0]['KodeNegara'])
col5a.markdown("Region: " + df_summary_clean.iloc[0]['Region'])
col5a.markdown("Sub-region: " + df_summary_clean.iloc[0]['Sub-region'])
col5a.markdown("Produksi Kumulatif: " + str(df_summary_clean.iloc[0]['produksi_kumulatif']) + " TMT")

col5a.text("")
col5a.markdown("\n**Negara dengan Produksi Kumulatif Terkecil:**")
col5a.markdown("Nama Negara: " + df_summary_clean.iloc[len(df_summary_clean)-1]['NamaNegara'])
col5a.markdown("Kode Negara: " + df_summary_clean.iloc[len(df_summary_clean)-1]['KodeNegara'])
col5a.markdown("Region: " + df_summary_clean.iloc[len(df_summary_clean)-1]['Region'])
col5a.markdown("Sub-region: " + df_summary_clean.iloc[len(df_summary_clean)-1]['Sub-region'])
col5a.markdown("Produksi Kumulatif: " + str(df_summary_clean.iloc[len(df_summary_clean)-1]['produksi_kumulatif']) + " TMT")

col5a.text("")
col5a.markdown("\n**Negara dengan Produksi Kumulatif Sama Dengan Nol:**")
namanol = dfsummary.iloc[len(df_summary_clean):len(dfsummary)]['NamaNegara']
negaranol = dfsummary.iloc[len(df_summary_clean):len(dfsummary)]['KodeNegara']
regionnol = dfsummary.iloc[len(df_summary_clean):len(dfsummary)]['Region']
subregionnol = dfsummary.iloc[len(df_summary_clean):len(dfsummary)]['Sub-region']
produksinol = dfsummary.iloc[len(df_summary_clean):len(dfsummary)]['produksi_kumulatif']
dfnol = pd.DataFrame(list(zip(namanol, negaranol, regionnol, subregionnol, produksinol)), columns=['Nama_Negara', 'Kode_Negara', 'Region', 'Sub-Region', 'Produksi_Kumulatif'])
col5a.dataframe(dfnol)

col5b.subheader("Summary Tahun Tertentu")
T2 = col5b.number_input("Tahun Berapa", min_value=1971, max_value=2015, value=1990, key=int)
dftahun2 = df_csv_clean.loc[df_csv_clean['tahun'] == T2]

dftahun2 = dftahun2.sort_values(by=['produksi'], ascending=False)


df_tahun_clean = dftahun2.set_index("produksi")
df_tahun_clean.head()
df_tahun_clean = df_tahun_clean.drop([0])
df_tahun_clean.reset_index(drop=False, inplace=True)

col5b.markdown("**Negara dengan Produksi Minyak Terbesar pada Tahun** " + str(T2) + "**:**")
col5b.markdown("Nama Negara: " + df_tahun_clean.iloc[0]['Nama_Negara'])
col5b.markdown("Kode Negara: " + df_tahun_clean.iloc[0]['kode_negara'])
col5b.markdown("Region: " + df_tahun_clean.iloc[0]['Region'])
col5b.markdown("Sub-Region: " + df_tahun_clean.iloc[0]['Sub-Region'])
col5b.markdown("Produksi: " + str(df_tahun_clean.iloc[0]['produksi']) + " TMT")

col5b.text("")
col5b.markdown("\n**Negara dengan Produksi Minyak Terkecil pada Tahun** " + str(T2) + "**:**")
col5b.markdown("Nama Negara: " + df_tahun_clean.iloc[len(df_tahun_clean)-1]['Nama_Negara'])
col5b.markdown("Kode Negara: " + df_tahun_clean.iloc[len(df_tahun_clean)-1]['kode_negara'])
col5b.markdown("Region: " + df_tahun_clean.iloc[len(df_tahun_clean)-1]['Region'])
col5b.markdown("Sub-Region: " + df_tahun_clean.iloc[len(df_tahun_clean)-1]['Sub-Region'])
col5b.markdown("Produksi: " + str(df_tahun_clean.iloc[len(df_tahun_clean)-1]['produksi']) + " TMT")

col5b.text("")
col5b.markdown("\n**Negara dengan Produksi Minyak Sama Dengan Nol pada Tahun** " + str(T2) + "**:**")
namanol2 = dftahun2.iloc[len(df_tahun_clean):len(dftahun2)]['Nama_Negara']
negaranol2 = dftahun2.iloc[len(df_tahun_clean):len(dftahun2)]['kode_negara']
regionnol2 = dftahun2.iloc[len(df_tahun_clean):len(dftahun2)]['Region']
subregionnol2 = dftahun2.iloc[len(df_tahun_clean):len(dftahun2)]['Sub-Region']
produksinol2 = dftahun2.iloc[len(df_tahun_clean):len(dftahun2)]['produksi']
dfnol2 = pd.DataFrame(list(zip(namanol2, negaranol2, regionnol2, subregionnol2, produksinol2)), columns=['Nama_Negara', 'Kode_Negara', 'Region', 'Sub-Region', 'Produksi'])
col5b.dataframe(dfnol2)
############### fifth column ###############

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
