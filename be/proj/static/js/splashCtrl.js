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

    // create counter
    var counterOptions = {
      increment: 30000,
      delayTime: 500,
      counterStart: 0,
      counterEnd: 0,
      numbersImage: 'http://rollingjubilee.org/assets/img/jodometer-numbers-24pt.png',
      widthNumber: 32,
      heightNumber: 54,
      spaceNumbers: 0,
      offsetRight: -14,
      maxDigits: 14,
      prefixChar: true
    }

    $http.get('/static/js/map_data.json').then(function (resp) {
        var total_amount = resp.data.total_amount;
        counterOptions.counterEnd = total_amount;
        counterOptions.counterStart = total_amount - 30000;
        $('.counter').jOdometer(counterOptions);
    });

});
