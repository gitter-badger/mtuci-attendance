$(window).on('load', function() {
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

});
