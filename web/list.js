
var indexCur = 0;
var indexCnt = 0;

var xDown = null;
var yDown = null;

function showIndex() {
    var text = '';
    for (i=0; i<indexCnt; i++) {
        text += '<a class="resultIndex" onclick="gotoIndex('+i.toString()+')">+</a>\n';
    }
    $('#resultIndexBox').html(text);
}

function gotoIndex(index) {
    $(".entryCluster").hide();
    $(".entryCluster[index='"+ index.toString() + "']").show();
    $("#resultIndexBox a").removeClass('resultIndexFocus');
    $("#resultIndexBox a:nth-child("+(index+1).toString()+")").addClass('resultIndexFocus');
}

function gotoNext() {
    if (indexCur >= indexCnt - 1) {
        indexCur = 0;
    } else {
        indexCur = indexCur + 1;
    }
    gotoIndex(indexCur);
}

function gotoPrev() {
    if (indexCur <= 0) {
        indexCur = indexCnt - 1;
    } else {
        indexCur = indexCur - 1;
    }
    gotoIndex(indexCur);
}

function handleTouchStart(evt) {
    xDown = evt.touches[0].clientX;
    yDown = evt.touches[0].clientY;
}

function handleTouchMove(evt) {

    evt.preventDefault();

    if ( !xDown || !yDown ) {
        return;
    }

    var xUp = evt.touches[0].clientX;
    var yUp = evt.touches[0].clientY;

    var xDiff = xDown - xUp;
    var yDiff = yDown - yUp;

    if ( Math.abs(xDiff) > 10 ) {
        if ( xDiff > 0 ) {
            gotoNext();
        } else {
            gotoPrev();
        }
    }

    /* reset values */
    xDown = null;
    yDown = null;
}

function handleKeyDown(evt) {
    if (evt.keyCode == 39) {
        evt.preventDefault();
        gotoNext();
    } else if (evt.keyCode == 37) {
        evt.preventDefault();
        gotoPrev();
    }
}

function setEntryCluster(entryMax) {
    for (var i = 1; i <= $('.imageContainer').length; i++) {
        if (i % entryMax == 1) {
            var old_str = '<!--Entry'+i.toString()+'-->';
            var new_str = '<div class=entryCluster index='+indexCnt.toString()+'>';
            indexCnt = indexCnt + 1
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
    var titleWidth = windowWidth - imageWidth - 64;
    $('.imageContainer').css('height', imageHeight);
    $('.imageContainer').css('width', imageWidth);
    $('h2').css('left', imageWidth);
    $('h2').css('width', titleWidth);
    $('h2').css('height', imageHeight);
}

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
        document.addEventListener('touchstart', handleTouchStart, false);
        document.addEventListener('touchmove', handleTouchMove, false);
        document.addEventListener('keydown', handleKeyDown, false);
        showIndex();
        gotoIndex(0);
    }

    $( "a[target='playVideo']" ).click(onPlayVideo);
    $('#loadingMessage').hide();
    showServerMessage();
}

function onDocumentReady() {
    onPageReady();
}
