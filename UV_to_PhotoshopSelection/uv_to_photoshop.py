import bpy
import os
import subprocess
import time
import random
import bmesh


#実行するjavascriptの名前
js_name = "UV2Selection.jsx"
#このスクリプトのあるディレクトリのパス
mydoc_dir = os.path.dirname(__file__)
#実行するスクリプトのパス
VB_Hub = os.path.abspath(os.path.join(mydoc_dir, "VB_Hub.vbs"))
jscript = os.path.abspath(os.path.join(mydoc_dir, js_name))
#Blenderの一時ファイルのパス
tmp_dir = bpy.context.user_preferences.filepaths.temporary_directory

#UVの頂点の値を取得
def get_uvloop(loops, uv_layer):
    uv_list = [list(v[uv_layer].uv) for v in loops]
    return(uv_list)


#面が選択されているかの判別
def uv_face_selected(bm_face, uv_layer):
    #use_uv_select_sync = True の時の取得できる面とFalseの時に取得できる選択頂点は異なる
    if bpy.context.scene.tool_settings.use_uv_select_sync:
        #面の選択状態
        return( bm_face.select )
    else:
        #3Dビューの選択面とUVの選択が独立している場合
        if bm_face.select :
            l = len( bm_face.loops)
            i = 0
            #ループが全て選択されている面を判別
            for v in bm_face.loops:
                if v[uv_layer].select: i += 1
            return( i == l )
        else: return(False)
#UVで選択されている面の取得
def get_uv_list():
    #状態の更新
    bpy.context.edit_object.update_from_editmode()
    #選択形状のデータ
    mesh = bpy.context.active_object.data
    bm = bmesh.new()　　　　# 空の BMeshを作成
    bm.from_mesh(mesh)   # メッシュからBMeshを作成
    #アクティブなUV_layer(bmeshで使うにはUVlayerもBMeshオブジェクトでないといけない)
    uv_layer = bm.loops.layers.uv.active
    #選択UVの面データを取得
    uv_list = []
    for f in bm.faces:
        if uv_face_selected(f, uv_layer):
            #UVの頂点の値を取得
            vert_uv_list = get_uvloop(f.loops, uv_layer)
            uv_list.append(vert_uv_list)
    return(uv_list)
    
def UV_to_photoshop(context):
    #ファイル名の作成
    source_str = 'abcdefghijklmnopqrstuvwxyz'
    f_name = time.strftime("%y%m%d%H%M") + "".join([random.choice(source_str) for x in range(3)]) + ".txt"
    file_path  = os.path.join(txt_dir,f_name)
    #UVデータの取得
    txt = str(get_uv_list())
    #ファイルへの書き込み
    with open(file_path, "w") as f:
        f.write(txt)
        f.close
    #スクリプトの実行
    subprocess.call(["CScript", VB_Hub, jscript, img_path, "//nologo"])
