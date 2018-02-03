project('Cantarell', version : '0.100')

datadir = join_paths(get_option('prefix'), get_option('datadir'))

fontsdir = get_option('fontsdir')
if fontsdir == ''
  fontsdir = join_paths(datadir, 'fonts', 'cantarell')
endif

fontconfigdir = get_option('fontconfigdir')
if fontconfigdir == ''
  fontconfigdir = join_paths(datadir, 'fontconfig', 'conf.avail')
endif

python3 = import('python3').find_python()
fontmake = find_program('fontmake')
fontmake_wrapper = join_paths(meson.current_source_dir(), 'scripts', 'fm.py')
psautohint = find_program('psautohint')

subdir('src')
subdir('appstream')
