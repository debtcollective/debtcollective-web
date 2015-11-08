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
        'static/vendor/angular-route.min.js',
        'static/vendor/angular-touch.min.js',
        'static/vendor/angular-scroll.min.js',
        'static/vendor/d3.min.js',
        'static/vendor/jquery.min.js',
        'static/vendor/ui-bootstrap-custom-0.10.0.min.js',
        'static/vendor/ui-bootstrap-custom-tpls-0.10.0.min.js',
        'static/vendor/jquery.jqgoogleforms.min.js',
        'static/js/debtis.js',
        'static/js/**/*.js',
        'static/directives/*.js',
        'static/directives/**/*.js'],
        dest: 'static/dist/<%= pkg.name %>.js'
      }
    },
    hashres: {
      assets: {
        src: [
          'static/dist/dc.js', 'static/css/base.css'
        ],
        dest: [
          'templates/proj/base_template.html',
        ],
      },
      options: {
        fileNameFormat: '${name}.${ext}?v${hash}',
        renameFiles: false
      }
    },
    sass: {
      dist: {
        files: {
          'static/css/base.css' : 'static/css/base.scss'
        }
      }
    },
    watch: {
      scripts: {
        files: [
          'static/js/**/*.js',
          'static/directives/**/*.js'],
        tasks: ['concat']
      },
      styles: {
        files: [
          'static/css/**/*.scss'
        ],
        tasks: [
          'sass', 'imageEmbed'
        ]
      }
    },
    imageEmbed: {
      dist: {
        src: ['static/css/base.css'],
        dest: 'static/css/base.css',
        options: {
          deleteAfterEncoding : false,
          target: ['**/*.png'],
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-hashres');
  grunt.loadNpmTasks("grunt-image-embed");

  grunt.registerTask('default', ['concat', 'hashres', 'imageEmbed']);

};
