function fnc_azimuth(values, context) {
    return false;
};

function fnc_project(values, context) {
    return false;
};

// Math
function fnc_abs(values, context) {
    return Math.abs(values[0]);
};

function fnc_degrees(values, context) {
    return values[0] * (180/Math.PI);
};

function fnc_radians(values, context) {
    return values[0] * (Math.PI/180);
};

function fnc_sqrt(values, context) {
    return Math.sqrt(values[0]);
};

function fnc_cos(values, context) {
    return Math.cos(values[0]);
};

function fnc_sin(values, context) {
    return Math.sin(values[0]);
};

function fnc_tan(values, context) {
    return Math.tan(values[0]);
};

function fnc_asin(values, context) {
    return Math.asin(values[0]);
};

function fnc_acos(values, context) {
    return Math.acos(values[0]);
};

function fnc_atan(values, context) {
    return Math.atan(values[0]);
};

function fnc_atan2(values, context) {
    return Math.atan2(values[0]);
};

function fnc_exp(values, context) {
    return Math.exp(values[0]);
};

function fnc_ln(values, context) {
    return Math.log(values[0]);
};

function fnc_log10(values, context) {
    return Math.LN10(values[0]);
};

function fnc_log(values, context) {
    return Math.log(values[0]) / Math.log(values[1]);
};

function fnc_round(values, context) {
    return Math.floor(values[0])
};

function fnc_rand(values, context) {
    return Math.floor(Math.random()*(values[1]-values[0]+1)+values[0]);
};

function fnc_randf(values, context) {
    return Math.random()*(values[1]-values[0]+1)+values[0];
};

function fnc_max(values, context) {
    return Math.max.apply(this, values);
};

function fnc_min(values, context) {
    return Math.min.apply(this, values);
};

function fnc_clamp(values, context) {
    return false;
};

function fnc_scale_linear(values, context) {
    return values[3] + ((values[4] - values[3]) * (values[0]-values[1]) / (values[2]- values[1]));
};

function fnc_scale_exp(values, context) {
    var minp = values[1];
    var maxp = values[2];

    var minv = Math.pow(values[3], 1/values[5]);
    var maxv = Math.pow(values[4], 1/values[5]);
    var scale = (maxv-minv) / (maxp-minp);
    return Math.pw(maxv + scale*(values[0]-minp), values[5]);
};

function fnc_floor(values, context) {
    return Math.floor(values[0]);
};

function fnc_ceil(values, context) {
    return Math.ceil(values[0]);
};

function fnc_pi(values, context) {
    return Math.PI;
};

function fnc_to_int(values, context) {
    return parseInt(values[0]);
};

function fnc_to_real(values, context) {
    return parseFloat(values[0]);
};

function fnc_to_string(values, context) {
    return String(values[0]);
};

function fnc_to_datetime(values, context) {
    return false;
};

function fnc_to_date(values, context) {
    return false;
};

function fnc_to_time(values, context) {
    return false;
};

function fnc_to_interval(values, context) {
    return false;
};

function fnc_coalesce(values, context) {
    for (var i = 0; i < values.length; i++) {
        if (values[i] !== null){
            return values[i];
        }
    }
    return null;
};

function fnc_if(values, context) {
    if (values[0]){
        return values[1];
    }
    else{
        return values[2];
    }
};


function getFieldValues(layer, feature, value){
    features = layer.getSource().getFeatures();
    attrs = layer.get('attributes');
    attr = attrs[0];
    for (i = 0; i < attrs.length; i++){
        if (feature.get(attrs[i]) == value){
            attr = attrs[i];
        }
    }
    values = [];
    for (i = 0; i < features.length; i++){
        v = features[i].get(attr);
        values.push(v);
    }
    return values;
}

function fnc_relation_aggregate(values, context) {
    return false;
};

function fnc_count(values, context) {
    layer = layersMap[context.layer];
    numbers = getFieldValues(layer, context.feature, values[0]);
    return numbers.length();
};

