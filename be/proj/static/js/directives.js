app.directive("scroll", function ($window) {
    return function($scope, $element, $attrs) {

        var OFFSET = 100;
        var MAX_RANGES = 21;
        var RANGE_COLORS = {
            15: "#281519",
            16: "#2e2327",
            17: "#393035",
            18: "#454b49",
            19: "#3f4543",
            20: "#38413e",
            21: "#39413F"
        }


        //$scope.one = true;
        $scope.yLoc = 0;
        $scope.ranges = []
        $scope.locLookup = {}

        function createRange() {
            var i = 0;
            var cur = 0;
            while (i < MAX_RANGES) {
                $scope.locLookup[cur] = i;
                $scope.ranges.push({
                    'yScroll': cur,
                    'num': i
                });
                cur += OFFSET;
                i += 1;
            }
        }

        createRange();

        $scope.$watch('yLoc', function(newVal, oldVal) {
            i = $scope.locLookup[newVal];
            $scope.backgroundStyle = {"background-color" : RANGE_COLORS[i]};
        });

        $scope.advance = function () {
            $scope.yLoc = $scope.yLoc + OFFSET;
        }

        function scrolling(i) {
            if (this.pageYOffset >= i * Math.floor(this.pageYOffset/OFFSET)*OFFSET) {
                $scope.yLoc = i * Math.ceil(this.pageYOffset/OFFSET)*OFFSET;
            }
            else {
                scrolling(i + 1);
            }
        }

        angular.element($window).bind("scroll", function() {
            scrolling(1);
            $scope.$apply();
        });
    };
});
