
function show() {
    var pages_str = localStorage.getItem("pages");
    if (pages_str === null) {
        $('#Result').html('<h2>抱歉，找不到您要的資料 | Oops! Not Found</h2>');
        return;
    }
    var pages = JSON.parse(pages_str);
    var text = '';
    var css = ["entryTitle", "entryTitle entryEven"];
    for (var i=0; i<pages.length; i++) {
        text += '<h2 class="'+css[i&1]+'">';
        if (pages[i].plink && pages[i].ptitle) {
            text += '<a href="'+pages[i].plink+'">'+pages[i].ptitle+'</a>  /  ';
        }
        text += '<a href="'+pages[i].link+'">'+pages[i].title+'</a></h2>';
    }
    $('#Result').html(text);
}

