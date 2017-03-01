
function saveCookie() {
    var expire_days = 3000;
    var d = new Date();
    d.setTime(d.getTime() + (expire_days * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toGMTString();
    document.cookie = 'format='+$('#format').val()+'; '+expires+'; ';
}

function save() {
    localStorage.setItem('Slider', $('#slider').val());
    localStorage.setItem('Format', $('#format').val());
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
    var defval = 'best[ext!=webm][protocol^=http]';
    var dict = {"480":"best[ext!=webm][protocol^=http][height<=480]", "720":"best[ext!=webm][protocol^=http][height<=720]", "default":defval};
    return select('format', 'formatSelect', dict, localStorage.getItem('Format') || defval);
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
    text += '<tr><th>Format</th><td>'+select_format()+'</td></tr>';
    text += '</table>';

    $('#Result').html(text);

    onchange('slider', 'sliderSelect');
    onchange('format', 'formatSelect');
}

