CORD-19 Data Explorer

This project is a simple Streamlit application to explore the CORD-19 COVID-19 research dataset. It allows users to filter, visualize, and analyze research papers interactively.

Features

Filter papers by publication year

Display top journals publishing COVID-19 research

Word cloud of paper titles

View a sample of the dataset

Summary statistics like average abstract length and total papers

Installation

Clone the repository:

git clone <your-repo-url>
cd Frameworks_Assignment


Install dependencies:

pip install pandas matplotlib wordcloud streamlit


Place the metadata.csv file in the project directory.

Usage

Run the Streamlit app:

streamlit run app.py


The app will open in your default web browser. Use the sidebar filters to explore data interactively.

Data Source

CORD-19 Dataset

Notes

Tested with Python 3.7+

Designed for beginner-friendly exploration and analysis
