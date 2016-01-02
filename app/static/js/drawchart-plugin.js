// Author: Morozov Igor
// Based (and work with) on Chartist.js and tooltip plugin
(function( $ ) {
  $.fn.drawChart = function(options) {

    var settings = $.extend( {
      'type'             : 'line',
      'data'             : {'labels': [], 'series': [[]]},
      'showPoint'        : true,
      'tooltip'          : false,
      'aspectRatio'      : 'ct-perfect-fourth'
    }, options);

    var chartistOptions = {
        showPoint: settings.showPoint,
        lineSmooth: true,
        axisX: {
            showGrid: false,
            showLabel: false
        },
        axisY: {
            showGrid: false,
            showLabel: false,
            offset: 60
        },
        plugins: []
    };
    if (settings.tooltip){
      chartistOptions.plugins.push(Chartist.plugins.tooltip({appendToBody: false}));
    }
    this.addClass(settings.aspectRatio);
    $(this).find('.default').css('display', 'none');
    if (settings.type == 'line') {
      new Chartist.Line(this.selector, settings.data, chartistOptions);
    }


    if (settings.tooltip) {

    }

    return this

  };
})(jQuery);
