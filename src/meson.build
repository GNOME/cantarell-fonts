cantarell_binaries = [
'Cantarell-Thin.otf',
'Cantarell-Light.otf',
'Cantarell-Regular.otf',
'Cantarell-Bold.otf',
'Cantarell-ExtraBold.otf'
]

custom_target('Cantarell',
              input : 'Cantarell.glyphs',
              output : cantarell_binaries,
              command : [python3, fontmake_wrapper, fontmake, psautohint,
                         '@INPUT@', '@OUTDIR@'],
              install: true,
              install_dir : fontsdir)
