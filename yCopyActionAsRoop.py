bl_info = {
    "name": "copy action as roop around preview area",
    "description": "選択したコントロールポイントをプレビュー範囲の前後にコピー",
    "author": "Yukimi",
    "version": (0,2),
    "blender": (2, 6, 0),
    "location": "Doop seet",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Animetion"}


import bpy

##ループ作成（選択されていない形状のものもループさせてしまうバグアリ）
def copy_as_roop_bug(context):
	#プレビューのスタートフレーム
	start = context.scene.frame_preview_start
	end = context.scene.frame_preview_end
	frame_length = end - start + 1
	actions = bpy.data.actions #シーン内の全てのアクションを調べてしまう
	for ac in actions:
		for fcurve in ac.fcurves:
			points = []
			for p in fcurve.keyframe_points:
				if not p.select_control_point:continue
				points.append(p.co)
			#ループの前方向にポイントを追加
			for p in points:
				t = p[0] - frame_length
				fcurve.keyframe_points.insert(frame = t, value = p[1])
			for p in points:
				t = p[0] + frame_length
				fcurve.keyframe_points.insert(frame = t, value = p[1])
	#画面の更新への対策
	context.scene.frame_set(context.scene.frame_current)


##ループ作成
def copy_as_roop(context):
	start = context.scene.frame_preview_start
	end = context.scene.frame_preview_end
	frame_length = end - start + 1
	action = context.active_object.animation_data.action
	if "fcurves" not in dir(action): return()	
	for fcurve in action.fcurves:
		points = []
		for p in fcurve.keyframe_points:
			if not p.select_control_point:continue
			points.append(p.co)
		#ループの前方向にポイントを追加
		for p in points:
			t = p[0] - frame_length
			fcurve.keyframe_points.insert(frame = t, value = p[1])
		for p in points:
			t = p[0] + frame_length
			fcurve.keyframe_points.insert(frame = t, value = p[1])
	#画面の更新への対策
	context.scene.frame_set(context.scene.frame_current)



###################################################
class CopyActionAsRoop(bpy.types.Operator):
	'''add Roop  '''
	bl_idname = "action.roopcopy"
	bl_label = "copy action as roop around preview area"
	def execute(self, context):
		copy_as_roop(context)
		return {'FINISHED'}


def menu_func(self, context):
	self.layout.operator("action.roopcopy", 
		text="プレビュー範囲の前後にコピー" )

def register():
	bpy.utils.register_module(__name__)
	bpy.types.DOPESHEET_MT_key.prepend(menu_func)

def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.DOPESHEET_MT_key.remove(menu_func)

if __name__ == "__main__":
	register()
##########################################################

