bl_info = {
    "name": "Add View Rotetion Empty",
    "author": "Yukimi",
    "version": (0,2),
    "blender": (2, 6, 0),
    "location": "View3D > Add ",
    "description": "Add a Empty as Cureent View Rotetion ",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"}

import bpy

#3DViewの軸に方向を合わせたEmptyを作成
def add_empty_axis():
	empty = bpy.data.objects.new('ViewAxis', None)
	space = bpy.context.area.spaces[0]#実行した画面の参照
	region = space.region_3d.view_rotation
	#エンプティの軸を3DViewの状態に合わせる
	ref_rotesion = empty.rotation_mode #回転モードの退避
	empty.rotation_mode = 'QUATERNION'
	empty.rotation_quaternion = region
	empty.rotation_mode = ref_rotesion
	
	empty.location = bpy.context.scene.cursor_location
	empty.empty_draw_type = 'ARROWS'
	empty.empty_draw_size = 0.1
	bpy.context.scene.objects.link(empty)


class AddEmptyAsViewAxis(bpy.types.Operator):
	'''Add a Empty as Cureent View Rotetion'''
	bl_idname = "empty.empty_view"
	bl_label = "Add Roteted Empty"
	bl_options = {'REGISTER', 'UNDO'}
	
	
	# Note: rotation in radians!
	
	def execute(self, context):
		add_empty_axis()
		return {'FINISHED'}

def menu_func(self, context):
	self.layout.operator("empty.empty_view", 
		text="ViewAxis" )


def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_add.prepend(menu_func)

def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.INFO_MT_add.remove(menu_func)

if __name__ == "__main__":
	register()



#add_empty_axis()