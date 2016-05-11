// ==SiteScript==
// @siteName    VideoWood.tv
// @siteUrl     http://videowood.tv/
// @author      mayan
// @authorUrl   
// @scriptUrl   
// @description 
// @date        2016/04/13
// @version     0.2
// ==/SiteScript==


function CravingSiteScript() {
    this._initialize();
}


CravingSiteScript.prototype = {
    _xhr: null,
    
    _initialize: function() {},
    
    _getXmlHttpRequest: function() {
        if ( this._xhr != null ) {
            return this._xhr;
        }
        
        var xhr = null;
        var these = [
              function() { return new XMLHttpRequest(); }
            , function() { return new ActiveXObject( "Msxml2.XMLHTTP" ); }
            , function() { return new ActiveXObject( "Microsoft.XMLHTTP" ); }
            , function() { return new ActiveXObject( "Msxml2.XMLHTTP.4.0" ); }
        ];
        
        for ( var i = 0, length = these.length; i < length; i++ ) {
            var func = these[ i ];
            try {
                xhr = func();
                break;
            }
            catch( e ) {}
        }
        this._xhr = xhr;
        
        return this._xhr;
    },
    
    _load: function( url, data, method ) {
        var req = this._getXmlHttpRequest();
        
        var mtd = ( method == null ) ? "GET" : "POST";
        
        req.open( mtd, url, false );
        
        if ( mtd == "POST" ) {
            req.setRequestHeader( "Content-Type", "application/x-www-form-urlencoded" );
        }
        
        req.send( data );
        
        return req.responseText;
    },
    
    getResponseText: function( url, data, method ) {
        return this._load( url, data, method );
    },
    
    getResponseJSON: function( url, data, method ) {
        var text = this._load( url, data, method );
        
        return eval( "("+text+")" );
    },
    
    /// Math
    random: function( limit ) {
        return Math.floor( Math.random() * limit );
    },
    
    /// String
    decodeHtml: function( str ) {
        return str.replace( /&(quot|#0*34);/ig,    "\"" )
                  .replace( /&(amp|#0*38);/ig,     "&"  )
                  .replace( /&(apos|#0*39);/ig,    "'"  )
                  .replace( /&(lt|#0*60);/ig,      "<"  )
                  .replace( /&(gt|#0*62);/ig,      ">"  )
                  .replace( /&(nbsp|#0*160);/ig,   " "  )
                  .replace( /&(frasl|#8260);/ig, "/"  );
    }
}


function isSiteUrl( url ) {
    if ( url.match( /http:\/\/(?:www\.)?videowood\.tv\/video\/[^\/?&#]+/ ) ) return true;
    if ( url.match( /http:\/\/(?:www\.)?videowood\.tv\/embed\/[^\/?&#]+/ ) ) return true;
    
    return false;
}


function getVideoDetail( url ) {
    
    if ( url.match( /http:\/\/(?:www\.)?videowood\.tv\/(?:video|embed)\/([^\/?&#]+)/ ) ) {
        var vid = RegExp.$1;
    } else {
        return null;
    }
    
    if ( !vid ) return null;
    var embedurl = "http://videowood.tv/embed/" + vid;
    var craving = new CravingSiteScript();
    try {
        var text = craving.getResponseText( embedurl );
    } catch( e ) {
        text = "";
    }
    if ( !text ) return null;
    
    if ( text.match( /<div\s+[^>]*?class\s*=\s*("|')?videotitle\1[^>]*>\s*<span(?:\s+[^>]*)?>\s*(.*?)\s*<\/span\s*>/im ) ) {
        var title = craving.decodeHtml( RegExp.$2 );
    }
    
    var realUrl = "";
    var objReg = /\(\s*ﾟДﾟ\s*\)\s*\[\s*'_'\s*\]\s*(\(\s*\(\s*ﾟДﾟ\s*\)\s*\[\s*'_'\s*\]\s*\([\s\S]+?\(\s*ﾟΘﾟ\s*\)\s*\))\s*\(\s*'_'\s*\)\s*;/gm;
    while ( objReg.test( text ) ) {
        var dec = decodeHtJs( RegExp.$1 );
        if ( !dec ) continue;
        realUrl = "";
        dec = dec.replace( /\\"/g, "\"" ).replace( /\\\//g, "/" );
        if ( dec.match( /window\.\w+\s*=\s*'([^']+)'/m ) ||
             dec.match( /window\.\w+\s*=\s*"([^"]+)"/m )    ) {
            realUrl = RegExp.$1;
            if ( realUrl.match( /^\s*https?:\/\/.+/ ) ) break;
        }
    }
    
    if ( !realUrl ) return null;
    if ( !title ) title = "videowood_" + vid;
    title = title.replace(/[\\\/:*?"<>|]/g, "_");
    
    return { videoTitle0: title, videoUrl0: realUrl };
}


function decodeHtJs( str ) {
    //2015/10/01
    var code = 'var ﾟωﾟﾉ=undefined,o=3,ﾟｰﾟ=4,_=3,c=0,ﾟΘﾟ=1,'
            + 'ﾟoﾟ="constructor",ﾟεﾟ="return",oﾟｰﾟo="u",'
            + 'ﾟДﾟ={"1":"f",ﾟΘﾟ:"_",ﾟωﾟﾉ:"a",ﾟｰﾟﾉ:"d",ﾟДﾟﾉ:"e",c:"c",o:"o","return":"\\\\",ﾟΘﾟﾉ:"b","constructor": "\\"",_: Function};';
    var rtn = "";
    try {
        rtn = new Function( code + "var a=" + str + ";return a;" )();
    } catch ( e ) {
        rtn = "";
    }
    if ( typeof rtn != "string" && !(rtn instanceof String) ) rtn = "";
    
    return rtn;
}

function getVideoDetail2(path)
{    
    var craving = new CravingSiteScript();
 
   try {
        var text = readFile(path);
    } catch( e ) {
        text = "";
    }
    if ( !text ) return null;
    
    if ( text.match( /<div\s+[^>]*?class\s*=\s*("|')?videotitle\1[^>]*>\s*<span(?:\s+[^>]*)?>\s*(.*?)\s*<\/span\s*>/im ) ) {
        var title = craving.decodeHtml( RegExp.$2 );
    }
    
    var realUrl = "";
    var objReg = /\(\s*ﾟДﾟ\s*\)\s*\[\s*'_'\s*\]\s*(\(\s*\(\s*ﾟДﾟ\s*\)\s*\[\s*'_'\s*\]\s*\([\s\S]+?\(\s*ﾟΘﾟ\s*\)\s*\))\s*\(\s*'_'\s*\)\s*;/gm;
    while ( objReg.test( text ) ) {
        var dec = decodeHtJs( RegExp.$1 );
        if ( !dec ) continue;
        realUrl = "";
        dec = dec.replace( /\\"/g, "\"" ).replace( /\\\//g, "/" );
        if ( dec.match( /window\.\w+\s*=\s*'([^']+)'/m ) ||
             dec.match( /window\.\w+\s*=\s*"([^"]+)"/m )    ) {
            realUrl = RegExp.$1;
            if ( realUrl.match( /^\s*https?:\/\/.+/ ) ) break;
        }
    }
    
    if ( !realUrl ) return null;
    
    return realUrl;
}

video = getVideoDetail2(arguments[0]);
if (video) print(video);
