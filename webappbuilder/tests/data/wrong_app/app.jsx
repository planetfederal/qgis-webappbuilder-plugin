import React from 'react';
import ReactDOM from 'react-dom';
import ol from 'openlayers';
import {IntlProvider} from 'react-intl';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import AppBar from 'material-ui/AppBar';
import IconMenu from 'material-ui/IconMenu';
import MenuItem from 'material-ui/MenuItem';
import Button from '@boundlessgeo/sdk/components/Button';
import enMessages from '@boundlessgeo/sdk/locale/en';
import InfoPopup from '@boundlessgeo/sdk/components/InfoPopup';
import MapPanel from '@boundlessgeo/sdk/components/MapPanel';
import {ToolbarGroup, ToolbarSeparator} from 'material-ui/Toolbar';

**********
THIS IS A WRONG LINE TO CAUSE A COMPILATION ERROR
**********

import injectTapEventPlugin from 'react-tap-event-plugin';

// Needed for onTouchTap
// Can go away when react 1.0 release
// Check this repo:
// https://github.com/zilverline/react-tap-event-plugin
injectTapEventPlugin();

var defaultFill = new ol.style.Fill({
   color: 'rgba(255,255,255,0.4)'
 });
 var defaultStroke = new ol.style.Stroke({
   color: '#3399CC',
   width: 1.25
 });
 var defaultSelectionFill = new ol.style.Fill({
   color: 'rgba(255,255,0,0.4)'
 });
 var defaultSelectionStroke = new ol.style.Stroke({
   color: '#FFFF00',
   width: 1.25
 });


var textStyleCache_groupped = {}
var clusterStyleCache_groupped = {}
var style_groupped = function(feature, resolution) {


    var value = "";
    var style = [new ol.style.Style({
        image: new ol.style.Circle({
            radius: 3.8,
            stroke: new ol.style.Stroke({
                color: "rgba(0,0,0,1.0)",
                lineDash: null,
                width: 0
            }),
            fill: new ol.style.Fill({
                color: "rgba(240,225,112,1.0)"
            })
        })
    })];
    var allStyles = [];

    allStyles.push.apply(allStyles, style);
    return allStyles;
};
var selectionStyle_groupped = function(feature, resolution) {

    var value = "";
    var style = [new ol.style.Style({
        image: new ol.style.Circle({
            radius: 3.8,
            stroke: new ol.style.Stroke({
                color: "rgba(255, 204, 0, 1)",
                lineDash: null,
                width: 0
            }),
            fill: new ol.style.Fill({
                color: "rgba(255, 204, 0, 1)"
            })
        })
    })]
    var allStyles = [];

    allStyles.push.apply(allStyles, style);
    return allStyles;
};

