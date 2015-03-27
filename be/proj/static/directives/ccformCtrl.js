app.directive('corinthianSignupForm', function () {
  return {
    restrict: 'E',
    templateUrl: '/static/directives/ccform.html',
    replace: true,
    controller: function ($scope, $element, $http, $window, users) {
      $scope.strikeFormSubmitted = false

      $scope.submitForm = function () {
        if (!$scope.debtAmount) {
          return
        }

        var userData = {
          'email': $scope.email,
          'point': undefined,
          'kind': 'student',
          'amount': parseFloat($scope.debtAmount.replace(',', ''))
        }

        users.createAnonymousUser(userData, function (resp, userId) {
          var salliemae = 0
          var corinthian = 1
          users.gDocsCollectiveCounter(salliemae, corinthian)

          var data = {
            "cm-nuriti-nuriti": $scope.email, // email
            "cm-name": userId, // name
            "callback": "JSON_CALLBACK"
          }

          $http.jsonp('//strikedebt.createsend.com/t/j/s/nuriti', {
            params: data
          }).then(function (resp) {
            console.log(resp)
            $scope.strikeFormSubmitted = true
          })
        })
      }
    }
  }
})