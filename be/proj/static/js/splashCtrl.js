app.controller('splashCtrl',
 function ($scope, $http, util_svc, $document, $timeout, $window) {
    var retries = 5;
    fetchTallies()
    function fetchTallies() {
      if (retries == 0) { return; }
      else retries -= 1;
      var ds = new Miso.Dataset({
          importer : Miso.Dataset.Importers.GoogleSpreadsheet,
          parser : Miso.Dataset.Parsers.GoogleSpreadsheet,
          key : "1WuTX0sbw9AatpVWwSOV9Obc9k4iiIO6Xyz8mzy3a-Q8",
          worksheet : "1"
        });
        $scope.salliemae = 500;
        $scope.corinthian = 830;
        ds.fetch({
          success: function () {
            $scope.salliemae += this.sum('salliemae');
            $scope.corinthian += this.sum('corinthian');
          },
          error : function() {
            console.log("Are you sure you are connected to the internet?");
            setTimeout(fetchTallies, 500)
          }
        })
    }

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
      formatNumber: true,
      numbersImage: 'http://rollingjubilee.org/assets/img/jodometer-numbers-24pt.png',
      widthNumber: 30,
      heightNumber: 54,
      spaceNumbers: 0,
      offsetRight: -11,
      maxDigits: 11,
      prefixChar: true
    }

    $http.get('/static/js/map_data.json').then(function (resp) {
        var total_amount = resp.data.total_amount;
        var total_users = 0;
        counterOptions.counterEnd = total_amount;
        counterOptions.counterStart = total_amount - 30000;
        $('.counter').jOdometer(counterOptions);
        $('.counter .jodometer_dot').last().hide();
    });

});
