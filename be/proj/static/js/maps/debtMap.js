app.controller('mapCtrl', function ($scope, $http, util_svc) {
    var map = new AmCharts.AmMap();

    map.pathToImages = "/static/js/vendor/ammap/images/";

    // square
    var targetSVG = "M-4.5,5.5 L5.5,5.5 L5.5,-4.5 L-4.5,-4.5 Z";

    var dataProvider = {
        map: "worldHigh"
    };

    map.addListener("clickMapObject", function (event) {
        console.log(event);
        if (event.mapObject.id != undefined && chartData[event.mapObject.id] != undefined) {
            console.log(event.mapObject.id);
        }
    });

    map.areasSettings = {
        autoZoom: true,
        selectedColor: "#CC0000"
    };

    map.useHandCursorOnClickableOjects = true
    map.handDrawn = true;
    map.handDrawScatter = 3;
    map.handDrawThickness = 4;

    $http.get('/map_data/').then(function (resp) {
        parsedImages = [];
        for (idx in resp.data) {
            point = resp.data[idx];
            parsedImages.push(amChartPoint(point));
        }
        dataProvider['images'] = parsedImages;
        map.dataProvider = dataProvider;
        map.validateNow();
        map.write("mapdiv");
    });

    function pointTitle(point) {
        /*
        Creates a title for the given point.
        e.g.
        Pasadena
        1 debtor

        New York
        32 debtors
        */
        var suffix = " debtor";
        if (point['num_users'] > 1) {
            suffix += 's';
        }
        return point['name'] + "<br>" + point['num_users'] + suffix;
    }

    function amChartPoint(point) {
        /*
        Creates an amChart point from the given point
        that is given to us in the backend.

        Parameters
        ----------
        - point (dict)
            latitude
            longitude
            name
            num_users
        */
        point['title'] = pointTitle(point);
        point['svgPath'] = targetSVG;
        point['color'] = '#B00000';
        point['scale'] = Math.min(point['num_users'], 3)
        return point
    }
});
