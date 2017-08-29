
function show() {
    var page_links = localStorage.getItem("page_links");
    var page_descs = localStorage.getItem("page_descs");
    if (page_links === null) {
        return;
    }
    var links = JSON.parse(page_links);
    var descs = JSON.parse(page_descs);
    var text = '';
    for (var i=0; i<links.length; i++) {
        text += '<h2><a href="'+links[i]+'">'+descs[i]+'</a></h2>';
    }
    $('#Result').html(text);
}

