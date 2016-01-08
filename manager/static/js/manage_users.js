$(function(){
  var users = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace,
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    remote: {
      url: '/ajax/search_accounts/?target=user&q=%QUERY',
      wildcard: '%QUERY'
    },
    prefetch: '/ajax/search_accounts/?target=all_users'
  });
  $('#users-search .typeahead').typeahead(null, {
    name: 'users',
    display: function(user){
      var universityGroup = user.universityGroup__name || 'Не в группе'
      return user.last_name+' '+user.first_name+' '+user.patronymic+' ('+universityGroup+')'
    },
    source: users,
    templates: {
      empty: [
        '<div class="empty-message">',
          'Не найдено, попробуйте воспользоваться поиском в панели администратора',
        '</div>'
      ].join('\n')
    }
  })
  .bind('typeahead:select', function(ev, suggestion) {
    loadAndDisplayUserInfo(suggestion.id);
  });
});
