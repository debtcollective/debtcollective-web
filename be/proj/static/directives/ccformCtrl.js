app.directive('corinthianSignupForm', function () {
  return {
    restrict: 'E',
    templateUrl: '/static/directives/ccform.html',
    replace: true,
    controller: function ($scope, $element, $document, $http, $window, users) {
      $scope.strikeFormSubmitted = false

      $scope.submitForm = function () {
        if (!$scope.debtAmount) {
          return
        }

        var data = {
          'email': $scope.email,
          'list': 'RUDSi1E892892XdpjO763892Zxq892hw'
        }

        $http.post('//mail.debtcollective.org/subscribe', data).then(function (resp) {
          $scope.strikeFormSubmitted = true
          var someElement = angular.element(document.getElementById('signup-prompt'));
          $document.scrollToElement(someElement, 150, 500);
        })
      }
    }
  }
})