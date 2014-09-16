app.controller('mapCtrl', function ($scope, $http, util_svc) {
    var map = new AmCharts.AmMap();

    /************
    MAP SETTINGS
    ************/

    var POINT_COLOR = "#e8ffa0";
    map.areasSettings = {
        autoZoom: true,
        selectedColor: "#CC0000",
        unlistedAreasColor: "#e0e0d5",
        unlistedAreasOutlineColor: "#000",
    };

    map.zoomControl = {
        zoomControlEnabled: false,
        panControlEnabled: false
    }

    map.pathToImages = "/static/js/vendor/ammap/images/";
    map.useHandCursorOnClickableOjects = true

    map.mouseWheelZoomEnabled = false;
    map.panEventsEnabled = false;


    // hand drawn look & feel
    map.handDrawn = true;
    map.handDrawScatter = 3;
    map.handDrawThickness = 4;

    // square
    var targetSVG = "M16,1.466C7.973,1.466,1.466,7.973,1.466,16c0,8.027,6.507,14.534,14.534,14.534c8.027,0,14.534-6.507,14.534-14.534C30.534,7.973,24.027,1.466,16,1.466z M17.255,23.88v2.047h-1.958v-2.024c-3.213-0.44-4.621-3.08-4.621-3.08l2.002-1.673c0,0,1.276,2.223,3.586,2.223c1.276,0,2.244-0.683,2.244-1.849c0-2.729-7.349-2.398-7.349-7.459c0-2.2,1.738-3.785,4.137-4.159V5.859h1.958v2.046c1.672,0.22,3.652,1.1,3.652,2.993v1.452h-2.596v-0.704c0-0.726-0.925-1.21-1.959-1.21c-1.32,0-2.288,0.66-2.288,1.584c0,2.794,7.349,2.112,7.349,7.415C21.413,21.614,19.785,23.506,17.255,23.88z"
    // get data
    var dataProvider = {
        map: "worldHigh",
        zoomLevel: 2,
        zoomLatitude: 39.096169,
        zoomLongitude: -98.198721
    };
    $http.get('/static/js/map_data.json').then(function (resp) {
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
        map.zoomIn();
    });

    var mapZoomed = false;

    $scope.$watch('yLoc', function (newVal, oldVal) {
        if(newVal >= 4000 && !mapZoomed) {
            mapZoomed = true;
            map.zoomIn();
        }
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
        return Math.min(4, Math.max(.75, .5 + percentage));
    }

    function getPointTitle(point) {
        /*
        Creates a title for the given point.
        */
        return point['name'] + "<br> $" + point['sum_amount'];
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
        point['type'] = 'circle';
        point['color'] = POINT_COLOR;
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
