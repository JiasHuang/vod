
var menuboxContent = 0;

var logs = {
    'lang'          : ['en', 'ch'],
    'NotFound'      : ['Oops! Not Found', '抱歉，找不到您要的資料'],
    'slider'        : ['Slider', '翻頁模式'],
    'entryMax'      : ['EntryMax', '條目數量'],
    'format'        : ['Format', '視訊格式'],
    'subtitle'      : ['Subtitle', '字幕選項'],
    'playbackMode'  : ['PlaybackMode', '播放模式'],
    'autoNext'      : ['AutoNext', '循序播放'],
    'loopOne'       : ['LoopOne', '重複播放'],
    'loopAll'       : ['LoopAll', '循環播放'],
    'youtubeID'     : ['YouTubeID', 'YouTube使用名稱'],
    'bookmarkURL'   : ['BookmarkURL', '書籤來源'],
    'MoreActions'   : ['More Actions', '更多選項'],
    'ClearHistory'  : ['Clear History', '清除紀錄'],
    'ResetSettings' : ['Reset Settings', '重置設定'],
    'Update'        : ['Update Version', '更新版本'],
    'success'       : ['Success', '成功'],
    'error'         : ['Error', '錯誤'],
    'playing'       : ['Playing', '開始播放'],
    'pause'         : ['Play/Pause', '播放/暫停'],
    'forward'       : ['Forward', '快進'],
    'backward'      : ['Backward', '快退'],
    'stop'          : ['Stop', '停止'],
    'percent'       : ['Percent', '進度'],
    'home'          : ['Home', '首頁'],
    'bookmark'      : ['Bookmark', '書籤'],
    'settings'      : ['Settings', '設定'],
    'history'       : ['History', '紀錄'],
    'dlconf'        : ['dlconf', 'dlconf'],
};

String.format = function() {
  var s = arguments[0];
  for (var i = 0; i < arguments.length - 1; i++) {
    var reg = new RegExp("\\{" + i + "\\}", "gm");
    s = s.replace(reg, arguments[i + 1]);
  }
  return s;
}

function getExpire() {
    var expire_days = 3000;
    var d = new Date();
    d.setTime(d.getTime() + (expire_days * 24 * 60 * 60 * 1000));
    return 'expires='+d.toGMTString();
}

function saveCookie(name, value) {
    document.cookie = name+'='+value+';'+getExpire();
}

function getCookie(name) {
    var arr = document.cookie.match(new RegExp("(^| )"+name+"=([^;]*)(;|$)"));
    if(arr != null)
        return unescape(arr[2]);
    return null;
}

function onPageClick() {
    var link = $(this).attr("href");
    var title = $(this).attr("title");
    var data = {};
    var pages = [];
    var pages_str = localStorage.getItem("pages");
    if (pages_str) {
        pages = JSON.parse(pages_str);
    }
    for (var i = 0; i < pages.length; i++) {
        if (pages[i].link == link) {
            pages.splice(i, 1);
            break;
        }
    }
    data.link = link
    data.title = title;

    var pos = window.location.href.search(/view.py\?p=/);
    if (pos > 0) {
        var plink = decodeURIComponent(window.location.href.substring(pos));
        for (var i = 0; i < pages.length; i++) {
            if (pages[i].link == plink) {
                data.plink = pages[i].link;
                data.ptitle = pages[i].title;
                pages.splice(i, 1);
                break;
            }
            else if (pages[i].plink == plink) {
                data.plink = pages[i].plink;
                data.ptitle = pages[i].ptitle;
                pages.splice(i, 1);
                break;
            }
        }
    }

    pages.splice(0, 0, data);
    if (pages.length > 30) {
        pages.pop();
    }
    localStorage.setItem("pages", JSON.stringify(pages));
    return true;
}

function onMenuClick() {
    event.stopPropagation();
}

function closeMenu() {
    $('#menubox').hide();
}

function onLoadMenuBoxCompleted (responseTxt, statusTxt, xhr) {
    if (statusTxt == "success")
        showMenuBtn();
    if(statusTxt == "error")
        alert("Error: " + xhr.status + ": " + xhr.statusText);
}

function toggleMenu() {
    if (menuboxContent == 0) {
        $('#menubox').load("menubox.html", onLoadMenuBoxCompleted);
        menuboxContent = 1;
    }
    $('#menubox').toggle();
    $('html').click(closeMenu);
    event.stopPropagation();
}

function getLangLog(key)
{
    if (!(key in logs)) {
        return key;
    }
    var idx = logs['lang'].indexOf(localStorage.getItem("lang"));
    if (idx < 0) {
        idx = 0;
    }
    return logs[key][idx];
}

function showMenuBtn()
{
    $('.menubtn').each(function () {
        $(this).html(getLangLog($(this).attr('id')));
    });
}

function GetURLParameter(sParam)
{
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++)
    {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam)
        {
            return sParameterName[1];
        }
    }
    return null;
}

function basename(path) {
  return path.split('/').reverse()[0];
}

function result_dir(obj) {
  var text = '';

  text += String.format('<h1>Index of {0}</h1>', obj.dir);
  text += '<div style="line-height:200%;font-size:32px">';

  for (var i=0; i<obj.entry.length; i++) {
    let e = obj.entry[i];
    if (e.is_file) {
      text += String.format('<li><img src="/icons/movie.gif"><a href="index.html?f={0}">{1}</a>', e.path, basename(e.path));
    }
    else {
      text += String.format('<li><img src="/icons/folder.gif"><a href="list.html?d={0}">{1}</a>', e.path, basename(e.path));
    }
  }

  text += '</div>';

  return text;
}

function result_page(obj) {
  var text = '';
  var onerr = 'this.onerror=null; this.src="Movies-icon.png"';

  if (!obj.entry.length) {
    return String.format('<h1>{0}</h1>', getLangLog('NotFound'));
  }

  for (var i=0; i<obj.entry.length; i++) {
    let e = obj.entry[i];
    let link_attr = null;
    text += '<div class="imageWrapper">';
    text += '<div class="imageContainer">';
    if (e.video == true) {
      link_attr = String.format('href="index.html?v={0}" target="playVideo"', e.link, e.image);
    }
    else {
      link_attr = String.format('href="list.html?p={0}" onclick="onPageClick.call(this);" title="{1}"', e.link, e.title);
    }
    text += String.format('<a {0}><img src="{1}" onerror=\'{2}\' /></a>', link_attr, e.image, onerr);
    if (e.desc) {
      text += String.format('<p>{0}</p>', e.desc);
    }
    text += '</div>';
    text += String.format('<h2><a {0}>{1}</a></h2>', link_attr, e.title);
    text += '</div>';
  }

  return text;
}

function result_play(obj) {
  var text = '';
  text += String.format('<h2><a href="{0}" target="_blank">{0}</a></h2>', obj.video);
  return text;
}

function result_act(obj) {
  var text = '';
  text += String.format('<h2>{0} {1}</h2>', getLangLog(obj.act), obj.num);
  return text
}

function result_cmd(obj) {
  var text = '';
  text += String.format('<h2>{0}</h2>', getLangLog(obj.status));
  return text
}

function getResultHTMLText(obj) {
  console.log(obj);
  if (obj.type == 'page') {
    return result_page(obj);
  }
  if (obj.type == 'dir') {
    return result_dir(obj);
  }
  if (obj.type == 'play') {
    return result_play(obj);
  }
  if (obj.type == 'act') {
    return result_act(obj);
  }
  if (obj.type == 'cmd') {
    return result_cmd(obj);
  }
}


