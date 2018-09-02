project('cantarell-fonts', version : '0.110')

datadir = join_paths(get_option('prefix'), get_option('datadir'))
appdatadir = join_paths(datadir, 'metainfo')

fontsdir = get_option('fontsdir')
if fontsdir == ''
  fontsdir = join_paths(datadir, 'fonts', 'cantarell')
endif

useprebuilt = get_option('useprebuilt')
if useprebuilt == false
  python3 = import('python3').find_python()
  fontmake = find_program('fontmake')
  fontmake_wrapper = join_paths(meson.current_source_dir(), 'scripts', 'fm.py')
  psautohint = find_program('psautohint')
  subdir('src')
else
  subdir('prebuilt')
endif

buildappstream = get_option('buildappstream')
if buildappstream == true
 subdir('appstream')
endif