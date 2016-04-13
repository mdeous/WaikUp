/*
 WaikUp Global JavaScript
 */

function getLinkInfo(e) {
  var linkID = e.getAttribute('id').split('-');
  return {'action': linkID[0], 'id': linkID[linkID.length-1]};
}

$('.collapser').click(function () {
  var itemSelector = 'div#' + $(this).attr('id');
  if ($(itemSelector).hasClass('out')) {
    $(itemSelector).addClass('in');
    $(itemSelector).removeClass('out');
  } else {
    $(itemSelector).addClass('out');
    $(itemSelector).removeClass('in');
  }
});
$('.expand-all').click(function () {
  $('.collapse.out').removeClass('out').addClass('in');
});
$('.collapse-all').click(function () {
  $('.collapse.in').removeClass('in').addClass('out');
});
$('#new-link-save').click(function () {
  $('#new-link-form').submit();
  return true;
});
$('#new-link-cancel').click(function () {
  $('#new-link-url').val('');
  $('#new-link-title').val('');
  $('#new-link-description').val('');
  return true;
});
$('#chpasswd-save').click(function () {
  $('#chpasswd-form').submit();
  return true;
});
$('#chpasswd-cancel').click(function () {
  $('#chpasswd-old').val('');
  $('#chpasswd-new').val('');
  $('#chpasswd-confirm').val('');
  return true;
});
$('.edit-link-modal').on('shown.bs.modal', function () {
  var linkInfo = getLinkInfo(this);
  $('#edit-link-save-' + linkInfo.id).click(function () {
    $('#edit-link-form-' + linkInfo.id).submit();
    return true;
  });
});
$('.delete-link').click(function () {
  var answer = confirm('Are you sure you want to delete this link?');
  if (answer) {
    var linkInfo = getLinkInfo(this);
    $('#' + linkInfo.action + '-form-' + linkInfo.id).submit();
  }
  return false;
});
$('.toggle-archive').click(function () {
  var linkInfo = getLinkInfo(this);
  console.log(linkInfo);
  $('#' + linkInfo.action + '-form-' + linkInfo.id).submit();
  return false;
});
