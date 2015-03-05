Array.prototype.chunk = function(chunkSize) {
    var array=this;
    return [].concat.apply([],
        array.map(function(elem,i) {
            return i%chunkSize ? [] : [array.slice(i,i+chunkSize)];
        })
    );
}

app.controller('corinthianCtrl',
  function ($scope, $window, $http, $document) {
    $scope.debtors = 13415;
    $scope.debt = 354135;
    $scope.money = 24194;

    $scope.corinthianLetterVisible = true;
    $scope.currentStriker = null;
    $scope.loading = true;
    $scope.corinthian = false;
    $scope.strikers = []

    $http.get('/static/js/strikers.json').then(function (resp) {
      $scope.loading = false;
      for (i in resp.data) {
        var striker = resp.data[i]
        striker.first_name = striker.name.split(' ')[0].toLowerCase()
        $scope.strikers.push(striker)
      }
      $scope.strikerChunks = $scope.strikers.chunk(5)
    });

    $scope.agreeButton = function () {
      $scope.normalsignup = true
    }

    $scope.showStriker = function (striker, $event) {
      history.pushState(null, striker.name, "#" + striker.first_name)
      $scope.currentStriker = striker
      if ($event) $event.stopPropagation()
    }

    $scope.closeStriker = function ($event) {
      $scope.currentStriker = null
      if ($event) $event.stopPropagation()
    }

    $scope.showCorinthianLetter = function () {
      $scope.corinthianLetterVisible = true
      setTimeout(function () {
        var elem = angular.element(document.getElementById('corinthianLetter'))
        $document.scrollToElementAnimated(elem)
      }, 100)
    }

    $scope.showSolidarityLetter = function () {
      $scope.corinthianLetterVisible = false
      setTimeout(function () {
        var elem = angular.element(document.getElementById('solidarityLetter'))
        $document.scrollToElementAnimated(elem)
      }, 100)
    }

    $window.addEventListener('popstate', function () {
      if ($scope.currentStriker) {
        $scope.closeStriker()
        $scope.$digest()
      }
    })

    $scope.formVisible = function () { return true; }
});
