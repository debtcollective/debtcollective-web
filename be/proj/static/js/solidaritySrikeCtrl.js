
Array.prototype.chunk = function(chunkSize) {
    var array=this;
    return [].concat.apply([],
        array.map(function(elem,i) {
            return i%chunkSize ? [] : [array.slice(i,i+chunkSize)];
        })
    );
}

app.controller('solidarityStrikeCtrl',
  function ($scope, $window, $http, $document) {
    $scope.solidarityStrikers = [];
    $scope.currentChunk = 0;
    $scope.num = 0;

    $scope.nextChunk = function () {
      if ($scope.currentChunk === ($scope.solidarityStrikers.length - 3)) return
      else $scope.currentChunk += 3
    }

    $scope.lastChunk = function () {
      if ($scope.currentChunk === 0) return
      else $scope.currentChunk -= 3
    }

    function fetchTallies () {

      var ds = new Miso.Dataset({
        importer : Miso.Dataset.Importers.GoogleSpreadsheet,
        parser : Miso.Dataset.Parsers.GoogleSpreadsheet,
        key : "1r4ZVySodsuZnFqabsSUezJ4CysEs1RwVX9jZj-AjzKQ",
        worksheet : "2"
      });
      ds.fetch({
        success: function () {
          var json = this.toJSON();
          $scope.num = json.length;
          $scope.solidarityStrikers = json.chunk(4)
          $scope.doneLoading = true;
          $scope.$digest();
        },
        error : function() {
          console.log("Are you sure you are connected to the internet?");
          setTimeout(fetchTallies, 500)
        }
      })
    }

    fetchTallies()
})