function fnc_count_distinct(values, context) {
    layer = layersMap[context.layer];
    numbers = getFieldValues(layer, context.feature, values[0]);
    var len = numbers.filter(function(val, i, arr) {
        return arr.indexOf(val) === i;
    }).length;
    return len;
};

function fnc_count_missing(values, context) {
    return false;
};

function fnc_maximum(values, context) {
    layer = layersMap[context.layer];
    numbers = getFieldValues(layer, context.feature, values[0]);
    return Math.max.apply(null, numbers);
};

function fnc_minimum(values, context) {
    layer = layersMap[context.layer];
    numbers = getFieldValues(layer, context.feature, values[0]);
    return Math.min.apply(null, numbers);
};

function fnc_sum(values, context) {
    layer = layersMap[context.layer];
    numbers = getFieldValues(layer, context.feature, values[0]);
    var total = 0, i;
    for (i = 0; i < numbers.length; i += 1) {
        total += numbers[i];
    }
    return total;
};

function average(numbers){
    var total = 0, i;
    for (i = 0; i < numbers.length; i += 1) {
        total += numbers[i];
    }
    return total / numbers.length;
}
function fnc_mean(values, context) {
    layer = layersMap[context.layer];
    numbers = getFieldValues(layer, context.feature, values[0]);
    return average(numbers);
};

function fnc_median(values, context) {
    layer = layersMap[context.layer];
    numbers = getFieldValues(layer, context.feature, values[0]);
    var median = 0, numsLen = numbers.length;
    numbers.sort();
    if (numsLen % 2 === 0) {
        median = (numbers[numsLen / 2 - 1] + numbers[numsLen / 2]) / 2;
    } else {
        median = numbers[(numsLen - 1) / 2];
    }
    return median;
};

function fnc_stdev(values, context) {
    var layer = layersMap[context.layer];
    var numbers = getFieldValues(layer, context.feature, values[0]);
    var avg = average(numbers);

    var squareDiffs = numbers.map(function(value){
        var diff = value - avg;
        var sqrDiff = diff * diff;
        return sqrDiff;
    });

    var avgSquareDiff = average(squareDiffs);
    var stdDev = Math.sqrt(avgSquareDiff);
    return stdDev;
};

function fnc_range(values, context) {
    layer = layersMap[context.layer];
    numbers = getFieldValues(layer, context.feature, values[0]);
    numbers.sort();
    return [numbers[0], numbers[numbers.length - 1]];
};

function fnc_minority(values, context) {
    return false;
};

function fnc_majority(values, context) {
    return false;
};

function fnc_q1(values, context) {
    return false;
};

function fnc_q3(values, context) {
    return false;
};

function fnc_iqr(values, context) {
    return false;
};

function fnc_min_length(values, context) {
    return false;
};

function fnc_max_length(values, context) {
    return false;
};

function fnc_concatenate(values, context) {
    return false;
};

function fnc_aggregate(values, context) {
    var newContext = {
        feature: context.feature,
        variables: {},
        layer: values[0]
    };
    if (values[0] == "count"){
        return fnc_count([values[1]], newContext);
    }
    else if (values[0] == "count_distinct"){
        return fnc_count_distinct([values[1]], newContext);
    }
    else if (values[0] == "min"){
        return fnc_minimum([values[1]], newContext);
    }
    else if (values[0] == "max"){
        return fnc_maximum([values[1]], newContext);
    }
    else if (values[0] == "sum"){
        return fnc_sum([values[1]], newContext);
    }
    else if (values[0] == "mean"){
        return fnc_mean([values[1]], newContext);
    }
    else if (values[0] == "median"){
        return fnc_median([values[1]], newContext);
    }
    else if (values[0] == "sdtdev"){
        return fnc_sdtdev([values[1]], newContext);
    }
    else if (values[0] == "range"){
        return fnc_range([values[1]], newContext);
    }
};

function fnc_regexp_match(values, context) {
    return false;
};

