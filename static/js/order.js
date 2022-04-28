$(document).ready(function () {
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