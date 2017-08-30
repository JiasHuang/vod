
function show() {
    var pages_str = localStorage.getItem("pages");
    if (pages_str === null) {
        return;
    }
    var pages = JSON.parse(pages_str);
    var text = '';
    var css = ["entryTitle", "entryTitle entryEven"];
    for (var i=0; i<pages.length; i++) {
        text += '<h2 class="'+css[i&1]+'"><a href="'+pages[i].link+'">'+pages[i].title+'</a></h2>';
    }
    $('#Result').html(text);
}

