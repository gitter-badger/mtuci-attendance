function loadAndDisplayUserInfo (userId){
  $('.user-info .error, .user-info header, .user-info .content, .user-info .not-student').hide();
  $('body').css({'overflow-x': 'hidden', 'overflow-y': 'hidden'});
  $('.alpha-bg').fadeIn(500, function(){
    $('.user-info').addClass('active');
  });
  $('.alpha-bg, .user-info .close').on('click', hideUserInfo);
  var data = $.ajax({url: '/ajax/user_info/', data: {id: userId}, dataType: 'json', type: 'GET'})
  .done(function(data, textStatus, jqXHR){
    console.log('Данные пользователя '+userId+ ' успешно загружены');
    $('.user-info header').html(data.last_name+' '+data.first_name+' '+data.patronymic).promise().done(function(){
      $('.user-info header').show();
    });
    if (data.universityGroup) {
      $('.user-info .group').html(data.universityGroup).show();
    } else {
      $('.user-info .group').html('Не в группе').show();
    }
    if (data.notStudent) {
      $('.user-info .content, .user-info .group').hide();
      $('.user-info .not-student').show();
    } else {
      $('.user-info .not-student').hide();
      $('.user-info .content').show();
    }
    userChartAndTable(userId, $('.charts-control a.active').data('statistics-period'), function(){
      $('.user-info .user-preloader').fadeOut(1000, function(){
        $('.user-info .statistics-charts').fadeIn(500, function(){
          $('.user-info .chart-table').fadeIn(500);
        });
      });
    });
    $('.user-info .chart-card .reload, .user-info .statistics-chart .chart .default').on('click', function(){
      userChartAndTable(userId, $('.charts-control a.active').data('statistics-period'),function(){
        $('.user-info .chart-table').fadeIn(1000);
      });
    });
    $('.user-info .charts-control a').on('click', function(){
      $('.user-info .charts-control a.active').removeClass('active');
      $(this).addClass('active');
      userChartAndTable(userId, $(this).data('statistics-period'),function(){
        $('.user-info .chart-table').fadeIn(1000);
      });
    });
    $('.user-info .chart-back, .user-info .chart-forward').on('click', function(){
      $('.user-info .charts-control a').toggleClass('active').promise().done(function(){
        userChartAndTable(userId, $('.user-info .charts-control a.active').data('statistics-period'),function(){
          $('.user-info .chart-table').fadeIn(1000);
        });
      });
    });
  })
  .fail(function(jqXHR, textStatus, errorThrown){
    console.error('Не удалось получить данные пользователя с id '+ userId +': '+textStatus+' '+errorThrown);
    $('.user-info .user-preloader').fadeOut(1000);
    $('.user-info .error').fadeIn(1000);
  });
}
function hideUserInfo(){
  $('.user-info .chart-card .reload, .user-info .charts-control a, .user-info .chart-back, .user-info .chart-forward, '+
    '.user-info .statistics-chart .chart .default, .alpha-bg, .user-info .close').off('click');
  $('.user-info .error, .user-info header, .user-info .content, .user-info .not-student').hide();
  $('.user-info').removeClass('active');
  $('.alpha-bg').fadeOut(500);
  $('body').css({'overflow-y': 'visible', 'overflow-x': 'hidden'});
  $('.user-info .user-preloader').show();
}
function userChartAndTable(userId, period, callback) {
  callback = callback || function(){};
  $('.user-info .chart-table').fadeOut(1000);
  loadAndDisplayChartData($('.user-info .chart'),
                          '/ajax/get_statistics/user/',
                          {id: userId, period: period},
                          'blue',
                          'red',
                          'ct-double-octave',
                          function(data){
                            if (period == 'semester') {
                              $('.user-info .chart-table .title').html('Номер недели');
                            } else {
                              $('.user-info .chart-table .title').html('Номер посещения');
                            }
                            $('.user-info .chart-table .number').html('Количество часов');
                            tbody = []
                            for (var i = 0; i < data.labels.length; i++) {
                              tbody.push('<tr><td>'+data.labels[i]+'</td><td>');
                              tbody.push(data.series[0][i].value+'</td></tr>');
                            }
                            $('.user-info .chart-table tbody').html(tbody.join(''));
                            callback();
                          });
}
