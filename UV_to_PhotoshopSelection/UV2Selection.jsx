#target photoshop;
#include "json2.js";

//ドキュメントの設定を退避
var refRulerUnits = app.preferences.rulerUnits;
var refTypeUnits = app.preferences.typeUnits;
var refDisplayDialogs = app.displayDialogs;
//画像の単位をピクセルに
app.preferences.rulerUnits = Units.PIXELS;
app.preferences.typeUnits = TypeUnits.PIXELS;
app.displayDialogs = DialogModes.NO;

//ファイルの読み込み
var txt_file =  File(arguments[0]);
var txt = load_text(txt_file);
//jsonでパース
var layoutJson = JSON.parse(txt);
for(var i =0 ; i < layoutJson.length; i++){
    //選択範囲の作成
    uv2selection(layoutJson[i])
}
//選択範囲に細かい隙間ができるため補正
adjustLevelsSelection()
//ドキュメント設定を書き戻す
app.preferences.rulerUnits = refRulerUnits;
app.preferences.typeUnits = refTypeUnits;
app.displayDialogs = refDisplayDialogs;

//UVデータから選択範囲の作成
function uv2selection(uv_list){
    var point_list = new Array()
    width = activeDocument.width
    height = activeDocument.height
    for(var i = 0; i < uv_list.length; i++){
        var pos_x = uv_list[i][0] * width
        var pos_y = (1 - uv_list[i][1])  * height
        point_list.push( [pos_x, pos_y] )
        }
    //選択範囲を追加
    activeDocument.selection.select(point_list, SelectionType.EXTEND)
    }

//テキストファイルの読み込み
function load_text(f_path){ 
    if (f_path){
        fileObj = new File(f_path);
        flag= fileObj.open("r");
        if (flag == true){
            var text = fileObj.read();
            fileObj.close();  
			}
		else{
            alert("ファイルが開けませんでした");
			}
		}
    return(text)
	}

//多角形選択で隙間ができるものを補正
function adjustLevelsSelection(){
    //クイックマスクモード
    // =======================================================
    var idsetd = charIDToTypeID( "setd" );
        var desc1 = new ActionDescriptor();
        var idnull = charIDToTypeID( "null" );
            var ref1 = new ActionReference();
            var idPrpr = charIDToTypeID( "Prpr" );
            var idQucM = charIDToTypeID( "QucM" );
            ref1.putProperty( idPrpr, idQucM );
            var idDcmn = charIDToTypeID( "Dcmn" );
            var idOrdn = charIDToTypeID( "Ordn" );
            var idTrgt = charIDToTypeID( "Trgt" );
            ref1.putEnumerated( idDcmn, idOrdn, idTrgt );
        desc1.putReference( idnull, ref1 );
    executeAction( idsetd, desc1, DialogModes.NO );
    //レベル補正
    // =======================================================
    var idLvls = charIDToTypeID( "Lvls" );
        var desc2 = new ActionDescriptor();
        var idpresetKind = stringIDToTypeID( "presetKind" );
        var idpresetKindType = stringIDToTypeID( "presetKindType" );
        var idpresetKindCustom = stringIDToTypeID( "presetKindCustom" );
        desc2.putEnumerated( idpresetKind, idpresetKindType, idpresetKindCustom );
        var idAdjs = charIDToTypeID( "Adjs" );
            var list5 = new ActionList();
                var desc3 = new ActionDescriptor();
                var idChnl = charIDToTypeID( "Chnl" );
                    var ref2 = new ActionReference();
                    var idChnl = charIDToTypeID( "Chnl" );
                    var idOrdn = charIDToTypeID( "Ordn" );
                    var idTrgt = charIDToTypeID( "Trgt" );
                    ref2.putEnumerated( idChnl, idOrdn, idTrgt );
                desc3.putReference( idChnl, ref2 );
                var idInpt = charIDToTypeID( "Inpt" );
                    var list6 = new ActionList();
                    list6.putInteger( 60 );
                    list6.putInteger( 255 );
                desc3.putList( idInpt, list6 );
            var idLvlA = charIDToTypeID( "LvlA" );
            list5.putObject( idLvlA, desc3 );
        desc2.putList( idAdjs, list5 );
    executeAction( idLvls, desc2, DialogModes.NO );
    //クイックマスク解除
    // =======================================================
    var idCler = charIDToTypeID( "Cler" );
        var desc4 = new ActionDescriptor();
        var idnull = charIDToTypeID( "null" );
            var ref3 = new ActionReference();
            var idPrpr = charIDToTypeID( "Prpr" );
            var idQucM = charIDToTypeID( "QucM" );
            ref3.putProperty( idPrpr, idQucM );
            var idDcmn = charIDToTypeID( "Dcmn" );
            var idOrdn = charIDToTypeID( "Ordn" );
            var idTrgt = charIDToTypeID( "Trgt" );
            ref3.putEnumerated( idDcmn, idOrdn, idTrgt );
        desc4.putReference( idnull, ref3 );
    executeAction( idCler, desc4, DialogModes.NO );
    }