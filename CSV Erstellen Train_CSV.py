import os
import csv


def create_csv_from_folder(image_folder, output_csv):
    # Liste alle Dateien im Ordner auf
    files = os.listdir(image_folder)

    # Filtere nur Bild- und Label-Dateien
    images = [f for f in files if f.endswith(('.jpg', '.png'))]  # Du kannst hier weitere Bildformate hinzufügen

    # Schreibe die Daten in die CSV-Datei
    with open(output_csv, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        # Für jede Bilddatei im Ordner
        for image_file in images:
            # Erzeuge den entsprechenden Label-Dateinamen
            label_file = image_file.rsplit('.', 1)[0] + ".txt"  # Ändert die Dateiendung zu .txt

            # Überprüfen, ob die Label-Datei existiert
            if os.path.exists(os.path.join(image_folder, label_file)):
                data = [image_file, label_file]  # Schreibe Bild und zugehöriges Label in die CSV
                writer.writerow(data)
            else:
                print(f"Warnung: Keine Label-Datei für {image_file} gefunden.")


# Erstelle eine CSV-Datei für Bilder und Labels im angegebenen Ordner
image_folder = r'D:\Bienen_KI2\PYthon\Eigene Daten\Neuer Ordner'
create_csv_from_folder(image_folder, "train.csv")

