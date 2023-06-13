import os
import sys
import zipfile
import requests
from osgeo import gdal
import numpy as np

def set_user_dir():
	'''
	Defines the working directory.
	'''

	current_dir = os.getcwd()

	# current working directory should be set as the user directory ?
	while True:
		q_dir = str(input(f"Möchtest Du in diesem Ordner arbeiten: {current_dir}? Tippe j (ja) oder n (nein) "))
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

def check_zip_filename(zip_filename):
	'''
	Checks if the name of a zip file is the zip file the user wants to work with.

        Parameters:
	    	zip_filename (str): name of a zip file

		Returns:
	        zip_filename (str): zip file the user wants to work with
	'''
	while True:
		q_zip = str(input(f"Geht es um diese Datei: {zip_filename}? Tippe j (ja) oder n (nein) "))
		if q_zip.lower() == "j":
			break
		if q_zip.lower() == "n":
			zip_filename = str(input("Gib den Dateinamen ein, um den es geht: "))
			break
		else:
			print("Ungültige Eingabe. Bitte 'j' oder 'n' eingeben.")

	return zip_filename

def file_exists(filename, subfolder=""):
	'''
	Checks if a given file is located in the working directory or in a given subfolder of the working directory.

	    Parameters:
		    filename (str): file whose existence is to be checked
		    subfolder (str), optional: subfolder in which the file may be located

		Returns:
		    exists (bool): boolean expression if file exists
	'''

	if os.path.exists(filename) or os.path.exists(os.path.join(".", subfolder, filename)):
		print(f"Datei {filename} existiert in dem aktuellen Arbeitsverzeichnis.")
		exists = True
	else:
		print(f"Die Datei {filename} existiert in dem aktuellen Arbeitsverzeichnis nicht.")
		exists = False

	return exists

def download(zip_filename, url):
	'''
	< Was macht die Funktion?>

		Parameters:
			zip_filename (<data type>): <Beschreibung>
			url (<data type>): <Beschreibung>

	'''
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
	'''
	< Was macht die Funktion?>

		Parameters:
			filename (<data type>): <Beschreibung>
			folder_name (<data type>): <Beschreibung>

	'''

	if not os.path.exists(folder_name):
		os.mkdir(folder_name)  # gleichnamigen Ordner anlegen

	while True:
		print(f"\rOrdner {filename} wird entpackt ... ", end="")
		with zipfile.ZipFile(filename) as zf:
			zf.extractall(folder_name)
			zf.close()
			break

	print("\nFertig entpackt.")

def scale_geotiff(filename):
	'''
	< Was macht die Funktion?>

		Parameters:
			filename (<data type>): <Beschreibung>
	'''

	# open geotiff raster file
	ds_lin = gdal.Open(filename)
	# convert to numpy array
	arr_lin = ds_lin.GetRasterBand(1).ReadAsArray()

	# logarithmic scaling of the backscatter intensity
	print(f"{filename} wird logarithmisch skaliert...")
	arr_db = 10 * np.log10(arr_lin, where=arr_lin > 0)
	print(f"Skalierung beendet")

	# set filename
	extension = ".tif"
	while True:
		q_filename = str(input(f"Gib einen Dateinamen ein: "))
		filename_result = q_filename + extension
		if not os.path.exists(filename_result):
			break
		else: print("Die Datei existiert bereits.")

	# Create new Dataset
	driver = gdal.GetDriverByName("GTiff")
	driver.Register()
	ds_db = driver.Create(filename_result, xsize=arr_db.shape[1], ysize=arr_db.shape[0],
						  bands=1, eType=gdal.GDT_Float32)

	# set extension of output raster
	ds_db.SetGeoTransform(ds_lin.GetGeoTransform())
	# set spatial reference system of output raster
	ds_db.SetProjection(ds_lin.GetProjection())

	# Write new backscatter values to rasterband
	band_db = ds_db.GetRasterBand(1)
	band_db.WriteArray(arr_db)
	band_db.SetNoDataValue(np.nan)
	band_db.FlushCache()

	# close output dataset
	band_db = None
	ds_db = None

	print(f"Ergebnis wurde im Verzeichnis {os.getcwd()} unter {filename_result} gespeichert.")

def visualise():
	# Für die Darstellung des Ergebnisses können verschiedene Pakete und Funktionen verwendet werden.
	# Wichtig ist eine Beschriftung der Achsen mit Koordinaten, eine Legende zur Darstellung des Wertebereichs,
	# sowie eine sinnvolle Farbkodierung der Bereiche ohne Werte („no data“). Gegebenenfalls ist eine weitere
	# Skalierung der Werte sinnvoll, um den Kontrast zu erhöhen.
	pass


def run(wd=None):
	'''
	< Was macht die Funktion?>

	Parameters:
			wd (str): <Beschreibung>
	'''

	zip_filename = "GEO419A_Testdatensatz.zip"
	url = "https://upload.uni-jena.de/data/641c17ff33dd02.60763151/GEO419A_Testdatensatz.zip"
	geotiff = "S1A_IW_20230214T031857_DVP_RTC10_G_gpunem_A42B_VH.tif"

	# set user directory
	if wd is None:
		set_user_dir()
	else:
		os.chdir(wd)
	check_zip_filename(zip_filename)

	# zip exists? Otherwise Download
	if not file_exists(zip_filename):
		download(zip_filename, url)

	# file exists? Otherwise unpack zip
	zip_folder = os.path.splitext(zip_filename)[0]  # Dateinamen ohne Erweiterung extrahieren
	if not file_exists(geotiff, subfolder=zip_folder):
		unpack(zip_filename, zip_folder)
		os.chdir(zip_folder)
		file_exists(geotiff, subfolder=zip_folder)

	os.chdir(zip_folder)
	print(os.getcwd())
	# scaling geotiff from linear to logarithmical
	scale_geotiff(geotiff)

	# <visualise()>

	print("Programm wurde beendet.")


if __name__ == "__main__":
	if len(sys.argv) > 1:
		run(sys.argv[1]) # TO DO: Überprüfen, ob der Code funktioniert, wenn man eine wd beim Aufruf eingibt
	else:
		run()