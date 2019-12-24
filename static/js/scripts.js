var onSubmit = function () {
  $.post("add", {
      nickname: $('#nickname').val(),
      content: $('#content').val(),
      remark: $('#remark').val(),
      recaptcha: grecaptcha.getResponse()
    }, function(data, status) {
      $('#nickname').val("");
      $('#content').val("");
      $('#remark').val("");
      $("#dialog").modal('hide');
  });
}

$(document).ready(function() {
  // var socket = io.connect(window.location.href);
  var last = null;
  /*socket.on('recordUpdate', function(data) {
    record = toRecord(data);
    $('#records').prepend(record);
  });*/
  function getRecords(number, callback) {
    $.ajax({
      url: 'query',
      type: "get",
      data: {
        since: last,
        number: number
      },
      success: function(response) {
        callback(null, response);
      },
      error: function(err) {
        callback(err, null);
      }
    });
  }
  function toRecord(data) {
    let date = new Date(data.timestamp);
    let record = `
<div class="info-tile">
  <div class="tile-heading">
    ${data.nickname}
    <small>${date.toLocaleString()} ${data.remark}</small>
  </div>
  <div class="tile-body">
    <p>${data.content.replace(/\n+/g, '<br/>')}</p>
  </div>
</div>`;
    return record;
  }

  $("#dialog").on('shown.bs.modal', function (e) {
    $("#submit").click(function(e) {
      e.preventDefault();
      grecaptcha.execute();
    });
  });

  $('.footer').waypoint(function() {
    $('.loader-wrapper').fadeIn();
    getRecords(5, function (err, response) {
      if(!err) {
        $('.loader-wrapper').fadeOut();
        var len = response.length;
        if (len > 0) {
          last = response[0].timestamp;
          for (var i = 0; i < len; i++) {
            record = toRecord(response[i]);
            $('#records').append(record);
          }
        }
      }
    });
  }, {
    offset: 'bottom-in-view'
  });
});
