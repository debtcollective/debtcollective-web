app.directive('corinthianSignupForm', function () {
  return {
    restrict: 'E',
    templateUrl: '/static/directives/ccform.html',
    replace: true,
    controller: function ($scope, $element, $http, $window, users) {

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
            "email": $scope.email,
            "name": userId,
            "list": "RUDSi1E892892XdpjO763892Zxq892hw"
          }

          $http.post('//mail.debtcollective.org/subscribe', data)
          .then(function (resp) {
            console.log(resp)
            $window.location.href = '/thankyou'
          })
        })
      }
    }
  }
})