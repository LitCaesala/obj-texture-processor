# obj_texture_processor/processor.py

import os
import cv2

def process_obj_with_texture(obj_file_path, output_file_path):
    v = []
    vt = []
    materials = {}
    vt_rgb = {}
    material_faces = {}

    def load_mtl(mtl_file):
        current_material = None
        with open(mtl_file, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith('newmtl'):
                    current_material = line.split()[-1].strip()
                    print(f"Found material: {current_material}")
                elif line.startswith('map_Kd') and current_material:
                    texture_file = line.split()[-1].strip()
                    materials[current_material] = texture_file

    obj_dir = os.path.dirname(obj_file_path)
    mtl_file_path = os.path.join(obj_dir, 'texturedMesh.mtl')

    load_mtl(mtl_file_path)

    with open(obj_file_path, mode='r', encoding='utf-8') as file_obj:
        temp = file_obj.readlines()

    current_material = None
    for line in temp:
        if line.startswith('usemtl '):
            current_material = line.split()[1].strip()
            if current_material not in material_faces:
                material_faces[current_material] = []
        elif line.startswith('v '):
            v.append(line.split()[1:])
        elif line.startswith('vt '):
            vt.append(list(map(float, line.split()[1:])))
        elif line.startswith('f '):
            material_faces[current_material].append(line.split()[1:])

    print(f"Materials and their textures: {materials}")

    def load_texture_colors():
        for material, texture_file in materials.items():
            print(texture_file)
            img = cv2.imread(os.path.join(obj_dir, texture_file))
            height, width, _ = img.shape
            vt_rgb[material] = []
            for i in range(len(vt)):
                temp_vt = list(vt[i])
                h = (temp_vt[0] % 1) * height
                w = (temp_vt[1] % 1) * width
                color = img[width - int(w) - 1][int(h) - 1]
                red = float(color[2] / 255)
                green = float(color[1] / 255)
                blue = float(color[0] / 255)
                vt_rgb[material].append([red, green, blue])

    load_texture_colors()

    print(f"vt_rgb keys: {vt_rgb.keys()}")

    for material, faces in material_faces.items():
        for fi in faces:
            for j in range(3):
                tem = fi[j].split('/')
                vi, vti = int(tem[0]) - 1, int(tem[1]) - 1
                if len(v[vi]) == 3:
                    v[vi].extend([str(vt_rgb[material][vti][0]), str(vt_rgb[material][vti][1]), str(vt_rgb[material][vti][2])])

    with open(output_file_path, mode='w', encoding='utf-8') as file_obj:
        for vertex in v:
            if len(vertex) == 6:
                line = f"v {vertex[0]} {vertex[1]} {vertex[2]} {vertex[3]} {vertex[4]} {vertex[5]}\n"
            else:
                line = f"v {vertex[0]} {vertex[1]} {vertex[2]}\n"
            file_obj.write(line)

        for material, faces in material_faces.items():
            for face in faces:
                face_line = f"f {face[0]} {face[1]} {face[2]}\n"
                file_obj.write(face_line)

    print("OBJ file with embedded color information created successfully.")
    return output_file_path

