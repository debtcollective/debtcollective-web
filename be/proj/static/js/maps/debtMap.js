app.controller('mapCtrl', function ($scope, $http, util_svc) {
    var map = new AmCharts.AmMap();

    /************
    MAP SETTINGS
    ************/
    map.areasSettings = {
        autoZoom: true,
        selectedColor: "#CC0000"
    };

    map.pathToImages = "/static/js/vendor/ammap/images/";
    map.useHandCursorOnClickableOjects = true

    // hand drawn look & feel
    map.handDrawn = true;
    map.handDrawScatter = 3;
    map.handDrawThickness = 4;

    // square
    var targetSVG = "M-4.5,5.5 L5.5,5.5 L5.5,-4.5 L-4.5,-4.5 Z";

    // get data
    var dataProvider = {
        map: "worldHigh"
    };
    $http.get('/map_data/').then(function (resp) {
        var parsedImages = [];
        var total_amount = resp.data.total_amount;
        var points = resp.data.points;

        var point;
        for (idx in points) {
            point = createAmChartPoint(points[idx]);
            point['scale'] = getPointScale(parseFloat(point['sum_amount']/total_amount));
            parsedImages.push(point);
        }

        dataProvider['images'] = parsedImages;
        map.dataProvider = dataProvider;
        map.validateNow();
        map.write("mapdiv");
    });

    /**********
     FUNCTIONS
    ***********/
    function getPointScale(percentage) {
        /*
        Gets the point's scale based on the percentage of
        users in that location vs. all locations.
        */

        // TODO
        return Math.min(5, Math.max(.75, .5 + percentage));
    }

    function getPointTitle(point) {
        /*
        Creates a title for the given point. Examples:
        "Pasadena
         1 member"
        "New York
         32 members"
        */

        var suffix = " member";
        if (point['num_users'] > 1) {
            suffix += 's';
        }
        return point['name'] + "<br>" + point['num_users'] + suffix;
    }

    function createAmChartPoint(point) {
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

        point['title'] = getPointTitle(point);
        point['svgPath'] = targetSVG;
        point['color'] = '#B00000';
        return point
    }

    // TODO: on map object click
    map.addListener("clickMapObject", function (event) {
        console.log(event);
        if (event.mapObject.id != undefined && chartData[event.mapObject.id] != undefined) {
            console.log(event.mapObject.id);
        }
    });

});
