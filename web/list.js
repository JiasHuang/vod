
function setEntryCluster(entryMax) {
    for (var i = 1; i <= $('.imageContainer').length; i++) {
        if (i % entryMax == 1) {
            var old_str = '<!--Entry'+i.toString()+'-->';
            var new_str = '<div class=entryCluster>';
            if (i > entryMax) {
                new_str = '</div>'+new_str;
            }
            document.body.innerHTML = document.body.innerHTML.replace(old_str, new_str);
        }
    }
    document.body.innerHTML = document.body.innerHTML.replace('<!--EntryEnd-->', '</div>');
}

function setWidthHeight(entryMax) {
    var windowHeight = $(window).innerHeight();
    var windowWidth = $(window).innerWidth();
    var imageHeight = windowHeight * 90 / entryMax / 100;
    var imageWidth = windowHeight * 120 / entryMax / 100;
    var titleWidth = windowWidth - imageWidth - 32;
    $('.imageContainer').css('height', imageHeight);
    $('.imageContainer').css('width', imageWidth);
    $('h2').css('left', imageWidth);
    $('h2').css('width', titleWidth);
    $('h2').css('height', imageHeight);
};

function onPlayVideo() {
    if ($('#pageinfo').length)
        saveCookie('pagelist', $('#pageinfo').attr('pagelist'));
}

function onPageReady() {

    var slider = localStorage.getItem('slider');
    var entryMax = parseInt(localStorage.getItem('entryMax') || '5');

    if (slider != 'no' && $('.imageContainer').length > entryMax) {
        setEntryCluster(entryMax);
        setWidthHeight(entryMax);
        bxslider = $('#result').bxSlider({
            keyboardEnabled: true,
            speed: 100,
        });
    }

    $( "a[target='playVideo']" ).click(onPlayVideo);
    $('#loadingMessage').hide();
    showServerMessage();
}

function onDocumentReady() {
    onPageReady();
}

