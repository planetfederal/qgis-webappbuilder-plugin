ol.control.HomeButton = function(opt_options) {

  var options = opt_options || {};

  var button = document.createElement('button');
  button.innerHTML = '<i class="glyphicon glyphicon-home"></i>';

  var this_ = this;
  var goHome = function(e) {
    map.getView().fit(originalExtent, map.getSize());
  };

  button.addEventListener('click', goHome, false);
  button.addEventListener('touchstart', goHome, false);

  var element = document.createElement('div');
  element.className = 'home-button ol-unselectable ol-control';
  element.appendChild(button);

  ol.control.Control.call(this, {
    element: element,
    target: options.target
  });

};
ol.inherits(ol.control.HomeButton, ol.control.Control);
