function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function getCookie(name) {
    let cookieVal = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = jQuery.trim(cookie);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieVal = decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
    }
    return cookieVal;
}

function postLink() {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });
    let postURL = this.getAttribute('data-url');
    $.post(postURL, null, () => {
        $(this).parent().parent().fadeOut();
    });
    console.log(postURL);
    return false;
}

function closeNewLinkModal() {
    return true;
}

$(document).ready(() => {
    $('#new-link-close').click(closeNewLinkModal);
    $('#new-link-save').click(postLink);
    $('.modal').modal();
    $('select').material_select();
});
