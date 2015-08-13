
// get source list
$.ajax({
    url: '/api/mirrors/list',
    type: 'get'
})
.done(function (resData) {
    //resData = JSON.parse(resData);
    showSourceList(resData);
})

// get notice
$.ajax({
    url: '/api/mirrors/notice',
    type: 'get'
})
.done(function (resData) {
    //resData = JSON.parse(resData);
    showNotice(resData);
})

// update status
//$.ajax({
//    url: '/api/mirrors/status',
//    type: 'get'
//})
//.done(function (resData) {
//    //resData = JSON.parse(resData);
//    updateStatus(resData);
//})

// show source list
function showSourceList(resData) {
    var length = resData.count;
    var data = resData.targets;

    

    for (var i = 0; i < length; ++i) {

        var newIcon = $('<span class="label label-new label-success">New</span>');

        var rowHTML = '<td class="name"><a></a></td><td class="last-update"></td><td class="statu"></td>';

        // node for statu
        var successLabel = $('<span class="label label-statu label-success">Success</span>');
        var unknownLabel = $('<span class="label label-statu label-default">Unknown</span>');
        var syclingLabel = $('<span class="label label-statu label-info">Syncing</span>');

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

        if (data[i].status == 100) $('.' + data[i].id).children('.statu').html(syclingLabel);
        if (data[i].status == 200) $('.' + data[i].id).children('.statu').html(successLabel);
        if (data[i].status == 300 || data[i].status == 400) $('.' + data[i].id).children('.statu').html(unknownLabel);

        // extra info
        if (data[i].comment == 'new') $('.' + data[i].id).children('.name').append(newIcon);
        if (data[i].help != '') {
            var help = $('<a class="help-icon" href="javascript:;" title="Help"></a>').append($('<span class="glyphicon glyphicon-question-sign"></span>'));
            help.attr('href', data[i].help);
            $('.' + data[i].id).children('.name').append(help);
        }
    }
}


// show notice
function showNotice(resData) {
    // if have new notice
    if (resData.count > 0) {
        $('.new-notice .notice-detail').html(resData.targets[0].notice);
        $('.new-notice').css('display', 'block');
    }
}


// update status
function updateStatus(resData) {
    var length = resData.count;
    var data = resData.targets;

    for (var i = 0; i < length; ++i) {
        // node for statu
        var successLabel = $('<span class="label label-statu label-success">Success</span>');
        var unknownLabel = $('<span class="label label-statu label-default">Unknown</span>');
        var syclingLabel = $('<span class="label label-statu label-info">Syncing</span>');
        // update last update
        $('.' + data[i].id).children('.last-update').html(data[i].last_update);
        // update statu
        if (data[i].status == 100) $('.' + data[i].id).children('.statu').html(syclingLabel);
        if (data[i].status == 200) $('.' + data[i].id).children('.statu').html(successLabel);
        if (data[i].status == 300 || data[i].status == 400) $('.' + data[i].id).children('.statu').html(syclingLabel);

    }
}

function showDownloadList(resData) {
    var length = resData.count;
    var data = resData.targets;

    for (var i = 0; i < length; ++i) {
        var item = $('<li></li>');
        var itemA = $('<a href="javascript:;"></a>');

        itemA.addClass(data[i].id);
        itemA.html(data[i].name);
        item.append(itemA);

        $('.release-selector').append(item);

        // when click release
        itemA.click(function () {
            $('.release-val').html(this.text);
            $('.version-btn').attr("disabled", false);

            showVersionList($(this).attr('class'), data);
        });

    }
}

