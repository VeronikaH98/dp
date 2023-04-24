"""
Veronika Hajdúchová
2023
Diplomová práca: Detekcia hrán na lidarových dátach pomocou decimácie trojuholníkovej siete.
"""
# import of libraries
import trimesh
import numpy as np
import ezdxf
import sys
import time

def extract_edges(input, output, threshold_angle):
    start_time = time.time()   # record the script start time

    mesh = trimesh.load(input) # load mesh
    print(f"Loaded {len(mesh.faces)} triangles")

    # extract vertices and faces of the mesh
    vertices = mesh.vertices
    faces = mesh.faces

    is_edge = np.zeros(len(faces), dtype=bool)  # create boolean array for sharp/non sharp edges

    vertex_faces = {}  # initialize a dictionary for mapping vertices to the faces that they belong to
    for i, vertex in enumerate(vertices):
        vertex_faces[i] = [j for j, face in enumerate(faces) if i in face]  # map vertex i to all faces that contain it

    sharp_edges = []  # initialize an empty list for storing the sharp edges
    for i in range(len(faces)):
        vertex_indices = faces[i]  # get the indices of the vertices in the current face
        neighbors = []  # initialize a list for storing the neighboring faces
        for vertex_index in vertex_indices:
            neighbor_faces = vertex_faces[vertex_index]  # get the faces that contain the current vertex
            for neighbor_face in neighbor_faces:
                if neighbor_face != i:  # skip the current face
                    intersection = np.intersect1d(vertex_indices, faces[neighbor_face])  # get the shared vertices between the current face and the neighbor face
                    if len(intersection) == 2:  # if the neighbor face shares exactly two vertices with the current face
                        if neighbor_face not in neighbors:  # add the neighbor face to the list of neighboring faces
                            neighbors.append(neighbor_face)
        for n in neighbors:
            normal_i = mesh.face_normals[i]  # get the normal vector of the current face
            normal_n = mesh.face_normals[n]  # get the normal vector of the neighbor face
            theta = np.clip(np.dot(normal_i, normal_n) / (np.linalg.norm(normal_i) * np.linalg.norm(normal_n)), -1, 1)  # compute the cosine of the angle between the two normal vectors
            angle = np.degrees(np.arccos(theta))  # convert the cosine to degrees to get the angle between the two normal vectors
            if angle > threshold_angle:  # if the angle is greater than the threshold angle, mark the edge as sharp
                shared_vertices = set(faces[i]).intersection(set(faces[n]))  # get the shared vertices between the current face and the neighbor face
                sharp_edges.append((tuple(shared_vertices), i, n))  # add the sharp edge to the list of sharp edges
                is_edge[i] = True  # mark the current face as having a sharp edge
                is_edge[n] = True  # mark the neighbor face as having a sharp edge

    # extract the faces that are marked as sharp edges
    sharp_faces = faces[is_edge]
    num_selected_faces = len(sharp_faces)
    total_num_faces = len(mesh.faces)
    print(f"Selected {num_selected_faces} triangles out of {total_num_faces} loaded.")

    sharp_mesh = trimesh.Trimesh(vertices, sharp_faces) # create a new mesh object that only contains the faces that are marked as sharp edges
    sharp_mesh.export(output + ".obj") # export the sharp mesh to a file

    doc = ezdxf.new()    # create a new DXF document
    msp = doc.modelspace()   # get the model space of the DXF document
    layer = doc.layers.new('Sharp Edges')   # create a new layer called "Sharp Edges"

    # loops over each selected sharp edge in the sharp_edges list
    for edge in sharp_edges:
        start = vertices[edge[0][0]]    # retrieves the starting vertex of the sharp edge from the vertices array
        end = vertices[edge[0][1]]      # retrieves the ending vertex of the sharp edge from the vertices array
        msp.add_line(start, end, dxfattribs={'layer': layer})   # adds a new line to the model space of the DXF document, with the specified starting and ending points

    dxf_output = output + ".dxf"  # specifies the output file name for the DXF file to be created, by concatenating the output argument with the '.dxf' file extension
    doc.saveas(dxf_output) # saves the DXF document to the specified file path

    end_time = time.time()  # records the end time of the script

    print(f"Script took {end_time - start_time:.2f} seconds to run.")

if __name__ == "__main__":
    if len(sys.argv) != 4:  # check the number of command line agruments
        print("Help: python extract_edges.py <input> <output> <threshold_angle>")
        sys.exit(1)
    # retieving arguments from command line
    input = sys.argv[1]
    output = sys.argv[2]
    threshold_angle = float(sys.argv[3])
    extract_edges(input, output, threshold_angle) #passing in the command line arguments as arguments to the function
