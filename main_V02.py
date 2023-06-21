import os
import sys
import zipfile
import requests
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib_scalebar.scalebar import ScaleBar

def set_user_dir(wd):
	'''
	Defines the working directory.

        Parameters:
	    	wd (str): working directory
	'''

	if wd == None:
		# if no wd, sets current working directory
		wd = os.getcwd()

	while True:
		q_dir = str(input(f"Möchtest Du in diesem Ordner arbeiten? \n {wd} \n Ja (Pfad behalten) \n Nein (Pfad ändern) \n [j/n]: "))
		if q_dir.lower() == "j":
			break
		elif q_dir.lower() == "n":
			directory_exists = False
			while directory_exists is False:
				wd = str(input("Gib den Pfad zu dem Ordner ein, in dem Du arbeiten möchtest: "))
				if not os.path.isdir(wd):
					print("Dieses Verzeichnis existiert nicht. Gib erneut einen Ordnerpfad ein: ")
				else:
					directory_exists = True
			break
		else:
			print("Ungültige Eingabe. Bitte 'j' oder 'n' eingeben.")

	# set working directory
	os.chdir(wd)
	print(f"Nutzerverzeichnis festgelegt: {wd}\n\n")

def check_filename(filename):
	'''
	Checks if the name of a file is th file the user wants to work with.

        Parameters:
	    	filename (str): name of a file

		Returns:
	        filename (str): file the user wants to work with
	'''
	while True:
		q_file = str(input(f"Geht es um diese Datei {filename}? \n Ja \n Nein (Datei ändern)\n[j/n] "))
		if q_file.lower() == "j":
			break
		elif q_file.lower() == "n":
			filename = str(input("Gib den Dateinamen ein, um den es geht: "))
			break
		else:
			print("Ungültige Eingabe. Bitte 'j' oder 'n' eingeben.")

	return filename

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
		print(f"Datei {filename} existiert in dem aktuellen Arbeitsverzeichnis.\n\n")
		exists = True
	else:
		print(f"Die Datei {filename} existiert in dem aktuellen Arbeitsverzeichnis nicht.\n\n")
		exists = False

	return exists

def download(zip_filename, url):
	'''
	Download zip file from url

		Parameters:
			zip_filename (str): name of the zip file
			url (str): link to download the given zip file

	'''
	while True:
		q_down = str(input(f"Soll die Datei {zip_filename} herunterladen werden? \n [j/n] "))
		if q_down.lower() == "j":
			if zip_filename != "GEO419A_Testdatensatz.zip":
				# if it's about a different file, it needs a different link as well
				url = str(input(f"Bitte Downloadlink eingeben: "))
			break
		elif q_down.lower() == "n":
			sys.exit("Download nicht gestartet.")
		else:
			print("Ungültige Eingabe. Bitte 'j' oder 'n' eingeben")
	try:
		response = requests.get(url, stream=True)  # stream=True Download data in blocks
		response.raise_for_status()  # HTTP error message when request fails

		# show progress:
		total_size = int(response.headers.get("content-length", 0))  # Determine the size of the file to be downloaded, otherwise 0
		block_size = 1024  # blocksize
		download_size = 0  # Variable to store the already downloaded data

		# File to write the downloaded file in binary mode (wb)
		with open(os.path.join(os.getcwd(), zip_filename), "wb") as file:
			# Iterate over data to show progress
			for data in response.iter_content(block_size):
				file.write(data)  # write data
				download_size += len(data)  # Update already downloaded data
				progress = download_size / total_size * 100  # Percent progress
				print(f"\rDownload {zip_filename}: {progress:.2f}%",end="")  # Show progress (\r same line)
		print("Download erfolgreich abgeschlossen.\n\n")

	except requests.exceptions.HTTPError as http_err:
		print(f"HTTP Fehler aufgetreten: {http_err}")
	except requests.exceptions.ConnectionError as conn_err:
		print(f"Netzwerkfehler aufgetreten: {conn_err}")
	except Exception as e:
		print(f"Fehler aufgetreten: {e}")

def unpack(filename, folder_name):
	'''
	unpacks the zip file

		Parameters:
			filename (str): zip file to be extracted
			folder_name (str): name of the zip file without file ending

	'''

	if not os.path.exists(folder_name):
		os.mkdir(folder_name)  # gleichnamigen Ordner anlegen

	while True:
		print(f"\rOrdner {filename} wird entpackt ... ", end="")
		with zipfile.ZipFile(filename) as zf:
			zf.extractall(folder_name)
			zf.close()
			break

	print("\nFertig entpackt.\n\n")

