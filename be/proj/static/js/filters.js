app.filter('humanize', function(){
    return function humanize(number) {
        if(number < 1000) {
            return Math.round(number);
        }
        var si = ['K', 'M', 'G', 'T', 'P', 'H'];
        var exp = Math.floor(Math.log(number) / Math.log(1000));
        var result = number / Math.pow(1000, exp);
        result = (result % 1 > (1 / Math.pow(1000, exp - 1))) ? result.toFixed(2) : result.toFixed(0);
        return result + si[exp - 1];
    };
});
