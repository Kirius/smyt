$(function () {
    $("table.editable").on('click', 'td', function () {
        var cell = $(this)
        var OriginalContent = cell.text();
        cell.addClass("cellEditing");

        var input = $("<input type='text'>").val(OriginalContent);
        cell.html(input);
        input.focus();

        input.keypress(function (e) {
            if (e.which == 13) {
                cell.text(input.val());
                cell.removeClass("cellEditing");
            }
        });

        input.blur(function(){
            cell.text(OriginalContent);
            cell.removeClass("cellEditing");
        });
    });
});
