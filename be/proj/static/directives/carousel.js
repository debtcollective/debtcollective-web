app.directive('carousel', function ($window) {
  return {
    restrict: 'E',
    scope: {
      'data': '=data'
    },
    replace: true,
    templateUrl: '/static/directives/carousel.html',
    controller: function ($scope) {
      $scope.selectionIndex = 0;

      $scope.prev = function () {
        $scope.selectionIndex -= 1;
        if ($scope.selectionIndex < 0) {
          $scope.selectionIndex = $scope.data.length - 1
        }
      }

      $scope.next = function () {
        $scope.selectionIndex += 1;
        if ($scope.selectionIndex >= $scope.data.length) {
          $scope.selectionIndex = 0
        }
      }

    }
  }
})
