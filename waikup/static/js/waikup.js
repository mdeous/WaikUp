/*
    WaikUp Global JavaScript
 */

hasClassName = function(element, cls) {
    return (' '+element.className+' ').indexOf(' '+cls+' ') > -1;
}

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
    $('.collapse.out').removeClass('out').addClass('in');
});
$('.collapse-all').click(function() {
    $('.collapse.in').removeClass('in').addClass('out');
});
$('#newlink-save').click(function() {
    $('#new-link-form').submit();
    return true;
});
$('#newlink-cancel').click(function() {
    $('#link-url').val('');
    $('#link-title').val('');
    $('#link-desc').val('');
    return true
});
$('#chpasswd-save').click(function() {
    $('#chpasswd-form').submit();
    return true;
});
$('#chpasswd-cancel').click(function() {
    $('#old-password').val('');
    $('#new-password').val('');
    $('#confirm-password').val('');
});
