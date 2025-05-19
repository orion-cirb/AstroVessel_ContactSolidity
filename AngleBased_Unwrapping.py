'''
Description: Open 4-flattened-XX.obj files obtained with featuresFromIsosurface.py script
             Perform Angle Based Unwrapping of the object
             Save resulting UV map as .blend and .png files
Author: Thomas Caille & Héloïse Monnet @ ORION-CIRB
Date: May 2025
Repository: https://github.com/orion-cirb/AstroVessel_ContactSolidity.git
Dependencies: None
'''


import os
import bmesh
import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator
from bpy.props import StringProperty


class ImportAndProcessOBJs(Operator, ImportHelper):
    bl_idname = 'import_scene.batch_uv_obj'
    bl_label = 'Perform Unwrapping'
    
    directory: StringProperty(
        name='Folder',
        description='Folder with -flattened-XX.obj files',
        subtype='DIR_PATH'
    )

    def execute(self, context):
        # Ask for input folder
        folder = self.directory
        if not os.path.isdir(folder):
            self.report({'ERROR'}, 'Invalid folder')
            return {'CANCELLED'}

        # Retrieve 4-flattened-XX.obj files obtained with featuresFromIsosurface.py
        obj_files = [f for f in os.listdir(folder) if f.startswith('4-')  and f.endswith('.obj')]
        if not obj_files:
            self.report({'ERROR'}, 'No 4-flattened-XX.obj file found in folder')
            return {'CANCELLED'}

        # Iterate over retrieved files
        for filename in obj_files:
            filepath = os.path.join(folder, filename)
            name = os.path.splitext(filename)[0]
            self.report({'INFO'}, f'Unwrapping {name} file...')

            # Import file
            bpy.ops.wm.obj_import(filepath=filepath)
            # Select the new imported object
            obj = bpy.context.selected_objects[0]  
            # Set is as active
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)

            # Convert to mesh if not already
            if obj.type != 'MESH':
                bpy.ops.object.convert(target='MESH')

            # Enter edit mode to access mesh data
            bpy.ops.object.mode_set(mode='EDIT')
            bm = bmesh.from_edit_mesh(obj.data)

            # Select all faces
            for face in bm.faces:
                face.select = True
            bmesh.update_edit_mesh(obj.data)

            # Perform UV unwrapping using angle-based method
            bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=1.001)
            bpy.ops.object.mode_set(mode='OBJECT')

            # Export UV map as .png file
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj

            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.uv.select_all(action='SELECT')
            bpy.ops.object.mode_set(mode='OBJECT')

            uv_output_path = os.path.join(folder, f'{name}_uv.png')
            bpy.ops.uv.export_layout(filepath=uv_output_path,
                                     export_all=True,
                                     modified=False,
                                     mode='PNG',
                                     size=(512, 512),
                                     opacity=1.0)
                                     
            # Save the current state to a .blend file
            blend_output_path = os.path.join(folder, f'{name}_uv.blend')
            bpy.ops.wm.save_as_mainfile(filepath=blend_output_path)                      
            bpy.ops.object.delete()

        self.report({'INFO'}, 'Unwrapping done for all files!')
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ImportAndProcessOBJs)

def unregister():
    bpy.utils.unregister_class(ImportAndProcessOBJs)



if __name__ == '__main__':
    register()

    bpy.ops.import_scene.batch_uv_obj('INVOKE_DEFAULT')