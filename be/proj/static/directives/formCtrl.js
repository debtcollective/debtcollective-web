app.directive('signupform', function () {
  return {
    restrict: 'E',
    templateUrl: '/static/directives/form.html',
    replace: true,
    scope: {
      visible: '='
    },
    controller: function ($scope, $element, $http, util_svc, $document, $timeout, $window) {

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

      $scope.addDebt = function () {
        $scope.debts.push({
          debtType: 5,
          amount: null
        })
      }
      $scope.addDebt()

      $scope.formFocus = function () {
        $scope.showForm = true;
      }

      $scope.$watch('corinthianStudent', function (newVal, oldVal) {
        if (newVal) {
          $scope.showForm = true
          $scope.debts[0].debtType = {
            id: 'student',
            name: 'Student'
          }
          form.setAttribute('action', '//strikedebt.createsend.com/t/j/s/nuriti/')
        }
        else {
          form.setAttribute('action', '//strikedebt.createsend.com/t/j/s/nskul/')
        }
      })

      $scope.corinthianSubmitClick = function ($event) {
        $scope.formSubmitted = true
      }

      $scope.onSubmitClick = function ($event) {
        // temporarily, email is the password
        // so that we can protect anonymity of our users.
        // campaign monitor handles mailing lists
        $scope.username = util_svc.generateUUID();

        // just store one debt type for now.
        var debt = $scope.debts[0]
        data = {
            'username': $scope.username,
            'password': $scope.email,
            'point': $scope.location.id,
            'kind': debt.debtType.id,
            'amount': parseFloat(debt.amount.replace(',', ''))
        }

        $http.post('/signup/', data).then(function (resp) {
          console.log(resp)
        });

        $scope.formSubmitted = true;
        $scope.showForm = true;
      }
    }
  }
})