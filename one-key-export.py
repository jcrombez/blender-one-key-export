bl_info = {
    "name": "One Key Export",
    "version": (0, 4, 5),
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


class UnrealEngine_OneKeyExport(bpy.types.Operator):
    """One Key Export - Unreal Engine""" # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.one_key_export__unreal_engine" # Unique identifier for buttons and menu items to reference.
    bl_label = "One Key Export - Unreal Engine" # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'} # Enable undo for the operator.
    
    def execute(self, context):
        rename_unreal_collisions(context)
        
        initially_seleted_objects = context.selected_objects
        
        selected_root_objects = get_selected_root_objects(context, unselect=True)
                
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
                check_existing=True,
                filter_glob='*.fbx', 
                use_selection=True, 
                use_visible=False, 
                use_active_collection=False,
                global_scale=1.0,
                apply_unit_scale=True, # Apply Unit
                apply_scale_options='FBX_SCALE_NONE',
                use_space_transform=True,
                bake_space_transform=True, # Apply Transform
                object_types={'ARMATURE', 'EMPTY', 'MESH'}, 
                use_mesh_modifiers=True, # Apply Modifiers
                use_mesh_modifiers_render=True,
                mesh_smooth_type='FACE', # Smoothing
                colors_type='SRGB',
                prioritize_active_color=False,
                use_subsurf=False,
                use_mesh_edges=False,
                use_tspace=False,
                use_triangles=False,
                use_custom_props=False,
                add_leaf_bones=False,
                primary_bone_axis='Y',
                secondary_bone_axis='X',
                use_armature_deform_only=True, # Only Deform Bones
                armature_nodetype='NULL',
                bake_anim=True,
                bake_anim_use_all_bones=True,
                bake_anim_use_nla_strips=True,
                bake_anim_use_all_actions=True,
                bake_anim_force_startend_keying=True,
                bake_anim_step=1.0,
                bake_anim_simplify_factor=1.0,
                path_mode='AUTO',
                embed_textures=False,
                batch_mode='OFF',
                use_batch_own_dir=True,
                use_metadata=True,
                axis_forward='-X', # Forward
                axis_up='Z' # Up
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


class UnrealEngine_Collision_OneKeyExport(bpy.types.Operator):
    """One Key Export - Unreal Engine Collision""" # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.one_key_export__unreal_engine_collision" # Unique identifier for buttons and menu items to reference.
    bl_label = "One Key Export - Unreal Engine Collision" # Display name in the interface.

    def execute(self, context):
        processed = rename_unreal_collisions(context)
        self.report({'INFO'}, "Collisions processed : " + str(processed))
        return {'FINISHED'}

# --- --- --- #

def get_selected_root_objects(context, unselect=False):
    selected_root_objects = []
    
    for selected_object in context.selected_objects:
        if unselect:
            selected_object.select_set(False)
        
        if selected_object.parent is None:
            selected_root_objects.append(selected_object)
            
    return selected_root_objects

def unhide_hierarchy(object, exclude_collision = False):
    if exclude_collision and is_collision(object):
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


def is_collision(obj):
    return re.search('_col|_scol|_mcol', obj.name, re.IGNORECASE) is not None

def rename_unreal_collisions(context):
    processed = 0

    for root in get_selected_root_objects(context):
        unreal_collisions = get_unreal_collisions(root, [])
                        
        for index, col in enumerate(unreal_collisions):
            col.name = generate_unreal_collision_name(col, index + 1)
            col.display_type = 'WIRE'
            processed += 1
            
    return processed

def get_unreal_collisions(parent, unreal_collisions = []):
    for child in parent.children:
        if is_unreal_collision(child):
            unreal_collisions.append(child)
        else:
            get_unreal_collisions(child, unreal_collisions)
            
    return unreal_collisions
    
def is_unreal_collision(obj):
    return (re.search('_col|_ucx|ucx', obj.name, re.IGNORECASE) is not None and obj.parent is not None)

def generate_unreal_collision_name(obj, position):
    if obj.parent is None:
        return
    
    new_collision_name = f'UCX_{obj.parent.name}_{position}'
    return new_collision_name
        
# --- --- --- #


def menu_func(self, context):
    self.layout.operator(Snowdrop_OneKeyExport.bl_idname)
    self.layout.operator(SubstancePainter_OneKeyExport.bl_idname)
    self.layout.operator(UnrealEngine_OneKeyExport.bl_idname)
    self.layout.operator(UnrealEngine_Collision_OneKeyExport.bl_idname)

def register():
    bpy.utils.register_class(Snowdrop_OneKeyExport)
    bpy.utils.register_class(SubstancePainter_OneKeyExport)
    bpy.utils.register_class(UnrealEngine_OneKeyExport)
    bpy.utils.register_class(UnrealEngine_Collision_OneKeyExport)
    
    # Avoid adding the operator in the if it's already there.
    if hasattr(bpy.types.VIEW3D_MT_object.draw, '_draw_funcs'):
        if menu_func.__name__ not in (f.__name__ for f in bpy.types.VIEW3D_MT_object.draw._draw_funcs):
            bpy.types.VIEW3D_MT_object.prepend(menu_func)
    else:
        bpy.types.VIEW3D_MT_object.prepend(menu_func)

def unregister():
    bpy.utils.unregister_class(Snowdrop_OneKeyExport)
    bpy.utils.unregister_class(SubstancePainter_OneKeyExport)
    bpy.utils.unregister_class(UnrealEngine_OneKeyExport)
    bpy.utils.unregister_class(UnrealEngine_Collision_OneKeyExport)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
