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

    // If the user clicks on an artist, show the page
    // appropriate items belonging to that artist
    $("p.artist").on('click', function () {
        console.log($(this));
        console.log($(this).attr('id'));

        $.ajax({
            url: '/select',
            type: 'POST',
            data: JSON.stringify({ id: $(this).attr('id') }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (response) {
                console.log(response);
                prev = $(response).attr('prev');
                id = $(response).attr('id');

                // Clear default and previous table
                $('#artist_table').text('');
                $('#artist_table' + prev).text('');

                // Add the default item table
                $('#artist_table').append($("\
                    <div class='row align-items-end'>\
                        <div class='col-10'>\
                            </br>\
                            <h2><b>"+ $(response).attr('type') + " by</br><i>" +
                    $(response).attr('artist') + "</i></b></h2>\
                        </div>\
                        <div class='col-2 text-center'>\
                            <h5><b>Score</b></h5>\
                        </div>\
                    </div>"));
                // For each item, add it to the table
                $.each($(response).attr('data'), function (ind, item) {
                    let score = item['score'];
                    if (score == null) score = "N/A";
                    $('#artist_table').append($("\
                    <div class='row'>\
                        <div class='col-10 bg-info text-white rounded border'>\
                            <h3>" + item['title'] + "</h3>\
                        </div>\
                        <div class='col-2 bg-info text-white rounded border text-center'>\
                            <h5>" + score + "</h5>\
                        </div>\
                    </div>"));
                });

                // Add item table under the specific album for mobile
                $('#artist_table' + id).append($("\
                    <div class='row align-items-end'>\
                        <div class='col-10'>\
                            </br>\
                            <h2><b>"+ $(response).attr('type') + " by</br><i>" +
                    $(response).attr('artist') + "</i></b></h2>\
                        </div>\
                        <div class='col-2 text-center'>\
                            <h5><b>Score</b></h5>\
                        </div>\
                    </div>"));
                // For each item, add it to the mobile table
                $.each($(response).attr('data'), function (ind, item) {
                    let score = item['score'];
                    if (score == null) score = "N/A";
                    $('#artist_table' + id).append($("\
                    <div class='row'>\
                        <div class='col-10 bg-info text-white rounded border'>\
                            <h3>" + item['title'] + "</h3>\
                        </div>\
                        <div class='col-2 bg-info text-white rounded border text-center'>\
                            <h5>" + score + "</h5>\
                        </div>\
                    </div>"));
                });
            },
            // The function which will be triggered if any error occurs.
            error: function (error) {
                console.log(error);
            }
        });
    });
});

