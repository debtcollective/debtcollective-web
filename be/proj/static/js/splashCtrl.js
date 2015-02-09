app.controller('splashCtrl',
    function ($scope, $http, util_svc, $document, $timeout, $window) {

    $scope.showSite = false;
    $scope.showStats = false;

    $scope.bannerFadeInTimeout = false;
    $timeout(function () {
        $scope.bannerFadeInTimeout = true;
    }, 500)

    function scrollToElement(id) {
        var someElement = angular.element(document.getElementById(id));
        $document.scrollToElement(someElement, 150, 500);
    }

    function showSite() {
        $scope.showSite = true;
    }

    $scope.agree = function () {
        showSite()
    }

    $scope.disagree = function () {
        showSite()
        $scope.showStats = true;
        $timeout(function () {
            scrollToElement('page')
        }, 500)
    }

    $http.get('/static/js/map_data.json').then(function (resp) {
        var total_amount = resp.data.total_amount;
        odometer.innerHTML = total_amount;
        //counterOptions.counterStart = total_amount - 30000;
    });

});
