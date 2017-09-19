
var logs = {
    'lang'          : ['en', 'ch'],
    'NotFound'      : ['Oops! Not Found', '抱歉，找不到您要的資料'],
    'slider'        : ['Slider', '翻頁模式'],
    'entryMax'      : ['EntryMax', '條目數量'],
    'format'        : ['Format', '視訊格式'],
    'autosub'       : ['AutoSub', '自動字幕'],
    'playbackMode'  : ['PlaybackMode', '播放模式'],
    'Normal'        : ['Normal', '正常播放'],
    'AutoNext'      : ['Auto Next', '依序播放'],
    'LoopOne'       : ['Loop One', '單首重複'],
    'LoopAll'       : ['Loop All', '循環播放'],
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
        showMenuLink();
    }
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

function showServerMessage()
{
    var x = document.getElementsByClassName("message");
    for (var i=0; i<x.length; i++) {
        $(x[i]).html(getLangLog(x[i].id));
    }
}

function showMenuLink()
{
    var x = document.getElementsByClassName("menulink");
    for (var i=0; i<x.length; i++) {
        $(x[i]).html(getLangLog(x[i].id));
    }
}
