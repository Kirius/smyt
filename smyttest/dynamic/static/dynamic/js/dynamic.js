$(function () {
    var current_model;

    $.ajaxSetup({
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name=csrfmiddlewaretoken]').val());
        }
    });

    function getData(model) {
        $.getJSON('/dynamic/api/get', {'model': model}).success(function(data) {
            var headers = data.headers;
            var rows = data.rows;
            var cur_row = $('<tr></tr>');
            // fill in table headers
            for (var name in headers) {
                $('<th></th>').text(headers[name][0]).appendTo(cur_row);
            }
            $('table.editable').empty().append(cur_row);
            // fill in received data in table rows
            for (var i = 0; i < rows.length; i++) {
                var cur_row = $('<tr></tr>').prop('id', rows[i].id);
                for (var name in headers) {
                    $('<td></td>').text(rows[i][name])
                        .prop('type', headers[name][1])
                        .prop('field', name)
                        .appendTo(cur_row);
                }
                $('table.editable').append(cur_row);
            }
        })
    }

    function updateOnServer(cell) {
        var data = {
            'model': current_model,
            'id': cell.parent().prop('id'),
            'field': cell.prop('field'),
            'value': cell.text()
        }
        $.post('/dynamic/api/update', data).success(function () {
            $('#message').removeClass('error')
                .text('Record has been successfully updated')
                .show()
                .fadeOut(2000)
        }).error(function () {
            $('#message').addClass('error')
                .text('There was an error during update')
                .show()
                .fadeOut(2000)
        })
    }

    function validate(value, type){
        if (type === 'date'){
            var date = new Date(value);
            return !isNaN(date);
        }
        if (type === 'int'){
            var re = /\D+/;
            return !re.test(value);
        }
        return true;
    }


    // make data editable
    $("table.editable").on('click', 'td', function () {
        var cell = $(this);
        var type = cell.prop('type');
        var original_data = cell.text();
        var input = $("<input type='text'>").val(original_data)
            .width(cell.width());

        if (type === 'date') {
            input.datepicker({'onSelect': function() {
                input.datepicker('hide');
                if (validate(input.val(), 'date')) {
                    original_data = input.val();
                    cell.text(input.val());
                    updateOnServer(cell);
                }
            },
            'onClose': function() {
                cell.text(original_data);
                cell.off('click');
            },
            'dateFormat': 'yy-mm-dd'});
        }
        cell.html(input);
        cell.click(function(e){
            e.stopPropagation();
        });
        input.focus();

        input.keypress(function (e) {
            if (e.which === 13 && type !== 'date')  {
                if (validate($.trim(input.val()), type)) {
                    cell.text(input.val());
                    cell.off('click');
                    updateOnServer(cell);
                } else {
                    input.addClass('invalid');
                }
            }
        });

        input.blur(function(){
            if (type !== 'date') {
                cell.text(original_data);
                cell.off('click');
            }
        });
});

    // load model on click
    $('#models a').click(function() {
        current_model = $(this).attr('id')
        getData(current_model);
    });
    // load first model
    $('#models a:first').click();

});

