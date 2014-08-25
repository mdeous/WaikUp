/*
    WaikUp Global JavaScript
 */

function submitFormLink(aLinkID) {
    var linkID = aLinkID[aLinkID.length-1];
    var actionType = aLinkID[0];
    $('#'+actionType+'-form-'+linkID).submit();
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
$('#new-link-save').click(function() {
    $('#new-link-form').submit();
    return true;
});
$('#new-link-cancel').click(function() {
    $('#new-link-url').val('');
    $('#new-link-title').val('');
    $('#new-link-description').val('');
    return true;
});
$('#chpasswd-save').click(function() {
    $('#chpasswd-form').submit();
    return true;
});
$('#chpasswd-cancel').click(function() {
    $('#chpasswd-old').val('');
    $('#chpasswd-new').val('');
    $('#chpasswd-confirm').val('');
    return true;
});
$('.edit-link-modal').on('shown.bs.modal', function() {
    var modalID = this.getAttribute('id');
    var tmp_array = modalID.split('-');
    var link_id = tmp_array[tmp_array.length-1];
    $('#edit-link-save-'+link_id).click(function() {
        $('#edit-link-form-'+link_id).submit();
        return true;
    });
});
$('.delete-link').click(function(e) {
    var answer = confirm('Are you sure you want to delete this link?');
    if (answer) {
        var aLinkID = $(this).attr('id').split('-');
        submitFormLink(aLinkID);
    }
    return false;
});
$('.toggle-archive').click(function() {
    var aLinkID = $(this).attr('id').split('-');
    submitFormLink(aLinkID);
    return false;
});
