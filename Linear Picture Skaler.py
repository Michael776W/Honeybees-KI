import os
from PIL import Image

# Pfad zum Ordner, in dem die Bilder liegen
input_folder = r"D:\Bienenerkennung Ki\Synthetischen Datensatz\SYN_Datensatz"
output_folder = r"D:\Bienenerkennung Ki\Synthetischen Datensatz\SYN_Datensatz_Klein"

# Downscaling-Faktor
scale_factor = 2.40

# Falls der Ausgabeordner noch nicht existiert, wird er erstellt
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Gehe durch alle Dateien im Eingabeordner
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".png"):
        # Bild öffnen
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)

        # Neue Größe berechnen
        new_size = (int(img.width / scale_factor), int(img.height / scale_factor))

        # Bild skalieren (mit LANCZOS-Filter)
        img_resized = img.resize(new_size, Image.Resampling.LANCZOS)

        # Neues Bild speichern
        output_path = os.path.join(output_folder, filename)
        img_resized.save(output_path)

        print(f"Bild {filename} wurde skaliert")
