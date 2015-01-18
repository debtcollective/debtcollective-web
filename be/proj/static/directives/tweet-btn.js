app.directive('tweetBtn', function ($window) {
  return {
    restrict: 'E',
    replace: true,
    scope: {
      'tweetText': '&'
    },
    templateUrl: '/static/directives/tweetBtn.html',
    controller: function ($scope, $element, $attrs) {
      $scope.tweetText = $scope.text
      //$scope.twitterText = encodeURIComponent($scope.text);
    }
  }
})