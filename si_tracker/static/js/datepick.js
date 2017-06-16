/**
 * Created by Александр on 16.06.2017.
 */

$(function () {
    var def = dateConvert($('#id_date_due').val());
    $('#datetimepicker1').datetimepicker({
        format: 'DD/MM/YYYY'
    });
    $('#id_date_due').val(def);

    function dateConvert(dateStr) {
        if(!dateStr)
            return dateStr;
        var dateAr = dateStr.split('-');
        dateAr.reverse();
        return dateAr.join('/');
    }
});
