$(document).ready(function () {
    validateOrder();
});

function validateOrder() {
    let phone_pattern = /(\+380\d{9}$)/;
    $("input[required]").each(function () {
        $(this).change(function () {
            console.log('Val');
            if ($(this).val().length < 3) {
                $(this).addClass("invalid");
            } else {
                $(this).removeClass("invalid");
            }
        })
    });
    $('#make_order_btn').click(function () {
        $("input[required]").each(function () {
            if ($(this).val().length === 0) {
                $(this).addClass("invalid");
            }
        });
    });
    $('#id_phone').change(function () {
        console.log(phone_pattern.test($(this).val()))
        if (!phone_pattern.test($(this).val())) {
            $(this).addClass("invalid");
        } else {
            $(this).removeClass("invalid");
        }
    })

    $('#id_order_date').blur(function () {
        let data = {
            date: $(this).val()
        }
        $.ajax({
            method: "GET",
            dataType: "json",
            data: data,
            success: function (response) {
                if (response['is_correct']) {
                    $('#id_order_date').removeClass('invalid');
                } else {
                    $('#id_order_date').addClass('invalid');
                    let message = 'Дата отправки должна быть больше сегоднешней!'
                    $('#title').after(
                        "<div class=\"alert alert-danger alert-dismissible fade show\" role=\"alert\">\n" +
                        "    <strong>" + message + "</strong>\n" +
                        "    <button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\">\n" +
                        "        <span aria-hidden=\"true\">&times;</span>\n" +
                        "    </button>\n" +
                        "</div>"
                    );
                }
                $('#make_order_btn').prop("disabled", !response['is_correct']);
            }
        });
    });
}