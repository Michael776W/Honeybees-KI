import os

# Funktion zur Überprüfung und Korrektur von Bounding Boxen
def check_and_fix_bboxes(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_name in os.listdir(input_dir):
        if file_name.endswith('.txt'):
            input_file_path = os.path.join(input_dir, file_name)
            output_file_path = os.path.join(output_dir, file_name)

            with open(input_file_path, 'r') as infile:
                lines = infile.readlines()

            with open(output_file_path, 'w') as outfile:
                for line in lines:
                    data = line.strip().split()
                    class_id = int(float(data[0]))
                    x_center, y_center, width, height = map(float, data[1:])

                    # Berechne min/max Werte der Bounding Box
                    x_min = max(0.0, x_center - width / 2)
                    y_min = max(0.0, y_center - height / 2)
                    x_max = min(1.0, x_center + width / 2)
                    y_max = min(1.0, y_center + height / 2)

                    # Berechne die korrigierte Bounding Box
                    new_x_center = (x_min + x_max) / 2
                    new_y_center = (y_min + y_max) / 2
                    new_width = x_max - x_min
                    new_height = y_max - y_min

                    # Schreibe die korrigierte Bounding Box in die neue Datei
                    outfile.write(f"{class_id} {new_x_center} {new_y_center} {new_width} {new_height}\n")

            print(f'Korrigiert: {file_name}')

# Beispiel-Aufruf
input_directory = r'D:\Bienen_KI2\PYthon\data\labels'  # Ordner mit den fehlerhaften .txt Dateien
output_directory = r'D:\Bienen_KI2\PYthon\data\Korektur'  # Zielordner für korrigierte .txt Dateien

check_and_fix_bboxes(input_directory, output_directory)

