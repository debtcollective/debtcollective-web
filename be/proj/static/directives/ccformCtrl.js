app.directive('corinthianSignupForm', function () {
  return {
    restrict: 'E',
    templateUrl: '/static/directives/ccform.html',
    replace: true,
    controller: function ($scope, $element, $window, users) {

      $scope.submitForm = function () {
        var userData = {
          'email': $scope.email,
          'point': undefined,
          'kind': 'student',
          'amount': parseFloat($scope.debtAmount.replace(',', ''))
        }

        users.createAnonymousUser(userData, function () {
          var salliemae = 0
          var corinthian = 1
          users.gDocsCollectiveCounter(salliemae, corinthian)
          $window.location.href = '/thankyou'
        })
      }
    }
  }
})