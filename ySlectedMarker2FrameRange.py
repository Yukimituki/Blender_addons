bl_info = {
	"name": "Slected Marker to frame range",
	"author": "Yukimi",
	"version": (1, 0),
	"blender": (2, 70, 0),
	"location": "Animation",
	"description": "set playback/rendering range from selected timeline_marker",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Animation"}

import bpy

#set selected makers range to playback/rendering range
def marker_to_renge(context):
	scene = context.scene
	selected_makers = []

	for m in scene.timeline_markers:
		if m.select:
			selected_makers.append(m.frame)
	
	selected_makers.sort()
	frame_start = selected_makers[ 0]
	frame_end   = selected_makers[-1] -1
	if scene.use_preview_range:
		scene.frame_preview_start = frame_start
		scene.frame_preview_end   = frame_end
	else:
		scene.frame_start = frame_start
		scene.frame_end   = frame_end


class MarkertoframerangeOperator(bpy.types.Operator):
	"""ToolTip of MarkertoframerangeOperator"""
	bl_idname = "addongen.marker_to_frame_range_operator"
	bl_label = "Selected marker to frame range"
	bl_options = {'REGISTER'}
	def execute(self, context):
		marker_to_renge(context)
		return {'FINISHED'}


def menu_func(self, context):
	self.layout.operator(MarkertoframerangeOperator.bl_idname)


def register():
	bpy.utils.register_class(MarkertoframerangeOperator)
	bpy.types.TIME_MT_marker.append(menu_func) #plase Timeline
	bpy.types.GRAPH_MT_marker.append(menu_func) #plase Graph editor
	bpy.types.DOPESHEET_MT_marker.append(menu_func) #plase DopeSheet
	bpy.types.NLA_MT_marker.append(menu_func) #plase NLA editor


def unregister():
	bpy.utils.unregister_class(MarkertoframerangeOperator)
	bpy.types.TIME_MT_marker.remove(menu_func) #plase Timeline
	bpy.types.GRAPH_MT_marker.remove(menu_func) #plase Graph editor
	bpy.types.DOPESHEET_MT_marker.remove(menu_func) #plase DopeSheet
	bpy.types.NLA_MT_marker.remove(menu_func) #plase NLA editor
    
if __name__ == "__main__":
	register()
