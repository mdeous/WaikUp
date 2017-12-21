function postLink() {
  $(this).parents().find('li.active').fadeOut();
  return false;
}

$(document).ready(() => {
  $('a.post-link').click(postLink);
});
