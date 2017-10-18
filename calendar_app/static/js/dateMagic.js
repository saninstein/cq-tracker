$(function () {
    dateMagic('#id_date');
    console.log("Magic!")
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
}/**
 * Created by Александр on 09.09.2017.
 */