function fnc_now(values, context) {
    return new Date().toISOString();
};

function fnc_age(values, context) {
    return false;
};

function fnc_year(values, context) {
    return false;
};

function fnc_month(values, context) {
    return false;
};

function fnc_week(values, context) {
    return false;
};

function fnc_day(values, context) {
    return false;
};

function fnc_hour(values, context) {
    return false;
};

function fnc_minute(values, context) {
    return false;
};

function fnc_second(values, context) {
    return false;
};

function fnc_day_of_week(values, context) {
    return false;
};

function fnc_lower(values, context) {
    return values[0].toLowerCase();
};

function fnc_upper(values, context) {
    return values[0].toLowerCase();
};

function fnc_title(values, context) {
    return values[0].split(' ').map(w => w[0].toUpperCase() + w.substr(1).toLowerCase()).join(' ');
};

function fnc_trim(values, context) {
    return values[0].trim();
};

function fnc_levenshtein(values, context) {
    var a = this, b = values[0] + "", m = [], i, j, min = Math.min;

    if (!(a && b)) return (b || a).length;

    for (i = 0; i <= b.length; m[i] = [i++]);
    for (j = 0; j <= a.length; m[0][j] = j++);

    for (i = 1; i <= b.length; i++) {
        for (j = 1; j <= a.length; j++) {
            m[i][j] = b.charAt(i - 1) == a.charAt(j - 1)
                ? m[i - 1][j - 1]
                : m[i][j] = min(
                    m[i - 1][j - 1] + 1,
                    min(m[i][j - 1] + 1, m[i - 1 ][j] + 1))
        }
    }

    return m[b.length][a.length];
};

var indexMap = function(list) {
  var map = {}
  list.forEach(function(each, i) {
    map[each] = map[each] || []
    map[each].push(i)
  })
  return map
}

function fnc_longest_common_substring(values, context) {
    var result = {startString1:0, startString2:0, length:0}
      var indexMapBefore = indexMap(values[0])
      var previousOverlap = []
      values[1].forEach(function(eachAfter, indexAfter) {
        var overlapLength
        var overlap = []
        var indexesBefore = indexMapBefore[eachAfter] || []
        indexesBefore.forEach(function(indexBefore) {
          overlapLength = ((indexBefore && previousOverlap[indexBefore-1]) || 0) + 1;
          if (overlapLength > result.length) {
            result.length = overlapLength;
            result.startString1 = indexBefore - overlapLength + 1;
            result.startString2 = indexAfter - overlapLength + 1;
          }
          overlap[indexBefore] = overlapLength
        })
        previousOverlap = overlap
      })
      return result
};

function fnc_hamming_distance(values, context) {
    return false;
};

function fnc_soundex(values, context) {
    return false;
};

function fnc_char(values, context) {
    return String.fromCharCode(values[0]);
};

function fnc_wordwrap(values, context) {
    var re = new RegExp("([\\w\\s]{" + (values[1] - 2) + ",}?\\w)\\s?\\b", "g")
    return values[0].replace(re,"$1\n")
};

function fnc_length(values, context) {
    return values[0].length;
};

function fnc_replace(values, context) {
    try{
        return values[0].replace(values[1], values[2]);
    }catch(e){
        return "";
    }

};

function fnc_regexp_replace(values, context) {
    var re = new RegExp(values[1])
    return values[0].replace(re, values[2])
};

function fnc_regexp_substr(values, context) {
    return values[0].match(values[1])[1];
};

function fnc_substr(values, context) {
    return values[0].substring(values[1], values[2] + values[1]);
};

function fnc_concat(values, context) {
    s = ""
    for (var i = 0; i < values.length; i++) {
        if (values[i] !== null){
            s += values[i];
        }
    }
    return s
};

function fnc_strpos(values, context) {
    return values[0].indeOf(values[1]);
};

function fnc_left(values, context) {
    return values[0].substring(0, values[1]);
};

