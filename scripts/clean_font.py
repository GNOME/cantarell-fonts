import io
from pathlib import Path

import uharfbuzz as hb


def clean_font(font_path: Path) -> None:
    """Remove unreachable glyphs from a font and clean up the GDEF table."""

    blob = hb.Blob.from_file_path(font_path)
    face = hb.Face(blob)

    # We want to keep everything except all glyph IDs, so that the subsetter will
    # keep all glyphs reachable through Unicode codepoints and OpenType features.
    subset_input = hb.SubsetInput()
    subset_input.keep_everything()
    subset_input.sets(hb.SubsetInputSets.GLYPH_INDEX).clear()

    instance_face = hb.subset(face, subset_input)
    instance_data = io.BytesIO(instance_face.blob.data)

    font_path.write_bytes(instance_data.getvalue())
