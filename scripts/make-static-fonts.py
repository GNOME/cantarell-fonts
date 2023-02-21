#!/bin/env python3

import argparse
import multiprocessing
import subprocess
from pathlib import Path

import cffsubr
import fontTools.designspaceLib
import fontTools.designspaceLib.split
import fontTools.ttLib
import instantiator
import ufo2ft

try:
    import pathops

    have_pathops = True
except ImportError:
    have_pathops = False


def generate_and_write_autohinted_instance(
    instantiator: instantiator.Instantiator,
    instance_descriptor: fontTools.designspaceLib.InstanceDescriptor,
    output_dir: Path,
    psautohint: str,
):
    # 3. Generate instance UFO.
    instance = instantiator.generate_instance(instance_descriptor)
    file_stem = f"{instance.info.familyName}-{instance.info.styleName}".replace(" ", "")

    # 3.5. Optionally write instance UFO to disk, for debugging.
    # instance.save(output_dir / f"{file_stem}.ufo", overwrite=True)

    # 4. Compile and write instance OTF to disk. Do not optimize, because we have to
    # do it again after autohinting.
    instance_font = ufo2ft.compileOTF(
        instance,
        removeOverlaps=True,
        overlapsBackend="pathops" if have_pathops else "booleanOperations",
        inplace=True,
        useProductionNames=True,
        optimizeCFF=ufo2ft.CFFOptimization.NONE,
    )
    output_path = output_dir / f"{file_stem}.otf"
    instance_font.save(output_path)

    # 5. Run psautohint on it.
    subprocess.run([psautohint, str(output_path)])

    # 6. Subroutinize (compress) it
    instance_font = fontTools.ttLib.TTFont(output_path)
    cffsubr.subroutinize(instance_font).save(output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "designspace_path", type=Path, help="The path to the Designspace file."
    )
    parser.add_argument("psautohint", type=str, help="The path to psautohint.")
    parser.add_argument("output_dir", type=Path, help="The output directory.")
    args = parser.parse_args()

    # 1. Load Designspace and filter out instances that are marked as non-exportable.
    designspace = fontTools.designspaceLib.DesignSpaceDocument.fromfile(
        args.designspace_path
    )
    designspace.instances = [
        s
        for s in designspace.instances
        if s.lib.get("com.schriftgestaltung.export", True)
    ]

    # 1.5. Fill in style names, etc.
    converted_designspaces = fontTools.designspaceLib.split.convert5to4(designspace)
    designspace = converted_designspaces["Cantarell-VF"]

    # 2. Prepare masters.
    generator = instantiator.Instantiator.from_designspace(
        designspace, round_geometry=True
    )

    # (Fork one process per instance)
    processes = []
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    for instance in designspace.instances:
        processes.append(
            pool.apply_async(
                generate_and_write_autohinted_instance,
                args=(generator, instance, args.output_dir, args.psautohint),
            )
        )
    pool.close()
    pool.join()
    for process in processes:
        process.get()  # Catch exceptions.
