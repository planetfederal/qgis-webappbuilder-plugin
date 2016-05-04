Web App Builder
===============

A QGIS plugin to easily create web apps based on OpenLayers and the Boundless WebSDK.

Installation
============

To install, download the latest release from the `releases page <https://github.com/boundlessgeo/qgis-webappbuilder-plugin/releases>`_ and unzip it in the QGIS plugins folder at ``[your_user_folder]/.qgis2/python/plugins``


Installing from sources
========================

To install the latest  version for the repository sources, clone this repository, open a console in the repo folder and type

    paver setup

This will get all the dependencies needed by the plugin, including those of WebSDK.

Install into QGIS by running

    paver install

Documentation
==============

Usage is documented `here <http://boundlessgeo.github.io/qgis-plugins-documentation/webappbuilder/>`_


Cloning this repository
=======================

This repository uses external repositories as submodules. Therefore in order to include the external repositories during cloning you should use the *--recursive* option:

git clone --recursive http://github.com/boundlessgeo/qgis-webappbuilder-plugin.git

Also, to update the submodules whenever there are changes in the remote repositories one should do:

git submodule update --remote
