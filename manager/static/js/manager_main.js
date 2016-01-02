function loadAndDisplayChartData(chart, url, params, errorCallback, successCallback){
  chart.find('.default').css('display', 'none');
  chart.find('svg g.ct-series').closest('svg').remove();
  if(chart.height()<300){
    chart.height(300);
  }
  chart.find('.chart-preloader').height(chart.height()).fadeIn(500);
  params = params || {};
  errorCallback = errorCallback || function(){};
  successCallback = successCallback || function(){};
  var data = $.getJSON(url, params);
  data.success(function(data){
    console.log('Данные по адресу '+url+ ' успешно загружены');
    chart.find('.chart-preloader').fadeOut(1000);
    chart.drawChart({'data': data, 'tooltip': true});
  });
  data.error(function(){
    console.error('Не удалось получить данные по адресу '+ url);
    chart.find('.chart-preloader').fadeOut(1000);
    chart.find('.default').css('display', 'block');
  });
}
$(function(){
  loadAndDisplayChartData($('.global-statistics-chart'),
                          '/ajax/get_global_statistics/');
  $('div.chart-wrapper .chart-desc').on('click', function(){
    $(this).closest('.chart-wrapper').find('.full-chart-desc').toggleClass('active');
  });
  $('.chart-wrapper .reload').on('click', function(){
    loadAndDisplayChartData($(this).closest('.chart-wrapper').find('.chart'),
                            '/ajax/get_global_statistics/');
  });
});
$(window).load(function(){
  //setTimeout(loadAndDisplayChartData($(this).closest('.chart-wrapper').find('.chart'),
  //                        '/ajax/get_global_statistics/'),3000);
});
