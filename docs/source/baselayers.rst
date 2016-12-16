.. _qgis.webappbuilder.baselayers:

Customizing Web App Builder base layersand WebSDK
===================================================

A predefined set of base layers is available to be selected for a Web App, when creating it using WAB. Unlike regular layers, which is populated using the layers in the current QGIS project, base layers are harcoded, and the user has no way of modifying the list of available ones. However, it can be edited before starting QGIS and WAB, adding or removing new connections. This document describes how to do it.

To edit the list of available base layers, follow these steps:

- If you want to add a new base layer, open the *baselayers/baselayers.txt* file in the WAB folder. If you want to add a new overlay base layer, open the *baselayers/baseoverlays.txt* file.

- The structure in both files is the same. You will find blocks of text separated by empty lines. Each block of tests contains the information corresponding to a base layer or overlay. The first line is the name of the layer to display in the WAB interface, in the form 

::

	/*name of the layer*/

The remaining lines are the OL3 definition of the layer.

Here is an example:

/*CartoDB*/
new ol.layer.Tile({
    type: 'base',
    title: 'CartoDB light',
    source: new ol.source.XYZ({
        url: 'http://s.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png',
        attributions: [new ol.Attribution({ html: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
        })]
    }),
    projection: 'EPSG:3857'
})

You can add new layers or remove the existing ones. editing the corresponding text file

- Each base layer must have an associated thumbnail image, in the *baselayers* folder (same one where the *baselayers.txt* file is located). Recommended size for thumbnails is 160x80 pixels. The name of the image file is created from the layer name, as defined in the *baselayers.txt* file, removing blank spaces and in lower case. Thumbnails files must be png files. 

