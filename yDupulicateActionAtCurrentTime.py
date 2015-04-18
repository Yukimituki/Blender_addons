bl_info = {
    "name": "dupulicate action at cusor",
    "description": "選択したコントロールポイントを現在のカーソル基準に複製",
    "author": "Yukimi",
    "version": (0,2),
    "blender": (2, 6, 0),
    "location": "Doop seet",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Animetion"}

import bpy


def copy_at_cusor(context):
	current_time = context.scene.frame_current
	action = context.active_object.animation_data.action
	if "fcurves" not in dir(action): return()
	#選択されたポイントの中で一番先頭の物の時間を求める
	offset = 80000
	for fcurve in action.fcurves:
		for p in fcurve.keyframe_points:
			if p.select_control_point:
				if p.co[0] < offset:
					offset = p.co[0]
	
	#カレントフレームを基準にしてキーフレームを挿入
	for fcurve in action.fcurves:
		points = []
		for p in fcurve.keyframe_points:
			if not p.select_control_point:continue
			points.append(p.co)
		for p in points:
			t = p[0] - offset + current_time
			fcurve.keyframe_points.insert(frame = t, value = p[1])
	#画面の更新への対策
	context.scene.frame_set(context.scene.frame_current)

#アンピンドされた状態でのコピペはNALストリップ移動前の座標になる
#NLAの移動や拡大縮小のデータを取得する必要あり

def copy_at_strip(context):
	current_time = context.scene.frame_current
	action = context.active_object.animation_data.action
	#参照元のNLAストリップを調べる
	active_track = context.active_object.animation_data.nla_tracks.active
	if active_track == "":return()
	for strip in active_track.strips:
		if strip.active:
			active_strip = strip
	#ストリップの情報を取得
	frame_start = strip.frame_start
	action_frame_start = strip.action_frame_start
	#action_frame_end = strip.action_frame_end
	
	time_offset = action_frame_start + (current_time - frame_start)/strip.scale
	
	#選択されたポイントの中で一番先頭の物の時間を求める
	CP_offset = 80000
	for fcurve in action.fcurves:
		for p in fcurve.keyframe_points:
			if p.select_control_point:
				if p.co[0] < CP_offset:
					CP_offset = p.co[0]
	
	#カレントフレームを基準にしてキーフレームを挿入
	for fcurve in action.fcurves:
		points = []
		for p in fcurve.keyframe_points:
			if not p.select_control_point:continue
			points.append(p.co)
		for p in points:
			t = p[0] - CP_offset + time_offset
			fcurve.keyframe_points.insert(frame = t, value = p[1])
	#画面の更新への対策
	context.scene.frame_set(context.scene.frame_current)



###################################################
class DupulicateActionAtCurrentTime(bpy.types.Operator):
	'''add Roop  '''
	bl_idname = "action.dup_keyframe"
	bl_label = "copy action at current time"
	def execute(self, context):
		if context.scene.is_nla_tweakmode:
			copy_at_strip(context)
		else:
			copy_at_cusor(context)
		return {'FINISHED'}


def menu_func(self, context):
	self.layout.operator("action.dup_keyframe", 
		text="カーソル位置にコピー" )

def register():
	bpy.utils.register_module(__name__)
	bpy.types.DOPESHEET_MT_key.prepend(menu_func)

def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.DOPESHEET_MT_key.remove(menu_func)

if __name__ == "__main__":
	register()
##########################################################