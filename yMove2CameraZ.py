bl_info = {
    "name": "move object/vertex to camera Plane",
    "description": "カメラのZ方向でオブジェクト/頂点を移動",
    "author": "Yukimi",
    "version": (0,2),
    "blender": (2, 6, 0),
    "location": "Objecr",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"}




import bpy
import math
import bmesh 

class ModalCmeraOperator(bpy.types.Operator):
	"""Move an object with the mouse, example"""
	bl_idname = "object.move_cameraplane"
	bl_label = "move to camera Z-plane"
	bl_options = {'REGISTER', 'UNDO'}
	
	ref_mouse_x = 0
	delta = 0
	ref_position = []
	v_camera_vec = []
	
	def execute(self, context):
		mode = context.mode
		M = self.delta * 0.01
		if  (mode == 'OBJECT'):
			bm = context.object.data
			for i,v in enumerate(bm.vertices):
				v.co.x = self.ref_position[i][0] + self.v_camera_vec[i][0]*M
				v.co.y = self.ref_position[i][1] + self.v_camera_vec[i][1]*M
				v.co.z = self.ref_position[i][2] + self.v_camera_vec[i][2]*M
		elif (mode == 'EDIT_MESH'):
			bm = bmesh.from_edit_mesh(context.edit_object.data)
			for i,v in enumerate( bm.verts ):
				if v.select:
					v.co.x = self.ref_position[i][0] + self.v_camera_vec[i][0]*M
					v.co.y = self.ref_position[i][1] + self.v_camera_vec[i][1]*M
					v.co.z = self.ref_position[i][2] + self.v_camera_vec[i][2]*M
			#bmesh.update_edit_mesh(bm, True)
			context.edit_object.data.update()
		return {'RUNNING_MODAL'}
	
	def modal(self, context, event):
		if  event.type == 'MOUSEMOVE':  # Apply
			self.delta = self.ref_mouse_x - event.mouse_x 
			self.execute(context)
		elif event.type == 'LEFTMOUSE':  # Confirm
			return {'FINISHED'}
		elif event.type in ('RIGHTMOUSE', 'ESC'):  # Cancel
			mode = context.mode
			if  (mode == 'OBJECT'):
				bm = context.object.data
				for i,v in enumerate(bm.vertices):
					v.co = self.ref_position[i]
			elif (mode == 'EDIT_MESH'):
				bm = bmesh.from_edit_mesh(context.edit_object.data)
				for i, v in enumerate( bm.verts ):
					v.co = self.ref_position[i]
				#bmesh.update_edit_mesh(bm, True)
				context.edit_object.data.update()
				#bm.free()
			return {'CANCELLED'}
		return {'RUNNING_MODAL'}
	def invoke(self, context, event):
		if context.object:
			self.ref_mouse_x = event.mouse_x
			#カメラの位置を取得
			camera_pos = bpy.context.area.spaces[0].camera.location
			#頂点の初期位置を取得
			ref_v = []
			vec_camera = []
			
			mode = context.mode
			if  (mode == 'OBJECT'):
				bm = context.object.data
				vertices = bm.vertices
			elif (mode == 'EDIT_MESH'):
				bm = bmesh.from_edit_mesh(context.edit_object.data)
				vertices = bm.verts
			for v in vertices:
				co = list(v.co)
				ref_v.append(co)
				co_w = context.object.matrix_world * v.co
				#カメラの座標をオブジェクト基準のベクターに
				#camera_pos_v = context.object.matrix_world * camera_pos
				d = []
				for i in range(3):
					d.append(co_w[i] - camera_pos[i])
				L = math.sqrt( d[0]**2 + d[1]**2 + d[2]**2 )
				vec_camera.append([d[0]/L, d[1]/L, d[2]/L])
			
			self.ref_position = ref_v
			self.v_camera_vec = vec_camera
			
			context.window_manager.modal_handler_add(self)
			
			return {'RUNNING_MODAL'}
		else:
			self.report({'WARNING'}, "No active object, could not finish")
			return {'CANCELLED'}


def register():
	bpy.utils.register_class(ModalCmeraOperator)


def unregister():
	bpy.utils.unregister_class(ModalCmeraOperator)


if __name__ == "__main__":
	register()
	# test call
	#bpy.ops.object.modal_operator('INVOKE_DEFAULT')