Web app builder
=====================

A QGIS plugin to easily create web apps based on OpenLayers and the Boundless WebSDK.

Installation
============

To install, clone this repository, open a console in the repo folder and type

    paver setup
    
This will get all the dependencies needed by the plugin, including those of WebSDK.

Install into QGIS by running

    paver install

Documentation
==============

Usage is documented `here <http://boundlessgeo.github.io/qgis-app-builder>`_

Deploying
=========

Running

	paver package

will create a zip file containing Web App Builder

