import pytesseract
from pytesseract import Output
import pandas as pd
from PIL import Image

# Chemin vers le fichier Tesseract (à adapter selon votre installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\ekalboussi\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Charger l'image
image_path = r'C:\Users\ekalboussi\OneDrive - ALTEN Group\Bureau\Project_NLP\OCR-and-Classifier-Doc\extraction\Table\test\img_6.png'
image = Image.open(image_path)

# Extraire le texte avec les informations de position
data = pytesseract.image_to_data(image, output_type=Output.DICT)

# Initialiser les listes pour stocker les données du tableau
rows = []
current_row = []

# Parcourir les données pour regrouper les textes ligne par ligne
for i in range(len(data['text'])):
    # On récupère les coordonnées de chaque mot
    word = data['text'][i].strip()
    top = data['top'][i]
    
    # Si le mot n'est pas vide, on l'ajoute à la ligne en cours
    if word:
        current_row.append(word)
    
    # Vérifier si on change de ligne (différence de position verticale)
    if i < len(data['text']) - 1 and abs(top - data['top'][i+1]) > 10:
        # Ajouter la ligne actuelle aux lignes
        rows.append(current_row)
        current_row = []

# Ajouter la dernière ligne si elle n'est pas vide
if current_row:
    rows.append(current_row)

# Créer un DataFrame à partir des lignes
df = pd.DataFrame(rows)

# Exporter le DataFrame en fichier Excel
output_excel_path = r'C:\Users\ekalboussi\OneDrive - ALTEN Group\Bureau\Project_NLP\OCR-and-Classifier-Doc\extraction\Table\Resultas\output_table6.xlsx'
df.to_excel(output_excel_path, index=False, header=False)

print(f'Tableau extrait et enregistré dans : {output_excel_path}')
