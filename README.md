# A Feature to Believe In

The scripts in this features-thesis repository are used to calculate and create contextual features, as well as calculate population density and urban attribute variables from OpenStreetMap. The scripts also use these data as inputs to build models based on the relationships between contextual features and urban attributes and between contextual features and population density.

The scripts were developed for and used in Chao (2020).

## Getting Started

These instructions will help you get started on replicating the methodology.

### Suggested Folder Structure

The suggested folder structure to conduct this analysis can be implemented using the script in 0_create-folders:

* ```data``` - contains the raw imagery and all of the non-imagery data, to include zone polygons (e.g., census tracts), population data (e.g., census counts), and urban attributes (i.e., OpenStreetMap data)
* ```outputs``` - contains outputs from the scripts in ```1_calculate-contextual-features```. Generally, the scripts from the scripts folder should be moved into the corresponding folder to facilitate processing and reduce the chances of getting errors (e.g., ```1-1_spfeas_create-vrt-spfeas.sh``` should be moved into the ```vrt``` folder, ```1-3b_spfeas_run-zonal-stats.sh``` and ```1-4_spfeas_combine-zonal-stats.py``` should be moved into the ```zonal_stats``` folder).
* ```regressions``` - contains the files (CSVs) used to run and outputs (```.pkl``` files, CSVs) from the regression analysis. Generally, the scripts from the scripts folder should be moved into the corresponding folder to facilitate processing and reduce the chances of getting errors (e.g., the scripts in the ```3_run-regression``` directory should be moved here)
* ```scripts``` - contains the scripts from this repository. Some scripts are able to run from this folder; others have to be directly in the folder they are processing.

### Installation

In addition to Python 3, the following packages are needed to run the scripts in this repository.

```
arcpy
geopandas
glob
joblib
os
pandas
rasterstats
scikit-learn
scipy
spfeas
statistics
time
```

