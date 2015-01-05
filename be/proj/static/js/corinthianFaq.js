app.controller('corinthianFaqCtrl',
  function ($scope, $http, $document, util_svc) {

    $scope.visible = {};

    $scope.all = true;
    $scope.current = false;
    $scope.grad = false;
    $scope.attending = false;
    $scope.concerns = false;
    $scope.charges = false;
    $scope.status = false;
    $scope.paying = false;
    $scope.genesis = false;

    var FAQ_ANSWERS = {
      "all" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
      "current": [1, 5, 6, 9, 12, 13, 14],
      "grad": [3, 8, 10],
      "attending": [1, 14],
      "value": [1, 12, 13, 14],
      "charges": [2, 4],
      "status": [5, 6, 7],
      "paying": [3, 8, 10, 11],
      "genesis": [15]
    }

    $scope.isVisible = function (i) {
      if($scope.visible[i] == undefined) {
        return false;
      }
      return $scope.visible[i];
    }

    $scope.scrollClick = function () {
      var someElement = angular.element(document.getElementById('mapdiv'));
      $document.scrollToElement(someElement, 0, 18000);
    }

    $scope.updateVis = function () {
      $scope.visible = {}
      for(key in FAQ_ANSWERS) {
        if($scope[key]) {
          for(idx in FAQ_ANSWERS[key]) {
            $scope.all = false;
            q = FAQ_ANSWERS[key][idx];
            $scope.visible[q] = true;
          }
        }
      }
    }
    $scope.updateVis();

});
