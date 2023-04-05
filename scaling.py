import os.path
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt

def scale_geotiff():

	path = r"C:\Users\Nora\Desktop\Dokumente\Uni\Geoinformatik\2_SoSe_2023\GEO419A_Python_FE\Test"
	filename = r"S1A_IW_20230214T031857_DVP_RTC10_G_gpunem_A42B_VH.tif"
	# < Mit dieser Datei funktioniert die Umwandlung in einen Array >
	# filename = r"test.tif"

	# set working directory
	os.chdir(path)
	# open geotiff raster file
	dataset = gdal.Open(filename)

	# convert to array
	# < funktioniert irgendwie nicht, liegt es vielleicht an der Datei? Mit einer anderen tiff Datei funktioniert es. >
	img_lin = dataset.GetRasterBand(1).ReadAsArray() # Fehlermeldung!
	print(type(dataset))
	print(type(img_lin)) # Fehler: Array ist vom Typ None
	print(img_lin) # Fehler: Array ist None

	# logarithmic scaling of the backscatter intensity
	img_db = 10 * np.log10(img_lin)

	# < write result in new file >





	# < Für die spätere Visualisierung >
	#plt.figure()
	#plt.imshow(array)


#------------------------------------------------------------------------------
if __name__ == '__main__':  scale_geotiff()
#------------------------------------------------------------------------------