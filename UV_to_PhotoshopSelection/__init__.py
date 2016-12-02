bl_info = {
    "name": "UV to Photoshop",
    "description": "選択したUV面をPhotoshopの選択範囲に",
    "author": "Yukimi",
    "version": (0,4),
    "blender": (2, 6, 0),
    "location": "image",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "http://yukimi-blend.blogspot.jp/",
    "category": "Import-Export"}

	
import bpy

if "bpy" in locals():
    import imp
    imp.reload(uv_to_photoshop)
else:
    from . import uv_to_photoshop

###################################################
class DupulicateActionAtCurrentTime(bpy.types.Operator):
	'''SelectedUV to Photoshop selection'''
	bl_idname = "action.uv_to_photoshop"
	bl_label = "SelectedUV to Photoshop selection"
	def execute(self, context):
		UV_to_photoshop(context)
		return {'FINISHED'}

# メニューの構築処理
def menu_func(self, context):
	self.layout.operator("action.uv_to_photoshop", 
		text="選択UVをPhotoshop選択範囲に" )
# アドオン有効化時の処理
def register():
	bpy.utils.register_module(__name__)
	bpy.types.IMAGE_MT_uvs.prepend(menu_func)
# アドオン無効化時の処理
def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.IMAGE_MT_uvs.remove(menu_func)

if __name__ == "__main__":
	register()
##########################################################