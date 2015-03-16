//var baseUrl = "https://mirrors.cqu.edu.cn"
var baseUrl = "./"

$.ajax({
    url: baseUrl + '/index.json',
    type: 'get'
})
.done(function (resData) {
    renderIndex(JSON.parse(resData));
});

function renderIndex(resData)
{
    showNotice(resData.notice)
    showSourceList(resData.mirrorlist);
}

// get notice
// $.ajax({
//     url: '/api/mirrors',
//     type: 'get'
// })
// .done(function (resData) {
//     //resData = JSON.parse(resData);
//     showNotice(resData);
// });

// update status
// setInterval(function () {
//     $.ajax({
//         url: '/api/mirrors/status',
//         type: 'get'
//     })
//     .done(function (resData) {
//         //resData = JSON.parse(resData);
//         updateStatus(resData);
//     })
// }, 10000);

// show source list
function showSourceList(resData)
{
    var length = resData.count;
    var data = resData.targets;

    for (var i = 0; i < length; ++i) {

        var newIcon = $('<span class="label label-new label-success">New</span>');

        var rowHTML = $('<td class="name"><a></a></td><td class="last-update"></td><td class="statu"></td>');

        // node for statu
        var successLabel = $('<span class="label label-statu label-success">Success</span>');
        var unknownLabel = $('<span class="label label-statu label-default">Unknown</span>');
        var syclingLabel = $('<span class="label label-statu label-info">Syncing</span>');

        // create a row node
        var row = $("<tr></tr>");
        row.html(rowHTML);
        row.addClass(data[i].cname);
        // console.log(data[i].cname);

        // append the row to the table
        $('.the-list').append(row);

        // update the row's info
        $('.' + data[i].cname).children('.name').children('a').html(data[i].cname);
        $('.' + data[i].cname).children('.name').children('a').attr('href', data[i].url);
        $('.' + data[i].cname).children('.last-update').append(data[i].synced_at);

        // update status
        if (data[i].status == 100) {
            $('.' + data[i].cname).children('.statu').html(syclingLabel);
        } else if (data[i].status == 200) {
            $('.' + data[i].cname).children('.statu').html(successLabel);
        } else {
            if (data[i].status == 300) unknownLabel.html('Freeze');
            if (data[i].status == 400) unknownLabel.html('Failed');

            $('.' + data[i].cname).children('.statu').html(unknownLabel);
        }

        // extra info
        if (data[i].has_comment) {
            if (data[i].comment == 'new') $('.' + data[i].cname).children('.name').append(newIcon);
        }

        if (data[i].has_help) {
            var help_url = $('<a class="help-icon" href="javascript:;" title="Help"></a>').append($('<span class="glyphicon glyphicon-question-sign"></span>'));
            help_url.attr('href', data[i].help_url);
            $('.' + data[i].cname).children('.name').append(help_url);
        }
    }
}


// show notice
function showNotice(resData) {
    // if have new notice
    if (resData.count > 0) {
        // not just one notice
        var string = '';
        for (var i = 0; i < resData.count; ++i) {
            string += resData.targets[i].notice;
            if (i != resData.count - 1) {
                string += '</br>';
            }
        }
        $('.new-notice .notice-detail').html(string);
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
        var unknownLabel = $('<span class="label label-statu label-default"></span>');
        var syclingLabel = $('<span class="label label-statu label-info">Syncing</span>');
        // update last update
        $('.' + data[i].name).children('.last-update').html(data[i].last_sync);
        // update statu
        if (data[i].status == 100) $('.' + data[i].name).children('.statu').html(syclingLabel);
        else if (data[i].status == 200) $('.' + data[i].name).children('.statu').html(successLabel);
        else {
            if (data[i].status == 300) unknownLabel.html('Freeze');
            if (data[i].status == 400) unknownLabel.html('Failed');
            if (data[i].status == 500) unknownLabel.html('Unknown');
            $('.' + data[i].name).children('.statu').html(unknownLabel);
        }
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
    $.ajax({
        url: url,
        type: 'get'
    })
    .done(function (resData) {
        $('.release-selector').html('');
        showDownloadList(resData);
    });

    //$('.release-selector').html('');
    //var resData = {

    //    "count": 2,
    //    "targets": [{
    //        "id": "archlinux",
    //        "name": "Arch Linux",
    //        "url": "http://b.mirrors.lanunion.org/archlinux",
    //        "type": "os",
    //        "count": 3,
    //        "versions": [{ "version": "2015.08.01", "url": "http://b.mirrors.lanunion.org/archlinux/iso/2015.08.01/archlinux-2015.08.01-dual.iso" },
    //                     { "version": "2015.07.01", "url": "http://b.mirrors.lanunion.org/archlinux/iso/2015.07.01/archlinux-2015.07.01-dual.iso" },
    //                     { "version": "2015.06.01", "url": "http://b.mirrors.lanunion.org/archlinux/iso/2015.07.01/archlinux-2015.07.01-dual.iso" }]
    //    },
    //    {
    //        "id": "linux",
    //        "name": "Linux",
    //        "url": "http://b.mirrors.lanunion.org/archlinux",
    //        "type": "os",
    //        "count": 3,
    //        "versions": [{ "version": "1", "url": "http://b.mirrors.lanunion.org/archlinux/iso/2015.08.01/archlinux-2015.08.01-dual.iso" },
    //                     { "version": "2", "url": "http://b.mirrors.lanunion.org/archlinux/iso/2015.07.01/archlinux-2015.07.01-dual.iso" },
    //                     { "version": "3", "url": "http://b.mirrors.lanunion.org/archlinux/iso/2015.07.01/archlinux-2015.07.01-dual.iso" }]
    //    }
    //    ]


    //}
    //showDownloadList(resData);
});
