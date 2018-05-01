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

$(document).ready(() => {
    // initialize Semantic UI plugins
    $('.ui.dropdown').dropdown();
    $('.ui.modal').modal();
    $('.ui.accordion').accordion();
    // custom events
    $('.ui.message i.close').click((ev) => { $(ev.currentTarget).closest('.message').transition(); });
    $('button#new-link-btn').click(() => { $('.ui.modal#new-link-modal').modal('show') });
    $('a#profile-link').click(() => { $('.ui.modal#profile-modal').modal('show') });
    $('button#new-link-save').click(postLink);
    // $('select').material_select();
});
