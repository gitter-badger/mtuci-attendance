window.index = {
  supports_html5_storage: function () {
    try {
        return 'localStorage' in window && window['localStorage'] !== null;
    } catch (e) {
        return false;
      }
  }
}
$(function(){
  if ("ActiveXObject" in window) {
    if (index.supports_html5_storage()) {
      if (parseInt(localStorage['hide_ie']) == 0) {
        $('.ie').slideDown(1000);
      }
    } else {
      $('.ie').slideDown(1000);
    }
  }
  $('.ie .close').on('click', function(){
    $('.ie').slideUp(1000);
    if (!index.supports_html5_storage()) {
      alert('Локальное хранилище не поддерживается. Предупреждение будет показываться снова.');
      console.log("Local Storage doesn't support");
    } else {
      localStorage['hide_ie'] = 1
    }
  });
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
  $('.nav-btn').on('click', function(){
		$('main, nav, .nav-btn, .page-header, .nexus, #wrap').toggleClass('menu-open');
    $('header.page-header a.btn').toggleClass('disabled');
    $('main.menu-open, header.page-header, main, .nexus').on('click', function(){
      $('main, nav, .nav-btn, .page-header, .nexus, #wrap').removeClass('menu-open');
      $('header.page-header a.btn').removeClass('disabled');
      $('main.menu-open, header.page-header, main, .nexus').off();
    });
	});
  $('body').click(function(evt){
    if(!$(evt.target).closest('.user-actions, ul.menu .user').length) {
      $('.user-actions').removeClass('open');
    }
  });
  $('ul.menu .user').on('click', function(){
    $('.user-actions').toggleClass('open');
  });
  $('ul.user-actions li').last().hover(function(){
    $('ul.user-actions').addClass('last-active');
  },
  function(){
    $('ul.user-actions').removeClass('last-active');
  });


//---
(function() {
  new Slideshow( document.getElementById( 'slideshow' ) );

  /* Mockup responsiveness */
  var body = docElem = window.document.documentElement,
    wrap = document.getElementById( 'wrap' ),
    mockup = wrap.querySelector( '.mockup' ),
    mockupWidth = mockup.offsetWidth,
    mockupHeight = mockup.offsetHeight;

    if (mockupHeight==0) {
      mockupHeight=1100;
    }

  scaleMockup();

  function scaleMockup() {
    var wrapWidth = wrap.offsetWidth,
        wrapHeight = wrap.offsetHeight
    if (mockupWidth/mockupHeight<window.innerWidth/window.innerHeight) {
      val = window.innerWidth / mockupWidth;
      mockup.style.transform = 'scale3d(' + val + ', ' + val + ', 1)';
    } else {
      val = window.innerHeight / mockupHeight;
      mockup.style.transform = 'scale3d(' + val + ', ' + val + ', 1) translateX(-'+(mockupWidth*val-window.innerWidth)+'px)';
    }

  }

  window.addEventListener( 'resize', resizeHandler );

  function resizeHandler() {
    function delayed() {
      resize();
      resizeTimeout = null;
    }
    if ( typeof resizeTimeout != 'undefined' ) {
      clearTimeout( resizeTimeout );
    }
    resizeTimeout = setTimeout( delayed, 50 );
  }

  function resize() {
    scaleMockup();
  }
})();
//---

$('.slide').hover(function(){
  $('#wrap').addClass('blur');
}, function(){
  $('#wrap').removeClass('blur');
});
$('.carousel').carousel();
$('.modal-trigger').leanModal();
$('.page-header a.btn').on('click', function(){
  if (!$(this).hasClass('disabled')) {
    $('.page-header h1').css('animation-delay', '0s').removeClass('zoomInDown').addClass('zoomOutUp');
    $('.page-header h6').css('animation-delay', '0s').removeClass('flipInX').addClass('flipOutX');
    $('.page-header h4').css('animation-delay', '0s').removeClass('zoomInUp').addClass('zoomOutDown');
    $('.page-header a.btn').css('animation-delay', '0s').removeClass('zoomIn').addClass('zoomOut');
      SVG.select('.nexus svg image.screen-1').animate(10000, '<>', 2500).move(2494.8, -580.84 - 9630 + 1920).loop(999, true);
    setTimeout(function(){
      $('.page-header').addClass('started');
      $('.page-header h1').css('animation-delay', '.5s').removeClass('zoomOutUp').addClass('zoomIn');
      $('.page-header h4').css('animation-delay', '.5s').removeClass('zoomOutDown').addClass('zoomIn');
      $('figure.nexus, section.slide-1').addClass('on');

    }, 1000);
  }
});
$('.slide-1 .next').on('click', function(){
  $('figure.nexus, section.slide-1').removeClass('on');
  SVG.select('.nexus svg image.screen-1').stop();
  $('.nexus svg image.screen-1').hide();
  $('.slide-2').addClass('on');
});
$('.slide-2 .next').on('click', function(){
  $('.slide-2').removeClass('on');
  $('.slide-3').addClass('on');
});
$('.slide-3 .next').on('click', function(){
  $('.slide-3').removeClass('on');
  $('.slide-4, .slide-4-carousel').addClass('on');
});
$('.slide-4 .next').on('click', function(){
  $('.slide-4, .slide-4-carousel').removeClass('on');
  $('.slide-5').addClass('on');
});
$('.slide-5 .next').on('click', function(){
  $('.slide-5').removeClass('on');
  $('.nexus svg image.screen-2').show();
  $('.slide-6, figure.nexus').addClass('on');
  moveSecondScreen();
});
$('.slide-6 .next').on('click', function(){
  $('.slide-6, .nexus').removeClass('on');
  $('.slide-7').addClass('on');
});



});

function moveSecondScreen() {
  setTimeout(function(){SVG.select('.nexus svg image.screen-2').animate(2000, '<>', 0).move(2494.8-1080, -580.84);}, 2000);
  setTimeout(function(){SVG.select('.nexus svg image.screen-2').animate(2000, '<>', 0).move(2494.8-1080*2, -580.84);}, 6000);
  setTimeout(function(){SVG.select('.nexus svg image.screen-2').animate(2000, '<>', 0).move(2494.8-1080, -580.84);}, 9000);
  setTimeout(function(){SVG.select('.nexus svg image.screen-2').animate(2000, '<>', 0).move(2494.8, -580.84);}, 13000);
  setTimeout(moveSecondScreen, 15000);
}
