
function saveCookie() {
    var expire_days = 3000;
    var d = new Date();
    d.setTime(d.getTime() + (expire_days * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toGMTString();
    var format = "format=" + $('#format').val();
    document.cookie = format+'; '+expires+'; ';
}

function save() {
    localStorage.setItem('Slider', $('#slider').val());
    localStorage.setItem('EntryMax', $('#entryMax').val());
    localStorage.setItem('Format', $('#format').val());
    localStorage.setItem('Username', $('#username').val());
    saveCookie();
    window.location.href = 'view.py';
}

function cancel() {
    window.location.href = 'view.py';
}

function onchange(element) {
    console.log(element);
}

function select(inputID, selectID, dict, defval) {
    var text = '';
    text += '<div class="row">'
    text += '<input type="text" name="data" class="datatext" id="'+inputID+'" value="'+defval+'">'
    text += '<select class="contentselect" id="'+selectID+'">'
    text += '<option disabled selected value>-- select --</option>'
    for (var key in dict) {
        text += '<option value="'+dict[key]+'">'+key+'</option>'
    }
    text += '</select>'
    text += '</div>'
    return text
}

function select_slider() {
    var defval = 'yes';
    var dict = {"yes":"yes", "no":"no", "default":defval};
    return select('slider', 'sliderSelect', dict, localStorage.getItem('Slider') || defval);
}

function select_format() {
    var defval = 'best[ext!=webm][protocol^=http]/best[ext!=webm]';
    var dict = {
        "http-720p":"best[ext!=webm][protocol^=http][height<=720]",
        "http-480p":"best[ext!=webm][protocol^=http][height<=480]",
        "http-360p":"best[ext!=webm][protocol^=http][height<=360]",
        "720p":"best[ext!=webm][height<=720]",
        "480p":"best[ext!=webm][height<=480]",
        "360p":"best[ext!=webm][height<=360]",
        "default":defval
    };
    return select('format', 'formatSelect', dict, localStorage.getItem('Format') || defval);
}

function select_entryMax() {
    var defval = '5';
    var dict = {"1":"1", "2":"2", "3":"3", "4":"4", "5":"5", "default":defval};
    return select('entryMax', 'entryMaxSelect', dict, localStorage.getItem('EntryMax') || defval);
}

function select_username() {
    var defval = 'YouTube';
    var dict = {"default":defval};
    return select('username', 'usernameSelect', dict, localStorage.getItem('Username') || defval);
}

function onchange(inputID, selectID) {
    var textfield = document.getElementById(inputID);
    var contentselect = document.getElementById(selectID);
    contentselect.onchange = function() {
        var text = contentselect.options[contentselect.selectedIndex].value;
        if(text != "") {
            textfield.value = text;
        }
    }
}

function show() {

    var text = '<table>';
    text += '<tr><th>Slider</th><td>'+select_slider()+'</td></tr>';
    text += '<tr><th>Slider-EntryMax</th><td>'+select_entryMax()+'</td></tr>';
    text += '<tr><th>Format</th><td>'+select_format()+'</td></tr>';
    text += '<tr><th>YouTube-Username</th><td>'+select_username()+'</td></tr>';
    text += '</table>';

    $('#Result').html(text);

    onchange('slider', 'sliderSelect');
    onchange('format', 'formatSelect');
    onchange('entryMax', 'entryMaxSelect');
    onchange('username', 'usernameSelect');
}

