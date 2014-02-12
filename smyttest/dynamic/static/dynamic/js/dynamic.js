$(function () {
    var current_model;

    $.ajaxSetup({
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name=csrfmiddlewaretoken]').val());
        }
    });

    function getData(model) {
        $.getJSON('/dynamic/api/get', {'model': model}).success(function(data) {
            if (!data.success) {
                showMessage('There was an error during getting data', true);
                return;
            }
            var headers = data.headers;
            var rows = data.rows;
            var cur_row = $('<tr></tr>');
            // fill in table headers
            for (var name in headers) {
                $('<th></th>').text(headers[name][0]).appendTo(cur_row);
                // create inputs for new record
                var new_input = $("<input type='text'>")
                    .attr('name', name)
                    .data('type', headers[name][1])
                    .appendTo('#new_record')
                    .before("<span>" + headers[name][0] + "</span>")
                    .focus(function () {
                        $(this).removeClass('invalid');
                    });
                if (new_input.data('type') === 'date') {
                    new_input.datepicker({'dateFormat': 'yy-mm-dd'});
                }
            }
            $('table.editable').empty().append(cur_row);
            // fill in received data in table rows
            for (var i = 0; i < rows.length; i++) {
                var cur_row = $('<tr></tr>').data('id', rows[i].id);
                for (var name in headers) {
                    $('<td></td>').text(rows[i][name])
                        .data('type', headers[name][1])
                        .data('field', name)
                        .appendTo(cur_row);
                }
                $('table.editable').append(cur_row);
            }


        })
    }

    function showMessage(text, error){
        var msg = $('#message')
        if (error) {
            msg.addClass('error');
        } else {
            msg.removeClass('error');
        }
        msg.text(text).show().fadeOut(2000);
    }

    function updateRecord(cell) {
        var data = {
            'model': current_model,
            'id': cell.parent().data('id'),
            'field': cell.data('field'),
            'value': cell.text()
        }
        $.post('/dynamic/api/update', data).success(function(data) {
            if (!data.success) {
                showMessage('There was an error during update', true);
            } else {
                showMessage('Record has been successfully updated', false);
            }
        })
    }

    function insertRecord(params) {
        $.post('/dynamic/api/insert', params).success(function(data) {
            if (!data.success){
                showMessage('There was an error during insert', true);
            } else {
                $('#models a#' + current_model).click();
                showMessage('Record has been successfully inserted', false);
            }
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
        var type = cell.data('type');
        var original_data = cell.text();
        var input = $("<input type='text'>").val(original_data)
            .width(cell.width());

        if (type === 'date') {
            input.datepicker({'onSelect': function() {
                input.datepicker('hide');
                if (validate(input.val(), 'date')) {
                    original_data = input.val();
                    cell.text(input.val());
                    updateRecord(cell);
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
                    updateRecord(cell);
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
        $('#new_record').empty();
        current_model = $(this).attr('id')
        getData(current_model);
    });
    // load first model
    $('#models a:first').click();

    // validate fields and insert new record
    $('#submit').click(function() {
        var valid = true;
        $('#new_record input').each(function() {
            var elm = $(this);
            if (!validate(elm.val(), elm.data('type'))) {
                elm.addClass('invalid');
                valid = false;
            }
        });
        if (valid) {
            var params = $('#new_record').serialize() + '&model=' + current_model;
            insertRecord(params);
        }
    })

});

