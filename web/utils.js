
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
    pages.splice(0, 0, data);
    if (pages.length > 30) {
        pages.pop();
    }
    localStorage.setItem("pages", JSON.stringify(pages));
    return true;
}