function showVersionList(className, data) {
    // clear the childen
    $('.version-selector').html('');
    var index = -1;

    for (var i = 0; i < data.length; ++i) {
        if (data[i].id == className) {
            index = i;
            break;
        }
    }

    var length = data[i].count;
    var versionData = data[i].versions;
    
    for (var i = 0; i < length; ++i) {
        var item = $('<li></li>');
        var itemA = $('<a href="javascript:;"></a>');

        itemA.addClass(versionData[i].version);
        itemA.html(versionData[i].version);
        item.append(itemA);

        $('.version-selector').append(item);

        // when click release
        itemA.click(function () {
            $('.version-val').html(this.text);
            $('.download-btn').attr("disabled", false);

            // set download url
            var downloadURL = '';
            var versionNumber = $(this).attr('class');
            for (var j = 0; j < length; ++j) {
                //console.log(versionData[j]);
                if (versionNumber == versionData[j].version) {
                    downloadURL = versionData[j].url;
                }
            }

            // remove linsten first
            $('.download-btn').unbind("click");

            // add listen to download buttom
            $('.download-btn').click(function () {
                console.log('a')
                window.open(downloadURL);
            })
        });

    }
}

// listenEvent
$('.os-so-selector a').click(function () {

    $('.os-so-val').html(this.text);

    var url = '';
    if (this.text == '系统') url = '/api/mirrors/oses';
    if (this.text == '软件') url = '/api/mirrors/osses';

    $('.release-btn').attr("disabled", false);

    $('.release-selector').append($('<li>加载中...</li>'));
    // ask the list
    //$.ajax({
    //    url: url,
    //    type: 'get'
    //})
    //.done(function (resData) {
    //    $('.release-selector').html('');
    //    var resData = {

    //        "count": 1,
    //        "targets": [{
    //            "id": "archlinux",
    //            "name": "Arch Linux",
    //            "url": "http://b.mirrors.lanunion.org/archlinux",
    //            "type": "os",
    //            "count": 3,
    //            "versions": [{ "version": "2015.08.01", "url": "http://b.mirrors.lanunion.org/archlinux/iso/2015.08.01/archlinux-2015.08.01-dual.iso" },
    //                         { "version": "2015.07.01", "url": "http://b.mirrors.lanunion.org/archlinux/iso/2015.07.01/archlinux-2015.07.01-dual.iso" },
    //                         { "version": "2015.06.01", "url": "http://b.mirrors.lanunion.org/archlinux/iso/2015.07.01/archlinux-2015.07.01-dual.iso" }]
    //        }
    //        ]


    //    }
    //    showDownloadList(resData);
    //});
    
    $('.release-selector').html('');
    var resData = {

        "count": 2,
        "targets": [{
            "id": "archlinux",
            "name": "Arch Linux",
            "url": "http://b.mirrors.lanunion.org/archlinux",
            "type": "os",
            "count": 3,
            "versions": [{ "version": "2015.08.01", "url": "http://b.mirrors.lanunion.org/archlinux/iso/2015.08.01/archlinux-2015.08.01-dual.iso" },
                         { "version": "2015.07.01", "url": "http://b.mirrors.lanunion.org/archlinux/iso/2015.07.01/archlinux-2015.07.01-dual.iso" },
                         { "version": "2015.06.01", "url": "http://b.mirrors.lanunion.org/archlinux/iso/2015.07.01/archlinux-2015.07.01-dual.iso" }]
        },
        {
            "id": "linux",
            "name": "Linux",
            "url": "http://b.mirrors.lanunion.org/archlinux",
            "type": "os",
            "count": 3,
            "versions": [{ "version": "1", "url": "http://b.mirrors.lanunion.org/archlinux/iso/2015.08.01/archlinux-2015.08.01-dual.iso" },
                         { "version": "2", "url": "http://b.mirrors.lanunion.org/archlinux/iso/2015.07.01/archlinux-2015.07.01-dual.iso" },
                         { "version": "3", "url": "http://b.mirrors.lanunion.org/archlinux/iso/2015.07.01/archlinux-2015.07.01-dual.iso" }]
        }
        ]


    }
    showDownloadList(resData);
})

$('.release-selector a').click(function () {

    $('.release-val').html(this.text);

    $('.version-btn').attr("disabled", false);
})

$('.version-selector a').click(function () {

    $('.version-val').html(this.text);

    $('.download-btn').attr("disabled", false);
})