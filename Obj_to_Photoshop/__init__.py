bl_info = {
    "name": "3D Object to Photoshop",
    "description": "選択形状をPhotoshopの3Dレイヤに",
    "author": "Yukimi",
    "version": (0,4),
    "blender": (2, 6, 0),
    "location": "object",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "http://yukimi-blend.blogspot.jp/",
    "category": "Import-Export"}
 
import bpy
from io_scene_obj import export_obj
from bpy_extras.io_utils import axis_conversion

import os
import subprocess
import time
import random


#実行するjavascriptの名前
js_name = "Add3DLayerFromFile.jsx"
#このスクリプトのあるディレクトリのパス
mydoc_dir = os.path.dirname(__file__)
#実行するスクリプトのパス
VB_Hub = os.path.abspath(os.path.join(mydoc_dir, "VB_Hub.vbs"))
jscript = os.path.abspath(os.path.join(mydoc_dir, js_name))
#Blenderの一時ファイルディレクトリを利用する場合
tmp_dir = bpy.context.user_preferences.filepaths.temporary_directory
#ファイルの書き出し先をデスクトップにしたい場合は↓をコメントアウト
#tmp_dir = os.path.join(os.getenv("HOMEDRIVE"), os.getenv("HOMEPATH") , "Desktop")

def obj_to_photoshop(context):
    #ファイル名の作成
    source_str = 'abcdefghijklmnopqrstuvwxyz'
    f_name = time.strftime("%y%m%d%H%M") + "".join([random.choice(source_str) for x in range(3)]) + ".obj"
    obj_path  = os.path.join(tmp_dir,f_name)
    #Objデータの出力
    scale = 1.0
    obj_export(scale, obj_path)
    #javascriptの実行
    subprocess.call(["CScript", VB_Hub, jscript, obj_path, "//nologo"])

def obj_export(scale, obj_path):
    if len(bpy.context.selected_objects) == 0: return()
    from mathutils import Matrix
    global_matrix = (Matrix.Scale(scale, 4) *
                     axis_conversion(to_forward= '-Z',
                                     to_up='Y',
                                     ).to_4x4())
    export_obj.save(bpy.context,
                         filepath      = obj_path,
                         global_matrix = global_matrix,
                         use_triangles = True,
                         use_selection = True,
                         path_mode     = 'STRIP')




###################################################
class DupulicateActionAtCurrentTime(bpy.types.Operator):
    '''selected 3D Object to Photoshop 3D Layer'''
    bl_idname = "action.obj_to_photoshop"
    bl_label = "3D Object to Photoshop 3D Layer"
    def execute(self, context):
         obj_to_photoshop(context)
         return {'FINISHED'}
# メニューの構築処理
def menu_func(self, context):
    self.layout.operator("action.obj_to_photoshop", 
           text="選択形状をPhotoshopへ" )
# アドオン有効化時の処理
def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_object.prepend(menu_func)
# アドオン無効化時の処理
def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
 
if __name__ == "__main__":
    register()
##########################################################