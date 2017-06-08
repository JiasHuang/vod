
var settings_dict = {
    'Slider':'slider',
    'Slider-EntryMax':'entryMax',
    'Format':'format',
    'YouTube-Username':'username',
    'Bookmark.json':'bookmark',
    'AutoSub':'autosub',
    'AutoNext':'autonext'
};

var settings_defs = {
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
        'http-1080p':'37/best[ext!=webm][protocol^=http][height<=1080]',
        'http-720p':'22/best[ext!=webm][protocol^=http][height<=720]',
        'http-480p':'best[ext!=webm][protocol^=http][height<=480]',
        'http-360p':'best[ext!=webm][protocol^=http][height<=360]',
        '1080p':'37/best[ext!=webm][height<=1080]',
        '720p':'22/best[ext!=webm][height<=720]',
        '480p':'best[ext!=webm][height<=480]',
        '360p':'best[ext!=webm][height<=360]',
        'audio-only':'bestaudio',
        'default':'22/best[ext!=webm][protocol^=http]',
    },
    'username' : {
        'default':'',
    },
    'bookmark' : {
        'default':'',
    },
    'autosub' : {
        'yes':'yes',
        'no':'no',
        'default':'no',
    },
    'autonext' : {
        'yes':'yes',
        'no':'no',
        'default':'no',
    }
};

var settings_cookies = ['format', 'autosub', 'autonext'];

function saveCookies() {
    var lists = settings_cookies;
    for (var i=0; i<lists.length; i++) {
        saveCookie(lists[i], document.getElementById(lists[i]).value);
    }
}

function save() {
    var dict = settings_dict;
    for (var key in dict) {
        localStorage.setItem(dict[key], document.getElementById(dict[key]).value);
    }
    saveCookies();
    window.location.href = 'view.py';
}

function cancel() {
    window.location.href = 'view.py';
}

function getDefault(key) {
    return settings_defs[key];
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
    var dict = settings_dict;
    var text = '<table>';
    for (var key in dict) {
        text += '<tr><th>'+key+'</th><td>'+select(dict[key])+'</td></tr>';
    }
    text += '</table>';
    $('#Result').html(text);
}

