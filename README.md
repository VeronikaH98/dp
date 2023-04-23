# Extract the edges
Extract the sharp edges from the triangular mesh file

This is a Python script that takes a mesh file as input, extracts sharp edges based on a given threshold angle, and exports selected triangles as an .obj file and lines between selected triangles = edges as a .dxf file. The script loops through each face in the mesh to identify sharp edges by comparing the normal vectors of adjacent faces. If the angle between the two normal vectors is greater than the threshold angle, the edge is marked as sharp.

To run this script, you must define in the command line: input.obj output threshold_angle

+ input = should be any triangular mesh file that already has normals calculated (input should be in a format that the Trimesh library can read)
+ output = base name for outputs (.obj and .dxf)
+ angle_threshold = angle threshold for edge detection in degrees
