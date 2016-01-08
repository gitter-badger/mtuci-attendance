function uploadFromHoursInput() {
    displayAttMsg('preloader', $(this).data('attendance-id'));
    var hoursData = $.getJSON('/ajax/change_attendance_hours/',{
                                    'attendance_id': $(this).data('attendance-id'),
                                    'hours': parseInt($(this).val())
                                    });
    hoursData.success(function(hoursData){
      $('inout.hours[data-attendance-id='+ hoursData.id +']').val(hoursData.hours);
      displayAttMsg('success', hoursData.id);
      console.log(hoursData.id + ' attendance changed hours to '+ hoursData.hours);
    });
    hoursData.attId = $(this).data('attendance-id');
    hoursData.error(function(){
      displayAttMsg('error', hoursData.attId);
      console.error("Can't change attendance hours");
    });
}
function uploadFromHoursInputByObj(obj) {
  displayAttMsg('preloader', obj.data('attendance-id'));
  var hoursData = $.getJSON('/ajax/change_attendance_hours/',{
                                  'attendance_id': obj.data('attendance-id'),
                                  'hours': parseInt(obj.val())
                                  });
  hoursData.success(function(hoursData){
    $('inout.hours[data-attendance-id='+ hoursData.id +']').val(hoursData.hours);
    displayAttMsg('success', hoursData.id);
    console.log(hoursData.id + ' attendance changed hours to '+ hoursData.hours);
  });
  hoursData.attId = obj.data('attendance-id');
  hoursData.error(function(hoursData){
    displayAttMsg('error', hoursData.attId);
    console.error("Can't change attendance hours");
  });
}
function displayAttMsg(msg, attId) {
  att = $('input.hours[data-attendance-id='+ attId +']').closest('.list-group-item');
  att.find('div.att-msg').remove();
  if (msg == 'preloader') {
    var preloader = '<div class="md-preloader">' +
    '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" height="56" ' +
    'width="56" viewbox="0 0 56 56"><circle cx="28" ' +
    'cy="28" r="27" stroke-width="2"/></svg></div></div>';
    att.append('<div class="att-msg" style="bottom:-6px;cursor:wait">'+
      preloader +'</div>');
  }
  else if (msg == 'error') {
    att.append('<div class="att-msg error"><i class="material-icons">clear</i></div>');
    $('div.att-msg.error').on('click', function(){
      uploadFromHoursInputByObj(att.find('input.hours'));
    });
  }
  else if (msg == 'success') {
    att.append('<div class="att-msg success"><i class="material-icons">done</i></div>');
  }
}
function generateGroupList(list) {
  function generateItem(attendance, tabindex, item_class) {
    return '<div class="list-group-item '+item_class+'"><div class="row-action-primary">' +
    '<i class="material-icons">person</i></div><div class="row-content">' +
    '<div data-user-id="'+attendance.student.id+'" class="action-secondary">'+
    '<i class="material-icons">info</i></div>'+
    '<h4 class="list-group-item-heading">' + attendance.student.last_name + ' ' +
    attendance.student.first_name + '</h4>' +
    '<p class="list-group-item-text"><input type="number" class="form-control hours"' +
    ' placeholder="Введите кол-во часов" value="' + attendance.hours + '" ' +
    'data-attendance-id="' + attendance.id + '" min="0" tabindex="'+tabindex +
    '"></p></div></div>'
  };
  var result = [];
  if (list.length >= 10) {
    var firstHalf = Math.ceil(list.length / 2);
    var secondHalf = Math.floor(list.length / 2);
    result.push('<div class="row group"><div class="col-xs-12 col-sm-6">');
    result.push('<div class="list-group group">');
    for (index=0; index<firstHalf; ++index)
    {
      result.push(generateItem(list[index], index, 'wow fadeInLeft'));
    }
    result.push('</div></div><div class="col-xs-12 col-sm-6">');
    result.push('<div class="list-group group">');
    for (index=firstHalf; index<firstHalf+secondHalf; ++index)
    {
      result.push(generateItem(list[index], index, 'wow fadeInRight'));
    }
    result.push('</div></div></div>');
  }
  else {
    result.push('<div class="list-group group">');
    for (index=0; index<list.length; ++index)
    {
      result.push(generateItem(list[index], index, 'wow fadeInLeft'));
    }
    result.push('</div>');
  }
  return result.join('');
}
function loadWeek(startStudyYear, semester, number) {
  groupDisplayMsg('preloader');
  $('.group-display .list-group-item .action-secondary').off('click');
  $('input.hours').off();

  var weekData = $.getJSON('/ajax/get_week_group_attendance/',{
                                                'start_study_year':startStudyYear,
                                                'semester':semester,
                                                'number':number
                                              });
  weekData.success(function(weekData){
      console.log('Week data loaded');
      $('.group-display').html('');
      $('.group-display').height('auto');
      $('.group-display').html(generateGroupList(weekData.attendance));
      $.material.init();
      $('input.hours').change(uploadFromHoursInput);
      $('.group-display .list-group-item .action-secondary').on('click', function(){
        loadAndDisplayUserInfo($(this).data('user-id'));
      });
  });
  weekData.error(function(weekData){
      console.error('Week data not loaded');
      groupDisplayMsg('error');
  });
}
function groupDisplayMsg(msg) {
  $('.group-display').height($('.group-display').height());
  $('.group-display').html('');
  if (msg == 'preloader') {
    var preloader = '<div class="md-preloader">' +
    '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" height="75" ' +
    'width="75" viewbox="0 0 75 75"><circle style="stroke:white" cx="37.5" ' +
    'cy="37.5" r="33.5" stroke-width="2"/></svg></div></div>';
    $('.group-display').html('<div class="msg"><div class="msg-cont">' +
    preloader + '</div>');
  }
  else if (msg == 'error') {
    $('.group-display').html('<div class="msg red"><div class="msg-cont">' +
    '<i class="material-icons">error</i><br><p>Возникла ошибка</p></div></div>');
  }
}
function changeActiveWeek(active) {
  number = $(this).data('week-number') || $('li.week.active').data('week-number');
  semester = $('h1.semester').data('semester-number') - 1;
  startStudyYear = $('h1.semester').data('start-study-year');
  $('li.week.active').removeClass('active');
  $('li.week[data-week-number=' + number + ']').addClass('active');
  loadWeek(startStudyYear, semester, number);
}

$(function(){
  if (Boolean(Number(localStorage['weeks-numbers-minimized']))) {
    $('ul.weeks-numbers').addClass('minimized');
    console.log('Position of ul.weeks-numbers loaded from Local Storage');
  }
  $('h1.semester').on('click', function(){
    $('ul.weeks-numbers').toggleClass('minimized');
    if (!supports_html5_storage()) {
      console.log("Local Storage doesn't support");
    }
    else {
      if ($('ul.weeks-numbers').hasClass('minimized')) {
        localStorage['weeks-numbers-minimized'] = 1;
      }
      else {
        localStorage['weeks-numbers-minimized'] = 0;
      }
      console.log('Position of ul.weeks-numbers saved to Local Storage');
    }
  });
  changeActiveWeek();
  $('li.week').on('click', changeActiveWeek);
});
