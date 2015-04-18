"""
レンダーレイヤ名と同じ名前でレンダリング画像をPNG出力
シーンが複数ある場合シーン毎にファイル出力ノードを作成

スクリプトを実行 または アドオンとして登録すると
ノードエディッタのノードメニューに "レンダーレイヤーノードツリーの作成" という項目が追加される

"""


bl_info = {
    "name": "Add Outpute Node to RenderLayer,respectively",
    "description": "レンダーレイヤーに対応したノード作成",
    "author": "Yukimi",
    "version": (0,2),
    "blender": (2, 6, 0),
    "location": "Node Editer",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Node"}


import bpy

#ノードの基準位置
node_origin = (0, 0)
#レンダーノードと出力ノードの距離
node_w_offset1 = 300
#レンダーノード同士の縦の距離
node_h_offset = 300

#レンダーノードのグループ毎の距離
node_w_offset2 = 500

#保存先の基本パス "//"はファイルと同一ディレクトリ
base_path ="//mov/"


#ノードツリーを作成
def make_node_tree(context):
	#ノードが表示されているスペースを取得
	space_data = get_node_spaces(context)[0]
	#スペースの表示をコンポジションノードに
	space_data.tree_type = 'CompositorNodeTree'
	
	#ノードを使用
	context.scene.use_nodes = True
	#コンポジションノードで使われてるノードツリーを取得
	nodetree = bpy.context.scene.node_tree
	
	
	for i,scene in enumerate(bpy.data.scenes):
		##シーン毎にアウトプットノードを作成
		#ノードの表示位置
		pos = [ node_origin[0] +node_w_offset1 + node_w_offset2 *i, node_origin[1] ]
		OF_Node = make_OF_Node(nodetree, scene.name, base_path,pos)
		
		#レンダーレイヤーの情報を取得
		layers = scene.render.layers
		for j, L in enumerate(layers):
			##レンダーレイヤのノード作成
			position = [ node_origin[0] +node_w_offset2 *i, node_origin[1] +node_h_offset *-j]
			RL_Node = meke_RL_Node(nodetree,scene, L, L.name, position)
			
			##ファイルアウトプットノードのスロットを追加
			#出力ファイルのパスを作成
			f_path = "%s/%s"%(L.name,L.name)
			F_Slot = OF_Node.file_slots.new(f_path)
			##ノード間をリンク
			nodetree.links.new(RL_Node.outputs[0], F_Slot)


#レンダーレイヤノードの作成
def meke_RL_Node( nodetree, RScene, RLayer, name, position ):
	RNode = nodetree.nodes.new('CompositorNodeRLayers')
	RNode.name = name
	RNode.location = (position)
	RNode.scene = RScene     #シーンの参照
	RNode.layer = RLayer.name#レンダーレイヤ名
	return(RNode)

#ファイルアウトプットノードの作成
def make_OF_Node(nodetree, name, base_path, position):
	FNode = nodetree.nodes.new('CompositorNodeOutputFile')
	FNode.name = name
	FNode.location = position
	FNode.base_path = base_path
	#初期設定の入力スロットを削除
	FNode.file_slots.remove(FNode.inputs[0])
	
	#8bitRGBAのPNGに設定
	FNode.format.color_depth = "8"
	FNode.format.color_mode = "RGBA"
	FNode.format.file_format = "PNG"
	return (FNode)
	
#ノードエディッタが表示されているスペースを取得
def get_node_spaces(context):
	for area in bpy.context.screen.areas:
		if area.type == "NODE_EDITOR":
			return (area.spaces)



###################interface############################
class addRenderLayerNode(bpy.types.Operator):
	'''Add a Node each as RenderLayer '''
	bl_idname = "node.render_layer_output"
	bl_label = "Add a Node each as RenderLayer"
	def execute(self, context):
		make_node_tree(context)
		return {'FINISHED'}

#メニュに追加する項目の設定
def menu_func(self, context):
	self.layout.operator("node.render_layer_output", text="レンダーレイヤーノードツリーの作成" )

def register():
	bpy.utils.register_module(__name__)
	bpy.types.NODE_MT_node.prepend(menu_func)# ノードエディッタの"ノード"メニューに項目を追加
	#bpy.types.NODE_MT_add.prepend(menu_func)# ノードエディッタの"追加"メニューに項目を追加

def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.NODE_MT_node.remove(menu_func)


##########################################################

if __name__ == "__main__":
	register()
