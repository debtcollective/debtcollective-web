app.controller('carouselCtrl', function ($scope, $http, $interval) {
  var items = $('.carousel-item')
  var navItems = $('.carousel-nav-item')

  var autoAdvance = true
  var i = 0

  function scrollItems () {
    if (!autoAdvance) return
    nextItem(i)
  }
  $interval(scrollItems, 5000)

  function nextItem () {
    if (i >= (items.length - 1)) i = 0
    else i += 1
    activateItem(i)
  }

  function previousItem () {
    if (i === 0) i = items.length - 1
    else i -= 1
    activateItem(i)
  }

  function activateItem (i) {
    items.each(function (index, item) {
      $(item).removeClass('active')
    })

    var item = items[i]
    $(item).addClass('active')

    navItems.each(function (index, item) {
      $(item).removeClass('active')
    })

    var navItem = navItems[i]
    $(navItem).addClass('active')
  }

  $scope.nextItemButton = function () {
    nextItem()
    autoAdvance = false
  }

  $scope.prevItemButton = function () {
    previousItem()
    autoAdvance = false
  }

  $scope.chooseItemButton = function (i) {
    activateItem(i)
    autoAdvance = false
  }

})
