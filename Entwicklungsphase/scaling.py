import os.path
import numpy as np
from osgeo import gdal
import rasterio


def scale_geotiff():

	path = r"C:\Users\Nora\Desktop\Dokumente\Uni\Geoinformatik\2_SoSe_2023\GEO419A_Python_FE\Test"
	#filename = "S1A_IW_20230214T031857_DVP_RTC10_G_gpunem_A42B_VH_clipped.tif"
	filename = r"S1A_IW_20230214T031857_DVP_RTC10_G_gpunem_A42B_VH.tif"
	# < Mit dieser Datei funktioniert die Umwandlung in einen Array >
	#filename = r"test.tif"

	# set working directory
	os.chdir(path)
	# open geotiff raster file

	#ds_lin = gdal.Open(filename)
	arr_lin = rasterio.open(filename).read(1)
	print(arr_lin)

	'''
	# convert to numpy array
	# < funktioniert irgendwie nicht, liegt es vielleicht an der Datei? Mit einer anderen tiff Datei funktioniert es. >
	arr_lin = ds_lin.GetRasterBand(1).ReadAsArray()
	print(type(ds_lin))
	print(type(arr_lin)) # Fehler: Array ist vom Typ None
	print(arr_lin) # Fehler: Array ist None

	# logarithmic scaling of the backscatter intensity
	arr_db = 10 * np.log10(arr_lin, where=arr_lin > 0) # Fehlermeldung!
	print(arr_db)

	# Create new Dataset
	driver = gdal.GetDriverByName("GTiff") # Was ist ein Driver uns was macht er?
	driver.Register()
	ds_db = driver.Create("new_geotiff.tif", xsize=arr_db.shape[1], ysize=arr_db.shape[0],
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
	
	'''

#------------------------------------------------------------------------------
if __name__ == '__main__':  scale_geotiff()
#------------------------------------------------------------------------------