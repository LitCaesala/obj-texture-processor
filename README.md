# obj_texture_processor

A Python library to process OBJ files with texture information.
It's used to create obj file(vertices with colors) from obj file(with texture file).

## Installation

```bash
pip install obj_texture_processor

## Usage

```python
from obj_texture_processor.processor import process_obj_with_texture

obj_input_path = './path/to/your/texturedMesh.obj'
obj_output_path = './path/to/output.obj'

new_obj_file = process_obj_with_texture(obj_input_path, obj_output_path)
print(f"New OBJ file created at: {new_obj_file}")
