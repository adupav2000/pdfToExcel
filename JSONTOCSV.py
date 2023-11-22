import json
import os
import pandas as pd

# Chemin du dossier contenant les fichiers JSON
dossier_json = './AllResponsesInJson1'

# Fonction pour aplatir les données JSON
def aplatir_json(data, parent_key='', sep='_'):
    items = []
    if isinstance(data, list):
        for i, element in enumerate(data):
            new_key = f"{parent_key}{sep}{i}" if parent_key else str(i)
            items.extend(aplatir_json(element, new_key, sep=sep).items())
    elif isinstance(data, dict):
        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            items.extend(aplatir_json(v, new_key, sep=sep).items())
    else:
        items.append((parent_key, data))
    return dict(items)

all_data = []

for fichier in os.listdir(dossier_json):
    if fichier.endswith('.json'):
        with open(os.path.join(dossier_json, fichier), 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Check if the data is a string and try to load it as JSON
            if isinstance(data, str):
                try:
                    data = json.loads(data)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file: {fichier}")
                    continue

            flat_data = aplatir_json(data)
            all_data.append(flat_data)

df = pd.DataFrame(all_data)

# Uncomment the line below to save the DataFrame to an Excel file
df.to_excel('informations1.xlsx', index=False)

# Print the first few rows of the DataFrame for verification
print("DataFrame preview:\n", df.head())
