# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# --- Streamlit Page Config ---
st.set_page_config(page_title="CORD-19 Data Explorer", layout="wide")

# --- Title & Description ---
st.title("CORD-19 Data Explorer")
st.write("""
Interactive exploration of COVID-19 research papers.
Use the widgets below to filter data and visualize trends.
""")

# --- Load Data ---
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
    df['abstract_word_count'] = df['abstract'].fillna('').apply(lambda x: len(x.split()))
    df['journal'].fillna('Unknown', inplace=True)
    df.dropna(subset=['title', 'year'], inplace=True)
    return df

df = load_data('metadata.csv')

# --- Sidebar Filters ---
st.sidebar.header("Filters")
year_range = st.sidebar.slider(
    "Select year range", int(df['year'].min()), int(df['year'].max()),
    (int(df['year'].min()), int(df['year'].max()))
)

top_n = st.sidebar.slider("Number of top journals to display", 5, 20, 10)

# Apply year filter
df_filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# --- Main Layout ---
st.subheader("Data Overview")
st.write(f"Showing {len(df_filtered)} papers from {year_range[0]} to {year_range[1]}")
st.dataframe(df_filtered[['title', 'authors', 'journal', 'year']].head(10))

# --- Publications by Year ---
st.subheader("Publications by Year")
year_counts = df_filtered['year'].value_counts().sort_index()
fig1, ax1 = plt.subplots()
ax1.bar(year_counts.index, year_counts.values, color='skyblue')
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of Papers")
ax1.set_title("Publications Over Time")
st.pyplot(fig1)

# --- Top Journals ---
st.subheader(f"Top {top_n} Journals")
top_journals = df_filtered['journal'].value_counts().head(top_n)
fig2, ax2 = plt.subplots()
ax2.barh(top_journals.index[::-1], top_journals.values[::-1], color='orange')
ax2.set_xlabel("Number of Papers")
ax2.set_ylabel("Journal")
ax2.set_title(f"Top {top_n} Journals Publishing COVID-19 Research")
st.pyplot(fig2)

# --- Word Cloud of Titles ---
st.subheader("Word Cloud of Paper Titles")
text = ' '.join(df_filtered['title'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
fig3, ax3 = plt.subplots(figsize=(10,5))
ax3.imshow(wordcloud, interpolation='bilinear')
ax3.axis('off')
st.pyplot(fig3)

# --- Summary Stats ---
st.subheader("Summary Statistics")
st.write(f"Average abstract length: {df_filtered['abstract_word_count'].mean():.1f} words")
st.write(f"Total papers: {len(df_filtered)}")
st.write(f"Total journals: {df_filtered['journal'].nunique()}")

# --- Footer ---
st.write("Data Source: [CORD-19 Dataset](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge)")
