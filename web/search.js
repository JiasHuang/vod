
var pagelist = null;

function parseJSON(obj) {
  $('#result').html(getResultHTMLText(obj));
  pagelist = obj.meta;
  onSearchReady();
}

function onTimeout() {
  console.log('timeout');
}

function query(s, q) {
    if (q) {
        $('#loadingMessage').show();
        url = "load.py?q="+encodeURIComponent(q);
        if (s)
            url += "&s="+s;
        $.ajax({
          url: url,
          dataType: 'json',
          error: onTimeout,
          success: parseJSON,
          timeout: 20000
        });
    }
    else {
        $('#loadingMessage').hide();
    }
}

function onSelectChange() {
    var q = $('#input_q').val();
    var engine = $(this).val();
    window.location.href = 'search.html?q=' + q + '&s=' + engine;
}

function onPlayVideo() {
    if (pagelist) {
        saveCookie('pagelist', pagelist);
    }
}

function onSearchReady() {
    $( "a[target='playVideo']" ).click(onPlayVideo);
    $('#loadingMessage').hide();
}

function onDocumentReady() {
    var s = GetURLParameter("s") || 'youtube';
    var q = GetURLParameter("q");
    if (q) {
        q = decodeURIComponent(q.replace(/\+/g," "));
        $('#input_q').val(q);
    }
    $('#select_engine').val(s);
    query(s, q);
}
