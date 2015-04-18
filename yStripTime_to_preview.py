bl_info = {
    "name": "set activeStripTime to preview",
    "description": "アクティブなストリップの範囲をプレビュー範囲に設定",
    "author": "Yukimi",
    "version": (0,2),
    "blender": (2, 6, 0),
    "location": "NLA",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Animetion"}

import bpy

def Striptime_to_preview(context):
	active_track = context.active_object.animation_data.nla_tracks.active
	if active_track == "":return()
	for strip in active_track.strips:
		if strip.active:
			active_strip = strip
	if active_strip == "":return()
	#ストリップの情報を取得
	frame_start = strip.frame_start
	frame_end = strip.frame_end
	repeat = strip.repeat
	#リピートの一回目のみをプレビュー
	context.scene.frame_preview_start = frame_start
	context.scene.frame_preview_end = frame_start + int(( frame_end - frame_start)/ repeat) -1
	context.scene.use_preview_range = True


###################################################
class SetActiveStripTimeToPreview(bpy.types.Operator):
	'''    set activestrip to preview '''
	bl_idname = "action.striptime_to_preview"
	bl_label = "set activeStripTime to preview"
	def execute(self, context):
		Striptime_to_preview(context)
		return {'FINISHED'}


def menu_func(self, context):
	self.layout.operator("action.striptime_to_preview", 
		text="ストリップをプレビュー範囲に" )

def register():
	bpy.utils.register_module(__name__)
	bpy.types.NLA_MT_select.prepend(menu_func)

def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.NLA_MT_select.remove(menu_func)

if __name__ == "__main__":
	register()