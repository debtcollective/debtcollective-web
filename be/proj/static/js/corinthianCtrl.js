app.controller('corinthianCtrl',
  function ($scope, $http, util_svc) {

    $scope.visChoice = 'all';
    $scope.visible = {};

    var FAQ_ANSWERS = {
      "all" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
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

    $scope.$watch('visChoice', function (newVal, oldVal) {
        $scope.visible = {}
        for(idx in FAQ_ANSWERS[newVal]) {
          q = FAQ_ANSWERS[newVal][idx];
          $scope.visible[q] = true;
        }
    });

});
