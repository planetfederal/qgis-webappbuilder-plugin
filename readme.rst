Web app builder
=====================

A QGIS plugin to easily create web apps based on OpenLayers the Boundless WebSDK.

Installation
============

To install, clone this repository, open a console in the repo folder and type

    paver setup
    
This will get all the dependencies needed by the plugin, including those of WebSDK, needed for the enterprise version of the plugin. If you do not want to get all SDK dependencies (stored in the node_modules folder), you can use

   paver setup --nonpm

Install into QGIS by running

    paver install

Documentation
==============

Documentation for the Web App Builder is kept along with the OpenGeo Suite documentation

https://github.com/boundlessgeo/suite/tree/master/docs/usermanual/source/qgis/webappbuilder

Deploying
=========

Running

	paver package

will create 2 zip files containing the free (for releasing on the QGIS plugins server) and enterprise versions of the Web App Builder

The enterprise version requires a Node.js installation, which is not provided in the resulting zip file. All other dependencies, including WebSDK itself are contained in that file

To create only the free version, you can run

	paver package --noenterprise
