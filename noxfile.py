# pyright: strict

import shutil
import tempfile
from pathlib import Path

import nox
import nox_uv

nox.options.default_venv_backend = "uv"
nox.options.sessions = ["build_variable"]


@nox_uv.session
def build_variable(session: nox.Session) -> None:
    build_fonts(session, build_vf=True, build_statics=False)


@nox_uv.session
def build_static(session: nox.Session) -> None:
    build_fonts(session, build_vf=False, build_statics=True)


@nox_uv.session
def build_both(session: nox.Session) -> None:
    build_fonts(session, build_vf=True, build_statics=True)


def build_fonts(session: nox.Session, build_vf: bool, build_statics: bool) -> None:
    if not Path("build_fonts").exists():
        session.run("meson", "setup", "build_fonts", external=True)
    session.run(
        "meson",
        "configure",
        "--no-pager",
        "-Duseprebuilt=false",
        f"-Dbuildstatics={str(build_statics)}",
        f"-Dbuildvf={str(build_vf)}",
        "build_fonts",
        external=True,
    )
    session.run("meson", "compile", "-C", "build_fonts", external=True)


@nox_uv.session
def dist(session: nox.Session) -> None:
    """Create a distribution package on the CI.

    NOTE: Don't run it locally, it creates a commit.
    """

    destdir = tempfile.TemporaryDirectory()
    destdir_path = Path(destdir.name)

    session.run(
        "meson",
        "install",
        "-C",
        "build_fonts",
        env={"DESTDIR": destdir.name},
        external=True,
    )

    # Flip the default mode in the tarball to use the prebuilt fonts.
    option_file = Path("meson_options.txt")
    option_file_text = option_file.read_text().replace(
        "useprebuilt', type : 'boolean', value : false",
        "useprebuilt', type : 'boolean', value : true",
    )
    option_file.write_text(option_file_text)
    session.run("git", "add", "meson_options.txt", external=True)

    for font in (destdir_path / "usr/local/share/fonts/cantarell").glob("*.otf"):
        shutil.copy(font, "prebuilt")
    session.run("git", "add", "prebuilt/*.otf", external=True)

    session.run(
        "git", "config", "--global", "user.email", "you@example.com", external=True
    )
    session.run("git", "config", "--global", "user.name", "Your Name", external=True)
    session.run(
        "git", "commit", "-m", "Meson packages commits, not file trees.", external=True
    )

    session.run("meson", "dist", "-C", "build_fonts", external=True)
