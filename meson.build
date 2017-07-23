project('Cantarell', version : '0.30')

datadir = join_paths(get_option('prefix'), get_option('datadir'))
fontsdir = join_paths(datadir, 'fonts', 'cantarell')
fontconfigdir = join_paths(datadir, 'fontconfig', 'conf.avail')

python3 = import('python3').find_python()
fontmake = find_program('fontmake')
fontmake_wrapper = join_paths(meson.current_source_dir(), 'scripts', 'fontmakewrapper.py')
psautohint = find_program('psautohint')

legacy_fonts = ['CantarellLegacy-Regular.@0@',
                'CantarellLegacy-Bold.@0@']

foreach font : legacy_fonts
  custom_target(font.format('otf'),
    input : join_paths('src', font.format('ufo')),
    output : font.format('otf'),
    command : [python3, fontmake_wrapper, fontmake, psautohint, '@INPUT@'],
    install : true,
    install_dir : '/tmp')
endforeach
