/*
 * Description: Open 4-flattened-XX.png files obtained with AngleBased_Unwrapping.py and compute solidity of the UV map
 * Authors: Thomas Caille & Héloïse Monnet @ ORION-CIRB
 * Date: May 2025
 * Repository: https://github.com/orion-cirb/AstroVessel_ContactSolidity.git
 * Dependencies: None
*/

// Hide on-screen updates for faster macro execution
setBatchMode(true);

// Prompt user to select directory containing input images
inputDir = getDirectory("Please select a directory containing images to analyze");

// Retrieve list of all files in input directory
inputFiles = getFileList(inputDir);

// Create results_solidity.csv file
fileResults = File.open(inputDir + "results_solidity.csv");
print(fileResults, "Image name,Area,Convex hull area,Solidity\n");

// Process each .png file in the input directory
for (i = 0; i < inputFiles.length; i=i+1) {
    if (endsWith(inputFiles[i], ".png")) {
    	print("Analyzing image " + inputFiles[i] + "...");
    	imgName = replace(inputFiles[i], "_uv.png", "");
    	
    	// Open image
    	open(inputDir + inputFiles[i]);
    	
    	// Convert to 8-bit and invert LUT
    	run("8-bit");
    	run("Invert LUT");
    	
    	// Segment UV map using manual thresholding
    	setThreshold(0, 250, "raw");
    	setOption("BlackBackground", true);
		run("Convert to Mask");
		
		// Measure area and solidity
		run("Create Selection");
		run("Set Measurements...", "area shape redirect=None decimal=2");
		run("Measure");
		List.setMeasurements;
		area = List.getValue("Area"); 
		solidity = List.getValue("Solidity");
		
		// Compute convex hull and measure area
		run("Convex Hull");
		List.setMeasurements;
		convexHullArea = List.getValue("Area");
		
		// Save parameters in results file
		print(fileResults, imgName +","+ area +","+ convexHullArea +","+ solidity +"\n");
    	
    	// Close all windows
		close("*");
		close("Results");
    }
}

// Print completion message
print("Analysis done!");

// Restore batch mode to default
setBatchMode(false);
