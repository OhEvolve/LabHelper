
$(function () {

  // Accept group join request
  $(".accept-request").click(function () {

    var span = $(this);
    var membership = $(this).closest(".membership").attr("membership-id");
    var csrf = $("input[name='csrfmiddlewaretoken']", $(this).closest(".membership")).val();
    console.log(csrf)
    $.ajax({
      url: '/groups/accept_request/',
      data: {
        'membership': membership,
        'csrfmiddlewaretoken': csrf
      },
      type: 'post',
      cache: false,
    });
  });
  
  // Delete group join request
  $(".reject-request").click(function () {

    var span = $(this);
    var membership = $(this).closest(".membership").attr("membership-id");
    var csrf = $("input[name='csrfmiddlewaretoken']", $(this).closest(".membership")).val();
    console.log(csrf)
    $.ajax({
      url: '/groups/reject_request/',
      data: {
        'membership': membership,
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

