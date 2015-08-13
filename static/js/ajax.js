
// get source list
$.ajax({
    url: '/api/mirrors/list',
    type: 'get'
})
.done(function (resData) {
    resData = JSON.parse(resData);
    showSourceList(resData);
})

// get notice
$.ajax({
    url: '/api/mirrors/notice',
    type: 'get'
})
.done(function (resData) {
    resData = JSON.parse(resData);
    showNotice(resData);
})

// update status
$.ajax({
    url: '/api/mirrors/status',
    type: 'get'
})
.done(function (resData) {
    resData = JSON.parse(resData);
    updateStatus(resData);
})

// get quick download
$.ajax({
    url: '/api/mirrors/downloads',
    type: 'get'
})
.done(function (resData) {
    resData = JSON.parse(resData);
    showDownloadList(resData);
})

// show source list
function showSourceList(resData) {
    var length = resData.count;
    var data = resData.targets;

    var newIcon  = $('<span class="label label-new label-success">New</span>');
    var helpIcon = $('<a class="help-icon" href="javascript:;" title="Help"></a>').append($('<span class="glyphicon glyphicon-question-sign"></span>'));
    var rowHTML = '<td class="name"><a></a></td><td class="last-update"></td><td class="statu"></td>';

    // node for statu
    var successLabel = $('<span class="label label-statu label-success">Success</span>');
    var unknownLabel = $('<span class="label label-statu label-default">Unknown</span>');
    var syclingLabel = $('<span class="label label-statu label-info">Syncing</span>');

    for (var i = 0; i < count; ++i) {
        // create a row node
        var row = $("<tr></tr>");
        row.html(rowHTML);
        row.addClass(data[i].id);

        // append the row to the table
        $('.the-list').append(row);

        // update the row's info
        $('.' + data[i].id).children('.name').children('a').append(data[i].name);
        $('.' + data[i].id).children('.name').children('a').attr('href', data[i].url);
        $('.' + data[i].id).children('.last-update').append(data[i].last_update);

        if (data[i].status == 100) $('.' + data[i].id).children('.statu').append(syclingLabel);
        if (data[i].status == 200) $('.' + data[i].id).children('.statu').append(successLabel);
        if (data[i].status == 300 || data[i].status == 400) $('.' + data[i].id).children('.statu').append(syclingLabel);

        // extra info
        if (data[i].comment == 'new') $('.' + data[i].id).children('.name').append(newIcon);
        if (data[i].help) {
            help = helpIcon; // new one
            help.attr('href', data[i].help);
            $('.' + data[i].id).children('.name').append(help);
        }
    }
}


// show notice
function showNotice(resData) {
    // if have new notice
    if (resData.count > 0) {
        $('.new-notice .notice-detail').html(resData.targets[i].notice);
        $('.new-notice .notice-detail').css('display', 'block');
    }
}


// update status
function updateStatus(resData) {
    var length = resData.count;
    var data = resData.targets;

    for (var i = 0; i < length; ++i) {
        // update last update
        $('.' + data[i].id).children('.last-update').html(data[i].last_update);
        // update statu
        if (data[i].status == 100) $('.' + data[i].id).children('.statu').html(syclingLabel);
        if (data[i].status == 200) $('.' + data[i].id).children('.statu').html(successLabel);
        if (data[i].status == 300 || data[i].status == 400) $('.' + data[i].id).children('.statu').html(syclingLabel);

    }
}