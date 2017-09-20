
function showResults() {
    var pages_str = localStorage.getItem("pages");
    if (pages_str === null) {
        $('#Result').html('<h2>'+getLangLog('NotFound')+'</h2>');
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

function removePage(link) {
    var pages_str = localStorage.getItem("pages");
    var pages = JSON.parse(pages_str);
    var css = ["entryTitle", "entryTitle entryEven"];
    for (var i=0; i<pages.length; i++) {
        if (pages[i].link == link) {
            pages.splice(i, 1);
            break;
        }
    }
    localStorage.setItem("pages", JSON.stringify(pages));
    return true;
}

function swipeHandler(event) {
    var link = $(event.target).children(":last-child").attr("href");
    var title = $(event.target).children(":last-child").text();
    var r = confirm("Are you sure to delete it ?\n"+title);
    if (r == true) {
        removePage(link);
        show();
    }
}

function show() {
    showResults();
    $("h2").on("swipe", swipeHandler);
}
