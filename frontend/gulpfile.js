// -*- coding: utf-8 -*-
var fs = require('fs');
var gulp = require('gulp');
var child_process = require('child_process');

var lib_dir = 'lib/'
var bower_dir = 'bower_components/';

var lib = function (path){return lib_dir + path};
var bower = function (path){return bower_dir + path};
var bower_to_lib = function(options){
    for(var src in options){
        var dst = options[src];
        console.log(src + ' -> ' + dst);
        gulp.src(bower(src))
            .pipe(gulp.dest(lib(dst)));
    }
};

//--- do'nt edit me --------------
gulp.task('template', function (){
    bower_to_lib({'': ''});
});
//--------------------------------

gulp.task('watch', function (){
    var path = 'static/*/**';
    gulp.watch(path, function (ev){
        gulp.run('baast');
    });
});

gulp.task('director', function (){
    bower_to_lib({'director/build/*': 'director/build/'});
});

gulp.task('pnotify', function (){
    bower_to_lib({'pnotify/pnotify.*': 'pnotify/'});
});

gulp.task('threejs', function (){
    bower_to_lib({'threejs/build/*': 'threejs/build'});
});

gulp.task('d3', function (){
    bower_to_lib({'d3/d3.**': 'd3'});
});

gulp.task('nvd3', function (){
    bower_to_lib({'nvd3/nv.d3.**': 'nvd3'});
});

gulp.task('baast', function (){
    bower_to_lib({
        'static/css/app.css': 'baast/css'
    });
});


gulp.task('spin.js', function (){
    bower_to_lib({'spin.js/spin.js': 'spin.js/'});
});

gulp.task('hogan', function (){
    bower_to_lib({
        '': ''
    });
});


gulp.task('vue', function (){
    bower_to_lib({'vue/dist/**': 'vue/dist'});
});

gulp.task('angular', function (){
    bower_to_lib({
        'angular/angular.min.js': 'angular',
        'angular/angular.min.js.map': 'angular'
    });
});

gulp.task('angular-animate', function (){
    bower_to_lib({
        'angular-animate/angular*.js': 'angular-animate',
        'angular-animate/angular*.js.map': 'angular-animate'
    });
});

gulp.task('angular-resource', function (){
    bower_to_lib({
        'angular-resource/angular*.js': 'angular-resource',
        'angular-resource/angular*.js.map': 'angular-resource'
    });
});

gulp.task('angular-route', function (){
    bower_to_lib({
        'angular-route/angular*.js': 'angular-route',
        'angular-route/angular*.js.map': 'angular-route'
    });
});

gulp.task('font-awesome', function (){
    bower_to_lib({
        'font-awesome/css/**': 'font-awesome/css',
        'font-awesome/fonts/**': 'font-awesome/fonts'
    });
});


gulp.task('jquery-ui', function (){
    bower_to_lib({
        'jquery-ui/ui/**': 'jquery-ui/ui',
        'jquery-ui/themes/**': 'jquery-ui/themes',
        'jquery-ui/jquery-ui.js': 'jquery-ui/',
        'jquery-ui/jquery-ui.min.js': 'jquery-ui/'
    });
});

gulp.task('jquery', function (){
    bower_to_lib({'jquery/dist/**': 'jquery'});
});

gulp.task('bootstrap', function (){
    bower_to_lib({
        'bootstrap/dist/css/**': 'bootstrap/css',
        'bootstrap/dist/js/**': 'bootstrap/js',
        'bootstrap/dist/fonts/**': 'bootstrap/fonts'
    });
});

gulp.task('bootstrap-dialog', function (){
    bower_to_lib({
        'bootstrap-dialog/dist/js/**': 'bootstrap-dialog/dist/js',
        'bootstrap-dialog/dist/css/**': 'bootstrap-dialog/dist/css'
    });
});

gulp.task('bootstrap3-dialog', function (){
    bower_to_lib({
        'bootstrap3-dialog/dist/**': 'bootstrap3-dialog/dist'
    });
});

gulp.task('underscore', function (){
    bower_to_lib({'underscore/underscore.js': 'underscore'});
});


gulp.task('backbone', function (){
    bower_to_lib({'backbone/backbone.js': 'backbone'});
});


gulp.task('backbone.marionette', function (){
    bower_to_lib({'backbone.marionette/lib/**': 'backbone.marionette/lib'});
});

gulp.task('backbone.babysitter', function (){
    bower_to_lib({'backbone.babysitter/lib/**': 'backbone.babysitter/lib'});
});

gulp.task('backbone.wreqr', function (){
    bower_to_lib({'backbone.wreqr/lib/**': 'backbone.wreqr/lib'});
});

gulp.task('backbone.localStorage', function (){
    bower_to_lib({'backbone.localStorage/backbone.localStorage.js': 'backbone.localStorage'});
});

gulp.task('all', function(){
    var names = fs.readdirSync('bower_components');
    names.forEach(function (name, ii){
        gulp.run(name);
    });

    // fs.readFile('./bower.json', 'utf8', function (err, text){
    //     var data = JSON.parse(text);
    //     Object.keys(data.dependencies).forEach(function (name){
    //         gulp.run(name);
    //     });
    // });
});

gulp.task('default', function (){
    gulp.run('all');
});
