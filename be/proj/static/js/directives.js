app.directive("", function () {

});

app.directive("scroll", function ($window) {
    return function($scope, $element, $attrs) {

        var OFFSET = 100;
        var MAX_RANGES = 27;
        var RANGE_COLORS = {
            13: "#281519",
            14: "#281519",
            15: "#2e2327",
            16: "#2e2327",
            17: "#393035",
            18: "#393035",
            19: "#454b49",
            20: "#454b49",
            21: "#3f4543",
            22: "#3f4543",
            23: "#38413e",
            24: "#38413e",
            25: "#39413F",
            26: "#39413F",
            27: "#39413F"
        }

        for(var i = 1; i < 13; i ++){
            RANGE_COLORS[i] =  "#28151a";
        }


        //$scope.one = true;
        $scope.yLoc = 0;
        $scope.ranges = []
        $scope.locLookup = {}

        function createRange() {
            var i = 1;
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