function fnc_right(values, context) {
    return values[0].substring(values[0].length - values[1], values[0].length);
};

function fnc_rpad(values, context) {
    return values[0] + Array(values[1]-values[0].length+1).join(values[2]);
};

function fnc_lpad(values, context) {
    return Array(values[1]-values[0].length+1).join(values[2])+values[0];
};

function fnc_format(values, context) {
    var s = values[0];
    for (var i = 1; i < values.length; i++) {
      s = s.replace("%" + String(i), values[i]);
    }
    return s;

};

function fnc_format_number(values, context) {
    return values[0].toFixed(values[1]);
};

function fnc_format_date(values, context) {
    return false;
};

function fnc_color_rgb(values, context) {
    return false;
};

function fnc_color_rgba(values, context) {
    return false;
};

function fnc_ramp_color(values, context) {
    return false;
};

function fnc_color_hsl(values, context) {
    return false;
};

function fnc_color_hsla(values, context) {
    return false;
};

function fnc_color_hsv(values, context) {
    return false;
};

function fnc_color_hsva(values, context) {
    return false;
};

function fnc_color_cmyk(values, context) {
    return false;
};

function fnc_color_cmyka(values, context) {
    return false;
};

function fnc_color_part(values, context) {
    return false;
};

function fnc_darker(values, context) {
    return false;
};

function fnc_lighter(values, context) {
    return false;
};

function fnc_set_color_part(values, context) {
    return false;
};

function fnc_area(values, context) {
    return values[0].getArea()
};

function fnc_perimeter(values, context) {
    return new ol.geom.LineString(values[0].getCoordinates()).getLength()
};

function fnc_x(values, context) {
    return ol.extent.getCenter(values[0].getExtent())[0];
};

function fnc_y(values, context) {
    return ol.extent.getCenter(values[0].getExtent())[1];
};

function fnc_z(values, context) {
    return false;
};

function fnc_m(values, context) {
    return false;
};

function fnc_point_n(values, context) {
    return new ol.geom.Point(values[0].getCoordinates()[values[1]]);
};

function fnc_start_point(values, context) {
    return new ol.geom.Point(values[0].getCoordinates()[0]);
};

function fnc_end_point(values, context) {
    coords = values[0].getCoordinates()
    return new ol.geom.Point(coords[coords.length - 1]);
};

function fnc_nodes_to_points(values, context) {
    return false;
};

function fnc_segments_to_lines(values, context) {
    return false;
};

function fnc_make_point(values, context) {
    return false;
};

function fnc_make_point_m(values, context) {
    return false;
};

function fnc_make_line(values, context) {
    return false;
};

function fnc_make_polygon(values, context) {
    return false;
};

function fnc_x_min(values, context) {
    return ol.extent.getBottomLeft(values[0].getExtent())[0]
};

function fnc_x_max(values, context) {
    return ol.extent.getTopRight(values[0].getExtent())[0]
};

function fnc_y_min(values, context) {
    return ol.extent.getBottomLeft(values[0].getExtent())[1]
};

function fnc_y_max(values, context) {
    return ol.extent.getTopRight(values[0].getExtent())[1]
};

function fnc_geom_from_wkt(values, context) {
    return false;
};

function fnc_geom_from_gml(values, context) {
    return false;
};

function fnc_relate(values, context) {
    return false;
};

function fnc_intersects_bbox(values, context) {
    return false;
};

function fnc_disjoint(values, context) {
    return false;
};

function fnc_intersects(values, context) {
    return fnc_intersection(values, context) != undefined;
};

function fnc_touches(values, context) {
    return false;
};

function fnc_crosses(values, context) {
    return false;
};

function fnc_contains(values, context) {
    return false;
};

function fnc_overlaps(values, context) {
    return false;
};

function fnc_within(values, context) {
    return false;
};

function fnc_translate(values, context) {
    geom = values[0].clone();
    var translated = geom.translate(values[1], values[2]);
    return translated
};

