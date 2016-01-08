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
$(window).on('load', function() {
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
        lowerThan: 'transform',
        languagePath: ''
  });
  $.material.init();
  var $preloader = $('.preloader'),
    $spinner = $preloader.find('.md-preloader');
  $spinner.fadeOut();
  $preloader.delay(350).fadeOut('slow');
  $('.away').on('click', function() {
    $preloader.fadeIn('slow');
    $spinner.delay(350).fadeIn();
  });
  Offline.options = {
    checkOnLoad: true,
    checks: {
      xhr: {
        url: '/static/icons/favicon.ico'
      }
    }
  }
  $(".offline-ui-content").html("Online");
  Offline.on('down', function() {
    $(".offline-ui-content").html("")
  });
  Offline.on('up', function() {
    $(".offline-ui-content").html("Online")
  });
  $(".offline-ui").addClass("hidden-xs hidden-sm");
  $('[data-toggle="tooltip"]').tooltip();
  $('ul.nav a.user-info-activator').on('click', function(){
    loadAndDisplayUserInfo($(this).data('user-id'));
  });
  $('a.report-activator').on('click', function(){
    $('body').css({'overflow-x': 'hidden', 'overflow-y': 'hidden'});
    $('.alpha-bg').fadeIn(500, function(){
      $('.report-window').addClass('active');
    });
  });
  $('.alpha-bg, .report-window .close').on('click', function(){
    $('.alpha-bg').fadeOut(500);
    $('body').css({'overflow-y': 'visible', 'overflow-x': 'hidden'});
    $('.report-window').removeClass('active');
  });
});
