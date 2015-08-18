var showQueryPanel = function(){

    var select = document.getElementById('query-layer');
    if (select.options.length === 0){
        for (var i = 0, lay; i < getSelectableLayers().length; i++) {
            lay = getSelectableLayers()[i];
            var option = document.createElement('option');
            option.value = option.textContent = lay.get('title');
            select.appendChild(option);
        }
    }

    var close = document.getElementById('btn-close-query');
    if (close){
        close.onclick = function() {
            document.getElementById('query-panel').style.display = 'none';
            return false;
        };
    }

    var NEW_SELECTION = 0;
    var ADD_TO_SELECTION = 1;
    var IN_SELECTION = 2;

    this_ = this;
    var queryNew = document.getElementById('btn-query-new');
    queryNew.onclick = function(){
        this_.selectFromQuery(NEW_SELECTION);
    };
    var queryAdd = document.getElementById('btn-query-add');
    queryAdd.onclick = function(){
        this_.selectFromQuery(ADD_TO_SELECTION);
    };
    var queryIn = document.getElementById('btn-query-in');
    queryIn.onclick = function(){
        this_.selectFromQuery(IN_SELECTION);
    };
    this.selectFromQuery = function(mode) {
        if (this_.queryFilter){
            var layerName = document.getElementById('query-layer').value;
            var layer = getLayerFromLayerName(layerName);
            var layerFeatures = sourceFromLayer(layer).getFeatures();
            var selectedFeatures = selectionManager.getSelection(layer);
            var createFeatureObject = function(feature_){
                feature = {};
                keys = feature_.getKeys();
                for (var j = 0; j < keys.length; j++){
                    feature[keys[j]] = feature_.get(keys[j]);
                }
                return feature;
            };
            if (mode === NEW_SELECTION){
                var newSelection = [];
                for (var i = 0; i < layerFeatures.length; i++) {
                    var feature = createFeatureObject(layerFeatures[i]);
                    if (this_.queryFilter(feature)){
                        newSelection.push(layerFeatures[i]);
                    }
                }
                selectionManager.setSelection(newSelection, layer);
            }
            else if (mode === IN_SELECTION){
                var newSelection = [];
                for (var i = 0; i < selectedFeatures.length; i++) {
                    var feature = createFeatureObject(selectedFeatures[i]);
                    if (this_.queryFilter(feature)){
                        newSelection.push(selectedFeatures[i]);
                    }
                }
                selectionManager.setSelection(newSelection, layer);
            }
            else{
                var newSelection = [];
                for (var i = 0; i < layerFeatures.length; i++) {
                    if (selectedFeatures.indexOf(layerFeatures[i]) != -1){
                        newSelection.push(layerFeatures[i]);
                    }
                    else{
                        var feature = createFeatureObject(layerFeatures[i]);
                        if (this_.queryFilter(feature)){
                            newSelection.push(layerFeatures[i]);
                        }
                    }
                }
                selectionManager.setSelection(newSelection, layer);
            }
            selectionManager.setSelection(newSelection, layer);



        }
    };

    document.getElementById('query-panel').style.display = 'block';

    this.updateExpression = function(){
        var input = $('#query-expression');
        var expression = input.val();
        if (!expression) {
            this_.queryFilter = null;
            input.css('background-color', '#fff');
        }
        else {
            try {
                this_.queryFilter = compileExpression(expression);
                input.css('background-color', '#fff');
            }
            catch (e) {
                this_.queryFilter = null;
                input.css('background-color', '#fdd');
            }
        }
    };

    $('#query-expression').keyup(this.updateExpression)
    .focus();

};
