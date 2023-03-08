import pandas as pd
import warnings
warnings.simplefilter(action='ignore')
import os
import glob
import csv
import shutil

# spécifier le nom du nouveau dossier à créer
new_file = "Dataframes"

# spécifier le chemin du dossier où les fichiers .csv se trouvent
root = "C:/Users/paulc/Desktop/Stage/lmt-analysis-2022/LMT/scripts/"

# spécifier le chemin du dossier où le nouveau dossier sera créé
final_file = "C:/Users/paulc/Desktop/Stage/lmt-analysis-2022/LMT/scripts/"

# vérifier si le dossier existe déjà
if os.path.exists(os.path.join(final_file, new_file)):
    # si oui, le supprimer
    os.rmdir(os.path.join(final_file, new_file))

# créer le nouveau dossier dans le dossier de destination
new_path = os.path.join(final_file, new_file)
os.makedirs(new_path)

# parcourir tous les fichiers dans le dossier initial
for file in os.listdir(root):

    # vérifier si le fichier est un fichier .csv
    if file.endswith(".csv"):

        # spécifier le chemin complet du fichier
        path = os.path.join(root, file)

        # déplacer le fichier vers le nouveau dossier
        shutil.move(path, new_path)

#read the path
file_path = "C:/Users/paulc/Desktop/Stage/lmt-analysis-2022/LMT/scripts/Dataframes/"
os.chdir("C:/Users/paulc/Desktop/Stage/lmt-analysis-2022/LMT/scripts/Dataframes/")
#list all the files from the directory
file_list = os.listdir(file_path)

#list all csv files only
csv_files = glob.glob('*.{}'.format('csv'))
print(csv_files)

df_append = pd.DataFrame()  # append all files together

for file in csv_files:
    df_temp = pd.read_csv(file)
    df_append = df_append.append(df_temp, ignore_index=True)

print(df_append)

df_append.pop("Unnamed: 0") #Add this line if there is a column named "Unnamed: 0"
df_append.to_csv("C:/Users/paulc/Desktop/Stage/lmt-analysis-2022/LMT/scripts/Dataframes/Merge.csv")
