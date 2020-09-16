$(document).ready(function() {
    var titleFilter = ''
    var oldDateFilter = ''
    var newDateFilter = ''
    var url = $('form.filter-picker').attr('action') + $('div.account-header').attr('id') + '/';
    $('#title-picker').change(function() {
        console.log(url)
        if ($('#title-picker').val() == '') {
            $('form.filter-picker').attr('action', $('form.filter-picker').attr('action').replace(titleFilter, ''))
        } else {
            url = $('form.filter-picker').attr('action');
            titleFilter = $('#title-picker').val()
            url = url + '/' + titleFilter;
            $('form.filter-picker').attr('action', url);
        }
    });
    $('#date-picker').change(function() {
        url = $('form.filter-picker').attr('action') + $('div.account-header').attr('id') + '/';
        newDateFilter = $('#date-picker').val()
        if (oldDateFilter == '' ) {
            $('form.filter-picker').attr('action', url + newDateFilter);
            oldDateFilter = newDateFilter
        } else {
            url = $('form.filter-picker').attr('action');
            url = url.replace(oldDateFilter, newDateFilter);
            $('form.filter-picker').attr('action', url)
        }
    });
});

