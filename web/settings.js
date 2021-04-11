
var settings = {
    'slider' : {
        'type' : 'select',
        'vals' : ['yes', 'no'],
        'defs' :'yes',
    },
    'entryMax' : {
        'type' : 'select',
        'vals' : ['3', '4', '5', '6', '7'],
        'defs' : '5',
    },
    'format' : {
        'type' : 'select',
        'vals' : ['1080p', '720p', '480p', '360p', 'bestaudio'],
        'defs' : '720p',
    },
    'subtitle' : {
        'type' : 'select',
        'vals' : ['yes', 'auto-generated', 'no'],
        'defs' : 'no',
    },
    'youtubeID' : {
        'type' : 'input',
        'defs' : '',
    },
    'bookmarkURL' : {
        'type' : 'input',
        'defs' : '',
    },
    'dlconf' : {
        'type' : 'input',
        'defs' : 'zuida=4, pangzitv=4, .le.com=4, tiktokvideodown=4, iqiyi=4, gimy=4'
    },
};

var settings_cookies = ['format', 'subtitle', 'dlconf'];

function initCookies() {
  var lists = settings_cookies;
  for (let i=0; i<lists.length; i++) {
    saveCookie(lists[i], getValue(lists[i]));
  }
}

function delCookies() {
  var lists = settings_cookies;
  for (let i=0; i<lists.length; i++) {
    delCookie(lists[i]);
  }
}

function saveCookies() {
    var lists = settings_cookies;
    for (var i=0; i<lists.length; i++) {
        saveCookie(lists[i], $('#'+lists[i]).val());
    }
}

function save() {
    for (var id in settings) {
        localStorage.setItem(id, $('#'+id).val());
    }
    saveCookies();
    window.location.href = 'index.html';
}

function resetSettings() {
    for (var id in settings) {
        localStorage.removeItem(id);
    }
    delCookies();
    location.reload();
}

function cancel() {
    window.location.href = 'index.html';
}

function getValue(id) {
    var val = localStorage.getItem(id);
    if (val === null) {
        val = settings[id]['defs'];
    }
    if ('sync' in settings[id]) {
        var sync_val = $('#'+settings[id]['sync']).attr('value');
        if (sync_val && sync_val.length > 0) {
            val = sync_val;
        }
    }
    return val;
}

function onLangSelect()
{
    localStorage.setItem("lang", $(this).val());
    onSettingsDocumentReady();
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
            window.location.href = 'index.html?c=update';
        }
    }
    $(this).val('');
}

function select(id) {
    var text = '';
    text += '<select id="'+id+'">';
    for (var i in settings[id]['vals']) {
        text += '<option value="'+settings[id]['vals'][i]+'">'+getLangLog(settings[id]['vals'][i])+'</option>';
    }
    text += '</select>';
    return text;
}

function input(id) {
    return '<input type="text" id="'+id+'">';
}

function result() {
    var text = '<table>';
    for (var id in settings) {
        if (settings[id]['type'] == 'select') {
            text += '<tr><th>'+getLangLog(id)+'</th><td>'+select(id)+'</td></tr>';
        } else if (settings[id]['type'] == 'input') {
            text += '<tr><th>'+getLangLog(id)+'</th><td>'+input(id)+'</td></tr>';
        }
    }
    text += '</table>';
    return text;
}

function onSettingsDocumentReady() {

    $('#'+getLangLog('lang')).prop('checked', true);

    $('#Result').html(result());
    for (var id in settings) {
        $('#'+id).val(getValue(id));
    }

    var options = $('#actionSelect').children().toArray();
    for (var i in options) {
        $(options[i]).text(getLangLog($(options[i]).val()));
    }
}

