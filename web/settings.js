
var settings = {
    'slider' : {
        'desc' : '翻頁模式 | Slider',
        'type' : 'select',
        'vals' : ['yes', 'no'],
        'defs' :'yes',
    },
    'entryMax' : {
        'desc' : '條目數量 | EntryMax',
        'type' : 'select',
        'vals' : ['3', '4', '5'],
        'defs' : '5',
    },
    'format' : {
        'desc' : '視訊格式 | Format',
        'type' : 'select',
        'vals' : ['1080p', '720p', '480p', '360p', 'bestaudio'],
        'defs' : '720p',
    },
    'autosub' : {
        'desc' : '自動字幕 | AutoSub',
        'type' : 'select',
        'vals' : ['yes', 'no'],
        'defs' : 'no',
    },
    'autonext' : {
        'desc' : '循序播放 | AutoNext',
        'type' : 'select',
        'vals' : ['yes', 'no'],
        'defs' : 'no',
    },
    'youtubeID' : {
        'desc' : '使用名稱 | YouTubeID',
        'type' : 'input',
        'defs' : '',
    },
    'bookmark' : {
        'desc' : '書籤來源 | Bookmark',
        'type' : 'input',
        'defs' : '',
    },
};

var settings_cookies = ['format', 'autosub', 'autonext'];

function saveCookies() {
    var lists = settings_cookies;
    for (var i=0; i<lists.length; i++) {
        saveCookie(lists[i], document.getElementById(lists[i]).value);
    }
}

function save() {
    for (var id in settings) {
        localStorage.setItem(id, document.getElementById(id).value);
    }
    saveCookies();
    window.location.href = 'view.py';
}

function resetSettings() {
    for (var id in settings) {
        localStorage.removeItem(id);
    }
    saveCookies();
    location.reload();
}

function cancel() {
    window.location.href = 'view.py';
}

function getValue(id) {
    var val = localStorage.getItem(id);
    if (val === null) {
        val = settings[id]['defs'];
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

function select(id) {
    var text = '';
    text += '<select class="input" id="'+id+'" >';
    for (var i in settings[id]['vals']) {
        text += '<option value="'+settings[id]['vals'][i]+'">'+settings[id]['vals'][i]+'</option>';
    }
    text += '</select>';
    return text;
}

function input(id) {
    return '<input type="text" class="input" id="'+id+'" >';
}

function show() {
    var text = '<table>';
    for (var id in settings) {
        if (settings[id]['type'] == 'select') {
            text += '<tr><th>'+settings[id]['desc']+'</th><td>'+select(id)+'</td></tr>';
        } else {
            text += '<tr><th>'+settings[id]['desc']+'</th><td>'+input(id)+'</td></tr>';
        }
    }
    text += '</table>';
    $('#Result').html(text);
    for (var id in settings) {
        $('#'+id).val(getValue(id));
    }
}

