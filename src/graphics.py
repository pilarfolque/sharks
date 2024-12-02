import plotly.express as px

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64



sns.set(style="whitegrid")


def create_graph(shark_data):
 
    fig, axs = plt.subplots(2, 2, figsize=(15, 12))

    sns.countplot(data=shark_data, x='Mode', ax=axs[0, 0], palette="viridis",hue='Mode')
    axs[0, 0].set_title("Frecuencia de la actividad con accidentes con tiburones")
    axs[0, 0].set_xlabel("Actividad")
    axs[0, 0].set_ylabel("Frecuencia")
    axs[0, 0].tick_params(axis='x', rotation=45)

    sns.countplot(data=shark_data, x='Injury', ax=axs[0, 1], palette="magma",hue='Injury')
    axs[0, 1].set_title("Frecuencia de tipos de lesión")
    axs[0, 1].set_xlabel("Tipo de lesión")
    axs[0, 1].set_ylabel("Frecuencia")

    sns.countplot(data=shark_data, x='Species_simplified', ax=axs[1, 0], palette="cool",hue='Species_simplified')
    axs[1, 0].set_title("Frecuencia de especies de tiburón")
    axs[1, 0].set_xlabel("Especie simplificada")
    axs[1, 0].set_ylabel("Frecuencia")

    sns.countplot(data=shark_data, x='Moon Phase', ax=axs[1, 1], palette="Set2",hue='Moon Phase')
    axs[1, 1].set_title("Frecuencia de la fase lunar en el momento del accidente")
    axs[1, 1].set_xlabel("Fase Lunar")
    axs[1, 1].set_ylabel("Frecuencia")
    axs[1, 1].tick_params(axis='x', rotation=45)

    plt.tight_layout()

    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)

    img_base64 = base64.b64encode(img_stream.getvalue()).decode('utf-8')

    plt.close(fig)

    return img_base64


def create_graphs_2(shark_data_fatal):
   

    shark_data_fatal = shark_data_fatal.dropna(subset=['Activity', 'Injury', 'Age'])

    shark_data_fatal['Age'] = pd.to_numeric(shark_data_fatal['Age'], errors='coerce')
    shark_data_fatal = shark_data_fatal.dropna(subset=['Age'])  

    plt.figure(figsize=(12, 7))
    sns.histplot(shark_data_fatal['Age'], kde=True, bins=30, color='teal', stat='density')
    plt.title("Distribución de la edad de las víctimas", fontsize=16)
    plt.xlabel("Edad", fontsize=14)
    plt.ylabel("Densidad", fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    img_stream1 = io.BytesIO()
    plt.savefig(img_stream1, format='png')
    img_stream1.seek(0)
    img_base64_1 = base64.b64encode(img_stream1.getvalue()).decode('utf-8')
    plt.close()

    plt.figure(figsize=(12, 7))
    sns.set(style="whitegrid")
    ax = sns.violinplot(data=shark_data_fatal, x='Injury', y='Age', palette='Set2', inner="point", linewidth=2)
    ax.set_title("Distribución de la edad por el tipo de lesión", fontsize=16)
    ax.set_xlabel("Tipo de lesión", fontsize=14)
    ax.set_ylabel("Edad", fontsize=14)

    ax.set_xticklabels([])
    

    for i, category in enumerate(shark_data_fatal['Injury'].unique()):
        subset = shark_data_fatal[shark_data_fatal['Injury'] == category]
        for j in range(len(subset)):
            x_pos = i  
            y_pos = subset.iloc[j]['Age']  
            ax.text(x_pos + 0.05, y_pos, str(int(y_pos)), ha='center', va='center', fontsize=8, color='black')

    img_stream2 = io.BytesIO()
    plt.savefig(img_stream2, format='png')
    img_stream2.seek(0)
    img_base64_2 = base64.b64encode(img_stream2.getvalue()).decode('utf-8')
    plt.close()

    plt.figure(figsize=(12, 7))
    ax = sns.countplot(data=shark_data_fatal, x='Injury', palette='magma', hue='Injury')
    plt.title("Frecuencia de lesiones en accidentes con tiburones", fontsize=16)
    plt.xlabel("Tipo de lesión", fontsize=14)
    plt.ylabel("Frecuencia", fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    ax.set_xticks([])

    injury_categories = shark_data_fatal['Injury'].value_counts().index
    max_frequency = shark_data_fatal['Injury'].value_counts().max()

    threshold = max_frequency * 0.6

    for p in ax.patches:
        height = p.get_height()
        if height >= threshold: 
            injury_label = injury_categories[int(p.get_x() + p.get_width() / 2)]
            ax.text(p.get_x() + p.get_width() / 2, height + 0.1, 
                    f'{height:.0f} - {injury_label}', ha='center', va='bottom', fontsize=12, color='black')


    img_stream3 = io.BytesIO()
    plt.savefig(img_stream3, format='png')
    img_stream3.seek(0)
    img_base64_3 = base64.b64encode(img_stream3.getvalue()).decode('utf-8')
    plt.close()

    return img_base64_1, img_base64_2, img_base64_3
