app.directive('signupform', function () {
  return {
    restrict: 'E',
    templateUrl: '/static/directives/form.html',
    replace: true,
    scope: {
      visible: '='
    },
    controller: function ($scope, $element, $http, $document, $timeout, $window, users) {
      $scope.email = null;
      $scope.username = null;
      $scope.debts = [];
      $scope.amount = null;
      $scope.showForm = true;
      $scope.formSubmitted = false;
      $scope.location = null;
      $scope.focused = false;
      $scope.corinthianStudent = false;
      $scope.cities = []

      var form = $element.find('form')[0]

      $http.get('/debt_choices').then(function (resp) {
        $scope.debt_choices = resp.data
      });

      $http.get('/points').then(function (resp) {
        $scope.cities = resp.data
      });

      $scope.addDebt = function () {
        $scope.debts.push({
          debtType: 'none',
          amount: null
        })
      }
      $scope.addDebt()

      $scope.onSubmitClick = function ($event) {
        // temporarily, email is the password
        // so that we can protect anonymity of our users.
        // just store one debt type for now.
        $scope.formSubmitted = true;
        $scope.showForm = true;

        var debt = $scope.debts[0]
        var userData = {
          'email': $scope.email.toLowerCase(),
          'point': $scope.location ? $scope.location.id : null,
          'kind': debt.debtType.id,
          'amount': parseFloat(debt.amount.replace(',', ''))
        }

        users.createAnonymousUser(userData, function (resp) {
          console.log('created user', resp)
          $scope.formSubmitted = true
        })
        $event.preventDefault()
      }
    }
  }
})
