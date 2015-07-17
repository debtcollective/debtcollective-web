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

    $http.get('/static/data/sstrike.json').then(function (resp) {
      var json = resp.data.rows;
      $scope.num = json.length;
      $scope.solidarityStrikers = json.chunk(4);
      $scope.doneLoading = true;
    })
})
