# Blender_addons
これらは自分が仕事の作業で個人的に作ったBlnenderのアドオンです  
細かい調整はあまりしていないのでその点はご注意ください  

## モデリング関連
* yAdd_empty_mesh_object  
Addメニューのメッシュ項目にEmptyMeshという項目を追加して  
何も頂点が含まれないメッシュオブジェクトを作成します。  
何もないところから頂点を打つ時に既存のメッシュの頂点を消去する作業がなくなります   
メッシュ編集モードにもAddメニューに現れてしまいますが　エラーで動作しません  

* yAdd_View_Rotation_Empty  
AddメニューにViewAxisという項目を追加して  
現在の３Ｄビューを基準にしたエンプティオブジェクトを作成します。  
ビューの回転状態を保存したり(Shift+7)現在の回転状態と垂直な方向(Shift+1,Shift+3)から見たい場合に使えます  


* yMove2CameraZ  
カメラから見た奥行方向に向けて  
カメラビューでの形状をいじしたまま頂点を移動します  
オブジェクトモードでも不正な形で動いてしまいます  
また、オブジェクト自体の移動回転等の変形がかかってると意図しない動きになります  

* yDupulicate_sepaleted_object  
メッシュ編集モードで選択している頂点を別形状として複製します  
（Shift+D の後Pを押す流れと同じです）  


## アニメーション関連  

* yAdd_renderlayer_nodetree  
レンダーレイヤーの一つ一つに対応したファイル出力ノードを作成します  
出力ディレクトリ名とファイル名はレンダーレイヤーの名前を使用します  
アニメーションでセッティングを変えた差分ファイルを多数出力するために作成  

* yCopyActionAsRoop  
選択しているキーフレームをプレビュー範囲の前後にコピペします  
一定範囲で確実にアニメーションがループしてほしい場合に使用します  
（もっと賢い方法があるのかもしれませんが標準機能でうまくいかなかったので作成）  　


* yDupulicateActionAtCurrentTime  
選択したキーフレームをカレントフレームを基準にペーストしま  
NLAエディッタで時間軸を移動していると　通常の操作では意図しない位置にペーストされるために作成  

* ySlectedMarker2FrameRange  
タイムライン上の選択されたマーカーの両端をレンダリング範囲にします  
時間的な部分毎にレンダリングをやり直すことが多かったために作成  

* ySortRenderLayer  
レンダーレイヤーの表示の上下を入れ替えることができないので  
レンダーレイヤー設定と名前を上下入れ替え  
上記の出力ノードも併用しているために　ノードの出力も入れ替えるように作成  
ノードがない阿合の処理を書いていないためにノードの接続がないとエラーが出ます  　

* yStripTime_to_preview  
NLAエディッタで選択しているストリップをプレビュー範囲に設定します  
ストリップに繰り返しが設定されている場合　繰り返しの前までが範囲になります  
