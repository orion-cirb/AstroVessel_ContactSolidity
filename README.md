# Solidity_measurement

* **Developed by:** Thomas & Héloïse
* **Developed for:** Noémie
* **Team:** Cohen-Salmon
* **Date:** Mai 2025
* **Software:** Blender + Fiji


### Images description

Images obtained with featuresFromisosurfaces.py written by Clément Bendetti [Git Repo] (https://github.com/MontpellierRessourcesImagerie/imagej_macros_and_scripts/tree/master/clement/stand-alones/astrocytesBloodVessels)

### Description

#### AngleBased_Unwrapping.py :

* Take a .obj file in input, perform a Angle Based Unwrapping (Flattening) and register 2 outputs :
- One .blend with the object load into Blender and the UV map of the object
- One .png 512x512 with the Unwrap image of the object

#### Solidity_Measurement.ijm :

* Perform a Solidity measurement on all the .png images, output :
- One .csv file with for each line : the image name, the object area, the Convex hull area, the solidity

### Dependencies

Blender version 4.4.1
FIJI

### Version history

Version 1 released on Mai 14, 2025.

