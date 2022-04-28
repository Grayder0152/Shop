$(document).ready(function () {
    autoSetFields();
    validateOrder();
});

function validateOrder() {
    checkDate();
    validatePhone();
    $('#make_order_btn').click(function () {
        $("input[required]").each(function () {
            if ($(this).val().length === 0) {
                $(this).addClass("invalid");
            }
        });
    });
}

function checkDate() {
    $('#id_order_date').blur(function () {
        let data = {
            date: $(this).val()
        }
        $.ajax({
            method: "GET",
            dataType: "json",
            data: data,
            success: function (response) {
                changeFieldStyle($('#id_order_date'), response['is_correct'], 'Дата отправки должна быть больше сегоднешней!')
            }
        });
    });
}

function autoSetFields() {
    let data = {
        user: true
    }
    $.ajax({
        method: "GET",
        dataType: "json",
        data: data,
        success: function (response) {
            setField($('#id_first_name'), response['first_name'])
            setField($('#id_last_name'), response['last_name'])
            setField($('#id_phone'), response['phone'])
            setField($('#id_address'), response['address'])
        }
    });
}

function setField(field, value) {
    if (value) {
        field.val(value);
    }
}