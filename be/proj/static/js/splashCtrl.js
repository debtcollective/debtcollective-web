app.controller('splashCtrl',
 function ($scope, $http, util_svc, $document, $timeout, $window) {
    function scrollToElement(id) {
        var someElement = angular.element(document.getElementById(id));
        $document.scrollToElement(someElement, 150, 500);
    }

  
});