function fnc_buffer(values, context) {
    var parser = new jsts.io.OL3Parser();
    var geom = parser.read(values[0]);
    var buffer = geom.buffer(values[1]);
    return parser.write(buffer);
};

function fnc_centroid(values, context) {
    var parser = new jsts.io.OL3Parser();
    var geom = parser.read(values[0]);
    var coord = jsts.algorithm.Centroid.getCentroid(geom)
    return new ol.geom.Point([coord.x, coord.y])
};

function fnc_point_on_surface(values, context) {
    var geom = geojsonFromGeometry(values[0]);
    var pt =  turf.pointOnSurface(geom);
    return geometryFromGeojson(pt);
};

function fnc_reverse(values, context) {
    return false;
};

function fnc_exterior_ring(values, context) {
    return false;
};

function fnc_interior_ring_n(values, context) {
    return false;
};

function fnc_geometry_n(values, context) {
    return false;
};

function fnc_boundary(values, context) {
    return false;
};

function fnc_line_merge(values, context) {
    return false;
};

function fnc_bounds(values, context) {
    return false;
};

function fnc_num_points(values, context) {
    return values[0].getCoordinates().length
};

function fnc_num_interior_rings(values, context) {
    return false;
};

function fnc_num_rings(values, context) {
    return false;
};

function fnc_num_geometries(values, context) {
    return false;
};

function fnc_bounds_width(values, context) {
    return false;
};

function fnc_bounds_height(values, context) {
    return false;
};

function fnc_is_closed(values, context) {
    return false;
};

function fnc_convex_hull(values, context) {
    var parser = new jsts.io.OL3Parser();
    var geom = parser.read(values[0]);
    var hull = jsts.algorithm.ConvexHull.getConvexHull(geom)
    return parser.write(hull)
};

function fnc_difference(values, context) {
    var parser = new jsts.io.OL3Parser();
    var geom = parser.read(values[0]);
    var geom2 = parser.read(values[1]);
    var diff = geom.difference(geom2);
    return parser.write(diff);
};

function fnc_distance(values, context) {
    return false;
};

function fnc_intersection(values, context) {
    var parser = new jsts.io.OL3Parser();
    var geom = parser.read(values[0]);
    var geom2 = parser.read(values[1]);
    var diff = geom.intersection(geom2);
    return parser.write(diff);
};

function fnc_sym_difference(values, context) {
    return false;
};

function fnc_combine(values, context) {
    return false;
};

function fnc_union(values, context) {
    var parser = new jsts.io.OL3Parser();
    var geom = parser.read(values[0]);
    var geom2 = parser.read(values[1]);
    var diff = geom.union(geom2);
    return parser.write(diff);
};

function fnc_geom_to_wkt(values, context) {
    return false;
};

function fnc_geometry(values, context) {
    return false;
};

function fnc__geometry(values, context) {
    return context.feature.getGeometry();
};


function fnc_transform(values, context) {
    return false;
};

function fnc_extrude(values, context) {
    return false;
};

function fnc_order_parts(values, context) {
    return false;
};

function fnc_closest_point(values, context) {
    return false;
};

function fnc_shortest_line(values, context) {
    return false;
};

function fnc_line_interpolate_point(values, context) {
    return false;
};

function fnc_line_interpolate_angle(values, context) {
    return false;
};

function fnc_line_locate_point(values, context) {
    return false;
};

function fnc_angle_at_vertex(values, context) {
    return false;
};

function fnc_distance_to_vertex(values, context) {
    return false;
};

function fnc_uuid(values, context) {
    return false;
};

function fnc_get_feature(values, context) {
    return false;
};

function fnc_layer_property(values, context) {
    return false;
};

function fnc_var(values, context) {
    return false;
};

function fnc_eval(values, context) {
    return false;
};

function fnc_attribute(values, context) {
    return false;
};

function fnc__specialcol_(values, context) {
    return false;
};

function fnc_project_color(values, context) {
    return false;
};
