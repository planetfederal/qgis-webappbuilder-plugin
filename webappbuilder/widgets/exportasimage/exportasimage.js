var exportAsImage = function(){
    var exportPngElement = document.getElementById('export-as-image');
    map.once('postcompose', function(event) {
      var canvas = event.context.canvas;
      exportPngElement.href = canvas.toDataURL('image/png');
    });
    map.renderSync();
};