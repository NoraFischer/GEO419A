import os
import sys
import zipfile
import requests

def set_user_dir(current_dir):
	"""Nutzerverzeichnis festlegen"""
	# current working directory should be set as the user directory ?
	while True:
		q_dir = str(input(f"Möchtest Du in diesem Ordner arbeiten: {current_dir}? Tippe j (ja) oder n (nein) "
						  f"um den Pfad zu ändern: "))
		if q_dir.lower() == "j":
			path = current_dir
			break
		elif q_dir.lower() == "n":
			directory_exists = False
			while directory_exists is False:
				path = str(input("Gib den Pfad zu dem Ordner ein, in dem Du arbeiten möchtest: "))
				if not os.path.isdir(path):
					print("Dieses Verzeichnis existiert nicht. Gib erneut einen Ordnerpfad ein.")
				else:
					directory_exists = True
			break
		else:
			print("Ungültige Eingabe. Bitte 'j' oder 'n' eingeben.")

	# set working directory
	os.chdir(path)
	print(f"Nutzerverzeichnis festgelegt: {path}")

def set_zip_filename(zip_filename):
	while True:
		q_zip = str(input(f"Geht es um diese Datei: {zip_filename}? Tippe j (ja) oder n (nein) um die Datei "
						  f"zu ändern: "))
		if q_zip.lower() == "j":
			break
		if q_zip.lower() == "n":
			zip_filename = str(input("Gib den Dateinamen ein, um den es geht: "))
			break
		else:
			print("Ungültige Eingabe. Bitte 'j' oder 'n' eingeben.")
	return zip_filename

def file_exists(filename, subfolder=None):

	if os.path.exists(filename) or os.path.exists(os.path.join(".", subfolder, filename)):
		print(f"Datei {filename} existiert in dem aktuellen Arbeitsverzeichnis.")
		exists = True
	else:
		print(f"Die Datei {filename} existiert in dem aktuellen Arbeitsverzeichnis nicht.")
		exists = False

	return exists

def download(zip_filename, url):

	while True:
		q_down = str(input(f"Soll die Datei {zip_filename} herunterladen werden? Tippe j oder n ein: "))
		if q_down.lower() == "j":
			if zip_filename != "GEO419A_Testdatensatz.zip":
				# falls es um eine andere Datei geht, braucht es auch einen anderen Link
				url = str(input(f"Bitte Downloadlink eingeben: "))
			break
		elif q_down.lower() == "n":
			sys.exit("Download nicht gestartet.")
		else:
			print("Ungültige Eingabe. Bitte 'j' oder 'n' eingeben")
	try:
		response = requests.get(url, stream=True)  # stream=True Daten in Blöcken herunterladen
		response.raise_for_status()  # HTTP-Fehlermeldung, wenn Anfrage fehlschlägt

		# Für den Fortschritt:
		total_size = int(response.headers.get("content-length", 0))  # Größe der herunterzuladenen Datei ermitteln, sonst 0
		block_size = 1024  # Blockgröße in der Datei heruntladen
		download_size = 0  # Variable zum Speichern der bereits heruntergeladenen Daten

		# Datei zum Schreiben der heruntergeladenen Datei im Binärmodus (wb)
		with open(os.path.join(os.getcwd(), zip_filename), "wb") as file:
			# Über Daten iterieren, um Fortschritt anzeigen zu können
			for data in response.iter_content(block_size):
				file.write(data)  # Daten schreiben
				download_size += len(data)  # Bereits heruntergeladene Daten aktualisieren
				progress = download_size / total_size * 100  # Fortschritt in Prozent
				print(f"\rDownload {zip_filename}: {progress:.2f}%",end="")  # Forschritt anzeigen (\r gleiche Zeile)
		print("Download erfolgreich abgeschlossen.")

	except requests.exceptions.HTTPError as http_err:
		print(f"HTTP Fehler aufgetreten: {http_err}")
	except requests.exceptions.ConnectionError as conn_err:
		print(f"Netzwerkfehler aufgetreten: {conn_err}")
	except Exception as e:
		print(f"Fehler aufgetreten: {e}")

def unpack(filename, folder_name):

	if not os.path.exists(folder_name):
		os.mkdir(folder_name)  # gleichnamigen Ordner anlegen

	while True:
		print(f"\rOrdner {filename} wird entpackt ... ", end="")
		with zipfile.ZipFile(filename) as zf:
			zf.extractall(folder_name)
			zf.close()
			break

	print("\nFertig entpackt.")

def run():

	current_dir = os.getcwd()
	zip_filename = "GEO419A_Testdatensatz.zip"
	url = "https://upload.uni-jena.de/data/641c17ff33dd02.60763151/GEO419A_Testdatensatz.zip"
	geotiff = "S1A_IW_20230214T031857_DVP_RTC10_G_gpunem_A42B_VH.tif"

	# set user directory
	set_user_dir(current_dir)
	set_zip_filename(zip_filename)

	# zip exists? Otherwise Download
	if not file_exists(zip_filename):
		download(zip_filename, url)

	# file exists? Otherwise unpack zip
	zip_folder = os.path.splitext(zip_filename)[0]  # Dateinamen ohne Erweiterung extrahieren
	if not file_exists(geotiff, subfolder=zip_folder):
		unpack(zip_filename, zip_folder)
		file_exists(geotiff, subfolder=zip_folder)


if __name__ == "__main__":
    run()