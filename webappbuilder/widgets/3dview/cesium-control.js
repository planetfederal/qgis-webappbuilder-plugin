ol.control.CesiumControl = function(ol3d) {

  var button = document.createElement('button');
  button.innerHTML = '3D';

  var enable3DView = function(e) {
    if (ol3d.getEnabled()){
        ol3d.setEnabled(false);
        button.innerHTML = '3D';
    }
    else{
        button.innerHTML = '2D';
        ol3d.setEnabled(true);
    }
  };

  button.addEventListener('click', enable3DView, false);
  button.addEventListener('touchstart', enable3DView, false);

  var element = document.createElement('div');
  element.className = 'enable3d-control ol-unselectable ol-control';
  element.appendChild(button);

  ol.control.Control.call(this, {
    element: element
  });

};
ol.inherits(ol.control.CesiumControl, ol.control.Control);
