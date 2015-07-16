app.controller('splashCtrl',
 function ($scope, $http, util_svc, $document, $timeout, $window) {
    function scrollToElement(id) {
        var someElement = angular.element(document.getElementById(id));
        $document.scrollToElement(someElement, 150, 500);
    }

    // create counter
    var counterOptions = {
      increment: 30000,
      delayTime: 500,
      counterStart: 0,
      counterEnd: 0,
      formatNumber: true,
      numbersImage: '/static/img/jodometer-numbers-24pt.png',
      widthNumber: 30,
      heightNumber: 54,
      spaceNumbers: 0,
      offsetRight: -11,
      maxDigits: 11,
      prefixChar: true
    }
    var total_amount = 182170071;
    var total_users = 0;
    counterOptions.counterEnd = total_amount;
    counterOptions.counterStart = total_amount - 30000;
    $('.counter').jOdometer(counterOptions);
    $('.counter .jodometer_dot').last().hide();
});
