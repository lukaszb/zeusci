module.exports = function (config) {
  config.set({
    basePath: '../../zeusci/',

    preprocessors: {
        '**/*.coffee': ['coffee']
    },

    files: [
      'static/js/jquery-1.10.1.min.js',
      'zeus/static/zeus/js/moment.2.0.0.min.js',
      'zeus/static/zeus/js/angular.1.0.7.min.js',
      'zeus/static/zeus/js/angular-resource.1.0.7.min.js',
      'zeus/static/zeus/js/zeus.coffee',
      'zeus/static/zeus/js/controllers.coffee',
      'zeus/static/zeus/js/services.coffee',

      'zeus/static/zeus/js/tests/unit/controllerSpec.coffee',
      //'app/lib/angular/angular.js',
      //'app/lib/angular/angular-*.js',
      //'test/lib/angular/angular-mocks.js',
      //'app/js/**/*.js',
      //'test/unit/**/*.js'
    ],

    frameworks: ['jasmine'],

    autoWatch: true,
    singleRun: false,

    browsers: ['PhantomJS'],

    reporters: ['progress', 'growl'],

    junitReporter: {
      outputFile: 'test_out/unit.xml',
      suite: 'unit'
    },

    coffeePreprocessor: {
        // options passed to the coffee compiler
        options: {
            bare: true,
            sourceMap: false
        },
        // transforming the filenames
        transformPath: function(path) {
            return path.replace(/\.js$/, '.coffee');
        }
    }
  });
};

