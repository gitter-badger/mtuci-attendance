var itemsToDeleteCount = 0;
function showModal(title, text){
  $('.simple.modal').find('h4').html(title);
  $('.simple.modal').find('p').html(text);
  $('.simple.modal').openModal();
}
function showModalWithDisagree(title, text, agreeCallback, disagreeCallback){
  $('.disagree.modal').find('h4').html(title);
  $('.disagree.modal').find('p').html(text);
  $('.disagree.modal a.agree').bind('click', {'agreeCallback': agreeCallback}, function(event){
    $('.disagree.modal a.agree, .disagree.modal a.disagree').unbind('click');
    event.data.agreeCallback();
  });
  $('.disagree.modal a.disagree').bind('click', {'disagreeCallback': disagreeCallback}, function(event){
    $('.disagree.modal a.agree, .disagree.modal a.disagree').unbind('click');
    event.data.disagreeCallback();
  });
  $('.disagree.modal').openModal();
}
function getWeeksList() {
  var weeks = [];
  $('div.add-weeks-by-numbers input[type=checkbox]').each(function(){
    if ($(this)[0].checked === true) {
      weeks.push($(this).data('week-number'));
    }
  });
  return weeks;
}
function loadExistingWeeks(startStudyYear, semester, callback) {
  $('.schedule-manage.card .card-preloader').fadeIn(500);
  var existWeeks = $.getJSON('/ajax/get_existing_weeks/',{
                                  'start_study_year': startStudyYear,
                                  'semester': semester
                                  });
  existWeeks.success(function(existWeeks){
    $('.schedule-manage.card .card-preloader').fadeOut(500);
    console.log('Existing weeks successfuly loaded');
    callback(existWeeks.weeks);
  });
  existWeeks.error(function(){
    $('.schedule-manage.card .card-preloader').fadeOut(500);
    console.error("Can't load existing weeks");
    showModal('Ошибка', 'Не удалось получить список недель');
  });
}
function loadExistingWeeksForDelete(callback) {
  loadExistingWeeks($('input#start-study-year-delete').val(),
                    parseInt($('select.semester-delete').val()),
                    callback);
}
function displayExistingWeeksForDelete(weeks) {
  function getWeekListItem(id, str){
    return '<li class="collection-item"><div><input type="checkbox" id="delete-week-'+ id +
           '" data-delete-week-id="'+ id +'"/><label for="delete-week-'+ id +'">'+ str +
           '</label><a href="#!" data-week-id="'+ id +'"'+'class="secondary-content">'+
           '<i class="material-icons">clear</i></a></div></li>';
  }
  var cont = $('.weeks-to-delete');
  if (weeks.length == 0) {
    cont.html('<p>В данном семестре пока что нет недель.</p>');
  } else {
    var result = ['<ul class="collection">'];
    for (var i = 0; i < weeks.length; i++) {
      result.push(getWeekListItem(weeks[i].id, weeks[i].str));
    }
    result.push('</ul>');
    cont.html(result.join(''));
    $('div.weeks-to-delete li.collection-item input[type=checkbox]').change(function(){
      if ($(this)[0].checked) {
        ++itemsToDeleteCount;
      } else {
        --itemsToDeleteCount;
      }
      $('a.btn.delete-weeks span.badge').html(itemsToDeleteCount);
    });
  }
  $('div.weeks-to-delete li.collection-item i').on('click', function(){
    var weekId = $(this).closest('a').data('week-id');
    $('.schedule-manage.card .card-preloader').fadeIn(500);
    var deleteWeek = $.getJSON('/ajax/delete_weeks_by_id/',{
                                    'weeks_id': weekId
                                    });
    deleteWeek.success(function(deleteWeek){
      $('.schedule-manage.card .card-preloader').fadeOut(500);
      console.log('Week deleted');
      Materialize.toast('Неделя успешно удалена', 3000);
      loadExistingWeeksForDelete(displayExistingWeeksForDelete);
    });
    deleteWeek.error(function(){
      $('.schedule-manage.card .card-preloader').fadeOut(500);
      console.error("Can't delete week");
      showModal('Ошибка', 'Не удалось удалить неделю');
      loadExistingWeeksForDelete(displayExistingWeeksForDelete);
    });
  });
}
function deleteChoosenWeeks() {
  if (itemsToDeleteCount < 1) {
    showModal('Ошибка', 'Не выбрано ни одной недели');
  } else {
    showModalWithDisagree('Вы уверены?', 'Будет удалено: '+itemsToDeleteCount+' недель(и)', deleteWeeks, function(){console.log('Deleting was canceled')});
    function deleteWeeks() {
      var weeksId = [];
      $('div.weeks-to-delete li.collection-item').each(function(){
        if ($(this).find('input')[0].checked) {
          weeksId.push($(this).find('a').data('week-id'));
        }
      });
      var deletedWeeks = $.getJSON('/ajax/delete_weeks_by_id/', {
        'weeks_id': weeksId.join(',')
      });
      deletedWeeks.success(function(deletedWeeks){
        $('.schedule-manage.card .card-preloader').fadeOut(500);
        console.log(deletedWeeks.deleted + ' weeks deleted');
        loadExistingWeeksForDelete(displayExistingWeeksForDelete);
        itemsToDeleteCount -= deletedWeeks.deleted;
        $('a.btn.delete-weeks span.badge').html(itemsToDeleteCount);
        Materialize.toast(deletedWeeks.deleted + ' недель(и) было удалено', 3000);
      });
      deletedWeeks.error(function(){
        $('.schedule-manage.card .card-preloader').fadeOut(500);
        console.error("Can't delete weeks");
        showModal('Ошибка', 'Не удалось удалить недели');
        loadExistingWeeksForDelete(displayExistingWeeksForDelete);
      });
    }
  }
}
$(document).ready(function(){
  $('ul.weeks-add').tabs();
  var weekSlider = document.getElementById('weeks-start-end-slider');
  noUiSlider.create(weekSlider, {
    start: [2, 18],
    connect: true,
    step: 1,
    range: {
      'min': 1,
      'max': 24
    },
    format: wNumb({
      decimals: 0
    })
  });
  var startWeekInput = document.getElementById('start-week-input'),
  	  endWeekInput = document.getElementById('end-week-input');
  weekSlider.noUiSlider.on('update', function( values, handle ) {
  	if ( handle ) {
  		endWeekInput.value = values[handle];
  	} else {
  		startWeekInput.value = values[handle];
  	}
  });
  startWeekInput.addEventListener('change', function(){
  	weekSlider.noUiSlider.set([this.value, null]);
  });
  endWeekInput.addEventListener('change', function(){
  	weekSlider.noUiSlider.set([null, this.value]);
  });
  $('#step-week-input').attr('min', '1');
  $('select').material_select();
  $('.card .card-preloader').fadeOut(1000);
  $('ul.weeks-add.tabs li.tab a[href=#weeks-delete]').on('click', function() {
    loadExistingWeeksForDelete(displayExistingWeeksForDelete);
  });
  $('input#start-study-year-delete, select.semester-delete').change(function(){
    loadExistingWeeksForDelete(displayExistingWeeksForDelete);
  });
  $('a.btn.delete-weeks').on('click', deleteChoosenWeeks);
  $('div.add-weeks-by-numbers button[type=submit]').on('click', function(){
    var weeksNumbers = getWeeksList();
    if (weeksNumbers.length == 0) {
      showModal('Ошибка', 'Не выбрано ни одной недели');
    }
    else {
      var weeksNumbersStr = weeksNumbers.join(','),
          by = 'list',
          startStudyYear = $('input#start-study-year-add').val(),
          semester = parseInt($('select.semester-add').val());
      $('.schedule-manage.card .card-preloader').fadeIn(1000);
      var createWeeks = $.getJSON('/ajax/create_weeks/',{
                                      'by': by,
                                      'start_study_year': startStudyYear,
                                      'semester': semester,
                                      'weeks_numbers': weeksNumbersStr
                                      });
      createWeeks.success(function(createWeeks){
        $('.schedule-manage.card .card-preloader').fadeOut(1000);
        var created = parseInt(createWeeks.result);
        console.log(created + ' weeks were created');
        Materialize.toast(created + ' недель(и) было создано', 3000);
      });
      createWeeks.error(function(){
        console.error("Can't create weeks");
        $('.schedule-manage.card .card-preloader').fadeOut(1000);
        showModal('Ошибка', 'Не удалось создать недели');
      });
    }
  });
  $('div.add-weeks-by-start-end button[type=submit]').on('click', function(){
    var startWeek = $('#start-week-input').val(),
        endWeek = $('#end-week-input').val(),
        step = $('#step-week-input').val();
    if (startWeek > 25 || startWeek < 1 || endWeek < 1 || endWeek > 25 || step > 25 || step < 1) {
      showModal('Ошибка', 'Некорректные данные');
    }
    else {
      var by = 'start-end',
          startStudyYear = $('input#start-study-year-add').val(),
          semester = parseInt($('select.semester-add').val());
      $('.schedule-manage.card .card-preloader').fadeIn(1000);
      var createWeeks = $.getJSON('/ajax/create_weeks/',{
                                      'by': by,
                                      'start_study_year': startStudyYear,
                                      'semester': semester,
                                      'start_week_number': startWeek,
                                      'end_week_number': endWeek,
                                      'week_step': step
                                      });
      createWeeks.success(function(createWeeks){
        $('.schedule-manage.card .card-preloader').fadeOut(1000);
        var weekCase, created = parseInt(createWeeks.result);
        console.log(created + ' weeks were created');
        if ((created % 10 >= 5 && created % 10 <= 9) || created % 10 == 0) {
          weekCase = ' недель';
        } else if (created % 10 >= 2 && created % 10 <= 4) {
          weekCase = ' недели';
        } else {
          weekCase = ' неделя';
        }
        Materialize.toast(created + ' недель(и) было создано', 3000);
      });
      createWeeks.error(function(){
        console.error("Can't create weeks");
        $('.schedule-manage.card .card-preloader').fadeOut(1000);
        showModal('Ошибка', 'Не удалось создать недели');
      });
    }
  });
});
