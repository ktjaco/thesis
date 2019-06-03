# thesis

(uploads WIP)

In this repository you will find analysis, code and models related to my thesis research during my time at the Department of Geography and Environmental Studies (Carleton University - Ottawa, Ontario, Canada). My thesis research focused on quality assessment of Volunteered Geographic Information, specifically the OpenStreetMap (OSM) database.

My thesis paper can be found [here](https://curve.carleton.ca/fb66a114-871d-4cac-bfb1-092a65a28ccc).

## Requirements
* Python 3.6
* QGIS 3.4 LTR
* Jupyter Notebook

## /notebooks
In this folder you will find a series of Python Jupyter notebooks that relate to the methodology outlined in section 3.2.4 of my thesis paper. Much of the open-source code in this section can be credited to the open-source GIS team at [Oslandia](https://github.com/Oslandia/osm-data-classification). The code was altered and applied for my specific needs for the Ottawa-Gatineau OSM database.

## /qgis

### /2.18/models
Here you will find QGIS processing models related to road network and building map features. These models were developed for QGIS 2.18 and will not execute on QGIS 3.4 LTR. At the time of writing my thesis, QGIS 3.4 LTR was still in development. The [**Road Network Length Comparison**](https://anitagraser.com/2013/12/21/osm-quality-assessment-with-qgis-network-length/) and [**Road Network Position Accuracy Comparison**](https://anitagraser.com/2013/12/15/osm-quality-assessment-with-qgis-positional-accuracy/) model can be partially credited to [Anita Graser](https://anitagraser.com/) of the Austrian Institute of Technology.

### /3.4/models
These models are similar to those located in *qgis/2.18/models*, however they are for QGIS 3.4 LTR. These models are the **most stable** and **most recently updated**.

### /3.4/scripts
Exported Python scripts for the models located in *qgis/3.4/models*.

### /3.4/plugins

*In Development*

## Acknowledgements
* Carleton University, Department of Geography and Environmental Studies
* Oslandia
* Anita Graser, Austrian Institute of Technology
* OSM Contributors
* Open-Source Initiative
