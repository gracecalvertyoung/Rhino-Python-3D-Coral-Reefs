rugosity.py
rugosity_helper.3dm

Rhino Python script for computing linear rugosty on of curves of arbitrary length. A user can run the script from Rhino with the command ``RunPythonScript." The script will then ask them to select the curves for which they wish to know the rugosity. The script runs with a default chain link length of 2 cm, although comments in the script point the user to where to change this variable. 

ASSUMPTIONS: 
*Script assumes model units are meters. 
*Script assumes curve(s) are parallel to the X-axis. The user should rotate the curve parallel to the X-axis (using Rhino “Rotate” command) if it’s not already. 

Values of rugosity will print in the Rhino command screen. They can be copied from here into a spreadsheet.

rugosity_helper.3dm can be used to create curves following the topography of a mesh surface by copying-and-pasting the shape in rugosity_helper.3dm into the file with your mesh surface. The shape in rugosity_helper.3dm should then be positioned such that it intersects with the mesh surface. The user can then use “MeshIntersect” to find the intersection lines between the planes of rugosity_helper.3dm and their surface. 

See more information in PLOS ONE paper. 

Contact: G. C. Young <www.graceunderthesea.com>. 
