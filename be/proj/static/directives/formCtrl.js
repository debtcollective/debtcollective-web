app.directive('signupform', function () {
  return {
    restrict: 'E',
    templateUrl: '/static/directives/form.html',
    replace: true,
    scope: {
      open: '=',
      afterSubmit: '&'
    },
    controller: function ($scope, $element, $location, $http, $document, $timeout, $window, users, banner) {
      $scope.email = $location.search().email
      $scope.username = null
      $scope.debts = []
      $scope.amount = null
      $scope.showForm = false
      $scope.formSubmitted = false
      $scope.location = null
      $scope.focused = false
      $scope.corinthianStudent = false
      $scope.cities = []

      var form = $element.find('form')[0]


      if ($scope.open) $scope.showForm = true

      // TODO: get query. if 'email' in query params, auto-fill.

      $http.get('/debt_choices').then(function (resp) {
        $scope.debt_choices = resp.data
      })

      $http.get('/points').then(function (resp) {
        $scope.cities = resp.data
      })

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
        $scope.showForm = true

        var debt = $scope.debts[0]
        var userData = {
          'email': $scope.email.toLowerCase(),
          'password': $scope.password,
          'point': $scope.location ? $scope.location.id : null,
          'kind': debt.debtType.id,
          'amount': parseFloat(debt.amount.replace(',', ''))
        }

        users.create(userData, function (resp) {
          if (resp.data.status === 'error') return banner.message('error', resp.data.message)
          else if (resp.data.status === 'logged_in') window.location.href = '/profile'
          else if (resp.data.status === 'user_exists') window.location.href = '/login'
          else {
            $scope.afterSubmit()
            $scope.formSubmitted = true
          }
        })
        $event.preventDefault()
      }
    }
  }
})
