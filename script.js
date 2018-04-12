(function ($) {
    apiUrl = 'https://YOUR-GW-URL/test/ccbda-dynamoDB-python-CRUD';
    tableName = 'ccbda-example';

    // Load Table items when page loads
    // Call API Gateway GET Item
    $.ajax({
        url: apiUrl + "?" + $.param({TableName: tableName}),
        type: 'GET',
        crossDomain: true,
        success: function (result) {
            $.each(result.Items, function (i, item) {
                $('#items').append('<li>' + item.thingid.S + '</li>');
            });
        },
        error: function (result) {
            $('#error').toggle().append('<div>' + result.statusText + '</div>');
        }
    });

    // Form submit
    $("#form").submit(function (event) {
        event.preventDefault();
        thingid = $('#thingid').val();

        // Call API Gateway POST Item
        $.ajax({
            url: apiUrl,
            data: JSON.stringify({TableName: tableName, Item: {thingid: {S: thingid}}}),
            type: 'POST',
            crossDomain: true,
            success: function (result) {
                $('#thingid').val('');
                $('#items').append('<li>' + thingid + '</li>');
            },
            error: function (result) {
                $('#error').toggle().append('<div>' + result.statusText + '</div>');
            }
        });
    });

})(jQuery);