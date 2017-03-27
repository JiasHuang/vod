
function getExpire() {
    var expire_days = 3000;
    var d = new Date();
    d.setTime(d.getTime() + (expire_days * 24 * 60 * 60 * 1000));
    return 'expires='+d.toGMTString();
}

function saveCookie() {
    var lists = ['format'];
    var cookie = '';
    for (var i=0; i<lists.length; i++) {
        cookie += lists[i]+'='+document.getElementById(lists[i]).value+'; '
    }
    document.cookie = cookie+getExpire();
}

function save() {
    var lists = ['slider', 'entryMax', 'format', 'username', 'bookmark'];
    for (var i=0; i<lists.length; i++) {
        localStorage.setItem(lists[i], document.getElementById(lists[i]).value);
    }
    saveCookie();
    window.location.href = 'view.py';
}

function cancel() {
    window.location.href = 'view.py';
}

function getDefault(key) {
    var defs = {
        'slider' : {
            'yes':'yes',
            'no':'no',
            'default':'yes',
        },
        'entryMax' : {
            '3':'3',
            '4':'4',
            '5':'5',
            'default':'5',
        },
        'format' : {
            'http-720p':'best[ext!=webm][protocol^=http][height<=720]',
            'http-480p':'best[ext!=webm][protocol^=http][height<=480]',
            'http-360p':'best[ext!=webm][protocol^=http][height<=360]',
            '720p':'best[ext!=webm][height<=720]',
            '480p':'best[ext!=webm][height<=480]',
            '360p':'best[ext!=webm][height<=360]',
            'audio-only':'bestaudio',
            'default':'best[ext!=webm][protocol^=http]/best[ext!=webm]',
        },
        'username' : {
            'default':'',
        },
        'bookmark' : {
            'default':'',
        }
    };

    return defs[key];
}

function getValue(id) {
    var val = localStorage.getItem(id);
    if (val === null) {
        val = getDefault(id)['default'];
    }
    return val;
}

function onSelectChange() {
    $(this).siblings('input').val($(this).val());
}

function select(id) {
    var dict = getDefault(id);
    var text = '';
    text += '<div>';
    text += '<input type="text" name="data" class="datatext" id="'+id+'" value="'+getValue(id)+'">';
    text += '<select onchange="onSelectChange.call(this)" class="contentselect">';
    text += '<option disabled selected value>-select-</option>';
    for (var key in dict) {
        text += '<option value="'+dict[key]+'">'+key+'</option>';
    }
    text += '</select>';
    text += '</div>';
    return text;
}

function show() {

    var dict = {
        'Slider':'slider',
        'Slider-EntryMax':'entryMax',
        'Format':'format',
        'YouTube-Username':'username',
        'Bookmark.json':'bookmark'
    };

    var text = '<table>';
    for (var key in dict) {
        text += '<tr><th>'+key+'</th><td>'+select(dict[key])+'</td></tr>';
    }
    text += '</table>';

    $('#Result').html(text);
}

