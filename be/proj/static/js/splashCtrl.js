app.controller('splashCtrl',
    function ($scope, $http, util_svc, $document, $timeout, $window) {

    $scope.newsletter = true;

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

});
