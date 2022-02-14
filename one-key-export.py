bl_info = {
    "name": "One Key Export",
    "version": (0, 2),
    "blender": (2, 80, 0),
    "category": "Export",
    "author": "Jérémy Crombez",
}

import bpy
import os, time

class OneKeyExport(bpy.types.Operator):
    """One Key Export""" # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.one_key_export2" # Unique identifier for buttons and menu items to reference.
    bl_label = "One Key Export" # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'} # Enable undo for the operator.

    def execute(self, context): # execute() is called when running the operator.
        obs = [o for o in context.selected_objects if o.type == 'MESH']

        if len(context.selected_objects) != 1:
            raise Exception("invalid selection")
            
        root = context.selected_objects[0]

        hiddenObjects = []

        for child in root.children:
            if child.hide_get():
                hiddenObjects.append(child)
                child.hide_set(False)

            child.select_set(True)
            
        blend_file_path = bpy.data.filepath
        directory = os.path.dirname(blend_file_path)
        file_name = root.name + '.fbx'
        target_file = os.path.join(directory, file_name)
        
        initial_root_location_x = root.location.x
        initial_root_location_y = root.location.y
        initial_root_location_z = root.location.z
        
        root.location.x = 0
        root.location.y = 0
        root.location.z = 0

        bpy.ops.export_scene.fbx(
            filepath=target_file,
        #    check_existing=True,
        #    axis_forward='-Z',
        #    axis_up='Y',
        #    filter_glob="*.fbx",
        #    version='BIN7400',
        #    ui_tab='MAIN',
            use_selection=True,
        #    global_scale=1.0,
        #    apply_unit_scale=True,
        #    bake_space_transform=False,
        #    object_types={'ARMATURE', 'CAMERA', 'EMPTY', 'LAMP', 'MESH', 'OTHER'},
        #    use_mesh_modifiers=True,
        #    mesh_smooth_type='OFF',
        #    use_mesh_edges=False,
        #    use_tspace=False,
        #    use_custom_props=False,
        #    add_leaf_bones=True,
        #    primary_bone_axis='Y',
        #    secondary_bone_axis='X',
        #    use_armature_deform_only=False,
        #    armature_nodetype='NULL',
        #    bake_anim=True,
        #    bake_anim_use_all_bones=True,
        #    bake_anim_use_nla_strips=True,
        #    bake_anim_use_all_actions=True,
        #    bake_anim_force_startend_keying=True,
        #    bake_anim_step=1.0,
        #    bake_anim_simplify_factor=1.0,
        #    use_anim=True, use_anim_action_all=True,
        #    use_default_take=True,
        #    use_anim_optimize=True,
        #    anim_optimize_precision=6.0,
        #    path_mode='AUTO',
        #    embed_textures=False,
        #    batch_mode='OFF',
        #    use_batch_own_dir=True,
        #    use_metadata=True
        )

        time.sleep(0.3)

        bpy.ops.object.select_all(action='DESELECT')

        root.select_set(True)
        #bpy.context.view_layer.objects.active = child

        for o in hiddenObjects:
            o.hide_set(True)
            
        root.location.x = initial_root_location_x
        root.location.y = initial_root_location_y
        root.location.z = initial_root_location_z
        
        self.report({'INFO'}, "Export done ! (" + file_name + " -> " + directory + ")")

        return {'FINISHED'} # Lets Blender know the operator finished successfully.

def menu_func(self, context):
    self.layout.operator(OneKeyExport.bl_idname)

def register():
    bpy.utils.register_class(OneKeyExport)
    bpy.types.VIEW3D_MT_object.append(menu_func)  # Adds the new operator to an existing menu.

def unregister():
    bpy.utils.unregister_class(OneKeyExport)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
