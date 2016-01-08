$(function(){
  // Получаем общую статистику по загрузке страницы
  loadAndDisplayChartData($('.global-statistics-chart'),
                          '/ajax/get_statistics/global/',
                          {},
                          'blue',
                          'red',
                          'ct-minor-seventh');
  // Получаем общую статистику по клику на "обновить"
  $('.chart-card .reload').on('click', function(){
                            loadAndDisplayChartData($(this).closest('.chart-card').find('.chart'),
                                                    '/ajax/get_statistics/global',
                                                    {},
                                                    'blue',
                                                    'red',
                                                    'ct-minor-seventh');
                          });
  // Показываем подробное описание
  $('div.chart-card .chart-desc').on('click', function(){
    $(this).closest('.chart-card').find('.full-chart-desc').toggleClass('active');
  });
});
