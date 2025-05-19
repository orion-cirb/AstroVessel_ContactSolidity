# AstroVessel_ContactSolidity

* **Developed by:** Thomas & Héloïse
* **Developed for:** Noémie
* **Team:** Cohen-Salmon
* **Date:** May 2025
* **Software:** Blender (version 4.4.1) + Fiji


### Input files description

.obj files generated using the *featuresFromIsosurface.py* script developed by Clément Benedetti at the MRI Center for Image Analysis (available on their [GitHub repository](https://github.com/MontpellierRessourcesImagerie/imagej_macros_and_scripts/tree/master/clement/stand-alones/astrocytesBloodVessels)).

### Scripts description

#### AngleBased_Unwrapping.py:

Open each .obj file, perform Angle-Based Unwrapping (Flattening) of the contact surface between the astrocyte and the vessel, and save two outputs:
  - a .blend file containing the contact surface loaded into Blender along with its unwrapped UV map
  - a .png image (512×512 pixels) of the unwrapped UV map.

#### Solidity_Measurement.ijm:

Open each .png image, measure the solidity of the unwrapped UV map (defined as area / convex hull area), and save the results in a .csv file.

### Dependencies

None

### Version history

Version 1 released on May 14, 2025.

