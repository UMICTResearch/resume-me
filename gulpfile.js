var gulp = require('gulp'),
    concat = require('gulp-concat'),
    sass = require('gulp-sass'),
    sourcemaps = require('gulp-sourcemaps'),
    uglify = require('gulp-uglifyjs'),
    config = {
        sass: {
            watch: [
                './static/src/sass/**/*.scss'
            ],
            source: [
                './static/src/sass/main.scss'
            ],
            include: [
                './vendor/bootstrap-sass/assets/stylesheets'
            ],
            dest: './static/css',
            target: 'main.css'
        },
        js: {
            watch: [
                './static/src/js/**/*.js'
            ],
            source: [
                './vendor/jquery/dist/jquery.js',
                './vendor/bootstrap-sass/assets/javascripts/bootstrap.js',
                './static/src/js/main.js'
            ],
            dest: './static/js',
            target: 'global.js'
        },
        fonts: {
            source: [
                './vendor/bootstrap-sass/assets/fonts/**/*',
            ],
            dest: './static/fonts'
        }
    };

gulp.task('fonts', function () {
    return gulp.src(config.fonts.source)
        .pipe(gulp.dest(config.fonts.dest));
});

gulp.task('js', function () {
    gulp.src(config.js.source)
        .pipe(concat(config.js.target))
        .pipe(uglify({
            compress: true,
            outSourceMap: true
        }))
        .pipe(gulp.dest(config.js.dest));
});

gulp.task('js:watch', ['js'], function () {
    gulp.watch(config.js.watch, ['js']);
});

gulp.task('sass', function () {
    return gulp.src(config.sass.source)
        .pipe(sourcemaps.init())
        .pipe(sass({
            style: 'compressed',
            includePaths: [config.sass.include]
        }))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(config.sass.dest));
});

gulp.task('sass:watch', ['sass'], function () {
    gulp.watch(config.sass.watch, ['sass']);
});

gulp.task('watch', ['sass:watch']);

gulp.task('default', ['sass', 'fonts']);
