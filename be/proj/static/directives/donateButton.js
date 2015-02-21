app.directive('donateButton', function ($window) {
  return {
    restrict: 'E',
    scope: {
      'amount': '@',
      'flexbile': '='
    },
    transclude: true,
    replace: true,
    templateUrl: '/static/directives/donatebutton.html',
    controller: function ($scope, $element, $attrs) {
      var handler = StripeCheckout.configure({
        key: 'pk_test_SLHYKUBbqjnPFTXYcNrYaNAc'
      });

      $scope.flexible = !!$attrs.flexible
      $scope.form = {
        flexibleAmount: 10
      }

      var name = 'Donate'
      var panel = 'Donate'

      $element.find('button').on('click', function(e) {
        if ($scope.flexible) $scope.amount = $scope.form.flexibleAmount
        var description = "$" + $scope.amount + " to the strike fund!"

        handler.open({
          name: name,
          description: description,
          amount: $scope.amount * 100,
          panelLabel: panel
        });
        e.preventDefault();
      });

      // Close Checkout on page navigation
      $window.addEventListener('popstate', function() {
        handler.close();
      });
    }
  }
})