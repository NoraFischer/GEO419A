"""
/******************************************************************************
Dieses Modul ermöglicht den Download, das Entpacken und das Anzeigen einer Datei

        begin           : 2023-04-04
        git sha         : $Format:%H$
        copyright       : (C) 2023 by Nora Fischer and Sheila Tholen
        email           : nora.fischer@uni-jena.de / sheila.tholen@uni-jend.de
******************************************************************************/
"""

import os
import sys
import zipfile
import requests


class DownloadReadShow():
    """Implementation des Moduls"""

    def __init__(self):
        # Declare instance attributes
        self.current_dir = os.getcwd()
        self.zip_filename = "GEO419A_Testdatensatz.zip"
        self.url = "https://upload.uni-jena.de/data/641c17ff33dd02.60763151/GEO419A_Testdatensatz.zip"
        self.geotiff = "S1A_IW_20230214T031857_DVP_RTC10_G_gpunem_A42B_VH.tif"

    def user_dir(self):
        """Nutzerverzeichnis festlegen"""

        # current working directory should be set as the user directory ?
        while True:
            q_dir = str(input(f"Möchtest Du in diesem Ordner arbeiten: {self.current_dir}? Tippe j (ja) oder n (nein) "
                              f"um den Pfad zu ändern: "))
            if q_dir.lower() == "j":
                self.path = self.current_dir
                break
            elif q_dir.lower() == "n":
                directory_exists = False
                while directory_exists is False:
                    self.path = str(input("Gib den Pfad zu dem Ordner ein, in dem Du arbeiten möchtest: "))
                    if not os.path.isdir(self.path):
                        print("Dieses Verzeichnis existiert nicht. Gib erneut einen Ordnerpfad ein.")
                    else:
                        directory_exists = True
                break
            else:
                print("Ungültige Eingabe. Bitte 'j' oder 'n' eingeben.")

        # set working directory
        os.chdir(self.path)
        print(f"Nutzerverzeichnis festgelegt: {self.path}")

    def zip_exist(self):
        """Zip exist otherwise download"""

        while True:
            q_zip = str(input(f"Geht es um diese Datei: {self.zip_filename}? Tippe j (ja) oder n (nein) um die Datei "
                              f"zu ändern: "))
            if q_zip.lower() == "j":
                self.zip_file = self.zip_filename
                break
            elif q_zip.lower() == "n":
                self.zip_file = str(input("Gib den Dateinamen ein, um den es geht: "))
                break
            else:
                print("Ungültige Eingabe. Bitte 'j' oder 'n' eingeben.")

        if os.path.exists(self.zip_file):
            print(f"Datei {self.zip_file} existiert in dem aktuellen Arbeitsverzeichnis.")
        else:
            while True:
                q_down = str(input(f"Die Datei existiert nicht. Soll sie herunterladen werden? Tippe j oder n ein: "))
                if q_down.lower() == "j":
                    if self.zip_file != "GEO419A_Testdatensatz.zip":
                        # falls es um eine andere Datei geht, braucht es auch einen anderen Link
                        self.url = str(input(f"Bitte Downloadlink eingeben: "))
                    break
                elif q_down.lower() == "n":
                    sys.exit("Download nicht gestartet.")
                else:
                    print("Ungültige Eingabe. Bitte 'j' oder 'n' eingeben")
            try:
                response = requests.get(self.url, stream=True)  # stream=True Daten in Blöcken herunterladen
                response.raise_for_status()  # HTTP-Fehlermeldung, wenn Anfrage fehlschlägt

                # Für den Fortschritt:
                total_size = int(
                    response.headers.get("content-length", 0))  # Größe der herunterzuladenen Datei ermitteln, sonst 0
                block_size = 1024  # Blockgröße in der Datei heruntladen
                download_size = 0  # Variable zum Speichern der bereits heruntergeladenen Daten

                # Datei zum schreiben der heruntergeladenen Datei im Binärmodus (wb)
                with open(os.path.join(self.path, self.zip_file), "wb") as file:
                    # Über Daten iterieren, um Fortschritt anzeigen zu können
                    for data in response.iter_content(block_size):
                        file.write(data)  # Daten schreiben
                        download_size += len(data)  # Bereits heruntergeladene Daten aktualisieren
                        progress = download_size / total_size * 100  # Fortschritt in Prozent
                        print(f"\rDownload {self.zip_file}: {progress:.2f}%",
                              end="")  # Forschritt anzeigen (\r gleiche Zeile)
                print("Download erfolgreich abgeschlossen.")

            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP Fehler aufgetreten: {http_err}")
            except requests.exceptions.ConnectionError as conn_err:
                print(f"Netzwerkfehler aufgetreten: {conn_err}")
            except Exception as e:
                print(f"Fehler aufgetreten: {e}")

    def unpack(self):
        if self.geotiff != "S1A_IW_20230214T031857_DVP_RTC10_G_gpunem_A42B_VH.tif":
            q_file = str(input(f"Falls überprüft werden soll, ob es die Datei bereits gibt, bitte Dateinamen "
                               f"eingeben oder n (nein) um den Ordner ohne Überprüfung zu entpacken: "))
            if q_file != "n":
                self.geotiff = q_file  # neuer geotiff Name

        folder_name = os.path.splitext(self.zip_file)[0]  # Dateinamen ohne Erweiterung extrahieren
        if os.path.exists(self.geotiff) or os.path.exists(os.path.join("..", folder_name, self.geotiff)):
            print(f"Datei {self.geotiff} existiert in dem aktuellen Arbeitsverzeichnis.")
        else:
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)  # gleichnamigen Ordner anlegen

            while True:
                print(f"\rOrdner {self.zip_file} wird entpackt ... ", end="")
                with zipfile.ZipFile(self.zip_file) as zf:
                    zf.extractall(folder_name)
                    zf.close()
                    break

            print("\nFertig entpackt.")

    def run(self):
        """This is where all the real work happens"""
        # user directory
        self.user_dir()

        # zip exists? Otherwise Download
        self.zip_exist()

        # file exists? Otherwise unpack zip
        self.unpack()


if __name__ == "__main__":
    my_DownloadReadShow = DownloadReadShow()
    my_DownloadReadShow.run()

