import subprocess
import sys
from pathlib import Path

from fontTools.designspaceLib import DesignSpaceDocument


def main():
    if len(sys.argv) != 3:
        print("Usage: gensources.py <designspace> <dd_out>", file=sys.stderr)
        sys.exit(2)
    src_dir, dd_out = Path(sys.argv[1]), Path(sys.argv[2])

    if not src_dir.exists():
        print(f"Error: source not found: {src_dir}", file=sys.stderr)
        sys.exit(1)

    ds_files: dict[Path, list[str]] = {}
    for ds_path in src_dir.glob("*.designspace"):
        ds = DesignSpaceDocument.fromfile(ds_path)
        source_ufos: list[Path] = sorted({src_dir / s.filename for s in ds.sources})
        ds_files[ds_path] = [
            ninja_escape(p)
            for p in sorted(
                subprocess.check_output(["fd", ".", *source_ufos])
                .decode("utf-8")
                .splitlines()
            )
        ]

    dd_out.parent.mkdir(exist_ok=True)
    with open(dd_out, "w", encoding="utf-8") as f:
        print("ninja_dyndep_version = 1", file=f)
        for ds_path, files in ds_files.items():
            assert files
            print(
                f"build /tmp/{ds_path.stem}.ttf: dyndep | {ds_path} {' '.join(files)}",
                file=f,
            )

    # TODO: Try stamp files per UFO. The stamp files will need to be listed in build.ninja as phony rules.
    # dd_out.parent.mkdir(exist_ok=True)
    # with open(dd_out, "w", encoding="utf-8") as f:
    #     print("ninja_dyndep_version = 1", file=f)
    #     for ufo_path, files in ufo_files.items():
    #         assert files
    #         print(f"build /tmp/{ufo_path.name}.d: dyndep | {' '.join(files)}", file=f)
    #     for ds_path, source_ufos in ds2ufo.items():
    #         print(
    #             f"build /tmp/{ds_path.with_suffix('.ttf').name}: dyndep | {ds_path} {' '.join(f'/tmp/{u.name}.d' for u in source_ufos)}",
    #             file=f,
    #         )


def ninja_escape(p: str) -> str:
    # Escape spaces and $ for ninja lexical parsing. Backslashes doubled for safety.
    p = p.replace("\\", "\\\\")
    p = p.replace(" ", "\\ ")
    p = p.replace("$", "$$")
    return p


if __name__ == "__main__":
    main()
