bl_info = {
    "name": "Add Empty Mesh Object",
    "author": "Yukimi",
    "version": (0,2),
    "blender": (2, 6, 0),
    "location": "View3D > Add > Mesh",
    "description": "Adds Meshobject as Empty mesh ",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"}

import bpy, math

def addEmptyMesh():
	mesh = bpy.data.meshes.new("EmpMesh")
	obj = bpy.data.objects.new("EmpMesh",mesh)
	obj.location = bpy.context.scene.cursor_location   # オブジェクトを 3D カーソルの位置に
	bpy.context.scene.objects.link(obj)                        # オブジェクトをシーンにリンク
	bpy.context.scene.objects.active = obj
	return obj

#
#    User interface
#

from bpy.props import *

class MESH_OT_primitive_twisted_cylinder_add(bpy.types.Operator):
	'''Add a twisted cylinder'''
	bl_idname = "mesh.empty_mesh_add"
	bl_label = "Add Empty Mesh Object"
	bl_options = {'REGISTER', 'UNDO'}
	
	
	# Note: rotation in radians!
	
	def execute(self, context):
		bpy.ops.object.select_all(action='DESELECT')
		ob = addEmptyMesh()
		context.scene.objects.active = ob
		bpy.ops.object.mode_set(mode='EDIT')
		return {'FINISHED'}
 
#
#    Registration
#    Makes it possible to access the script from the Add > Mesh menu
#


def menu_func(self, context):
	self.layout.operator("mesh.empty_mesh_add", 
		text="EmptyMesh", 
		icon='MESH_TORUS')

def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_mesh_add.prepend(menu_func)

def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.INFO_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
	register()