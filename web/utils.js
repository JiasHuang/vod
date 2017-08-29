
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
    var links = [];
    var descs = [];
    var page_links = localStorage.getItem("page_links");
    var page_descs = localStorage.getItem("page_descs");
    if (page_links) {
        links = JSON.parse(page_links);
        descs = JSON.parse(page_descs);
        var index = links.indexOf($(this).attr("href"));
        if (index > -1) {
            links.splice(index, 1);
            descs.splice(index, 1);
        }
    }
    links.splice(0, 0, $(this).attr("href"));
    descs.splice(0, 0, $(this).attr("title"));
    if (links.length > 30) {
        links.pop();
        descs.pop();
    }
    localStorage.setItem("page_links", JSON.stringify(links));
    localStorage.setItem("page_descs", JSON.stringify(descs));
    return true;
}

