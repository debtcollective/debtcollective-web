app.directive("scroll", function ($window) {
    return function($scope, $element, $attrs) {

        var OFFSET = 100;
        var MAX_RANGES = 21;

        //$scope.one = true;
        $scope.yLoc = 0;
        $scope.ranges = []

        function createRange() {
            var i = 0;
            var cur = 0;
            while (i < MAX_RANGES) {
                $scope.ranges.push({
                    'yScroll': cur,
                    'num': i
                });
                cur += OFFSET;
                i += 1;
            }
        }

        createRange()

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
