app.directive('carousel', function ($window) {
  return {
    restrict: 'E',
    scope: {
      'data': '=data'
    },
    templateUrl: '/static/directives/carousel.html',
    controller: function ($scope) {
      $scope.selectionIndex = 0;

      $scope.prev = function() {
        $scope.selectionIndex += 1;
      }

      $scope.next = function() {
        $scope.selectionIndex += 1;
      }

    }
  }
})
