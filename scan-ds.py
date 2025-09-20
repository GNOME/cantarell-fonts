import os
import subprocess
import sys
from pathlib import Path

from fontTools.designspaceLib import DesignSpaceDocument


def ninja_escape(p: str) -> str:
    # Escape spaces and $ for ninja lexical parsing. Backslashes doubled for safety.
    p = p.replace("\\", "\\\\")
    p = p.replace(" ", "\\ ")
    p = p.replace("$", "$$")
    return p


def main():
    if len(sys.argv) != 4:
        print("Usage: gensources.py <designspace> <font_out> <dd_out>", file=sys.stderr)
        sys.exit(2)
    ds_path, font_out, dd_out = sys.argv[1], sys.argv[2], sys.argv[3]

    if not os.path.exists(ds_path):
        print(f"Error: designspace not found: {ds_path}", file=sys.stderr)
        sys.exit(1)

    ds_dir = Path(ds_path).parent
    ds = DesignSpaceDocument.fromfile(ds_path)
    source_ufos = sorted({ds_dir / s.filename for s in ds.sources})

    all_files = (
        # List files and dirs so that when files are added or deleted (folder mtime will be updated), ninja registers it.
        subprocess.check_output(["fd", ".", *(str(path) for path in source_ufos)])
        .decode("utf-8")
        .splitlines()
    )

    # Deduplicate and escape for ninja
    all_files = sorted(all_files)
    escaped = [ninja_escape(p) for p in all_files]

    # Write the dyndep file per ninja manual format
    os.makedirs(os.path.dirname(dd_out) or ".", exist_ok=True)
    with open(dd_out, "w", encoding="utf-8") as f:
        f.write("ninja_dyndep_version = 1\n")
        # If there are no implicit inputs, emit an empty list after the | (it's allowed).
        if escaped:
            f.write(f"build {font_out}: dyndep | {' '.join(escaped)}\n")
        else:
            # No UFO files found — still emit a valid dyndep for the explicit output
            f.write(f"build {font_out}: dyndep\n")


if __name__ == "__main__":
    main()
