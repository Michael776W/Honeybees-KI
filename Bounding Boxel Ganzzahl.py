import os

# Funktion zum Konvertieren der Klassen-IDs in den .txt Dateien
def convert_labels(input_dir, output_dir):
    # Sicherstellen, dass der Ausgabeordner existiert
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Alle Dateien im Input-Verzeichnis durchlaufen
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.txt'):
            input_file_path = os.path.join(input_dir, file_name)
            output_file_path = os.path.join(output_dir, file_name)

            # Die .txt Datei öffnen und Zeilen lesen
            with open(input_file_path, 'r') as infile:
                lines = infile.readlines()

            # Geänderte Zeilen speichern
            with open(output_file_path, 'w') as outfile:
                for line in lines:
                    data = line.strip().split()

                    # Klassen-ID in Ganzzahl umwandeln (z.B. von 0.0 zu 0, von 2.0 zu 2 usw.)
                    class_id = int(float(data[0]))  # Konvertiere Klasse in Ganzzahl

                    # Schreibe die konvertierten Daten in die neue Datei
                    new_line = f"{class_id} " + " ".join(data[1:]) + "\n"
                    outfile.write(new_line)

            print(f'Konvertiert: {file_name}')

# Beispiel-Aufruf
input_directory = r'D:\Bienen_KI2\PYthon\data\labels'  # Ordner mit fehlerhaften .txt Dateien
output_directory = r'D:\Bienen_KI2\PYthon\data\Korektur'  # Zielordner für korrigierte .txt Dateien

convert_labels(input_directory, output_directory)
