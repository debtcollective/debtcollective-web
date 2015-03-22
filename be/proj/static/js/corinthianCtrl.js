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
    $scope.showCorinthians = false;
    $scope.currentStriker = null;
    $scope.loading = true;
    $scope.corinthian = false;
    $scope.corinthian15 = []
    $scope.strikeTeam = []

    $http.get('/static/js/strikers.json').then(function (resp) {
      $scope.loading = false;
      for (i in resp.data) {
        var striker = resp.data[i]
        striker.first_name = striker.name.split(' ')[0].toLowerCase()
        striker.image = "/static/img/strikers/striker-portraits_" + striker.first_name + ".png"
        striker.bigImage = striker.image
        $scope.corinthian15.push(striker)
      }
      $scope.corinthian15Chunks = $scope.corinthian15.chunk(5)
    });


    $http.get('/static/js/new_strikers.json').then(function (resp) {
      $scope.loading = false;
      for (i in resp.data) {
        var striker = resp.data[i]
        striker.name = striker["Name"]
        striker.bio = striker["Striker Bio"]
        var photo = striker["Photo URL"]
        if (!photo || photo.indexOf('imgur.com') < 0) {
          striker.hasImage = false
        }
        else {
          striker.hasImage = true
          striker.image = photo.replace('.jpg', 'b.jpg')
          striker.bigImage = photo.replace('.jpg', 'm.jpg')
        }
        $scope.strikeTeam.push(striker)
      }
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
