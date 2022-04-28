function addAlert(message) {
    $('#alerts').prepend(
        "<div class=\"alert alert-danger alert-dismissible fade show\" role=\"alert\">\n" +
        "    <strong>" + message + "</strong>\n" +
        "    <button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\">\n" +
        "        <span aria-hidden=\"true\">&times;</span>\n" +
        "    </button>\n" +
        "</div>"
    );
    setTimeout(function () {
        $('#alerts').children(".alert:last").remove();
    }, 5000);
    $('body, html').scrollTop(0);
}

function changeFieldStyle(field, is_valid, message = null) {
    if (is_valid) {
        field.removeClass("invalid");
    } else {
        field.addClass("invalid");
        if (message) {
            addAlert(message)
        }
    }
    $('.btn-success[type="submit"]').prop("disabled", !is_valid);
}

function validatePasswords() {
    $("#id_password").blur(function () {
        let is_valid = $(this).val().length > 5;
        changeFieldStyle($(this), is_valid, 'Минимальная длина пароля 6 символов.')
    });
    $("#id_confirm_password").blur(function () {
        let is_valid = $("#id_password").val() === $('#id_confirm_password').val();
        changeFieldStyle($(this), is_valid, 'Пароли не совпадают.')
    });
}


function validatePhone() {
    let phone_pattern = /(\+380\d{9}$)/;
    $('#id_phone').change(function () {
        let is_valid = phone_pattern.test($(this).val())
        changeFieldStyle($(this), is_valid, 'Некорректный номер!')
    })
}

function validateEmail() {
    let email_pattern = /^\S+@\S+\.\S+$/;
    $('#id_email').change(function () {
        let is_valid = email_pattern.test($(this).val())
        changeFieldStyle($(this), is_valid, 'Некорректный емайл!')
    })
}