To use ArcPy, a valid [Esri ArcGIS](https://www.esri.com/en-us/arcgis/products/arcgis-pro/overview) license is required. For more information on spfeas, see the [spfeas GitHub repository](https://github.com/jgrss/spfeas). [Anaconda](https://www.anaconda.com/products/individual) is recommended to create and manage environments (in which you can install the necessary packages).

## Usage

The scripts are separated into four consecutive folders, starting with 0. Navigate through the folders in that order. Within each folder are scripts, whose filename begins with a number starting with 1. Run through the files within each folder in that order.

Each script has a commented-out header that describes in greater detail what the script does, provides version information, and states what input files and preprocessing are needed to run the script successfully. It is assumed that all datafiles will be somewhat clean and error-free prior to processing. Through each script, an asterisk (```*```) in the comments denotes that a comment's corresponding code should be changed as necessary to accommodate user inputs. Likewise, triple quotations that surround placeholder text (```"""text"""```) indicates that the text should be changed as necessary to accommodate user inputs.

### 0_create-folders

The script in this folder is used to create folders and subfolders, in which the inputs and outputs from the subsequent scripts can be stored. This is optional and is used to give an example of how a folder structure can be set up for this analysis.

### 1_calculate-contextual-features

These scripts are used to calculate contextual features from satellite imagery. Once contextual features are computed, the bands for each contextual feature output are separated into individual TIF files. Zonal statistics is subsequently run on each file. Input requirements include satellite imagery (TIF file) and zones data such as census tracts (shapefile). The output is a CSV that contains contextual feature statistics for each zone.

### 2_calculate-urban-attributes

These scripts are used to calculate urban attributes (building area, building count, building density, road area, road length, road density, built-up area, and built-up density) from OpenStreetMap. OpenStreetMap data can be downloaded from [GeoFabrik](https://www.geofabrik.de). Input requirements include OpenStreetMap building and road data (shapefiles) and zones data such as census tracts (shapefile). The output is a Microsoft Excel file that contains values for each urban attribute for each zone.

### 3_run-regression

These scripts are used to build models for (1) contextual features and urban attributes and (2) contextual features and population density. The input data is prepared for analysis by running subsetting data by Pearson's r, scaling and normalizing, and separating into independent and dependent variables. There are two options for model building: elastic net regularized (ENR) regression and random forest (RF) regression. Input requirements include contextual feature zonal statistics (CSV), urban attribute statistics (CSV), population counts (CSV), and the area of each zone (CSV). The outputs consist of CSV files that indicate the predictive power, accuracy, and parameters of the models.

## Contribute

If you have any questions or suggestions, please [contact me](www.stevenchao.me/contact.php).

## License

To be determined.

## Author

* [**Steven Chao**](www.stevenchao.me), M.Sc. '20, The George Washington University

## Acknowledgments

* [**Ryan Engstrom, PhD**](https://geography.columbian.gwu.edu/ryan-engstrom), Associate Professor of Geography and of International Affairs, The George Washington University
* [**Michael Mann, PhD**](https://geography.columbian.gwu.edu/michael-mann), Associate Professor of Geography, The George Washington University
* [**Adane "Eddie" Bedada**](https://github.com/adbeda), M.Sc. '19, The George Washington University
* **Robert Harrison**, M.Sc. '18, The George Washington University
* Portions of this research were funded by the 2019 Campbell Summer Research Grant from [the George Washington University Department of Geography](https://geography.columbian.gwu.edu)

## Supplementary Information

### Additional Reading
* Chao, S. (2020). *A feature to believe in: Evaluating the ability to use contextual features derived from multi-scale satellite imagery to map spatial patterns of urban attributes and population distributions* (Publication No. 27838037) [Master's thesis, The George Washington University]. ProQuest Dissertations Publishing. [http://proxygw.wrlc.org/login?url=https://search-proquest-com.proxygw.wrlc.org/docview/2407587565?accountid=11243](http://proxygw.wrlc.org/login?url=https://search-proquest-com.proxygw.wrlc.org/docview/2407587565?accountid=11243)
* Engstrom, R., Harrison, R., Mann, M., & Fletcher, A. (2019). Evaluating the relationship between contextual features derived from very high spatial resolution imagery and urban attributes: A case study in Sri Lanka. *2019 Joint Urban Remote Sensing Event (JURSE)*, 1–4. [https://doi.org/10.1109/JURSE.2019.8809041](https://doi.org/10.1109/JURSE.2019.8809041)
* Graesser, J., Cheriyadat, A., Vatsavai, R. R., Chandola, V., Long, J., & Bright, E. (2012). Image based characterization of formal and informal neighborhoods in an urban landscape. *IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing*, *5*(4), 1164–1176. [https://doi.org/10.1109/jstars.2012.2190383](https://doi.org/10.1109/jstars.2012.2190383)
* Further reading can be found in the References section in Chao (2020).

### Troubleshooting

* With the scripts in ```1_calculate-contextual-features```: ```spfeas```, ```gdalbuildvrt```, and ```gdal_translate``` are very picky about where you are putting your inputs, outputs, and scripts. In most cases, (1) the output must be in the same folder as the script itself or the input files and/or (2) the input files need to be in the same folder as the script itself. It is mostly trial and error, so if the code fails, try playing around with the input/output file paths. The general folder structure of the file paths in the provided scripts should work, so most likely, all you need to do is simply replace the names. You can set up your file structure however you’d like for the most part, though; just make sure it is reflected in your scripts.
* This script first merges the raw imagery to form one single VRT file and subsequently uses the VRT file as an input to calculate contextual features. It is also possible to these steps in reverse: calculate contextual features from the raw imagery to form one single image per feature. Be aware, however, that when doing this reverse method, when the images are merged together, it creates a “seam” (a row of black pixels) where they merge, which can mess up zonal statistic calculations. Thus, this is not recommended.
* Troubleshooting specific to a script can be found in the script's commented-out header.

### Command Line Basics

Here are some basic commands:

* ```cd [filepath]``` - opens and goes into that folder
* ```cd ..``` - goes back out one folder (the enclosing folder)
* ```ls``` - lists all the files/folders within the specified folder
* ```mkdir [foldername]``` - creates a new folder
* ```pwd``` - prints the complete filepath of your current location

### Slurm Basics (for supercomputer processing)

Slurm is an open-source job scheduler often used on supercomputers. Here are some basic commands:

* ```sinfo``` - gives status of nodes; you can use this to choose on which node to run your script(s), but note the maximum time limit for each node
* ```squeue``` - gives status of your job(s)
* ```sbatch [filename].sh``` - sends your file to a queue on the supercomputer to be run as a job (must be a ```.sh``` file); the job may not run immediately given time constraints and scheduling

In each ```.sh``` file, there is header information that is commented out. **Do not delete this text.**

* ```-p``` - the node name (see ```sinfo``` above)
* ```-J``` - job name (can be anything you want to name your job)
* ```-t``` - time you want your code to run for in days-hours:minutes:seconds; it cannot be greater than the time limit of the node you chose in ```-p```
* ```--mail-user=NetID@gwu.edu``` - email to which a message will be sent when the job starts and finishes (regardless if it completes successfully)

The ```.sh``` file can contain command line command or call Python files (by typing ```python [filename].py```). If you try sending a file using ```sbatch``` and it gives an error, it may be due to the content of the header. Some nodes require different arguments in the header. Note that these Python scripts can be run without a supercomputer; just ignore the ```.sh``` files.

Each time a code finishes (whether it fails or finishes successfully), an ```.out``` file is produced in the same folder as the ```.sh``` file, and you can open the ```.out``` file in a text editor. It consists of the printouts from your script (similar to the Python console), and it will tell you if something failed.

To install and use anaconda on Linux (including supercomputers), see [this documentation](https://problemsolvingwithpython.com/01-Orientation/01.05-Installing-Anaconda-on-Linux/). For more information on Slurm, see the [Slurm Quick Start User Guide](https://slurm.schedmd.com/quickstart.html).
