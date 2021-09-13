project('cantarell-fonts', version : '0.303')

datadir = join_paths(get_option('prefix'), get_option('datadir'))
appdatadir = join_paths(datadir, 'metainfo')

fontsdir = get_option('fontsdir')
if fontsdir == ''
    fontsdir = join_paths(datadir, 'fonts', 'cantarell')
endif

useprebuilt = get_option('useprebuilt')
if useprebuilt == false
    python3 = import('python').find_installation('python3')
    if get_option('buildstatics') == true
        make_static_fonts = join_paths(meson.current_source_dir(), 'scripts', 'make-static-fonts.py')
    endif
    if get_option('buildvf') == true
        make_variable_font = join_paths(meson.current_source_dir(), 'scripts', 'make-variable-font.py')
    endif
    psautohint = find_program('psautohint')
    subdir('src')
else
    subdir('prebuilt')
endif

buildappstream = get_option('buildappstream')
if buildappstream == true
    subdir('appstream')
endif
