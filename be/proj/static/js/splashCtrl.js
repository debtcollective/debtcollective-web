app.controller('splashCtrl',
    function ($scope, $http, util_svc, $document, $timeout, $window) {

    $scope.email = null;
    $scope.username = null;
    $scope.location = null;
    $scope.newsletter = true;
    $scope.debtType = null;
    $scope.amount = null;
    $scope.showForm = false;
    $scope.formSubmitted = false;
    $scope.focused = false;

    $scope.startShowingFormLoc = 4300;

    $http.get('/points').then(function (resp) {
        $scope.cities = resp.data
    });

    $scope.bannerFadeInTimeout = false;
    $timeout(function () {
        $scope.bannerFadeInTimeout = true;
    }, 500)

    $scope.scrollClick = function () {
        var someElement = angular.element(document.getElementById('mapdiv'));
        $document.scrollToElement(someElement, 0, 18000);
    }

    $scope.formValid = function () {
        return $scope.location != null && $scope.email != null
            && $scope.amount != null;
    }

    $scope.formVisible = function () {
        visible = ($scope.showForm || $scope.yLoc > $scope.startShowingFormLoc)
            && !$scope.forceClose && !$scope.formSubmitted;
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
});
