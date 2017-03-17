.. _qgis.webappbuilder.baselayers:

Customizing Web App Builder base layers
=======================================

Using |current_plugin|, a predefined set of base layers is available in the
:guilabel:`Other layers` to be selected for a Web App. Unlike
:guilabel:`QGIS layers`, which are populated using the layers in the current
QGIS project, base layers are hardcoded, and the user has no way of modifying
the list of available ones. However, it can be edited before starting QGIS and
WAB, adding or removing new connections. This document describes how to do it.

To edit the list of available base layers in :guilabel:`Other layers`,
you can edit one of these two files in the WAB folder (``[user_home_folder]/
.qgis2/python/plugins/webappbuilder/``):

- If you want to add a new base layer, open the ``baselayers/baselayers.txt``
  file in the WAB folder;
- If you want to add a new overlay base layer, open the
  ``baselayers/baseoverlays.txt`` file instead.

The structure in both files is the same. You will find blocks of text
separated by empty lines. Each block of text contains the information
corresponding to a base layer or an overlay. The first line is the name of the
layer to display in the WAB interface, in the following form:

::

	/*name of the layer*/

The remaining lines are the Open Layers 3 (OL3) definition of the layer.

Here is an example:

.. code-block:: none

   /*CartoDB light*/
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

You can add new layers or remove the existing ones editing the corresponding
texts blocks.

Each base layer must have an associated thumbnail image in the ``baselayers/``
folder (same place where the :file:`baselayers.txt` and :file:`baseoverlays.txt`
file are located). Thumbnails should be in PNG format with a recommended
size of 160x80 pixels. The name of the image file should match the layer
name, as defined in the *baselayers.txt* file, removing any blank spaces and
in lowercase. Using the example above, the file name should be named
:file:`cartodblight.png`.