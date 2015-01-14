app.directive('signupform', function () {
  return {
    restrict: 'E',
    templateUrl: '/static/directives/form.html',
    replace: true,
    controller: function ($scope, $http, util_svc, $document, $timeout, $window) {

      $scope.email = null;
      $scope.username = null;
      $scope.debtType = null;
      $scope.amount = null;
      $scope.showForm = false;
      $scope.formSubmitted = false;
      $scope.location = null;
      $scope.focused = false;

      $scope.formValid = function () {
        return $scope.location != null && $scope.email != null
            && $scope.amount != null;
      }

      $scope.formVisible = function () {
        visible = $scope.showForm && !$scope.forceClose && !$scope.formSubmitted;
        if (visible) {
        showForm();
        }
        return visible
      }

      function showForm() {
        $scope.showForm = true;
        $scope.forceClose = false;
        el = document.getElementById("email");
        el.placeholder =  'enter your email...';
      }

      $scope.emailFocus = function () {
        showForm();
        $scope.focused = true;
      }

      $scope.onSubmitClick = function () {
        $scope.username = util_svc.generateUUID();

        // temporarily, email is the password
        // so that we can protect anonymity of our users.
        // campaign monitor handles mailing lists

        amount = parseFloat($scope.amount.replace(',', ''));
        data = {
            'username': $scope.username,
            'password': $scope.email,
            'point': $scope.location.id,
            //'kind': $scope.debtType.name,
            'amount': amount
        }

        $http.post('/signup/', data).then(function (resp) {
            $scope.formSubmitted = true;
            $scope.showForm = true;
        });
      }
    }
  }
})