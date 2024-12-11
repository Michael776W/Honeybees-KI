import os
from PIL import Image


def convert_png_to_jpg(folder_path, output_folder=None):
    """
    Konvertiert alle PNG-Bilder in einem Ordner in JPG-Bilder.

    :param folder_path: Pfad zum Ordner mit PNG-Bildern.
    :param output_folder: Optional, Pfad zum Zielordner für JPG-Bilder.
                          Wenn nicht angegeben, wird der ursprüngliche Ordner verwendet.
    """
    # Erstelle den Ausgabeordner, falls nicht vorhanden
    if output_folder is None:
        output_folder = folder_path
    os.makedirs(output_folder, exist_ok=True)

    # Gehe durch alle Dateien im Ordner
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".png"):  # Überprüfen, ob es eine PNG-Datei ist
            png_path = os.path.join(folder_path, filename)
            jpg_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".jpg")

            # Öffne die PNG-Datei und konvertiere sie in JPG
            try:
                with Image.open(png_path) as img:
                    rgb_img = img.convert("RGB")  # Konvertiere zu RGB (JPG unterstützt kein Alpha)
                    rgb_img.save(jpg_path, "JPEG")
                print(f"Konvertiert: {png_path} -> {jpg_path}")
            except Exception as e:
                print(f"Fehler bei der Konvertierung von {png_path}: {e}")


# Beispielnutzung
if __name__ == "__main__":
    folder_path = r"D:\Bienenerkennung Ki\Synthetischen Datensatz\SYN_Datensatz_Klein"
    output_folder = r"D:\Bienenerkennung Ki\Synthetischen Datensatz\JPG_DATENSATZ"
    output_folder = output_folder.strip() or None
    convert_png_to_jpg(folder_path, output_folder)
