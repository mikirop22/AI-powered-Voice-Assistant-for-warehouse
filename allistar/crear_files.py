"""import pandas as pd
import pyttsx3
import os
import re

import pyttsx3

# Inicializa el motor TTS
engine = pyttsx3.init()

# Configura la voz en español
voices = engine.getProperty('voices')
for voice in voices:
    if 'spanish' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

# Lee el DataFrame
df = pd.read_csv('products_with_audios_oficial.csv')

def generate_audio(cleaned_name):
    output_file = f"{cleaned_name.replace(' ', '_')}.mp3"
    audio_file = os.path.join(ruta_audios, output_file)
    
    engine.save_to_file(cleaned_name, audio_file)
    engine.runAndWait()
    print(f"Se generó el archivo de audio: {output_file}")
    
    return audio_file

# Configura diferentes tonos y genera el audio
for i in range(100):
    ruta_audios = f'audio_path{i}'

    # Si la carpeta no existe, créala
    if not os.path.exists(ruta_audios):
        os.makedirs(ruta_audios)

    engine.setProperty('pitch', i*10)  # Ton normal
    # engine.setProperty('pitch', 150)  # Tono más alto
    # engine.setProperty('pitch', 50)   # Tono más bajo
    engine.setProperty('rate', 170)  # Valor de ejemplo
    
    df[ruta_audios] = df['cleaned_name'].apply(generate_audio)
    

# Guarda el DataFrame actualizado
df.to_csv('products_with_audio_updated.csv', index=False)

print("Se agregó la columna 'audio_file' al DataFrame y se guardó el archivo CSV actualizado.")
"""

import os
from gtts import gTTS
from gtts_token.gtts_token import Token
from pydub import AudioSegment

# Texto de ejemplo
texto = "Hola, ¿cómo estás?"

# Lista de tonos diferentes
tonos = [0.5, 1.0, 1.5]  # Tonos más bajos, normales y más altos

# Directorio para almacenar los archivos de audio
directorio_salida = "tonos"

# Si el directorio no existe, créalo
if not os.path.exists(directorio_salida):
    os.makedirs(directorio_salida)

# Generar archivos de audio con diferentes tonos
for tono in tonos:
    # Crear objeto Token con el texto
    token = Token(texto)

    # Generar el token necesario para gTTS
    token_str = token.calculate_token(texto)

    # Crear objeto gTTS con el texto y el token generado
    tts = gTTS(text=texto, lang='es', tld='com', token=token_str, slow=False)

    # Guardar el archivo de audio con el tono deseado
    nombre_archivo = f"tono_{tono}.mp3"
    ruta_archivo = os.path.join(directorio_salida, nombre_archivo)
    
    # Guardar el archivo de audio
    tts.save(ruta_archivo)

    # Cargar el audio como un AudioSegment
    audio_segment = AudioSegment.from_mp3(ruta_archivo)

    # Aplicar cambio de tono
    audio_modificado = audio_segment._spawn(audio_segment.raw_data, overrides={
        "frame_rate": int(audio_segment.frame_rate * tono)
    })

    # Guardar el archivo de audio modificado
    audio_modificado.export(ruta_archivo, format="mp3")

    print(f"Se generó el archivo de audio con tono {tono}: {ruta_archivo}")

