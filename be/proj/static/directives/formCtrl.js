//everything is awesome! :()
function qs (key) {
  key = key.replace(/[*+?^$.\[\]{}()|\\\/]/g, "\\$&"); // escape RegEx meta chars
  var match = location.search.match(new RegExp("[?&]"+key+"=([^&]+)(&|$)"));
  return match && decodeURIComponent(match[1].replace(/\+/g, " "));
}
app.directive('signupform', function () {
  return {
    restrict: 'E',
    templateUrl: '/static/directives/form.html',
    replace: true,
    scope: {
      open: '=',
      afterSubmit: '&',
      collectDebt: '=',
      noRedirect: '='
    },
    controller: function ($scope, $element, $location, $http, $document, $timeout, $window, users, banner) {
      $scope.email = qs('email')
      $scope.username = null
      $scope.debts = []
      $scope.showForm = false
      $scope.formSubmitted = false
      $scope.location = null
      $scope.focused = false
      $scope.corinthianStudent = false
      $scope.cities = []

      var form = $element.find('form')[0]

      if ($scope.open) $scope.showForm = true

      $http.get('/debt_choices').then(function (resp) {
        $scope.debt_choices = resp.data
      })

      $http.get('/points').then(function (resp) {
        $scope.cities = resp.data
      })

      $scope.addDebt = function (type, amount) {
        $scope.debts.push({
          debtType: type || 'none',
          amount: amount || null
        })
      }
      $scope.addDebt(null, qs('amount'))

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
          else if ($scope.noRedirect) return $scope.afterSubmit()
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
