baseLayers = [new ol.layer.Tile({
	type: 'base',
	title: 'CartoDB light',
	source: new ol.source.XYZ({
		url: 'http://s.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png',
		attributions: [new ol.Attribution({ html: ['&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>']
		})]
	})
})
,new ol.layer.Tile({
	type: 'base',
	title: 'Stamen toner labels',
	source: new ol.source.Stamen({layer: 'toner-labels'})
})
];var baseLayersGroup = new ol.layer.Group({'type': 'base', 'title': 'Base maps', layers: baseLayers});



var layersList = [];layersList.unshift(baseLayersGroup);
