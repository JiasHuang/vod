
$.fn.gotoSlide = function(index, offset = 0) {

    var slideIdx = this.data('slideIdx');
    var slideCnt = this.data('slideCnt');
    var settings = this.data('settings');

    if (index < 0) {
        index = (slideIdx + offset + slideCnt) % slideCnt;
    }

    this.children().filter(function() {
        return (Math.floor($(this).index()/settings.divGroup) == slideIdx);
    }).hide();

    this.children().filter(function() {
        return (Math.floor($(this).index()/settings.divGroup) == index);
    }).show();

    if (settings.slideIndexBox) {
        $('#'+settings.slideIndexBox + ' select').val(index);
    }

    this.data('slideIdx', index);

    return;
};

$.fn.initSlide = function(options) {

    var defaults = {
        divGroup: 1,
        slideIndexBox: null,
    };

    var settings = $.extend({}, defaults, options);

    var slideIdx = 0;
    var slideCnt = Math.ceil(this.children('div').length/settings.divGroup);

    this.data('slideIdx', slideIdx);
    this.data('slideCnt', slideCnt);
    this.data('settings', settings);

    if (settings.slideIndexBox) {
        var text = '<select onchange="$(\'#'+ this.attr('id') +'\').gotoSlide(this.selectedIndex)">\n';
        for (i=0; i<slideCnt; i++) {
            text += '\t<option value="'+i+'">'+(i+1)+'</option>\n';
        }
        text += '</select>\n';
        text += '<span>/'+this.data('slideCnt')+'</span>\n';
        $('#'+settings.slideIndexBox).html(text);
        $('#'+settings.slideIndexBox).show();
    }

    this.children('div').hide();
    this.gotoSlide(0);

    return;
};

