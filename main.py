import os.path
import unpack

def main():

	# < ist es sinnvoll den Code in der Main Datei so umfangreich zu schreiben oder wollen wir
	#   lieber mehrere Unterfunktionen schreiben, die dann der reihe nach aufgerufen werden? >

	# Nutzerverzeichnis einlesen
	directory_exists = False
	while directory_exists is False:
		path = str(input("Gib den Pfad zu dem Ordner ein, in dem Du arbeiten möchtest: "))
		if not os.path.isdir(path):
			print("Dieses Verzeichnis existiert nicht. Gib erneut einen Ordnerpfad ein.")
		else:
			print(f"Nutzerverzeichnis festgelegt: {path}")
			directory_exists = True
	# set working directory
	os.chdir(path)

	# < Hier könnte man noch schauen, ob es vielleicht möglich ist, den Dateinamen über die Konsole
	#   einzugeben. >
	zip_filename = "GEO419A_Testdatensatz.zip"
	# check if zipfile exists
	if not os.path.exists(zip_filename):
		print("Datei wird herunter geladen")
		# < Datei downloaden >
		print("Download beendet.")

	# unpack zip file
	print("Zip File wird entpackt.")
	unpack.unpack(path, zip_filename)
	print("Fertig entpackt.")



# GeoTiff exists?

# unpack zip

# result exists?

# load data, compute and write result

# read result

# display result

#------------------------------------------------------------------------------
if __name__ == '__main__':  main()
#------------------------------------------------------------------------------