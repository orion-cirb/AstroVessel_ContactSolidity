'''
Description: Process .obj files obtained with featuresFromIsosurface.py, unwrap (ANGLE_BASED) the object and save the resulting UV in .png
Author: Thomas Caille & Héloïse Monnet @ ORION-CIRB
Date: Mai 2025
Repository: https://github.com/orion-cirb/Solidity_measurement.git
Dependencies: None
'''
import bpy
import os
import bmesh

from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator
from bpy.props import StringProperty


class ImportAndProcessOBJs(Operator, ImportHelper):
    bl_idname = "import_scene.batch_uv_obj"
    bl_label = "import and export UV PNG"
    
    # Choose a folder and not a file
    directory: StringProperty(
        name="Folder",
        description="Folder with the .obj files",
        subtype='DIR_PATH'
    )

    def execute(self, context):
        folder = self.directory
        if not os.path.isdir(folder):
            self.report({'ERROR'}, "Wrong folder")
            return {'CANCELLED'}
        # select only the flattenned obj obtained with featuresFromIsosurface.py
        obj_files = [f for f in os.listdir(folder) if f.startswith('4-')  and f.endswith('.obj')]

        if not obj_files:
            self.report({'WARNING'}, "No .obj files found")
            return {'CANCELLED'}

        for filename in obj_files:
            filepath = os.path.join(folder, filename)
            name = os.path.splitext(filename)[0]
            uv_output_path = os.path.join(folder, f"{name}_uv.png")
            blend_output_path = os.path.join(folder, f"{name}.blend")

            # Import .obj file
            bpy.ops.wm.obj_import(filepath=filepath)
            obj = bpy.context.selected_objects[0]  # Select the new imported object

            # Active it
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)

            # Convert in mesh if needed
            if obj.type != 'MESH':
                bpy.ops.object.convert(target='MESH')

            # Edit mode
            bpy.ops.object.mode_set(mode='EDIT')
            bm = bmesh.from_edit_mesh(obj.data)

            # Select all faces
            for face in bm.faces:
                face.select = True
            bmesh.update_edit_mesh(obj.data)

            # Unwrap UV
            bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=1.001)
            bpy.ops.object.mode_set(mode='OBJECT')

            # Export UV map in PNG
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj

            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.uv.select_all(action='SELECT')
            bpy.ops.object.mode_set(mode='OBJECT')

            bpy.ops.uv.export_layout(filepath=uv_output_path,
                                     export_all=True,
                                     modified=False,
                                     mode='PNG',
                                     size=(512, 512),
                                     opacity=1.0)
                                     
            bpy.ops.wm.save_as_mainfile(filepath=blend_output_path)                      
            bpy.ops.object.delete()
            print(f"✅ {filename} : UV register -> {uv_output_path}")

        self.report({'INFO'}, "Analysis Done.")
        return {'FINISHED'}


# Register
def register():
    bpy.utils.register_class(ImportAndProcessOBJs)

def unregister():
    bpy.utils.unregister_class(ImportAndProcessOBJs)

if __name__ == "__main__":
    register()

    # Dialog box
    bpy.ops.import_scene.batch_uv_obj('INVOKE_DEFAULT')