var textStyleCache_groupped2 = {}
var clusterStyleCache_groupped2 = {}
var style_groupped2 = function(feature, resolution) {


    var value = "";
    var style = [new ol.style.Style({
        image: new ol.style.Circle({
            radius: 3.8,
            stroke: new ol.style.Stroke({
                color: "rgba(0,0,0,1.0)",
                lineDash: null,
                width: 0
            }),
            fill: new ol.style.Fill({
                color: "rgba(175,124,87,1.0)"
            })
        })
    })];
    var allStyles = [];

    allStyles.push.apply(allStyles, style);
    return allStyles;
};
var selectionStyle_groupped2 = function(feature, resolution) {

    var value = "";
    var style = [new ol.style.Style({
        image: new ol.style.Circle({
            radius: 3.8,
            stroke: new ol.style.Stroke({
                color: "rgba(255, 204, 0, 1)",
                lineDash: null,
                width: 0
            }),
            fill: new ol.style.Fill({
                color: "rgba(255, 204, 0, 1)"
            })
        })
    })]
    var allStyles = [];

    allStyles.push.apply(allStyles, style);
    return allStyles;
};
var patternFill_1 = new ol.style.Fill({});
var patternImg_1 = new Image();
patternImg_1.src = './data/styles/patternFill_1.svg';
patternImg_1.onload = function() {
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    var pattern = context.createPattern(patternImg_1, 'repeat');
    patternFill_1 = new ol.style.Fill({
        color: pattern
    });
    lyr_polygons.changed()
};
var patternFill_2 = new ol.style.Fill({});
var patternImg_2 = new Image();
patternImg_2.src = './data/styles/patternFill_2.svg';
patternImg_2.onload = function() {
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    var pattern = context.createPattern(patternImg_2, 'repeat');
    patternFill_2 = new ol.style.Fill({
        color: pattern
    });
    lyr_polygons.changed()
};
var patternFill_3 = new ol.style.Fill({});
var patternImg_3 = new Image();
patternImg_3.src = './data/styles/patternFill_3.svg';
patternImg_3.onload = function() {
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    var pattern = context.createPattern(patternImg_3, 'repeat');
    patternFill_3 = new ol.style.Fill({
        color: pattern
    });
    lyr_polygons.changed()
};
var patternFill_4 = new ol.style.Fill({});
var patternImg_4 = new Image();
patternImg_4.src = './data/styles/patternFill_4.svg';
patternImg_4.onload = function() {
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    var pattern = context.createPattern(patternImg_4, 'repeat');
    patternFill_4 = new ol.style.Fill({
        color: pattern
    });
    lyr_polygons.changed()
};
var categories_polygons = function() {
    return {
        "2": [new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: "rgba(0,0,0,1.0)",
                lineDash: [6],
                width: 0
            }),
            fill: new ol.style.Fill({
                color: "rgba(32,225,68,1.0)"
            })
        })],
        "3": [new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: "rgba(0,0,0,1.0)",
                lineDash: null,
                width: 3
            }),
            fill: new ol.style.Fill({
                color: "rgba(116,229,72,1.0)"
            })
        })],
        "4": [new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: "rgba(0,0,0,1.0)",
                lineDash: null,
                width: 0
            }),
            fill: new ol.style.Fill({
                color: "rgba(0,0,0,0.0)"
            })
        })],
        "5": [new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: "rgba(0,0,0,1.0)",
                lineDash: null,
                width: 0
            }),
            fill: new ol.style.Fill({
                color: "rgba(217,116,133,1.0)"
            })
        }), new ol.style.Style({
            fill: patternFill_1
        })],
        "6": [new ol.style.Style({
            fill: patternFill_2
        })],
        "7": [new ol.style.Style({
            fill: patternFill_3
        })],
        "8": [new ol.style.Style({
            fill: patternFill_4
        })],
        "9": [new ol.style.Style({

        })],
        "10": [new ol.style.Style({

        })],
        "11": [new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: "rgba(244,0,0,1.0)",
                lineDash: null,
                width: 0
            }),
            fill: new ol.style.Fill({
                color: "rgba(110,181,234,1.0)"
            })
        })],
        "": [new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: "rgba(0,0,0,1.0)",
                lineDash: null,
                width: 0
            }),
            fill: new ol.style.Fill({
                color: "rgba(29,37,130,1.0)"
            })
        })]
    };
};
var categoriesSelected_polygons = {
    "2": [new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: "rgba(255, 204, 0, 1)",
            lineDash: [6],
            width: 0
        }),
        fill: new ol.style.Fill({
            color: "rgba(255, 204, 0, 1)"
        })
    })],
    "3": [new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: "rgba(255, 204, 0, 1)",
            lineDash: null,
            width: 3
        }),
        fill: new ol.style.Fill({
            color: "rgba(255, 204, 0, 1)"
        })
    })],
    "4": [new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: "rgba(255, 204, 0, 1)",
            lineDash: null,
            width: 0
        }),
        fill: new ol.style.Fill({
            color: "rgba(255, 204, 0, 1)"
        })
    })],
    "5": [new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: "rgba(255, 204, 0, 1)",
            lineDash: null,
            width: 0
        }),
        fill: new ol.style.Fill({
            color: "rgba(255, 204, 0, 1)"
        })
    }), new ol.style.Style({

        fill: defaultSelectionFill,
        stroke: defaultSelectionStroke

    })],
    "6": [new ol.style.Style({

        fill: defaultSelectionFill,
        stroke: defaultSelectionStroke

    })],
    "7": [new ol.style.Style({

        fill: defaultSelectionFill,
        stroke: defaultSelectionStroke

    })],
    "8": [new ol.style.Style({

        fill: defaultSelectionFill,
        stroke: defaultSelectionStroke

    })],
    "9": [new ol.style.Style({

    })],
    "10": [new ol.style.Style({

    })],
    "11": [new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: "rgba(255, 204, 0, 1)",
            lineDash: null,
            width: 0
        }),
        fill: new ol.style.Fill({
            color: "rgba(255, 204, 0, 1)"
        })
    })],
    "": [new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: "rgba(255, 204, 0, 1)",
            lineDash: null,
            width: 0
        }),
        fill: new ol.style.Fill({
            color: "rgba(255, 204, 0, 1)"
        })
    })]
};
var textStyleCache_polygons = {}
var clusterStyleCache_polygons = {}
var style_polygons = function(feature, resolution) {


    var value = feature.get("n");
    var style = categories_polygons()[value];
    var allStyles = [];

    allStyles.push.apply(allStyles, style);
    return allStyles;
};
var selectionStyle_polygons = function(feature, resolution) {

    var value = feature.get("n");
    var style = categoriesSelected_polygons[value]
    var allStyles = [];

    allStyles.push.apply(allStyles, style);
    return allStyles;
};
var categories_points = function() {
    return {
        "2": [new ol.style.Style({
            image: new ol.style.Icon({
                scale: 0.025000,
                anchorOrigin: 'top-left',
                anchorXUnits: 'fraction',
                anchorYUnits: 'fraction',
                anchor: [0.5, 0.5],
                src: "./data/styles/plane00010.svg",
                rotation: 0.000000
            })
        })],
        "3": [new ol.style.Style({
            image: new ol.style.Icon({
                scale: 0.150000,
                anchorOrigin: 'top-left',
                anchorXUnits: 'fraction',
                anchorYUnits: 'fraction',
                anchor: [0.5, 0.5],
                src: "./data/styles/amenity=airport00010.svg",
                rotation: 0.000000
            })
        })],
        "4": [new ol.style.Style({
            image: new ol.style.Icon({
                scale: 0.025000,
                anchorOrigin: 'top-left',
                anchorXUnits: 'fraction',
                anchorYUnits: 'fraction',
                anchor: [0.5, 0.5],
                src: "./data/styles/landuse_coniferous0229010.svg",
                rotation: 0.000000
            })
        })],
        "5": [new ol.style.Style({
            image: new ol.style.RegularShape({
                points: 3,
                radius: 19.0,
                stroke: new ol.style.Stroke({
                    color: "rgba(0,0,0,1.0)",
                    lineDash: null,
                    width: 0
                }),
                fill: new ol.style.Fill({
                    color: "rgba(255,0,0,1.0)"
                }),
                angle: 0
            })
        }), new ol.style.Style({
            image: new ol.style.Circle({
                radius: 3.8,
                stroke: new ol.style.Stroke({
                    color: "rgba(0,0,0,1.0)",
                    lineDash: null,
                    width: 3
                }),
                fill: new ol.style.Fill({
                    color: "rgba(0,0,0,1.0)"
                })
            })
        })],
        "6": [new ol.style.Style({
            image: new ol.style.Circle({
                radius: 3.8,
                stroke: new ol.style.Stroke({
                    color: "rgba(0,0,0,1.0)",
                    lineDash: null,
                    width: 0
                }),
                fill: new ol.style.Fill({
                    color: "rgba(154,25,240,1.0)"
                })
            })
        })],
        "7": [new ol.style.Style({
            image: new ol.style.Circle({
                radius: 7.6,
                stroke: new ol.style.Stroke({
                    color: "rgba(0,0,0,1.0)",
                    lineDash: null,
                    width: 0
                }),
                fill: new ol.style.Fill({
                    color: "rgba(227,26,28,1.0)"
                })
            })
        })],
        "8": [new ol.style.Style({
            image: new ol.style.RegularShape({
                points: 4,
                radius: 3.8,
                stroke: new ol.style.Stroke({
                    color: "rgba(0,0,0,1.0)",
                    lineDash: null,
                    width: 0
                }),
                fill: new ol.style.Fill({
                    color: "rgba(202,109,108,1.0)"
                }),
                angle: 0
            })
        })],
        "9": [new ol.style.Style({
            image: new ol.style.RegularShape({
                points: 4,
                radius1: 3.8,
                radius2: 0,
                stroke: new ol.style.Stroke({
                    color: "rgba(0,0,0,1.0)",
                    lineDash: null,
                    width: 0
                }),
                fill: new ol.style.Fill({
                    color: "rgba(43,86,228,1.0)"
                }),
                angle: 0
            })
        })],
        "10": [new ol.style.Style({
            image: new ol.style.RegularShape({
                points: 4,
                radius1: 3.8,
                radius2: 0,
                stroke: new ol.style.Stroke({
                    color: "rgba(0,0,0,1.0)",
                    lineDash: null,
                    width: 0
                }),
                fill: new ol.style.Fill({
                    color: "rgba(211,236,141,1.0)"
                }),
                angle: 0.7853975
            })
        })],
        "11": [new ol.style.Style({
            image: new ol.style.RegularShape({
                points: 3,
                radius: 3.8,
                stroke: new ol.style.Stroke({
                    color: "rgba(0,0,0,1.0)",
                    lineDash: null,
                    width: 0
                }),
                fill: new ol.style.Fill({
                    color: "rgba(224,126,165,1.0)"
                }),
                angle: 0
            })
        })],
        "12": [new ol.style.Style({
            image: new ol.style.RegularShape({
                points: 5,
                radius1: 7.6,
                radius2: 3.8,
                stroke: new ol.style.Stroke({
                    color: "rgba(0,0,0,1.0)",
                    lineDash: null,
                    width: 0
                }),
                fill: new ol.style.Fill({
                    color: "rgba(227,26,28,1.0)"
                }),
                angle: 0
            })
        })],
        "13": [new ol.style.Style({
            image: new ol.style.Circle({
                radius: 38.0,
                stroke: new ol.style.Stroke({
                    color: "rgba(0,0,0,1.0)",
                    lineDash: null,
                    width: 0
                }),
                fill: new ol.style.Fill({
                    color: "rgba(70,205,171,1.0)"
                })
            })
        })],
        "14": [new ol.style.Style({
            image: new ol.style.Circle({
                radius: 9.5,
                stroke: new ol.style.Stroke({
                    color: "rgba(0,0,0,1.0)",
                    lineDash: null,
                    width: 11
                }),
                fill: new ol.style.Fill({
                    color: "rgba(47,219,56,1.0)"
                })
            })
        })],
        "15": [new ol.style.Style({
            image: new ol.style.Circle({
                radius: 20.9,
                stroke: new ol.style.Stroke({
                    color: "rgba(0,0,0,1.0)",
                    lineDash: null,
                    width: 3
                }),
                fill: new ol.style.Fill({
                    color: "rgba(173,30,216,1.0)"
                })
            })
        })],
        "16": [new ol.style.Style({
            image: new ol.style.Circle({
                radius: 3.8,
                stroke: new ol.style.Stroke({
                    color: "rgba(0,38,241,1.0)",
                    lineDash: null,
                    width: 3
                }),
                fill: new ol.style.Fill({
                    color: "rgba(32,217,19,1.0)"
                })
            })
        })],
        "": [new ol.style.Style({
            image: new ol.style.Circle({
                radius: 3.8,
                stroke: new ol.style.Stroke({
                    color: "rgba(0,0,0,1.0)",
                    lineDash: null,
                    width: 0
                }),
                fill: new ol.style.Fill({
                    color: "rgba(213,84,175,1.0)"
                })
            })
        })]
    };
};
var categoriesSelected_points = {
    "2": [new ol.style.Style({
        image: new ol.style.Icon({
            scale: 0.025000,
            anchorOrigin: 'top-left',
            anchorXUnits: 'fraction',
            anchorYUnits: 'fraction',
            anchor: [0.5, 0.5],
            src: "./data/styles/plane25520401.svg",
            rotation: 0.000000
        })
    })],
    "3": [new ol.style.Style({
        image: new ol.style.Icon({
            scale: 0.150000,
            anchorOrigin: 'top-left',
            anchorXUnits: 'fraction',
            anchorYUnits: 'fraction',
            anchor: [0.5, 0.5],
            src: "./data/styles/amenity=airport25520401.svg",
            rotation: 0.000000
        })
    })],
    "4": [new ol.style.Style({
        image: new ol.style.Icon({
            scale: 0.025000,
            anchorOrigin: 'top-left',
            anchorXUnits: 'fraction',
            anchorYUnits: 'fraction',
            anchor: [0.5, 0.5],
            src: "./data/styles/landuse_coniferous25520401.svg",
            rotation: 0.000000
        })
    })],
    "5": [new ol.style.Style({
        image: new ol.style.RegularShape({
            points: 3,
            radius: 19.0,
            stroke: new ol.style.Stroke({
                color: "rgba(255, 204, 0, 1)",
                lineDash: null,
                width: 0
            }),
            fill: new ol.style.Fill({
                color: "rgba(255, 204, 0, 1)"
            }),
            angle: 0
        })
    }), new ol.style.Style({
        image: new ol.style.Circle({
            radius: 3.8,
            stroke: new ol.style.Stroke({
                color: "rgba(255, 204, 0, 1)",
                lineDash: null,
                width: 3
            }),
            fill: new ol.style.Fill({
                color: "rgba(255, 204, 0, 1)"
            })
        })
    })],
    "6": [new ol.style.Style({
        image: new ol.style.Circle({
            radius: 3.8,
            stroke: new ol.style.Stroke({
                color: "rgba(255, 204, 0, 1)",
                lineDash: null,
                width: 0
            }),
            fill: new ol.style.Fill({
                color: "rgba(255, 204, 0, 1)"
            })
        })
    })],
    "7": [new ol.style.Style({
        image: new ol.style.Circle({
            radius: 7.6,
            stroke: new ol.style.Stroke({
                color: "rgba(255, 204, 0, 1)",
                lineDash: null,
                width: 0
            }),
            fill: new ol.style.Fill({
                color: "rgba(255, 204, 0, 1)"
            })
        })
    })],
    "8": [new ol.style.Style({
        image: new ol.style.RegularShape({
            points: 4,
            radius: 3.8,
            stroke: new ol.style.Stroke({
                color: "rgba(255, 204, 0, 1)",
                lineDash: null,
                width: 0
            }),
            fill: new ol.style.Fill({
                color: "rgba(255, 204, 0, 1)"
            }),
            angle: 0
        })
    })],
    "9": [new ol.style.Style({
        image: new ol.style.RegularShape({
            points: 4,
            radius1: 3.8,
            radius2: 0,
            stroke: new ol.style.Stroke({
                color: "rgba(255, 204, 0, 1)",
                lineDash: null,
                width: 0
            }),
            fill: new ol.style.Fill({
                color: "rgba(255, 204, 0, 1)"
            }),
            angle: 0
        })
    })],
    "10": [new ol.style.Style({
        image: new ol.style.RegularShape({
            points: 4,
            radius1: 3.8,
            radius2: 0,
            stroke: new ol.style.Stroke({
                color: "rgba(255, 204, 0, 1)",
                lineDash: null,
                width: 0
            }),
            fill: new ol.style.Fill({
                color: "rgba(255, 204, 0, 1)"
            }),
            angle: 0.7853975
        })
    })],
    "11": [new ol.style.Style({
        image: new ol.style.RegularShape({
            points: 3,
            radius: 3.8,
            stroke: new ol.style.Stroke({
                color: "rgba(255, 204, 0, 1)",
                lineDash: null,
                width: 0
            }),
            fill: new ol.style.Fill({
                color: "rgba(255, 204, 0, 1)"
            }),
            angle: 0
        })
    })],
    "12": [new ol.style.Style({
        image: new ol.style.RegularShape({
            points: 5,
            radius1: 7.6,
            radius2: 3.8,
            stroke: new ol.style.Stroke({
                color: "rgba(255, 204, 0, 1)",
                lineDash: null,
                width: 0
            }),
            fill: new ol.style.Fill({
                color: "rgba(255, 204, 0, 1)"
            }),
            angle: 0
        })
    })],
    "13": [new ol.style.Style({
        image: new ol.style.Circle({
            radius: 38.0,
            stroke: new ol.style.Stroke({
                color: "rgba(255, 204, 0, 1)",
                lineDash: null,
                width: 0
            }),
            fill: new ol.style.Fill({
                color: "rgba(255, 204, 0, 1)"
            })
        })
    })],
    "14": [new ol.style.Style({
        image: new ol.style.Circle({
            radius: 9.5,
            stroke: new ol.style.Stroke({
                color: "rgba(255, 204, 0, 1)",
                lineDash: null,
                width: 11
            }),
            fill: new ol.style.Fill({
                color: "rgba(255, 204, 0, 1)"
            })
        })
    })],
    "15": [new ol.style.Style({
        image: new ol.style.Circle({
            radius: 20.9,
            stroke: new ol.style.Stroke({
                color: "rgba(255, 204, 0, 1)",
                lineDash: null,
                width: 3
            }),
            fill: new ol.style.Fill({
                color: "rgba(255, 204, 0, 1)"
            })
        })
    })],
    "16": [new ol.style.Style({
        image: new ol.style.Circle({
            radius: 3.8,
            stroke: new ol.style.Stroke({
                color: "rgba(255, 204, 0, 1)",
                lineDash: null,
                width: 3
            }),
            fill: new ol.style.Fill({
                color: "rgba(255, 204, 0, 1)"
            })
        })
    })],
    "": [new ol.style.Style({
        image: new ol.style.Circle({
            radius: 3.8,
            stroke: new ol.style.Stroke({
                color: "rgba(255, 204, 0, 1)",
                lineDash: null,
                width: 0
            }),
            fill: new ol.style.Fill({
                color: "rgba(255, 204, 0, 1)"
            })
        })
    })]
};
var textStyleCache_points = {}
var clusterStyleCache_points = {}
var style_points = function(feature, resolution) {


    var value = feature.get("n");
    var style = categories_points()[value];
    var allStyles = [];

    allStyles.push.apply(allStyles, style);
    return allStyles;
};
var selectionStyle_points = function(feature, resolution) {

    var value = feature.get("n");
    var style = categoriesSelected_points[value]
    var allStyles = [];

    allStyles.push.apply(allStyles, style);
    return allStyles;
};
var categories_lines = function() {
    return {
        "2": [new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: "rgba(84,229,181,1.0)",
                lineDash: null,
                width: 0
            })
        })],
        "3": [new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: "rgba(59,37,41,1.0)",
                lineDash: [6],
                width: 0
            })
        })],
        "4": [new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: "rgba(122,245,0,1.0)",
                lineDash: null,
                width: 5
            })
        }), new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: "rgba(170,48,0,1.0)",
                lineDash: [6],
                width: 5
            })
        })],
        "5": [new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: "rgba(143,135,230,1.0)",
                lineDash: null,
                width: 7
            })
        })],
        "6": [new ol.style.Style({

        })],
        "7": [new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: "rgba(255,255,255,1.0)",
                lineDash: null,
                width: 4
            })
        }), new ol.style.Style({

        })],
        "8": [new ol.style.Style({

        })]
    };
};
var categoriesSelected_lines = {
    "2": [new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: "rgba(255, 204, 0, 1)",
            lineDash: null,
            width: 0
        })
    })],
    "3": [new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: "rgba(255, 204, 0, 1)",
            lineDash: [6],
            width: 0
        })
    })],
    "4": [new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: "rgba(255, 204, 0, 1)",
            lineDash: null,
            width: 5
        })
    }), new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: "rgba(255, 204, 0, 1)",
            lineDash: [6],
            width: 5
        })
    })],
    "5": [new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: "rgba(255, 204, 0, 1)",
            lineDash: null,
            width: 7
        })
    })],
    "6": [new ol.style.Style({

    })],
    "7": [new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: "rgba(255, 204, 0, 1)",
            lineDash: null,
            width: 4
        })
    }), new ol.style.Style({

    })],
    "8": [new ol.style.Style({

    })]
};
var textStyleCache_lines = {}
var clusterStyleCache_lines = {}
var style_lines = function(feature, resolution) {


    var value = feature.get("n");
    var style = categories_lines()[value];
    var allStyles = [];

    allStyles.push.apply(allStyles, style);
    return allStyles;
};
var selectionStyle_lines = function(feature, resolution) {

    var value = feature.get("n");
    var style = categoriesSelected_lines[value]
    var allStyles = [];

    allStyles.push.apply(allStyles, style);
    return allStyles;
};
var baseLayers = [];
var baseLayersGroup = new ol.layer.Group({
    showContent: true,
    'type': 'base-group',
    'title': 'Base maps',
    layers: baseLayers
});
var overlayLayers = [];
var overlaysGroup = new ol.layer.Group({
    showContent: true,
    'title': 'Overlays',
    layers: overlayLayers
});
var lyr_groupped = new ol.layer.Vector({
    opacity: 1.0,
    source: new ol.source.Vector({
        format: new ol.format.GeoJSON(),
        url: './data/lyr_groupped.json'
    }),

    style: style_groupped,
    selectedStyle: selectionStyle_groupped,
    title: "groupped",
    id: "points20150909090651234",
    filters: [],
    timeInfo: null,
    isSelectable: true,
    popupInfo: ""
});
var lyr_groupped2 = new ol.layer.Vector({
    opacity: 1.0,
    source: new ol.source.Vector({
        format: new ol.format.GeoJSON(),
        url: './data/lyr_groupped2.json'
    }),

    style: style_groupped2,
    selectedStyle: selectionStyle_groupped2,
    title: "groupped2",
    id: "points20150909090705810",
    filters: [],
    timeInfo: null,
    isSelectable: true,
    popupInfo: ""
});
var lyr_polygons = new ol.layer.Vector({
    opacity: 1.0,
    source: new ol.source.Vector({
        format: new ol.format.GeoJSON(),
        url: './data/lyr_polygons.json'
    }),

    style: style_polygons,
    selectedStyle: selectionStyle_polygons,
    title: "polygons",
    id: "graticule20150708141425208",
    filters: [],
    timeInfo: null,
    isSelectable: true,
    popupInfo: ""
});
var lyr_points = new ol.layer.Vector({
    opacity: 1.0,
    source: new ol.source.Vector({
        format: new ol.format.GeoJSON(),
        url: './data/lyr_points.json'
    }),

    style: style_points,
    selectedStyle: selectionStyle_points,
    title: "points",
    id: "points_shp20150708141950508",
    filters: [],
    timeInfo: null,
    isSelectable: true,
    popupInfo: ""
});
var lyr_lines = new ol.layer.Vector({
    opacity: 1.0,
    source: new ol.source.Vector({
        format: new ol.format.GeoJSON(),
        url: './data/lyr_lines.json'
    }),

    style: style_lines,
    selectedStyle: selectionStyle_lines,
    title: "lines",
    id: "lines_shp20150708163456077",
    filters: [],
    timeInfo: null,
    isSelectable: true,
    popupInfo: ""
});
var lyr_wms = new ol.layer.Tile({
    opacity: 1.0,
    timeInfo: null,

    source: new ol.source.TileWMS(({
        crossOrigin: 'anonymous',
        url: "http://demo.mapserver.org/cgi-bin/wms?",
        params: {
            "LAYERS": "continents",
            "TILED": "true",
            "STYLES": ""
        },
    })),
    title: "wms",
    id: "World_continents20161110111935176",
    popupInfo: "",
    projection: "EPSG:4326"
});
var src_raster = new ol.source.ImageStatic({
    url: "./data/raster.png",
    projection: "EPSG:3857",
    alwaysInRange: true,
    imageSize: [91, 91],
    imageExtent: [50093.770857, 50094.285871, 1063101.137076, 1068058.094050]
});

