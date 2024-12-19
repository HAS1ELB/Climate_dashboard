import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_data, filter_data_by_date, generate_summary_statistics

# Charger le fichier CSS pour appliquer les styles personnalisés
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Charger les styles définis dans style.css
load_css("assets/style.css")

# Titre de l'application
st.title("🌦️ Dashboard d'analyse des données climatiques")

# Description
st.markdown("""
Bienvenue dans l'application **Dashboard d'analyse des données climatiques**. 
Téléchargez vos données climatiques au format CSV, explorez-les à l'aide de graphiques et obtenez un résumé statistique !
""")

# Chargement du fichier CSV
uploaded_file = st.file_uploader("Téléchargez un fichier CSV", type=["csv"])
if uploaded_file:
    # Charger les données
    data = load_data(uploaded_file)
    st.write("Aperçu des données :", data.head())

    # Vérifier si la colonne 'date' est présente
    if 'date' in data.columns:
        data['date'] = pd.to_datetime(data['date'])

        # Filtrage par plage de dates
        st.subheader("📅 Filtrage par date")
        date_range = st.date_input(
            "Sélectionnez une plage de dates",
            [data['date'].min(), data['date'].max()]
        )
        if len(date_range) == 2:
            start_date, end_date = date_range

            # Convertir les dates en datetime
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)

            filtered_data = filter_data_by_date(data, start_date, end_date)
            st.write(f"Données filtrées ({len(filtered_data)} lignes) :", filtered_data)
        else:
            filtered_data = data
    else:
        st.warning("La colonne 'date' est absente. Les filtres par date seront ignorés.")
        filtered_data = data

    # Graphiques interactifs
    st.subheader("📊 Visualisation des données")
    column_to_plot = st.selectbox("Choisissez une colonne à visualiser", data.columns[1:])
    if column_to_plot:
        plt.figure(figsize=(15, 5))
        sns.lineplot(data=filtered_data, x='date', y=column_to_plot)
        plt.title(f"Évolution de {column_to_plot}")
        plt.xlabel("Date")
        plt.ylabel(column_to_plot)
        st.pyplot(plt)

    # Résumé statistique
    st.subheader("📈 Résumé statistique")
    stats = generate_summary_statistics(filtered_data)
    st.write(stats)

    # Télécharger les données filtrées
    st.subheader("💾 Télécharger les données filtrées")
    csv = filtered_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Télécharger le fichier CSV",
        data=csv,
        file_name="filtered_data.csv",
        mime="text/csv"
    )
else:
    st.info("Veuillez télécharger un fichier CSV pour commencer.")
