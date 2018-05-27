#target photoshop;

//ファイルの読み込み
var obj_file =  File(arguments[0]);
//指定したファイルから3Dレイヤを作成
// =======================================================
var idaddthreeDLayerFromFile = stringIDToTypeID( "add3DLayerFromFile" );
    var desc10 = new ActionDescriptor();
    var idfileList = stringIDToTypeID( "fileList" );
        var list1 = new ActionList();
        list1.putPath( obj_file );
    desc10.putList( idfileList, list1 );
executeAction( idaddthreeDLayerFromFile, desc10, DialogModes.NO );