var raster_raster = new ol.source.Raster({
    sources: [src_raster],
    operation: function(pixels, data) {
        var pixel = pixels[0];
        if (pixel[0] === 0 && pixel[1] === 0 && pixel[2] === 0) {
            pixel[3] = 0;
        }
        return pixel;
    }
});

var lyr_raster = new ol.layer.Image({
    opacity: 1.0,

    title: "raster",
    id: "raster20150909093752545",
    timeInfo: null,
    source: raster_raster
});
var group_group1 = new ol.layer.Group({
    layers: [lyr_groupped, lyr_groupped2],
    showContent: true,
    title: "group1"
});

lyr_groupped.setVisible(true);
lyr_groupped2.setVisible(true);
lyr_polygons.setVisible(true);
lyr_points.setVisible(true);
lyr_lines.setVisible(true);
lyr_wms.setVisible(true);
lyr_raster.setVisible(true);
var layersList = [group_group1, lyr_polygons, lyr_points, lyr_lines, lyr_wms, lyr_raster];
var view = new ol.View({
    maxZoom: 32,
    minZoom: 1,
    projection: 'EPSG:3857'
});
var originalExtent = [-404970.967958, 69274.361598, 1193282.999325, 1138935.965858];

var map = new ol.Map({
  layers: layersList,
  view: view,
  controls: []
});



