$(document).ready(function () {
    var csrf_token = $('meta[name=csrf-token]').attr('content');
    // Configure ajaxSetup so that the CSRF token is added to the header of every request
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    $("tr.table").mouseover(function () {
        console.log($(this));
        console.log($(this).attr('id'));
        id = $(this).attr('id')

        $.ajax({
            url: '/profile/edit',
            type: 'POST',
            data: JSON.stringify({ response: $(this).attr('id') }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (response) {
                console.log(response);

                $("p").text('');
                $("#p" + id).text(response.response);
            },
            // The function which will be triggered if any error occurs.
            error: function (error) {
                console.log(error);
            }
        });
    });

    $("tr.table").mouseleave(function () {
        console.log($(this));
        console.log($(this).attr('id'));
        id = $(this).attr('id')

        $.ajax({
            url: '/profile/edit',
            type: 'POST',
            data: JSON.stringify({ response: $(this).attr('id') }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (response) {
                console.log(response);

                $("p").text('');
            },
            // The function which will be triggered if any error occurs.
            error: function (error) {
                console.log(error);
            }
        });
    });
});

