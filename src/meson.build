custom_target('cantarell-fonts',
              input : 'Cantarell.glyphs',
              output : [
                'Cantarell-Thin.otf',
                'Cantarell-Light.otf',
                'Cantarell-Regular.otf',
                'Cantarell-Bold.otf',
                'Cantarell-ExtraBold.otf'
              ],
              command : [python3, fontmake_wrapper, fontmake, psautohint,
                         '@INPUT@', '@OUTDIR@'],
              install: true,
              install_dir : fontsdir)
