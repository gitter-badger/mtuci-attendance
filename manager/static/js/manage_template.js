$(function(){
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
