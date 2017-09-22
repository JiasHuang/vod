
function query(s, q, x) {
    if (q.length > 0) {
        $('#loadingMessage').show();
        url = "load.py?q="+encodeURIComponent(q);
        if (s)
            url += "&s="+s;
        if (x)
            url += "&x="+x;
        $('#result').load(url, onLoadCompleted);
    }
    else {
        $('#loadingMessage').hide();
    }
}

function onSelectChange() {
    var q = $('#input_q').val();
    var engine = $(this).val();
    saveCookie('engine', engine);
    query(engine, q);
}

function renderNextPages() {
    var text = '';
    var pages = $('[id^="div_page_"]').toArray();
    text += '<table><tr>';
    for(var i in pages) {
        var s = $(pages[i]).attr('s');
        var q = $(pages[i]).attr('q');
        var x = $(pages[i]).attr('x');
        var title = $(pages[i]).attr('title');
        text += '<td onclick="onPageClick('+i+');">'+title+'</td>';
    }
    text += '<tr></table>';
    $('#nextpageResult').html(text);
}

function onPageClick(index) {
    var pages = $('[id^="div_page_"]').toArray();
    var s = $(pages[index]).attr('s');
    var q = $(pages[index]).attr('q');
    var x = $(pages[index]).attr('x');
    query(s, q, x);
}

function onPageNav(e) {
    target = null;
    switch(e.which) {
        case 37: // left
            target = $('#div_page_prev');
            break;
        case 39: // right
            target = $('#div_page_next');
            break;
        default:
            return;
    }
    if (target.length)
        query(target.attr('s'), target.attr('q'), target.attr('x'))
    e.preventDefault(); // prevent the default action
}

function onPlayVideo() {
    pageinfo = document.getElementById('pageinfo');
    if (pageinfo)
        saveCookie('pagelist', pageinfo.getAttribute('pagelist'));
}

function onSearchReady() {
    renderNextPages();
    showServerMessage();
    $( "a[target='playVideo']" ).click(onPlayVideo);
    $('#loadingMessage').hide();
}

function onLoadCompleted (responseTxt, statusTxt, xhr) {
    if (statusTxt == "success")
        onSearchReady();
    if(statusTxt == "error")
        alert("Error: " + xhr.status + ": " + xhr.statusText);
}

function show() {
    var s = GetURLParameter("s") || getCookie('engine');
    var q = GetURLParameter("q");
    var x = GetURLParameter("x");
    if (q) {
        q = decodeURIComponent(q)
        $('#input_q').val(q);
    }
    if (s) {
        $('#select_engine').val(s);
    }
    query(s, q, x);
    $(document).keydown(onPageNav);
}
