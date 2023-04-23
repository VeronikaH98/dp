# Extract edges
Extract sharp edges from triangle mesh file

This is a Python script that takes as input a mesh file, extracts sharp edges based on a given threshold angle, and exports selected triangles as .obj file and a lines between selected triangles = edges as .dxf file. Script loops over each face in the mesh to identify sharp edges by comparing the normal vectors of neighboring faces. If the angle between the two normal vectors is greater than the threshold angle, the edge is marked as sharp.

To run this script, you need to define in command line: input.obj output threshold_angle

	input = should be any triangulated mesh file, which have already computed normals (the input should be in a format that can be loaded by the Trimesh library)
	output = base name for outputs (.obj and .dxf)
	threshold_angle = the angle threshold for edge detection in degrees
