var getBookmarkExtentInViewCrs = function(extent){
    var viewCrs = view.getProjection().getCode();
    return ol.proj.transformExtent(extent, "EPSG:3857", viewCrs);
};

var goToBookmarkByName = function(name){
    for(var i=0; i<bookmarks.length; i++){
        if (bookmarks[i][0] === name){
            map.getView().fit(getBookmarkExtentInViewCrs(bookmarks[i][1]),
                map.getSize());
        }
    }
};

var panToBookmark = function(i){
    var pan = ol.animation.pan({
        duration: 500,
        source: view.getCenter()
    });
    var zoom = ol.animation.zoom({
        duration: 500,
        resolution: view.getResolution(),
        source: view.getZoom()
    });
    map.beforeRender(pan,zoom);
    goToBookmark(i);

};

var goToBookmark = function(i){
    bookmark = bookmarks[i];
    if (bookmark){
        map.getView().fit(getBookmarkExtentInViewCrs(bookmark[1]), map.getSize());
    }
    else{
        map.getView().fit(originalExtent, map.getSize());
    }
};
