(function() {
  var url = 'http://' + document.domain + ':' + location.port
  var socket = io.connect(url);

  var videoArea = document.querySelector("video");
  //var videoSelect = document.querySelector('#camera');
  var profilePicCanvas = document.querySelector("#profilePicCanvas");
  var videoTag = document.querySelector("#videoTag");

  var width = 160; //Desired width of the picture
  var height = 0; //Calculated later based on image ratio
  var streaming = false; //Used to determine when the video has loaded

  videoTag.addEventListener('canplay', function(ev){
      if (!streaming) {
          height = videoTag.videoHeight / (videoTag.videoWidth/width);
          
              // Firefox currently has a bug where the height can't be read from
              // the video, so we will make assumptions if this happens.

              if (isNaN(height)) {
                  height = width / (3/4);
              }
          
              videoTag.setAttribute('width', width);
              videoTag.setAttribute('height', height);
              profilePicCanvas.setAttribute('width', width);
              profilePicCanvas.setAttribute('height', height);
              streaming = true;
      }
  }, false);

  function takePhoto() {
      var context = profilePicCanvas.getContext('2d');
      if (width && height) {
          context.drawImage(videoTag, 0, 0, width, height);

          var data = profilePicCanvas.toDataURL('image/png');
          socket.emit('stream', data);
      }
  }

  table = $('#events')
    .DataTable({
        pageLength: 8,
        searching: false,
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.10.16/i18n/Spanish.json'
        },
        ordering: false
    });

  socket.on('face', function(name) {
      if (name !== null) {
        if (isValidName(name)) {
          console.log(`I detect ${name}'s face`)
          greenStatus();
          date = moment();
          name = toTitleCase(name)
          table.row.add([
              date.format('dddd, D [de] MMMM [de] YYYY hh:mm A'),
              name
          ]).draw(false);
          sendEvent({ date: date.format('X'), name: name })
        } else {
          console.log("I'm detecting somebody, but I don't know who is it.")
          redStatus();
        }
      } else {
        console.log('There is no faces.')
        blackStatus();
      }
  })

  function greenStatus() {
    $('.ion-camera').addClass('green-text');
    $('.ion-camera').removeClass('red-text');
    $('.ion-camera').removeClass('black-text');
  }

  function redStatus() {
    $('.ion-camera').addClass('red-text');
    $('.ion-camera').removeClass('black-text');
    $('.ion-camera').removeClass('green-text');
  }

  function blackStatus() {
    $('.ion-camera').addClass('black-text');
    $('.ion-camera').removeClass('green-text');
    $('.ion-camera').removeClass('red-text');
  }

  function sendEvent(event) {
    $.ajax({
        type: 'POST',
        url: url + '/events',
        data: JSON.stringify({ event: event }),
        success: function () { },
        dataType: 'json'
    })
  }

  function toTitleCase(str)
  {
    str = str.toLowerCase();
    str = str.replace('-', ' ');
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
  }

  function isValidName(name) {
    name = name.toLowerCase();
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    return (name !== 'Desconocido' && !(name.startsWith('s') && numbers.includes(name.charAt(1)))) ? true : false;
  }

  window.isValidName = isValidName;

  setInterval(takePhoto, 1000)

  if (typeof MediaStreamTrack === 'undefined' || typeof MediaStreamTrack.getSources === 'undefined') {
  //	document.querySelector("#cameraSelector").style.display="none";
  } else {
      MediaStreamTrack.getSources(getCameras);
  }

  // videoSelect.onchange = startStream;

  startStream();

  function getCameras(sourceInfos) {
      for (var i = 0; i !== sourceInfos.length; ++i) {
          var sourceInfo = sourceInfos[i];
          var option = document.createElement('option');
          option.value = sourceInfo.id;
          if (sourceInfo.kind === 'video') {
              //option.text = sourceInfo.label || 'camera ' + (videoSelect.length + 1);
              //videoSelect.appendChild(option);
          }
      }
  }

  function startStream() {
      navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
      //var videoSource = videoSelect.value;
      var constraints = {
          audio: false, 
          video: true,
      };
      
      navigator.getUserMedia(constraints, onSuccess, onError);
  }

  function onSuccess(stream) {
      console.log("Success! We have a stream!");
      videoArea.src = window.URL.createObjectURL(stream);
      videoArea.play();
  }

  function onError(error) {
      console.log("Error with getUserMedia: ", error);
  }

  $('select').material_select();
  $(".dropdown-button").dropdown();
  moment.locale('es');
})()
