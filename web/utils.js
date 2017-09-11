
var logs = {
    'lang'          : ['en', 'ch'],
    'NotFound'      : ['Oops! Not Found', '抱歉，找不到您要的資料'],
    'slider'        : ['Slider', '翻頁模式'],
    'entryMax'      : ['EntryMax', '條目數量'],
    'format'        : ['Format', '視訊格式'],
    'autosub'       : ['AutoSub', '自動字幕'],
    'autonext'      : ['AutoNext', '循序播放'],
    'youtubeID'     : ['YouTubeID', '使用名稱'],
    'bookmarkURL'   : ['BookMarkURL', '書籤來源'],
    'MoreActions'   : ['More Actions', '更多選項'],
    'ClearHistory'  : ['Clear History', '清除紀錄'],
    'ResetSettings' : ['Reset Settings', '重置設定'],
    'Update'        : ['Update Version', '更新版本'],
    'success'       : ['Success', '成功'],
    'error'         : ['Error', '錯誤'],
};

function getExpire() {
    var expire_days = 3000;
    var d = new Date();
    d.setTime(d.getTime() + (expire_days * 24 * 60 * 60 * 1000));
    return 'expires='+d.toGMTString();
}

function saveCookie(name, value) {
    document.cookie = name+'='+value+';'+getExpire();
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
    var menubox = document.getElementById('menubox');
    menubox.style.display = "none";
}

function toggleMenu() {
    var menubox = document.getElementById('menubox');
    if (menubox.style.display == "block") {
        menubox.style.display = "none";
    } else {
        menubox.style.display = "block";
    }
    $('html').click(closeMenu);
    event.stopPropagation();
}

function getLangLog(key)
{
    var idx = logs['lang'].indexOf(localStorage.getItem("lang"));
    if (idx < 0) {
        idx = 0;
    }
    return logs[key][idx];
}

function showServerMessage()
{
    var x = document.getElementsByClassName("message");
    for (var i=0; i<x.length; i++) {
        $(x[i]).html('<h1>'+getLangLog(x[i].id)+'</h1>');
    }
}
