app.directive('fbButton', function ($window) {
  return {
    restrict: 'E',
    transclude: true,
    replace: true,
    templateUrl: '/static/directives/fbButton.html',
    controller: function ($scope, $element, $attrs) {

    }
  }
})