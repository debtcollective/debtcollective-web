app.controller('corinthianCtrl',
  function ($scope, $http, util_svc) {

    $scope.current = false;
    $scope.grad = false;
    $scope.attending = false;
    $scope.concerns = false;
    $scope.charges = false;
    $scope.status = false;
    $scope.paying = false;

    $scope.visible = {}

    $scope.isVisible = function (i) {
      if($scope.visible[i] == undefined) {
        return false;
      }
      return $scope.visible[i];
    }

    $scope.FAQ_ANSWERS = {
      "all" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
      "current": [1, 5, 6, 9, 12, 13, 14],
      "grad": [3, 8, 10],
      "attending": [1, 14],
      "value": [1, 12, 13, 14],
      "charges": [2, 4],
      "status": [5, 6, 7],
      "paying": [3, 8, 10, 11]
    }

    $scope.updateVis = function () {
      $scope.visible = {}
      for(key in $scope.FAQ_ANSWERS) {
        if($scope[key]) {
          for(idx in $scope.FAQ_ANSWERS[key]) {
            q = $scope.FAQ_ANSWERS[key][idx];
            $scope.visible[q] = true;
          }
        }
      }
    }
});
