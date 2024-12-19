import pandas as pd

def load_data(file):
    """
    Charge les données à partir d'un fichier CSV.
    :param file: Fichier téléchargé (CSV).
    :return: DataFrame contenant les données.
    """
    try:
        data = pd.read_csv(file)
        return data
    except Exception as e:
        raise ValueError(f"Erreur lors du chargement du fichier : {e}")

def filter_data_by_date(data, start_date, end_date):
    """
    Filtre les données en fonction d'une plage de dates.
    :param data: DataFrame contenant les données.
    :param start_date: Date de début (datetime).
    :param end_date: Date de fin (datetime).
    :return: DataFrame filtré.
    """
    return data[(data['date'] >= start_date) & (data['date'] <= end_date)]

def generate_summary_statistics(data):
    """
    Génère un résumé statistique des données numériques.
    :param data: DataFrame contenant les données.
    :return: DataFrame des statistiques descriptives.
    """
    return data.describe()
