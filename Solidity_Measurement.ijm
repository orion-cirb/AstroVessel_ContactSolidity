/*
 * Description: Process an RGB image and retrieved Solidity of the object
 * Author: Thomas Caille & Héloïse Monnet @ ORION-CIRB
 * Date: Mai 2025
 * Repository: https://github.com/orion-cirb/Solidity_measurement.git
 * Dependencies: None
*/

// Hide on-screen updates for faster macro execution
setBatchMode(true);

// Prompt user to select directory containing input images
inputDir = getDirectory("Please select a directory containing images to analyze");

// Generate results directory with timestamp
getDateAndTime(year, month, dayOfWeek, dayOfMonth, hour, minute, second, msec);
resultDir = inputDir + "Results_" + year + "-" + (month+1) + "-" + dayOfMonth + "_" + hour + "-" + minute + "-" + second + File.separator();
if (!File.isDirectory(resultDir)) {
	File.makeDirectory(resultDir);
}

// Retrieve list of all files in input directory
inputFiles = getFileList(inputDir);

fileResults = File.open(resultDir + "results_compactness.csv");
print(fileResults, "Image name, Area ,ConvHull Area,Compactness\n");

// Process each .TIF file in the input directory
for (i = 0; i < inputFiles.length; i=i+1) {
    if (endsWith(inputFiles[i], ".png")) {
    	print("Analyzing image " + inputFiles[i] + "...");
    	imgName = replace(inputFiles[i], "_uv.png", "");
    	
    	// Open the current image
    	open(inputDir + inputFiles[i]);
    	// Change from RGB to 8 bit and invert the Look Up Table
    	run("8-bit");
    	run("Invert LUT");
    	// Processing : Apply a trheshold based on the histogram of the image 
    	setThreshold(0, 250, "raw");
    	setOption("BlackBackground", true);
		run("Convert to Mask");
		run("Create Selection");
		// Compute the Measurements
		run("Set Measurements...", "area shape skewness kurtosis redirect=None decimal=2");
		run("Measure");
		List.setMeasurements;
		// Store the differents measure in variables
		objectArea = List.getValue("Area"); 
		objectSolidity = List.getValue("Solidity");
		
		// Apply a convex Hull and fill it to retrieve the Area
		run("Convex Hull");
		List.setMeasurements;
		convHullArea = List.getValue("Area");
		
		print(fileResults, imgName +","+ objectArea +","+ convHullArea +","+ objectSolidity +"\n");
    	
		close("*");
    }
}

// Print completion message
print("Analysis done!");

// Restore batch mode to default
setBatchMode(false);