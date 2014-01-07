$('.collapser').click(function() {
    var itemSelector = 'div#'+$(this).attr('id');
    if ($(itemSelector).hasClass('out')) {
        $(itemSelector).addClass('in');
        $(itemSelector).removeClass('out');
    } else {
        $(itemSelector).addClass('out');
        $(itemSelector).removeClass('in');
    }
});
$('.expand-all').click(function() {
    $('.collapse.out').addClass('in');
    $('.collapse.out').removeClass('out');
});
$('.collapse-all').click(function() {
    $('.collapse.in').addClass('out');
    $('.collapse.in').removeClass('in');
});
$('#new-link-save').click(function() {
    $('#new-link-form').submit();
    return true;
});
$('#new-link-cancel').click(function() {
    $('#link-url').val('');
    $('#link-title').val('');
    $('#link-desc').val('');
    return true
});
