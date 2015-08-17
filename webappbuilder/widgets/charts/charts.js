openChart = function(c){

    chartPanel = document.getElementById('chart-panel');
    chartPanel.style.display = 'block';

    this.drawFromSelection = function(){
        if (chartPanel.style.display === 'none'){
            return;
        }

        $('body').addClass('waiting');
        var layerName = charts[c].layer;
        var categoryField = charts[c].categoryField;
        var valueFields = charts[c].valueFields;
        var lyrs = map.getLayers().getArray();
        var lyr = null;
        for (var i = 0; i < lyrs.length; i++){
            if (lyrs[i].get('title') == layerName){
                lyr = lyrs[i];
                break;
            }
        }
        var selectedFeatures = selectionManager.getSelection(lyr);
        var columns = [["x"]];
        if (charts[c].displayMode === DISPLAY_MODE_COUNT){
            columns.push(["Feature count"]);
        }
        else{
            for (var i = 0; i < valueFields.length; i++) {
                columns.push([valueFields[i]]);
            }
        }
        var selectedCount = 0;
        if (charts[c].displayMode === DISPLAY_MODE_FEATURE){
            for (var i = 0; i < selectedFeatures.length; i++) {
                columns[0].push(selectedFeatures[i].get(categoryField));
                for (var j = 0; j < valueFields.length; j++) {
                    columns[j+1].push(selectedFeatures[i].get(valueFields[j]));
                }
            }
        }
        else if (charts[c].displayMode === DISPLAY_MODE_CATEGORY){
            values = {};
            for (var i = 0; i < selectedFeatures.length; i++) {
                cat = selectedFeatures[i].get(categoryField);
                if (cat == null){
                    continue;
                }
                cat = cat.toString();
                if (!(cat in values)){
                    values[cat] = [];
                    for (j = 0; j < valueFields.length; j++) {
                        values[cat].push([selectedFeatures[i].get(valueFields[j])]);
                    }
                }
                else{
                    for (j = 0; j < valueFields.length; j++) {
                        values[cat][j].push(selectedFeatures[i].get(valueFields[j]));
                    }
                }
            }
            for (var key in values){
                columns[0].push(key);
                aggregated = [];
                for (var i = 0; i < valueFields.length; i++) {
                    if (charts[c].operation === AGGREGATION_SUM || charts[c].operation === AGGREGATION_AVG){
                        v = 0;
                        for (var j = 0; j < values[key][i].length; j++){
                            v += values[key][i][j];
                        }
                        if (charts[c].operation === AGGREGATION_AVG){
                            v /= values[key][i].length;
                        }
                    }
                    else if (charts[c].operation === AGGREGATION_MIN){
                        Math.min.apply(Math, values[key][i]);
                    }
                    else if (charts[c].operation === AGGREGATION_MAX){
                        Math.max.apply(Math, values[key][i]);
                    }
                    columns[i + 1].push(v);
                }
            }
        }
        else if (charts[c].displayMode === DISPLAY_MODE_COUNT){
            values = {};
            for (var i = 0; i < selectedFeatures.length; i++) {
                cat = selectedFeatures[i].get(categoryField)
                if (cat == null){
                    continue;
                }
                cat = cat.toString();
                if (!(cat in values)){
                    values[cat] = 1;
                }
                else{
                    values[cat]++;
                }
            }

            var sorted = [];
            for (var key in values){
                sorted.push([key, values[key]]);
            }
            sorted.sort(function(a, b) {return b[1] - a[1]});

            for (var i = 0; i < sorted.length; i++) {
                columns[0].push(sorted[i][0]);
                columns[1].push(sorted[i][1]);
            }
        }
        var info = document.getElementById('chart-panel-info');
        info.innerHTML = selectedFeatures.length.toString() + " features selected in layer " + layerName;

        var chart = c3.generate({
            bindto: '#chart',
            data: {
                x: 'x',
                columns: columns,
                type: 'bar'
            },
            axis: {
                x: {
                    type: 'category',
                    tick: {
                        rotate: 70,
                        multiline:false
                    },
                    height: 80
                }
            }
        });
        $('body').addClass('waiting');
    };

    this.drawFromSelection();

    selectionManager.listen(this.drawFromSelection);

    var this_ = this;
    var closer = document.getElementById('chart-panel-closer');
    if (closer){
        closer.onclick = function() {
            chartPanel.style.display = 'none';
            closer.blur();
            return false;
        };
    }
};
