# pyright: strict

import shutil
import tempfile
from pathlib import Path

import nox

REQUIRED_PYTHON = "3.11"

nox.options.sessions = ["build_variable"]


@nox.session(python=REQUIRED_PYTHON)
def build_variable(session: nox.Session) -> None:
    build_fonts(session, build_statics=False)


@nox.session(python=REQUIRED_PYTHON)
def build_static(session: nox.Session) -> None:
    build_fonts(session, build_statics=True)


def build_fonts(session: nox.Session, build_statics: bool) -> None:
    session.install("meson", "ninja", "-r", "requirements.txt")
    if not Path("build").exists():
        session.run("meson", "setup", "build")
    session.run(
        "meson",
        "configure",
        "--no-pager",
        f"-Dbuildstatics={str(build_statics)}",
        f"-Dbuildvf={str(not build_statics)}",
        "build",
    )
    session.run("meson", "compile", "-C", "build")


@nox.session
def dist(session: nox.Session) -> None:
    """Create a distribution package on the CI.

    NOTE: Don't run it locally, it creates a commit.
    """

    destdir = tempfile.TemporaryDirectory()
    destdir_path = Path(destdir.name)

    session.install("meson", "ninja", "-r", "requirements.txt")
    session.run("ninja", "-C", "build", "install", env={"DESTDIR": destdir.name})
    session.run("meson", "rewrite", "default-options", "set", "useprebuilt", "true")
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
    session.run("ninja", "-C", "build", "dist")


@nox.session(python=REQUIRED_PYTHON)
def update_dependencies(session: nox.Session) -> None:
    session.install("pip-tools")
    session.run("pip-compile", "--resolver=backtracking", "-U", "requirements.in")
    session.run("pip-compile", "--resolver=backtracking", "-U", "requirements-dev.in")
