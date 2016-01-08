function supports_html5_storage() {
  try {
    return 'localStorage' in window && window['localStorage'] !== null;
} catch (e) {
    return false;
  }
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
});