def scale_geotiff(filename, result):
	'''
	Load data, compute and write result

		Parameters:
			filename (str): unedited file
			result (str): computed image (the result)
	'''

	# open geotiff raster file
	ds_lin = gdal.Open(filename)
	# convert to numpy array
	arr_lin = ds_lin.GetRasterBand(1).ReadAsArray()

	# logarithmic scaling of the backscatter intensity
	print(f"{filename} wird logarithmisch skaliert...")
	arr_db = 10 * np.log10(arr_lin, where=arr_lin > 0)
	print(f"Skalierung beendet.\n\n")

	# set filename
	#extension = ".tif"
	#while True:
	#	q_filename = str(input(f"Gib einen Dateinamen ein: "))
	#	filename_result = q_filename + extension
	#	if not os.path.exists(filename_result):
	#		break
	#	else: print("Die Datei existiert bereits.")

	# Create new Dataset
	driver = gdal.GetDriverByName("GTiff")
	driver.Register()
	ds_db = driver.Create(result, xsize=arr_db.shape[1], ysize=arr_db.shape[0],
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

	print(f"Ergebnis wurde im Verzeichnis {os.getcwd()} unter {result} gespeichert.\n\n")

def visualize(result):
	'''
	Visualisation of the result

		Parameters:
			result (str): computed image (the result) to visualize
	'''


	print("Visualisierung lädt...")
	# open geotiff
	dataset = gdal.Open(result)
	image = dataset.ReadAsArray()
	# extract the geographical information from metadata
	geotransform = dataset.GetGeoTransform()

	image[image == 0] = np.nan # Set 0 values as NaN

	fig, ax = plt.subplots() # figure and axes

	# Show the image with white background
	im = ax.imshow(image, cmap='gray', vmin=np.nanmin(image), vmax=np.nanmax(image),
				   extent=[geotransform[0], geotransform[0] + geotransform[1] * dataset.RasterXSize, geotransform[3] +
						   geotransform[5] * dataset.RasterYSize, geotransform[3]])

	cbar = fig.colorbar(im, ax=ax, extend='neither') # legend
	cbar.ax.tick_params(labelsize = 8) # size colorbarnumbers

	# numbers of ticks (axis)
	ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=3))
	ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=3))

	# labels
	fig.text(0.87, 0.50, 'Rückstreuintensität [dB]', va='center', rotation='vertical')
	plt.subplots_adjust(top=0.85) # differnece between image and title
	ax.set_title("Logarithmisch skalierte Szene", pad=20)
	ax.set_xlabel("Ostwert", fontdict={'fontsize': 10})
	ax.set_ylabel("Nordwert", fontdict={'fontsize': 10})
	ax.tick_params(axis='both', which='major', labelsize=8) # fontsize of coordinate numbers (axis)

	# scalebar
	scalebar = ScaleBar(1, units='m', location='lower left', frameon=False, color='black', box_alpha=0.0, font_properties={'size': 8})
	ax.add_artist(scalebar)

	# coordinate system
	srs = dataset.GetProjection()
	if "PROJCS" in srs:
		start_index = srs.index("PROJCS") + len("PROJCS") + 2
		end_index = srs.index(",", start_index)
		projcs = srs[start_index:end_index].strip()
		projcs = projcs.replace('"', '') # without ""
		# add coordinate system to plot
		text_x = geotransform[0] + 0.99 * geotransform[1] * dataset.RasterXSize
		text_y = geotransform[3] + 0.97 * geotransform[5] * dataset.RasterYSize
		ax.annotate(f"{projcs}", xy=(text_x, text_y), xycoords='data', fontsize=6, ha='right', va='top')

	# show plot
	print("Fertig.\n\n")
	plt.show()

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
	set_user_dir(wd)
	# zip_filename
	zip_filename = check_filename(zip_filename)

	# zip exists? Otherwise Download
	if not file_exists(zip_filename):
		download(zip_filename, url)

	# geotiff
	geotiff = check_filename(geotiff)
	# file (geotiff) exists? Otherwise unpack zip
	zip_folder = os.path.splitext(zip_filename)[0]  # Dateinamen ohne Erweiterung extrahieren
	if not file_exists(geotiff, subfolder=zip_folder):
		unpack(zip_filename, zip_folder)

	os.chdir(zip_folder)

	# result
	result = os.path.splitext(geotiff)[0] + "_result" + os.path.splitext(geotiff)[1]
	result = check_filename(result)
	# result exists: read it. Otherwise load data, compute and write result
	if not file_exists(result, subfolder=zip_folder):
		# scaling geotiff from linear to logarithmical
		scale_geotiff(geotiff, result)

	# display result
	visualize(result)

	print("Programm wurde beendet.")


if __name__ == "__main__":
	if len(sys.argv) > 1:
		run(sys.argv[1])
	else:
		run()