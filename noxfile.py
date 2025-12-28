# pyright: strict

import shutil
import tempfile
from pathlib import Path

import nox

nox.options.default_venv_backend = "uv"
nox.options.sessions = ["build_variable"]


@nox.session
def build_variable(session: nox.Session) -> None:
    build_fonts(session, build_statics=False)


@nox.session
def build_static(session: nox.Session) -> None:
    build_fonts(session, build_statics=True)


def build_fonts(session: nox.Session, build_statics: bool) -> None:
    session.install(".")
    if not Path("build_fonts").exists():
        session.run("meson", "setup", "build_fonts", external=True)
    session.run(
        "meson",
        "configure",
        "--no-pager",
        f"-Dbuildstatics={str(build_statics)}",
        f"-Dbuildvf={str(not build_statics)}",
        "build_fonts",
        external=True,
    )
    session.run("meson", "compile", "-C", "build_fonts", external=True)


@nox.session
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

    option_file = Path("meson_options.txt")
    option_file_text = option_file.read_text()
    option_file_text.replace(
        "useprebuilt', type : 'boolean', value : false",
        "useprebuilt', type : 'boolean', value : true",
    )
    option_file.write_text(option_file_text)

    session.run("git", "add", "meson.build", external=True)
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
