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
                $("#p" + id).append($("<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" \
                fill=\"currentColor\" class=\"bi bi-gear-fill\" viewBox=\"0 0 16 16\">\
                <path d=\"M9.405 1.05c-.413-1.4-2.397-1.4-2.81 0l-.1.34a1.464 1.464 0 0 1-2.105.872l-.31-.17c-1.283-.698-2.686.705-1.987 \
                1.987l.169.311c.446.82.023 1.841-.872 2.105l-.34.1c-1.4.413-1.4 2.397 0 2.81l.34.1a1.464 1.464 0 0 1 .872 \
                2.105l-.17.31c-.698 1.283.705 2.686 1.987 1.987l.311-.169a1.464 1.464 0 0 1 2.105.872l.1.34c.413 1.4 2.397 \
                1.4 2.81 0l.1-.34a1.464 1.464 0 0 1 2.105-.872l.31.17c1.283.698 2.686-.705 1.987-1.987l-.169-.311a1.464 1.464 \
                0 0 1 .872-2.105l.34-.1c1.4-.413 1.4-2.397 0-2.81l-.34-.1a1.464 1.464 0 0 \
                1-.872-2.105l.17-.31c.698-1.283-.705-2.686-1.987-1.987l-.311.169a1.464 1.464 \
                0 0 1-2.105-.872l-.1-.34zM8 10.93a2.929 2.929 0 1 1 0-5.86 2.929 2.929 0 0 1 0 5.858z\"/>\
                </svg>"));
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

