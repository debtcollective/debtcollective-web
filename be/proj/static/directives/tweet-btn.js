app.directive('tweetBtn', function ($window) {
  return {
    restrict: 'E',
    replace: true,
    scope: {
      'text': '='
    },
    templateUrl: '/static/directives/tweetBtn.html',
    controller: function ($scope, $element, $attrs) {
      $scope.tweetText = $attrs.text
      $scope.twitterText = encodeURIComponent($attrs.text);
    }
  }
})