bl_info = {
    "name": "One Key Export",
    "version": (0, 4),
    "blender": (2, 80, 0),
    "category": "Export",
    "author": "Jérémy Crombez",
}

import bpy
import os, time, re


# --- --- --- #


class Snowdrop_OneKeyExport(bpy.types.Operator):
    """One Key Export - Snowdrop""" # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.one_key_export__snowdrop" # Unique identifier for buttons and menu items to reference.
    bl_label = "One Key Export - Snowdrop" # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'} # Enable undo for the operator.
    
    def execute(self, context):      
        initially_seleted_objects = context.selected_objects
        
        selected_root_objects = []

        for selected_object in context.selected_objects:
            selected_object.select_set(False)
            
            if selected_object.parent is None:
                selected_root_objects.append(selected_object)
                
        for root in selected_root_objects:
            root.select_set(True)

            previously_hidden_objects = unhide_hierarchy(root)
            select_hierarchy(root)
            
            # Saving initial location
            initial_root_location_x = root.location.x
            initial_root_location_y = root.location.y
            initial_root_location_z = root.location.z
            
            # Resetting location
            root.location.x = 0
            root.location.y = 0
            root.location.z = 0
            
            # FBX Export
            
            blend_file_full_path = bpy.data.filepath
            blend_file_path = os.path.dirname(blend_file_full_path)
            fbx_file_name = root.name + '.fbx'
            fbx_file_full_path = os.path.join(blend_file_path, fbx_file_name)

            bpy.ops.export_scene.fbx(
                filepath=fbx_file_full_path,
                use_selection=True,
            )

            # Ugly workaround to wait for the export
            # TODO: wait for the file update date to change instead
            time.sleep(0.2)

            # Hide back what was hidden
            for object in previously_hidden_objects:
                object.hide_set(True)
                
            # Move back to origin location
            root.location.x = initial_root_location_x
            root.location.y = initial_root_location_y
            root.location.z = initial_root_location_z
            
            bpy.ops.object.select_all(action='DESELECT')
        
        # Select back what was selected        
        for object in initially_seleted_objects:
            object.select_set(True)
            
        self.report({'INFO'}, "Export done :-)")

        return {'FINISHED'}
    

# --- --- --- #


class SubstancePainter_OneKeyExport(bpy.types.Operator):
    """One Key Export - Substance Painter""" # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.one_key_export__substance_painter" # Unique identifier for buttons and menu items to reference.
    bl_label = "One Key Export - Substance Painter" # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'} # Enable undo for the operator.
    

    def execute(self, context):    
        initially_seleted_objects = context.selected_objects

        previously_hidden_objects = []
        
        selected_root_objects = []
        
        for selected_object in context.selected_objects:
            if selected_object.parent is None:
                selected_root_objects.append(selected_object)
                previously_hidden_objects += unhide_hierarchy(selected_object)
                select_hierarchy(selected_object, ignore_collision = True)            

        # Duplicate selected objects and then select duplicates
        bpy.ops.object.duplicate()
        
        # Remove all UVs but UV2 on all duplicates
        for selected_object in context.selected_objects:
            only_keep_uv2(selected_object)
                          
        blend_file_full_path = bpy.data.filepath
        blend_file_path = os.path.dirname(blend_file_full_path)
        
        # Find the best name
        first_root_name = selected_root_objects[0].name
        
        if len(selected_root_objects) == 1:
            fbx_base_name = first_root_name
        else:
            fbx_base_name = first_root_name.replace('_' + first_root_name.split('_')[-1], '')
            
        fbx_file_name = fbx_base_name + '.fbx'
        fbx_file_path = blend_file_path + '/workfiles/';
        
        # Create the directory if needed
        if not os.path.exists(fbx_file_path):
            os.makedirs(fbx_file_path)
            
        fbx_file_full_path = os.path.join(fbx_file_path, fbx_file_name)

        bpy.ops.export_scene.fbx(
            filepath=fbx_file_full_path,
            use_selection=True,
        )
        
        # Ugly workaround to wait for the export
        # TODO: wait for the file update date to change instead
        time.sleep(0.3)
        
        # Delete the selected objects (the duplicates)
        bpy.ops.object.delete()

        # Hide back what was hidden
        for object in previously_hidden_objects:
            object.hide_set(True)
        
        # Select back what was selected
        
        bpy.ops.object.select_all(action='DESELECT')
        
        for object in initially_seleted_objects:
            object.select_set(True)
                    
        self.report({'INFO'}, "Export done :-)")

        return {'FINISHED'}

    
# --- --- --- #


def unhide_hierarchy(object):
    if is_collision(object):
        return []
    
    previously_hidden_objects = []
    
    if object.hide_get():
        previously_hidden_objects.append(object)
        object.hide_set(False)
    
    for child in object.children:
        previously_hidden_objects += unhide_hierarchy(child)
        
    return previously_hidden_objects


def select_hierarchy(object, ignore_collision = False):    
    if ignore_collision and is_collision(object):
        object.select_set(False)
        return

    object.select_set(True)
    
    for child in object.children:
        select_hierarchy(child, ignore_collision)


def only_keep_uv2(object):        
    # Ignore objects (like Empties) who have no UVs
    if not hasattr(object.data, 'uv_layers'):
        return

    uvs = object.data.uv_layers
    
    # Ignore objects with only 1 uv
    if len(uvs) == 1:
        return
    
    # Set UV2 as the active one
    uvs.active_index = 1
    
    # Delete not active UVs
 
    not_active_uvs = [uv for uv in uvs if uv != uvs.active]
    
    while not_active_uvs:
        uvs.remove(not_active_uvs.pop())


def is_collision(object):
    return re.search('_col|_scol|_mcol', object.name, re.IGNORECASE) is not None


# --- --- --- #
    
    
def menu_func(self, context):
    self.layout.operator(Snowdrop_OneKeyExport.bl_idname)
    self.layout.operator(SubstancePainter_OneKeyExport.bl_idname)

    
def register():
    bpy.utils.register_class(Snowdrop_OneKeyExport)
    bpy.utils.register_class(SubstancePainter_OneKeyExport)
    
    # Avoid adding the operator in the if it's already there.
    if hasattr(bpy.types.VIEW3D_MT_object.draw, '_draw_funcs'):
        if menu_func.__name__ not in (f.__name__ for f in bpy.types.VIEW3D_MT_object.draw._draw_funcs):
            bpy.types.VIEW3D_MT_object.prepend(menu_func)
    else:
        bpy.types.VIEW3D_MT_object.prepend(menu_func)

def unregister():
    bpy.utils.unregister_class(Snowdrop_OneKeyExport)
    bpy.utils.unregister_class(SubstancePainter_OneKeyExport)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
