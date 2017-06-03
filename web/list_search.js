
function onSelectChange() {
    var search_q = $('#input_q').val();
    var href = 'view.py?s='+$(this).val()+'&q='+search_q;
    window.location.href = href;
}

function renderSearchSelect() {
    var enginez = $('[id^="div_enginez_"]').map(function () { return $(this).attr('value'); }).get();
    var text = '';
    text += '<select id="select_enginez" class="engineSelect" onchange="onSelectChange.call(this)">'
    text += '<option disabled selected value>Select</option>';
    for (var i=0; i<enginez.length; i++)
        text += '<option value="'+enginez[i]+'">'+enginez[i]+'</option>';
    text += '</select>';
    return text;
}

function renderSearchBar() {
    var engines = $('[id^="div_engines_"]').map(function () { return $(this).attr('value'); }).get();
    var search_s = $('#div_search_s').attr('value');
    var search_q = $('#div_search_q').attr('value');
    var text = '';

    text += '<table><tr>';

    for (var i=0; i<engines.length; i++)
        text += '<td class="engine"><a href="view.py?s='+engines[i]+'&q='+search_q+'">'+engines[i]+'</a></td>';

    text += '<td>'+renderSearchSelect()+'</td>'

    text += '<tr></table>';

    $('#searchbarTable').html(text);
    $('#input_s').val(search_s);
    $('#input_q').val(search_q.replace(/\+/g,' '));

    $('.engine').each( function() {
        if ($(this).children().text().toLowerCase() == search_s)
            $(this).addClass('highlight');
    });

    $('#select_enginez').children().each( function () {
        if ($(this).text().toLowerCase() == search_s) {
            $('#select_enginez').val($(this).text());
            $('#select_enginez').addClass('highlight');
        }
    });
}

function renderNextPages() {
    var title = $('[id^="div_page_"]').map(function () { return $(this).attr('title'); }).get();
    var value = $('[id^="div_page_"]').map(function () { return $(this).attr('value'); }).get();
    var text = '';

    text += '<table class="pages"><tr>';
    for (var i=0; i<title.length; i++)
        text += '<td class="page"><a id="page_'+title[i]+'" href="'+value[i]+'">'+title[i]+'</a></td>';
    text += '<tr></table>';

    $('#nextpageTable').html(text);
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

    renderSearchBar();
    renderNextPages();

    if ($('.page').length > 0) {
        $(document).keydown(onPageNav);
    }

    $( "a[target='playVideo']" ).click(onPlayVideo);
    $('#loadingMessage').hide();
}

