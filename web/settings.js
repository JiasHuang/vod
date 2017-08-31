
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
        '1080p':'1080p',
        '720p':'720p',
        '480p':'480p',
        '360p':'360p',
        'audio-only':'bestaudio',
        'default':'720p',
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

function resetSettings() {
    var dict = settings_dict;
    for (var key in dict) {
        localStorage.removeItem(dict[key]);
    }
    saveCookies();
    location.reload();
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

function onActinSelect()
{
    var r = confirm("Are you sure ?");
    if (r == true) {
        cmd = $(this).val();
        if (cmd == 'ClearHistory') {
            localStorage.removeItem('pages');
        } else if (cmd == 'ResetSettings') {
            resetSettings();
        } else if (cmd == 'Update') {
            window.location.href = 'view.py?c=update';
        }
    }
    $(this).val('');
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

