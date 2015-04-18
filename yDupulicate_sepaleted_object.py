bl_info = {
    "name": "Dupulcate Sepaleted Object",
    "description": "Adds Meshobject as Empty mesh ",
    "author": "Yukimi",
    "version": (0,2),
    "blender": (2, 6, 0),
    "location": "View3D > Add > Mesh",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"}

import bpy

#
#    User interface
#

from bpy.props import *

class Dupulicate_sepaleted_object(bpy.types.Operator):
	bl_idname = "object.dupulicate_object"
	bl_label = "別形状で複製"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		duplcate_object()
		return {'FINISHED'}


def menu_func(self, context):
	self.layout.operator(Dupulicate_sepaleted_object.bl_idname, text=Dupulicate_sepaleted_object.bl_label)

def register():
	bpy.utils.register_module(__name__)
	#メニューへの追加位置を指定	
	bpy.types.VIEW3D_MT_object.append(menu_func)       #オブジェクトメニュー
	bpy.types.VIEW3D_MT_edit_mesh.append(menu_func)    #エディットメッシュモードのメッシュメニュー
	bpy.types.VIEW3D_MT_edit_armature.append(menu_func)#エディットアーマチュアモードのアーマーチュアメニュー

def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.VIEW3D_MT_object	.remove(menu_func)






def duplcate_object():
	#現在の編集モードを取得
	mode = bpy.context.mode
	if  (mode == 'OBJECT'):
		bpy.ops.object.duplicate()
	elif (mode == 'EDIT_MESH'):
		#複製
		bpy.ops.mesh.duplicate() 
		#選択している頂点を別オブジェクトに分離
		bpy.ops.mesh.separate(type='SELECTED')
		#オブジェクトモードに
		bpy.ops.object.mode_set(mode='OBJECT')
		#複製したオブジェクトを選択
		objects = bpy.context.selected_objects
		bpy.ops.object.select_all(action='DESELECT')
		bpy.context.scene.objects.active = objects[0]
		bpy.ops.object.mode_set(mode='EDIT')
	elif (mode == 'EDIT_ARMATURE'):
		bpy.ops.armature.duplicate()
		bpy.ops.armature.separate()
		#オブジェクトモードに
		bpy.ops.object.mode_set(mode='OBJECT')
		#複製したオブジェクトを選択
		objects = bpy.context.selected_objects
		bpy.ops.object.select_all(action='DESELECT')
		bpy.context.scene.objects.active = objects[0]
		bpy.ops.object.mode_set(mode='EDIT')


if __name__ == "__main__":
	register()