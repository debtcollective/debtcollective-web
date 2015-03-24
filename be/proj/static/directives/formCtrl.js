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
      $scope.showForm = false;
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

      $scope.$watch('corinthianStudent', function (newVal, oldVal) {
        if (newVal == 'option1') { // true
          document.getElementById('email').setAttribute('name', 'cm-nuriti-nuriti')
          document.getElementById('signupForm').setAttribute('action', "//strikedebt.createsend.com/t/j/s/nuriti/")
        }
        if (newVal == 'option2') { // false
          document.getElementById('email').setAttribute('name', 'cm-nskul-nskul')
          document.getElementById('signupForm').setAttribute('action', "//strikedebt.createsend.com/t/j/s/nskul/")
        }
      })

      $scope.addDebt = function () {
        $scope.debts.push({
          debtType: 'none',
          amount: null
        })
      }
      $scope.addDebt()

      $scope.formFocus = function () {
        $scope.showForm = true;
      }

      $scope.corinthianSubmitClick = function ($event) {
        $scope.formSubmitted = true
      }

      $scope.onSubmitClick = function ($event) {
        // temporarily, email is the password
        // so that we can protect anonymity of our users.
        // campaign monitor handles mailing lists
        // just store one debt type for now.
        $scope.formSubmitted = true;
        $scope.showForm = true;

        var debt = $scope.debts[0]
        var userData = {
          'email': $scope.email,
          'point': $scope.location.id,
          'kind': debt.debtType.id,
          'amount': parseFloat(debt.amount.replace(',', ''))
        }

        users.createAnonymousUser(userData, function () {

          var salliemae = 0
          if ($scope.salliemae == 'option1') {
            salliemae = 1
          }

          var corinthian = 0
          if ($scope.corinthianStudent == 'option1') {
            corinthian = 1
          }

          users.gDocsCollectiveCounter(salliemae, corinthian)
        })
      }
    }
  }
})