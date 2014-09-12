app.controller('mapCtrl', function ($scope, $http, util_svc) {
    var map = new AmCharts.AmMap();

    map.pathToImages = "/static/js/vendor/ammap/images/";

    // square
    var targetSVG = "M-4.5,5.5 L5.5,5.5 L5.5,-4.5 L-4.5,-4.5 Z";

    var dataProvider = {
        map: "worldHigh",
        images:[
            // todo: get a list of the locations
            {latitude:32.57, longitude:-85.57, svgPath: targetSVG,
            color:"#B00000", title: "Arizona: 300 credit card debtors", scale: 1.5, zoomLevel: 5},
            {latitude:40.3951, longitude:-73.5619, svgPath: targetSVG,
            color:"#B00000", title: "Arizona: 300 credit card debtors", scale: 1.5, zoomLevel: 5},
        ]

    };

    map.addListener("clickMapObject", function (event) {
        console.log(event);
        if (event.mapObject.id != undefined && chartData[event.mapObject.id] != undefined) {
            console.log(event.mapObject.id);
        }
    });

    map.dataProvider = dataProvider;

    map.areasSettings = {
        autoZoom: true,
        selectedColor: "#CC0000"
    };

    map.useHandCursorOnClickableOjects = true
    map.handDrawn = true;
    map.handDrawScatter = 3;
    map.handDrawThickness = 4;
    map.write("mapdiv");

});
