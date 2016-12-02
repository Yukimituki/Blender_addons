Option Explicit
'（VBScriptは'がコメント）
'コマンドプロンプト上でのVBScriptの実行はCScriptにスペース区切りの引数
'第一引数で実行するjavascriptを実行　以降をjavascriptに渡す
'変数の宣言をしないとエラーになる　注意

'コマンドライン引数の取得
Dim oParam
Set oParam = WScript.Arguments
'Photoshopを指定
Dim objApp
Set objApp = CreateObject("Photoshop.Application")

Dim arg_count
arg_count = oParam.Count -1 
'WScript.Echo arg_count

If arg_count = 0 Then
    '追加の引数がない場合
    objApp.DoJavaScriptFile oParam(0)
Else
    Dim id
	'引数をjavascriptに渡すための配列
    Dim ArgArray()
	ReDim ArgArray(arg_count - 1  )
    '第一引数がスクリプトのパスのため取り除く
    For id = 0 To arg_count - 1
        ArgArray(id) = oParam(id + 1)
    Next
    ''スクリプトの実行
    objApp.DoJavaScriptFile oParam(0),ArgArray
End If
'Dim script_path = "C:\Users\moonstone\Documents\TempItems\" + oParam(0)
'Dim args(1)
'args(0) = oParam(1)
'objApp.DoJavaScriptFile oParam(0), args

'Pythonからのコマンド実行例
'import subprocess
'subprocess.call("CScript C:/Users/moonstone/Documents/TempItems/tast-vbs.vbs")
'または(戻り値が表示される)
'print subprocess.check_output("CScript C:/Users/moonstone/Documents/TempItems/tast-vbs.vbs")