
var xDown = null;
var yDown = null;

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
            $('#result').gotoSlide(-1, 1);
        } else {
            $('#result').gotoSlide(-1, -1);
        }
    }

    /* reset values */
    xDown = null;
    yDown = null;
}

function handleKeyDown(evt) {
    if (evt.keyCode == 39) {
        evt.preventDefault();
        $('#result').gotoSlide(-1, 1);
    } else if (evt.keyCode == 37) {
        evt.preventDefault();
        $('#result').gotoSlide(-1, -1);
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
    if ($('#pagelist').length)
        saveCookie('pagelist', $('#pagelist').attr('pagelist'));
}

function onPageReady() {

    var slider = localStorage.getItem('slider');
    entryMax = parseInt(localStorage.getItem('entryMax') || '5');
    if (slider != 'no' && $('.imageWrapper').length > entryMax) {
        setWidthHeight();
        document.addEventListener('touchstart', handleTouchStart, false);
        document.addEventListener('touchmove', handleTouchMove, false);
        document.addEventListener('keydown', handleKeyDown, false);
        $('#result').initSlide({divGroup:entryMax, slideIndexBox:'slideIndexBox'});
    }

    $( "a[target='playVideo']" ).click(onPlayVideo);
    $('#loadingMessage').hide();
    showServerMessage();
}

function onDocumentReady() {
    onPageReady();
}
