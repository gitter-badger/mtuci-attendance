function loadAndDisplayChartData($chart, url, params, basicColorClass, errorColorClass, aspectRatio, successCallback, errorCallback){
  params = params || {};
  aspectRatio = aspectRatio || 'ct-minor-seventh';
  errorCallback = errorCallback || function(){};
  successCallback = successCallback || function(){};
  basicColorClass = basicColorClass || 'blue';
  errorColorClass = errorColorClass || 'red';
  $chart.find('.default').fadeOut(500);
  $chart.find('svg g.ct-series').closest('svg').fadeOut(500, function(){
    $(this).remove();
  });
  var $chartCard = $chart.closest('.chart-card'),
      $preloader = $chartCard.find('.chart-preloader');
  $preloader.height($chartCard.find('.chart-wrapper').outerHeight());
  if($preloader.height()<150){
    $preloader.height(150);
  }
  $preloader.fadeIn(500);
  var data = $.ajax({url: url, data: params, dataType: 'json', type: 'GET'})
  .done(function(data, textStatus, jqXHR){
    if ($chartCard.hasClass(errorColorClass)) {
      $chartCard.removeClass(errorColorClass);
    }
    if (!$chartCard.hasClass(basicColorClass)) {
      $chartCard.addClass(basicColorClass);
    }
    console.log('Данные по адресу '+url+ ' успешно загружены');
    $chart.hide().drawChart({data: data, tooltip: true, aspectRatio: aspectRatio}).fadeIn(1500, function(){
      successCallback(data);
    });
    $preloader.fadeOut(500);

  })
  .fail(function(jqXHR, textStatus, errorThrown){
    if ($chartCard.hasClass(basicColorClass)) {
      $chartCard.removeClass(basicColorClass);
    }
    if (!$chartCard.hasClass(errorColorClass)) {
      $chartCard.addClass(errorColorClass);
    }
    console.error('Не удалось получить данные по адресу '+ url+': '+textStatus+' '+errorThrown);
    $chart.find('.default').css('display', 'flex').promise().done(function(){
      errorCallback(jqXHR);
      $preloader.fadeOut(1000);
    });

  })
}
