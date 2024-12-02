import pandas as pd

def cargar_datos(file_path):
    return pd.read_csv(file_path, encoding='ISO-8859-1', sep=';')

