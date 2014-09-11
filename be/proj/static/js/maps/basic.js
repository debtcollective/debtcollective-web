app.controller('mapCtrl', function ($scope, $http, util_svc) {
    // create AmMap object
    var map = new AmCharts.AmMap();
    // set path to images
    map.pathToImages = "/static/js/vendor/ammap/images/";

    /* create data provider object
     map property is usually the same as the name of the map file.

     getAreasFromMap indicates that amMap should read all the areas available
     in the map data and treat them as they are included in your data provider.
     in case you don't set it to true, all the areas except listed in data
     provider will be treated as unlisted.
    */
    var dataProvider = {
        map: "usaHigh",
        getAreasFromMap: false,
        images:[
            // todo: get a list of the locations
            {latitude:40.3951, longitude:-73.5619, type:"rectangle", color:"#B00000"}
        ]

    };
    // pass data provider to the map object
    map.dataProvider = dataProvider;

    /* create areas settings
     * autoZoom set to true means that the map will zoom-in when clicked on the area
     * selectedColor indicates color of the clicked area.
     */
    map.areasSettings = {
        autoZoom: true,
        selectedColor: "#CC0000"
    };

    // write the map to container div
    map.write("mapdiv");
});
