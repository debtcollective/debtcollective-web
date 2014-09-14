app.directive("scroll", function ($window) {
    return function($scope, $element, $attrs) {

        var OFFSET = 100;
        //$scope.one = true;
        $scope.yLoc = 0;

        $scope.advance = function () {
            $scope.yLoc = $scope.yLoc + OFFSET;
        }

        function advancingFunction(i) {
            if (this.pageYOffset >= i * Math.floor(this.pageYOffset/100)*100) {
                $scope.yLoc = i * Math.ceil(this.pageYOffset/100)*100;
            }
            else {
                advancingFunction(i + 1);
            }
        }

        angular.element($window).bind("scroll", function() {
            advancingFunction(1);
            $scope.$apply();
        });
    };
});