class BasicApp extends React.Component {
  getChildContext() {
    return {
      muiTheme: getMuiTheme()
    };
  }
  componentDidMount() {

  }
  _toggle(el) {
    if (el.style.display === 'block') {
      el.style.display = 'none';
    } else {
      el.style.display = 'block';
    }
  }
  _toggleTable() {
    this._toggle(document.getElementById('table-panel'));
    this.refs.table.getWrappedInstance().setDimensionsOnState();
  }
  _toggleWFST() {
    this._toggle(document.getElementById('wfst'));
  }
  _toggleQuery() {
    this._toggle(document.getElementById('query-panel'));
  }
  _toggleEdit() {
    this._toggle(document.getElementById('edit-tool-panel'));
  }
  _hideAboutPanel(evt) {
    evt.preventDefault();
    document.getElementById('about-panel').style.display = 'none';
  }
  _toggleChartPanel(evt) {
    evt.preventDefault();
    this._toggle(document.getElementById('chart-panel'));
  }
  render() {
    var toolbarOptions = {style:{height: 71}, showMenuIconButton: false, title:"My Web App"};
    return React.createElement("article", null,
       React.createElement(AppBar, toolbarOptions
       ),
      React.createElement("div", {id: 'content'},
        React.createElement(MapPanel, {id: 'map', map: map, extent: originalExtent, useHistory: true}
          ,
React.createElement("div", {id: 'popup', className: 'ol-popup'},
                                    React.createElement(InfoPopup, {toggleGroup: 'navigation', map: map, hover: false})
                                  )
        )

      )
    );
  }
}

BasicApp.childContextTypes = {
  muiTheme: React.PropTypes.object
};

ReactDOM.render(<IntlProvider locale='en' messages={enMessages}><BasicApp /></IntlProvider>, document.getElementById('main'));
