
app.controller('splashCtrl', function ($scope, $http, util_svc) {

    $scope.email = null;
    $scope.username = null;
    $scope.location = null;

    $http.get('/points/').then(function (resp) {
        $scope.cities = resp.data
    });

    $scope.formValid = function () {
        return $scope.location != null && $scope.email != null;
    }

    $scope.onSubmitClick = function () {
        $scope.username = util_svc.generateUUID();

        // temporarily, email is the password
        // so that we can protect anonymity of our users.
        // campaign monitor handles mailing lists
        data = {
            'username': $scope.username,
            'password': $scope.email,
            'location': $scope.location.id
        }

        $http.post('/signup/', data).then(function (resp) {

        });
    }
});
