# Abschlussprojekt
Friedrich Schiller University Jena <br>
Institut for Geography <br>
Wintersemester 2022/23 <br>
Course: GEO 419A - Modulare Programmierung in der Fernerkundung


## Description

This program was developed as a final project of a university course on modular programming in remote sensing. The aim is to implement functions that:
1) download and unpack a zip file 
2) scale a geotiff image from linear to logarithmic values
3) visualise a geotiff file

The program includes a link to a zip file that contains a geotiff file for testing the code. You will also have the opportunity to define your own download path if you want to use a different file.

## Installation

In addition to the program we provide a yml-file that can be used to create a conda environment with all the packages that are necessary to run the program. In order to do this you have to run the following code in your terminal or in an Anaconda Prompt.

```
conda env create -f GEO419Aenv.yml
```

## Usage

If you want to use the functions individually in your own code you can import them.

```
from main_GEO419A import <name of the function you want to use>
```

You can also execute the file directly by calling the file and defining a working directory.

```
python main_GEO419A.py <your/file/.../path>
```

If you don't define a user directory the programm will give you the opportunity to define a working directory after you started the program.

```
python <dateiname.py>
```

If you execute the file directly the program will define a zip file which contains a processed scene of the Copernicus SAR satellite Sentinel-1A with linear scaled backscatter intensity. If the zip file does not exist in your working directory it will be downloaded from a given url link. After unzipping the file the program will scale the backscatter intensity of the contained geotiff into logarithmic backscatter values. At the end the result is displayed on the screen.

## Credits

This project was developed by Nora Fischer and Sheila Tholen.
