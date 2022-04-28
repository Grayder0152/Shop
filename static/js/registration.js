$(document).ready(function () {
    validateRegistration()
});

function validateRegistration() {
    checkUsernameExist()
    validatePasswords();
    validatePhone()
    validateEmail()
}


function checkUsernameExist() {
    $('#id_username').blur(function () {
        let data = {
            username: $(this).val()
        }
        $.ajax({
            method: "GET",
            dataType: "json",
            data: data,
            success: function (response) {
                changeFieldStyle($('#id_username'), !response['is_exist'], 'Пользователь с таким логином уже существует!')
            }
        });
    });
}



