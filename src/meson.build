if get_option('buildstatics') == true
    custom_target(
        'cantarell-static-fonts',
        input: 'Cantarell.designspace',
        output: [
            'Cantarell-Thin.otf',
            'Cantarell-Light.otf',
            'Cantarell-Regular.otf',
            'Cantarell-Bold.otf',
            'Cantarell-ExtraBold.otf',
        ],
        command: [python3, make_static_fonts, '@INPUT@', psautohint, '@OUTDIR@'],
        install: true,
        install_dir: fontsdir,
    )
endif

if get_option('buildvf') == true
    custom_target(
        'cantarell-variable-font',
        input: 'Cantarell.designspace',
        output: 'Cantarell-VF.otf',
        command: [
            python3,
            make_variable_font,
            '@INPUT@',
            join_paths(meson.current_source_dir(), 'Cantarell.stylespace'),
            psautohint,
            '@OUTPUT@'
        ],
        install: true,
        install_dir: fontsdir,
    )
endif
