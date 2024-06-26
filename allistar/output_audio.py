import pandas as pd
import os
import re
from gtts import gTTS

# Define la ruta donde guardar los archivos de audio
ruta_audios = "audios"

# Si la carpeta no existe, créala
if not os.path.exists(ruta_audios):
    os.makedirs(ruta_audios)

# Función para limpiar el nombre
def clean_name(name):
    # Reemplazar comas por puntos decimales
    name = name.replace(",", ".")
    # Reemplazar guiones por espacios
    name = name.replace("-", " ")
    # Reemplazar '/' por 'por'
    name = name.replace("/", " por ")
    # Reemplazar 'ml' por 'mililitros'
    name = name.replace("ml", "mililitros")
    # Reemplazar 'mg' por 'miligramos'
    name = name.replace("mg", "miligramos")
    
    for i, nom in enumerate(name):
        if nom == 'x' or nom == 'X':
            if name[i+1].isdigit() and name[i-1].isdigit():
                name = name.replace("x", " por ")
    return name


# Leer el conjunto de datos
df = pd.read_csv("products.csv", sep=";")

# Limpiar los nombres en el dataframe
df["cleaned_name"] = df["name"].apply(clean_name)

# Generar y guardar archivos de audio para cada nombre limpio
for name in df["cleaned_name"]:
    # Elimina caracteres no válidos del nombre del archivo
    cleaned_name = re.sub(r'[^\w\s]', '', name)
    # Reemplaza los espacios en el nombre con guiones bajos (_) o elimínalos
    audio_file = os.path.join(ruta_audios, f"{cleaned_name.replace(' ', '_')}.mp3")
    tts = gTTS(text=name, lang='es')  # Genera el audio con la palabra original
    tts.save(audio_file)  # Guarda el archivo de audio

# Crear una lista con los nombres de los archivos de audio
audio_files = []
for name in df["cleaned_name"]:
    cleaned_name = re.sub(r'[^\w\s]', '', name)
    audio_file = os.path.join(ruta_audios, f"{cleaned_name.replace(' ', '_')}.mp3")
    audio_files.append(audio_file)

# Agregar la lista de nombres de archivos de audio como una nueva columna en el conjunto de datos
df["audio_file"] = audio_files

# Guardar el conjunto de datos actualizado
df.to_csv("products_with_audio.csv", index=False)

print("Columna de archivos de audio agregada al conjunto de datos.")
