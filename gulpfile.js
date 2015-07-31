"use strict";

var gulp = require('gulp');
var sass = require('gulp-sass');
var sourcemaps = require('gulp-sourcemaps');
var uglify = require('gulp-uglifyjs');

var config = {
    customDir: './static/src',
    bowerDir: './vendor',
    publicDir: './static'
};

gulp.task('fonts', function () {
    return gulp.src(config.bowerDir + '/bootstrap-sass/assets/fonts/**/*')
        .pipe(gulp.dest(config.publicDir + '/fonts'));
});

gulp.task('js', function () {
    return gulp.src([
        config.bowerDir + '/jquery/dist/jquery.min.js',
        config.bowerDir + '/bootstrap-sass/assets/javascripts/bootstrap.js',
    ])
        .pipe(uglify('app.js', {
            compress: true,
            outSourceMap: true
        }))
        .pipe(gulp.dest(config.publicDir + '/js'));
});

gulp.task('sass', function () {
    return gulp.src(config.customDir + '/sass/main.scss')
        .pipe(sourcemaps.init())
        //.pipe(sass({
        //    style: 'compressed',
        //    includePaths: [config.bowerDir + '/bootstrap-sass/assets/stylesheets']
        //}))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(config.publicDir + '/css'));
});

//gulp.task('default', ['sass', 'js', 'fonts']);
gulp.task('default', ['sass']);
