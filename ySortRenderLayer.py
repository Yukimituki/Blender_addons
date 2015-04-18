bl_info = {
    "name": "sort renderlayer list",
    "description": "レンダーレイヤの順序入れ替え",
    "author": "Yukimi",
    "version": (0,2),
    "blender": (2, 6, 0),
    "location": "property",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "object"}


import bpy

#レンダーレイヤノードの作成
def meke_RL_Node( nodetree, RScene, RLayer, name, position ):
	RNode = nodetree.nodes.new('CompositorNodeRLayers')
	RNode.name = name
	RNode.location = (position)
	RNode.scene = RScene     #シーンの参照
	RNode.layer = RLayer.name#レンダーレイヤ名
	return(RNode)

#ノードの接続の入れ替え
def switch_render_node(context, layer1, layer2):
	node_tree = context.scene.node_tree
	L1 = []
	L2 = []
	for L in node_tree.links:
		if L.from_node.layer == layer1.name:
			position = list(L.from_node.location)
			from_socket = L.from_socket
			to_socket = L.to_socket
			L1.append([L.from_node,position, from_socket.name, to_socket])
			node_tree.links.remove(L)
		elif L.from_node.layer == layer2.name:
			position = list(L.from_node.location)
			from_socket = L.from_socket
			to_socket = L.to_socket
			L2.append([L.from_node,position, from_socket.name, to_socket])
			node_tree.links.remove(L)
	from_node1 = ""
	from_node2 = ""
	#レンダーレイヤノードを検索（ノードがつながってない場合があるため）
	for n in node_tree.nodes:
		if n.type == 'R_LAYERS' and n.layer == layer1.name:
			from_node1 = n
		elif n.type == 'R_LAYERS' and n.layer == layer2.name:
			from_node2 = n
	if not from_node2:
		from_node2 = meke_RL_Node( node_tree, context.scene, layer2, layer2.name , (0,0))
	for L in L1:
		from_socket = from_node2.outputs[ L[2] ]
		to_socket = L[3]
		node_tree.links.new(from_socket,to_socket)
		from_node2.location = L[1]
	if not from_node1:
		from_node1 = meke_RL_Node( node_tree, context.scene, layer1, layer1.name , (0,0))
	for L in L2:
		from_socket = from_node1.outputs[ L[2] ]
		to_socket = L[3]
		node_tree.links.new(from_socket,to_socket)
		from_node1.location = L[1]


#レンダーレイヤの順序の入れ替え
def replace_renderLayers(layer1,layer2):
	ref1 = [layer1.name, list(layer1.layers), list(layer1.layers_zmask), layer1.use]
	ref2 = [layer2.name, layer2.layers, layer2.layers_zmask, layer2.use]
	layer2.name = "_____temporary name______"
	[layer1.name, layer1.layers, layer1.layers_zmask, layer1.use] = ref2
	[layer2.name, layer2.layers, layer2.layers_zmask, layer2.use] = ref1

def render_layer_up(context):
	render_layers = context.scene.render.layers
	layer_count = len(render_layers)
	active_index = render_layers.active_index
	if active_index >= 1:
		active_layer = render_layers[active_index]
		rep_layer = render_layers[active_index -1]
		#入れ替え処理
		switch_render_node(context,active_layer, rep_layer)
		replace_renderLayers(active_layer, rep_layer)
	#アクティブなレイヤの入れ替え
	render_layers.active_index = active_index -1

def render_layer_down(context):
	#下に
	render_layers = context.scene.render.layers
	layer_count = len(render_layers)
	active_index = render_layers.active_index
	if active_index < layer_count -1:
		active_layer = render_layers[active_index]
		rep_layer = render_layers[active_index +1]
		#入れ替え処理
		switch_render_node(context,active_layer, rep_layer)
		replace_renderLayers(active_layer, rep_layer)
	render_layers.active_index = active_index +1


class renderlayerdown(bpy.types.Operator):
	'''    set activestrip to preview '''
	bl_idname = "scene.render_layer_up"
	bl_label = "move up render layer on list"
	def execute(self, context):
		render_layer_up(context)
		return {'FINISHED'}

class renderlayerup(bpy.types.Operator):
	'''    set activestrip to preview '''
	bl_idname = "scene.render_layer_down"
	bl_label = "move down render layer on list"
	def execute(self, context):
		render_layer_down(context)
		return {'FINISHED'}

def register():
	bpy.utils.register_module(__name__)

def unregister():
	bpy.utils.unregister_module(__name__)

##########################################################

if __name__ == "__main__":
	register()
