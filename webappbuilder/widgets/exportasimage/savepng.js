saveAsPng = function(){
  canvas = document.getElementsByTagName('canvas')[0];
  canvas.toBlob(function (blob) {
    saveAs(blob, 'map.png');
  });
};