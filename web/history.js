
function showResults() {
    var pages_str = localStorage.getItem("pages");
    if (pages_str === null) {
        $('#result').html('<h1>'+getLangLog('NotFound')+'</h1>');
        return;
    }
    var pages = JSON.parse(pages_str);
    if (pages.length == 0) {
        $('#result').html('<h1>'+getLangLog('NotFound')+'</h1>');
        return;
    }
    var text = '<table>';
    for (var i=0; i<pages.length; i++) {
        text += '<tr><td>'
        if (pages[i].plink && pages[i].ptitle) {
            text += '<a href="'+pages[i].plink+'">'+pages[i].ptitle+'</a>  /  ';
        }
        text += '<a href="'+pages[i].link+'">'+pages[i].title+'</a>';
        text += '<img src="trash-icon-32.png" onclick="onTrash('+i+');" />';
        text += '</td></tr>'
    }
    text += '</table>'
    $('#result').html(text);
}

function removePageByIndex(index) {
    var pages_str = localStorage.getItem("pages");
    var pages = JSON.parse(pages_str);
    pages.splice(index, 1);
    localStorage.setItem("pages", JSON.stringify(pages));
}

function getPageTitleByIndex(index) {
    var pages_str = localStorage.getItem("pages");
    var pages = JSON.parse(pages_str);
    return pages[index].title;
}

function onTrash(index) {
    var title = getPageTitleByIndex(index);
    var r = confirm("Are you sure to delete it ?\n"+title);
    if (r == true) {
        removePageByIndex(index);
        show();
    }
}

function show() {
    showResults();
}
