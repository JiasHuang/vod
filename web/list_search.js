
function onSelectChange() {
    var search_q = $('#input_q').val();
    var href = 'view.py?q='+search_q;
    saveCookie('engine', $(this).val());
    window.location.href = href;
}

function renderNextPages() {
    var title = $('[id^="div_page_"]').map(function () { return $(this).attr('title'); }).get();
    var value = $('[id^="div_page_"]').map(function () { return $(this).attr('value'); }).get();
    var text = '';

    text += '<table><tr>';
    for (var i=0; i<title.length; i++)
        text += '<td><a id="page_'+title[i]+'" href="'+value[i]+'">'+title[i]+'</a></td>';
    text += '<tr></table>';

    $('#nextpageResult').html(text);
}

function onPageNav(e) {
    switch(e.which) {
        case 37: // left
            prev = document.getElementById('page_prev');
            if (prev)
                window.location.href = prev.href;
            break;
        case 39: // right
            next = document.getElementById('page_next');
            if (next)
                window.location.href = next.href;
            break;
        default:
            return;
    }
    e.preventDefault(); // prevent the default action
}

function onSearchReady() {

    renderNextPages();

    if ($('.page').length > 0) {
        $(document).keydown(onPageNav);
    }

    $( "a[target='playVideo']" ).click(onPlayVideo);
    $('#loadingMessage').hide();
    showServerMessage();
}

