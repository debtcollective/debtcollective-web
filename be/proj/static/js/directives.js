app.directive("scroll", function ($window) {
    return function($scope, $element, $attrs) {

        $scope.amountToScroll = 2700;

        var OFFSET = 120;
        var MAX_RANGES = 10;
        var RANGE_COLORS = {
            6: "#281519",
            7: "#281519",
        }

        for(var i = 1; i < 10; i ++){
            RANGE_COLORS[i] =  "#110d21";
        }
        for(var i = 18; i < MAX_RANGES; i ++){
            RANGE_COLORS[i] = "#39413f"
        }

        //$scope.one = true;

        $scope.yLoc = 0;
        $scope.ranges = []
        $scope.locLookup = {}

        function createRange() {
            var i = 1;
            var cur = 0;
            var next = 0;
            while (i < MAX_RANGES) {
                $scope.locLookup[cur] = i;
                next = cur += OFFSET;
                $scope.ranges.push({
                    'yScroll': cur,
                    'yScrollEnd': next*2,
                    'num': i
                });
                cur = next;
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

        function map_range(value, low1, high1, low2, high2) {
            /* for the scrollthing */
            return low2 + (high2 - low2) * (value - low1) / (high1 - low1);
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
            var windowHeight = $window.innerHeight;
            var scroll = this.pageYOffset;
            var height = map_range(scroll, 0, $scope.amountToScroll, 0, windowHeight);
            var opacity = 1;
            if(scroll > $scope.amountToScroll) {
                opacity = 0;
            }
            $scope.scrollThingStyle = {"height" : height, "opacity": opacity};
            $scope.$apply();
        });
    };
});

app.directive('scrollOnClick', function() {
  return {
    restrict: 'A',
    link: function(scope, $elm) {
      $elm.on('click', function() {
      });
    }
  }
});
