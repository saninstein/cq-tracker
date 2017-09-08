/**
 * Created by Александр on 16.06.2017.
 */

$(function () {
    dateMagic('#id_date_due');
    dateMagic('#id_date');
});


function dateMagic(item) {
    var def = dateConvert($(item).val());
    $('#datetimepicker1').datetimepicker({
        format: 'DD/MM/YYYY'
    });
    $(item).val(def);

    function dateConvert(dateStr) {
        if(!dateStr)
            return dateStr;
        var dateAr = dateStr.split('-');
        dateAr.reverse();
        return dateAr.join('/');
    }
}