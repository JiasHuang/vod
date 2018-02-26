
var entryMax = 0;
var slideIdx = 0;
var slideCnt = 0;

var xDown = null;
var yDown = null;

function initSlide() {
    var text = '';

    text += '<select onchange="gotoSlide(this.selectedIndex)">\n';
    for (i=0; i<slideCnt; i++) {
        text += '\t<option value="'+i+'">'+(i+1)+'</option>\n';
    }
    text += '</select>\n';
    text += '<span>/'+slideCnt+'</span>\n';

    //console.log(text);
    $('#slideIndexBox').html(text);
    $(".imageWrapper").hide();
}

function gotoSlide(index) {
    $(".imageWrapper").filter(function() {
        return (Math.floor($(this).attr('entryNo')/entryMax) == slideIdx);
    }).hide();
    $(".imageWrapper").filter(function() {
        return (Math.floor($(this).attr('entryNo')/entryMax) == index);
    }).show();
    $("#slideIndexBox select").val(index);
    slideIdx = index;
}

function gotoNext() {
    gotoSlide((slideIdx + 1) % slideCnt);
}

function gotoPrev() {
    gotoSlide((slideIdx + slideCnt - 1) % slideCnt);
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

function setWidthHeight() {
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
    entryMax = parseInt(localStorage.getItem('entryMax') || '5');
    slideCnt = Math.ceil($('.imageWrapper').length / entryMax)
    if (slider != 'no' && slideCnt > 1) {
        setWidthHeight();
        document.addEventListener('touchstart', handleTouchStart, false);
        document.addEventListener('touchmove', handleTouchMove, false);
        document.addEventListener('keydown', handleKeyDown, false);
        initSlide();
        gotoSlide(0);
    }

    $( "a[target='playVideo']" ).click(onPlayVideo);
    $('#loadingMessage').hide();
    showServerMessage();
}

function onDocumentReady() {
    onPageReady();
}
