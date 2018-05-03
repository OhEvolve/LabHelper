
$(function () {

  // Accept group join request
  $(".manage-group").click(function () {

    var span = $(this);
    var group_id = $(this).closest(".group").attr("group-id");
    var csrf = $("input[name='csrfmiddlewaretoken']", $(this).closest(".group")).val();
    console.log(csrf)
    $.ajax({
      //url: '/groups/manage_group/' + group_id "/",
      url: '/groups/manage_group/',
      data: {
        'group': group,
        'csrfmiddlewaretoken': csrf
      },
      type: 'post',
      cache: false,
    });
  });
  

  // Delete group join request
  $(".leave-group").click(function () {

    console.log('JHERE')
    var span = $(this);
    var membership = $(this).closest(".membership").attr("membership-id");
    var csrf = $("input[name='csrfmiddlewaretoken']", $(this).closest(".membership")).val();
    console.log(csrf)
    $.ajax({
      url: '/groups/leave_group/',
      data: {
        'membership': membership,
        'csrfmiddlewaretoken': csrf
      },
      type: 'post',
      cache: false,
    });
  });

});

