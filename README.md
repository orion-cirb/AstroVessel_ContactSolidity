# AstroVessel_ContactSolidity

* **Developed by:** Thomas & Héloïse
* **Developed for:** Noémie
* **Team:** Cohen-Salmon
* **Date:** May 2025
* **Software:** Blender (version 4.4.1) + Fiji


### Input files description

.obj files generated using the *featuresFromIsosurface.py* script developed by Clément Benedetti at the MRI Center for Image Analysis (available on their [GitHub repository](https://github.com/MontpellierRessourcesImagerie/imagej_macros_and_scripts/tree/master/clement/stand-alones/astrocytesBloodVessels)).

### Scripts description

#### AngleBased_Unwrapping.py :

Take a .obj file in input, perform a Angle Based Unwrapping (Flattening) and register 2 outputs :
  - One .blend with the object load into Blender and the UV map of the object
  - One .png 512x512 with the Unwrap image of the object

#### Solidity_Measurement.ijm :

Perform a Solidity measurement on all the .png images, output :
  - One .csv file with for each line : the image name, the object area, the Convex hull area, the solidity

### Dependencies

None

### Version history

Version 1 released on May 14, 2025.

