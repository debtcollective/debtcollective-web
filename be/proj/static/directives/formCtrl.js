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
        sendToBackend(function () {
          sendToGdocs()
        })
      }

      function sendToGdocs(cb) {
        var googleForm = $(window).jqGoogleForms({"formKey": "1Vk1WIqyyj4-tHetXZIqCvuoLDmPoDL6QTPQTZ4disUY"});
        var salliemae = 0
        if ($scope.salliemae == 'option1') {
          salliemae = 1
        }

        var corinthian = 0
        if ($scope.corinthianStudent == 'option1') {
          corinthian = 1
        }

        var data = {
          'entry.71652265': salliemae,
          'entry.256870148': corinthian
        }
        googleForm.sendFormData(data)
      }

      function sendToBackend(cb) {
        $scope.username = util_svc.generateUUID();
        var debt = $scope.debts[0]
        var backend_data = {
          'username': $scope.username,
          'password': $scope.email,
          'point': $scope.location.id,
          'kind': debt.debtType.id,
          'amount': parseFloat(debt.amount.replace(',', ''))
        }
        $http.post('/signup/', backend_data).then(function (resp) {
          console.log(resp)
          cb()
        });
      }

    }
  }
})