module.exports = function(grunt) {

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    concat: {
      options: {
        separator: ';'
      },
      dist: {
        src: ['static/vendor/angular.min.js',
        'static/vendor/angular-cookies.min.js',
        'static/vendor/angular-animate.min.js',
        'static/vendor/angular-scroll.min.js',
        'static/vendor/miso.ds.deps.min.0.2.2.js',
        'static/vendor/miso.ds.min.0.4.1.js',
        'static/vendor/d3.min.js',
        'static/vendor/checkout.js',
        'static/vendor/ui-bootstrap-custom-0.10.0.min.js',
        'static/vendor/ui-bootstrap-custom-tpls-0.10.0.min.js',
        'static/vendor/jquery.min.js',
        'static/vendor/jquery.jodometer.js',
        'static/vendor/ammap/ammap.js',
        'static/vendor/ammap/maps/js/worldHigh.js',
        'static/js/debtis.js',
        'static/js/**/*.js',
        'static/directives/**/*.js'],
        dest: 'static/dist/<%= pkg.name %>.js'
      }
    },
    watch: {
      files: ['static/js/**/*.js'],
      tasks: ['concat']
    }
  });

  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-concat');

  grunt.registerTask('default', ['concat']);

};