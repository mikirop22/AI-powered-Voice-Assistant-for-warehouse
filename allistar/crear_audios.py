import pandas as pd
import pyttsx3
import os
import re

# Inicializa el motor TTS
engine = pyttsx3.init()

ruta_audios = "Audios2"

# Si la carpeta no existe, créala
if not os.path.exists(ruta_audios):
    os.makedirs(ruta_audios)

# Configura la voz en español
voices = engine.getProperty('voices')
for voice in voices:
    if 'spanish' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

# Lee el DataFrame
df = pd.read_csv('products_with_audio.csv')

# Define una función para generar el audio y retornar el nombre del archivo
def generate_audio(cleaned_name):
    output_file = f"{cleaned_name.replace(' ', '_')}.mp3"
    audio_file = os.path.join(ruta_audios, output_file)
    
    engine.save_to_file(cleaned_name, audio_file)
    engine.runAndWait()
    print(f"Se generó el archivo de audio: {output_file}")
    
    return audio_file

# Aplica la función a cada fila y guarda el nombre del archivo en una nueva columna
df['audio_file2'] = df['cleaned_name'].apply(generate_audio)

# Guarda el DataFrame actualizado
df.to_csv('products_with_audio_updated.csv', index=False)

print("Se agregó la columna 'audio_file' al DataFrame y se guardó el archivo CSV actualizado.")
