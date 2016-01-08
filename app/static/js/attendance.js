var userChartState = 'semester',
    groupChartState = 'semester';
function supports_html5_storage() {
  try {
    return 'localStorage' in window && window['localStorage'] !== null;
} catch (e) {
    return false;
  }
}
function newWindow(e) {
  var h = 500,
      w = 500;
  window.open(e, '', 'scrollbars=1,height='+Math.min(h, screen.availHeight)+',width='+Math.min(w, screen.availWidth)+',left='+Math.max(0, (screen.availWidth - w)/2)+',top='+Math.max(0, (screen.availHeight - h)/2));
}
function userChart(change) {
  if (change) {
    userChartState=='semester'?userChartState='general':userChartState='semester';
  }
  loadAndDisplayChartData($('.user-statistics-chart'),
                          '/ajax/get_statistics/user/',
                          {id: $('.user-statistics-chart').data('user-id'), period: userChartState},
                          'indigo',
                          'red',
                          'ct-double-octave',
                          function(){
                            if (change) {
                              if (userChartState=='semester') {
                                $('.user-statistics header h5 span')
                                .fadeOut(800, function(){
                                  $('.user-statistics header h5 span')
                                  .html('статистика за семестр')
                                  .fadeIn(800);
                                });
                              } else {
                                $('.user-statistics header h5 span')
                                .fadeOut(800, function(){
                                  $('.user-statistics header h5 span')
                                  .html('статистика за все время')
                                  .fadeIn(800);
                                });
                              }
                            }
                          });
}
function groupChart(change) {
  if (change) {
    groupChartState=='semester'?groupChartState='general':groupChartState='semester';
  }
  loadAndDisplayChartData($('.group-statistics-chart'),
                          '/ajax/get_statistics/group/',
                          {id: $('.group-statistics-chart').data('group-id'), period: groupChartState},
                          'cyan',
                          'red',
                          'ct-double-octave',
                          function(){
                            if (change) {
                              if (groupChartState=='semester') {
                                $('.group-statistics header h5 span')
                                .fadeOut(800, function(){
                                  $('.group-statistics header h5 span')
                                  .html('статистика за семестр')
                                  .fadeIn(800);
                                });
                              } else {
                                $('.group-statistics header h5 span')
                                .fadeOut(800, function(){
                                  $('.group-statistics header h5 span')
                                  .html('статистика за все время')
                                  .fadeIn(800);
                                });
                              }
                            }
                          });
}
function loadAndDisplayTops(){
  $('.best .best-icon i').html('grade');
  $('.best .best-icon').removeClass('red');
  $('.best .best-icon.red i').css('cursor', 'default');
  $('.best header.best').removeClass('red darken-1');
  $('.best .best-icon i').addClass('animated flip');
  $('.best .progress').fadeTo(700,1);
  $.getJSON( "/ajax/get_statistics/top_5_attendance", {})
  .done(function( data ) {
    console.log('Tops loaded');
    if (data.students) {
      studentsList = ['<ol>']
      for (var i = 0; i < data.students.length; i++) {
        studentsList.push('<li data-wow-delay=".'+(i+1)+
            's" data-wow-duration="1s" class="wow fadeInLeft">'+data.students[i].name+
            ' <span>('+data.students[i].hours+' часов)</span>');
      }
      studentsList.push('</ol>')
      $('section.best-students').html(studentsList.join(''));
    } else {
      $('section.best-students').html('Пока что ничего<br><i class="material-icons">mood</i>');
    }
    if (data.groups) {
      groupsList = ['<ol>']
      for (var i = 0; i < data.groups.length; i++) {
        groupsList.push('<li data-wow-delay=".'+(i+1)+
            's" data-wow-duration="1s" class="wow fadeInRight">'+data.groups[i].name+
            ' <span>('+data.groups[i].hours+' часов)</span>');
      }
      groupsList.push('</ol>')
      $('section.best-groups').html(groupsList.join(''));
    } else {
      $('section.best-groups').html('Пока что ничего<br><i class="material-icons">mood</i>');
    }
  })
  .fail(function( jqxhr, textStatus, error ) {
    var err = textStatus + ", " + error;
    console.log("Loading tops failed: " + err );
    $('.best .best-icon i').html('error');
    $('.best .best-icon').addClass('red');
    $('.best header.best').addClass('red darken-1');
    $('.best .best-icon.red i').css('cursor', 'pointer');
  })
  .always(function(){
    $('.best .progress').fadeTo(700,0);
    $('.best .best-icon i').removeClass('animated flip');
  });
}
$(function(){
  if ("ActiveXObject" in window) {
    if (supports_html5_storage()) {
      if (parseInt(localStorage['hide_ie']) == 0) {
        $('.ie').slideDown(1000);
      }
    } else {
      $('.ie').slideDown(1000);
    }
  }
  $('.ie .close').on('click', function(){
    $('.ie').slideUp(1000);
    if (!supports_html5_storage()) {
      alert('Локальное хранилище не поддерживается. Предупреждение будет показываться снова.');
      console.log("Local Storage doesn't support");
    } else {
      localStorage['hide_ie'] = 1
    }
  });
  new WOW().init();
  outdatedBrowser({
        bgColor: '#f25648',
        color: '#ffffff',
        lowerThan: 'transform'
  });
  var $preloader = $('.preloader'),
      $spinner = $preloader.find('.md-preloader');
  $spinner.fadeOut();
  $preloader.delay(350).fadeOut('slow');
  $('.away').on('click', function() {
    $preloader.fadeIn('slow');
    $spinner.delay(350).fadeIn();
  });
  $(".button-collapse").sideNav();
  $('.parallax').parallax();
  $('div.arrow').on('click', function(){
    $('html, body').animate({
        scrollTop: $(".global-statistics").offset().top
    }, 3000, 'easeOutBack');
  });
  $('.modal-trigger').leanModal();
  if (!Boolean(parseInt(localStorage['hideBestDesc']))) {
    $('.best footer.desc').slideDown(800);
  }
  $('.best footer.desc .close').on('click', function(){
    $('.best footer.desc').slideUp(800);
    localStorage['hideBestDesc'] = 1;
  });
  $('ul#account li.user-info-activator, ul#account-mob li.user-info-activator').on('click', function(){
    loadAndDisplayUserInfo($(this).data('user-id'));
  });

  // Получаем общую статистику по загрузке страницы
  loadAndDisplayChartData($('.global-statistics-chart'),
                          '/ajax/get_statistics/global/',
                          {},
                          'green',
                          'red',
                          'ct-double-octave');
  // Получаем общую статистику по клику на "обновить"
  $('.global-statistics .reload').on('click', function(){
    loadAndDisplayChartData($('.global-statistics-chart'),
                            '/ajax/get_statistics/global',
                            {},
                            'green',
                            'red',
                            'ct-double-octave');
  });

  // Получаем статистику семестра по загрузке страницы
  loadAndDisplayChartData($('.semester-statistics-chart'),
                          '/ajax/get_statistics/semester/',
                          {},
                          'blue',
                          'red',
                          'ct-double-octave');
  // Получаем статистику семестра по клику на "обновить"
  $('.semester-statistics .reload').on('click', function(){
    loadAndDisplayChartData($('.semester-statistics-chart'),
                            '/ajax/get_statistics/semester',
                            {},
                            'blue',
                            'red',
                            'ct-double-octave');
  });

  userChart();
  $('.user-statistics .reload').on('click', function(){
    userChart(false);
  });
  $('.user-statistics .chart-back, .user-statistics .chart-forward').on('click', function(){
    userChart(true);
  });
  groupChart();
  $('.group-statistics .reload').on('click', function(){
    groupChart(false);
  });
  $('.group-statistics .chart-back, .group-statistics .chart-forward').on('click', function(){
    groupChart(true);
  });
  loadAndDisplayTops();
  $('.best .best-reload, .best .best-icon.red i').on('click', function(){
    loadAndDisplayTops();
  });
  var lastScrollTop = 0;
    $(window).on('scroll', function() {
      st = $(this).scrollTop();
      if(st < lastScrollTop) {
        $('.fixed-action-btn').addClass('vis');
      }
      else {
        $('.fixed-action-btn').removeClass('vis');
      }
      lastScrollTop = st;
    });

});
