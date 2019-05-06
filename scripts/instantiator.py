#!/bin/env python3
#
# This code is based on ufoProcessor code, see LICENSE_ufoProcessor, and is itself
# MIT-licensed.

"""Module for generating static font instances.

It is an alternative to mutatorMath (used internally by fontmake) and ufoProcessor. The
aim is to be a minimal implementation that is focussed on using ufoLib2 for font data
abstraction, varLib for instance computation and fontMath as a font data shell for
instance computation directly and exclusively.

At the time of this writing, varLib lacks support for anisotropic (x, y) locations and
extrapolation.

See the `scripts/make-static-fonts.py` script for how to use it.
"""

from pathlib import Path
from typing import Any, Dict, List, Mapping, Set, Tuple, Union

import attr
import fontMath
import fontTools.designspaceLib as designspaceLib
import fontTools.misc.fixedTools
import fontTools.ufoLib as ufoLib
import fontTools.varLib as varLib
import ufoLib2

FontMathObject = Union[fontMath.MathGlyph, fontMath.MathInfo, fontMath.MathKerning]
Location = Mapping[str, float]

# Use the same rounding function used by varLib to round things for the variable font
# to reduce differences between the variable and static instances.
fontMath.mathFunctions.setRoundIntegerFunction(fontTools.misc.fixedTools.otRound)


@attr.s(auto_attribs=True, frozen=True, slots=True)
class Instantiator:
    """Data class that holds all necessary information to generate a static
    font instance object at an arbitary location within the design space."""

    axis_bounds: Dict[str, Tuple[float, float, float]]  # Design space!
    copy_feature_text: str
    copy_groups: Mapping[str, List[str]]
    copy_info: ufoLib2.objects.Info
    copy_lib: Mapping[str, Any]
    designspace_rules: List[designspaceLib.RuleDescriptor]
    glyph_mutators: Mapping[str, "Variator"]
    info_mutator: "Variator"
    kerning_mutator: "Variator"
    round_geometry: bool
    skip_export_glyphs: List[str]
    weight_width_axes: Mapping[str, designspaceLib.AxisDescriptor]

    @classmethod
    def from_designspace(
        cls,
        designspace: designspaceLib.DesignSpaceDocument,
        round_geometry: bool = True,
    ):
        """Instantiates a new data class from a Designspace object."""
        if designspace.default is None:
            raise ValueError(
                "Can't generate UFOs from this designspace: no default font."
            )

        glyph_names: Set[str] = set()
        for source in designspace.sources:
            if source.font is None:
                if not Path(source.path).exists():
                    raise ValueError(f"Source at path '{source.path}' not found.")
                source.font = ufoLib2.Font.open(source.path, lazy=False)
            glyph_names.update(source.font.keys())

        # Construct Variators
        axis_bounds: Dict[str, Tuple[float, float, float]] = {}  # Design space!
        axis_order: List[str] = []
        weight_width_axes = {}
        for axis in designspace.axes:
            axis_order.append(axis.name)
            axis_bounds[axis.name] = (
                axis.map_forward(axis.minimum),
                axis.map_forward(axis.default),
                axis.map_forward(axis.maximum),
            )
            if axis.tag in ("wght", "wdth"):
                weight_width_axes[axis.tag] = axis

        masters_info = collect_info_masters(designspace, axis_bounds)
        info_mutator = Variator.from_masters(masters_info, axis_order)

        masters_kerning = collect_kerning_masters(designspace, axis_bounds)
        kerning_mutator = Variator.from_masters(masters_kerning, axis_order)

        glyph_mutators: Dict[str, Variator] = {}
        for glyph_name in glyph_names:
            items = collect_glyph_masters(designspace, glyph_name, axis_bounds)
            mutator = Variator.from_masters(items, axis_order)
            glyph_mutators[glyph_name] = mutator

        # Construct defaults to copy over
        default_source = designspace.findDefault()
        copy_feature_text: str = next(
            (s.font.features.text for s in designspace.sources if s.copyFeatures),
            default_source.font.features.text,
        )
        copy_groups: Mapping[str, List[str]] = next(
            (s.font.groups for s in designspace.sources if s.copyGroups),
            default_source.font.groups,
        )
        copy_info: ufoLib2.objects.Info = next(
            (s.font.info for s in designspace.sources if s.copyInfo),
            default_source.font.info,
        )
        copy_lib: Mapping[str, Any] = next(
            (s.font.lib for s in designspace.sources if s.copyLib),
            default_source.font.lib,
        )

        # The list of glyphs not to export and decompose where used as a component is
        # supposed to be taken from the Designspace when a Designspace is used as the
        # starting point of the compilation process. It should be exported to all
        # instance libs, where the ufo2ft compilation functions will pick it up.
        skip_export_glyphs = designspace.lib.get("public.skipExportGlyphs", [])

        return cls(
            axis_bounds,
            copy_feature_text,
            copy_groups,
            copy_info,
            copy_lib,
            designspace.rules,
            glyph_mutators,
            info_mutator,
            kerning_mutator,
            round_geometry,
            skip_export_glyphs,
            weight_width_axes,
        )

    def generate_instance(
        self, instance: designspaceLib.InstanceDescriptor
    ) -> ufoLib2.Font:
        """Generate a font object for an InstanceDescriptor."""
        font = ufoLib2.Font()

        location = instance.location
        if anisotropic(location):
            raise ValueError(
                f"Instance {instance.familyName}-"
                f"{instance.styleName}: Anisotropic location "
                f"{instance.location} not supported by varLib."
            )
        location_normalized = normalize_design_location(location, self.axis_bounds)

        # Kerning
        if instance.kerning:
            kerning_instance = self.kerning_mutator.instance_at(location_normalized)
            kerning_instance.extractKerning(font)

        # Info
        info_instance = self.info_mutator.instance_at(location_normalized)
        if self.round_geometry:
            info_instance = info_instance.round()
        info_instance.extractInfo(font.info)

        # Copy metadata from sources marked with `<copy info="1">` etc.
        for attribute in ufoLib.fontInfoAttributesVersion3:
            if hasattr(info_instance, attribute):
                continue  # Skip mutated attributes.
            if hasattr(self.copy_info, attribute):
                setattr(font.info, attribute, getattr(self.copy_info, attribute))
        for key, value in self.copy_lib.items():
            font.lib[key] = value
        font.lib["public.skipExportGlyphs"] = self.skip_export_glyphs
        for key, value in self.copy_groups.items():
            font.groups[key] = value
        font.features.text = self.copy_feature_text

        # TODO: multilingual names to replace possibly existing name records.
        if instance.familyName:
            font.info.familyName = instance.familyName
        if instance.styleName:
            font.info.styleName = instance.styleName
        if instance.postScriptFontName:
            font.info.postscriptFontName = instance.postScriptFontName
        if instance.styleMapFamilyName:
            font.info.styleMapFamilyName = instance.styleMapFamilyName
        if instance.styleMapStyleName:
            font.info.styleMapStyleName = instance.styleMapStyleName

        # If the masters haven't set the OS/2 weight and width class, use the
        # user-space values ("input") of the axis mapping in the Designspace file for
        # weight and width axes, if they exist.
        if info_instance.openTypeOS2WeightClass is None:
            if "wght" in self.weight_width_axes:
                weight_axis = self.weight_width_axes["wght"]
                weight_axis_instance_location = instance.location[weight_axis.name]
                font.info.openTypeOS2WeightClass = fontTools.misc.fixedTools.otRound(
                    weight_axis.map_backward(weight_axis_instance_location)
                )
        if info_instance.openTypeOS2WidthClass is None:
            if "wdth" in self.weight_width_axes:
                width_axis = self.weight_width_axes["wdth"]
                width_axis_instance_location = instance.location[width_axis.name]
                font.info.openTypeOS2WidthClass = fontTools.misc.fixedTools.otRound(
                    width_axis.map_backward(width_axis_instance_location)
                )

        # Glyphs
        for glyph_name, glyph_mutator in self.glyph_mutators.items():
            glyph = font.newGlyph(glyph_name)

            glyph_instance = glyph_mutator.instance_at(location_normalized)
            if self.round_geometry:
                glyph_instance = glyph_instance.round()

            # onlyGeometry=True does not set name and unicodes, in ufoLib2 we can't
            # modify a glyph's name. Copy unicodes.
            glyph_instance.extractGlyph(glyph, onlyGeometry=True)
            glyph.unicodes = glyph_instance.unicodes

        # Process rules
        glyph_names_list = self.glyph_mutators.keys()
        resultNames = designspaceLib.processRules(
            self.designspace_rules, location, glyph_names_list
        )
        for oldName, newName in zip(glyph_names_list, resultNames):
            if oldName != newName:
                swapGlyphNames(font, oldName, newName)

        font.lib["designspace.location"] = list(instance.location.items())

        return font


def anisotropic(location: Location) -> bool:
    for v in location.values():
        if isinstance(v, tuple):
            return True
    return False


def normalize_design_location(
    design_space_location: Location,
    design_space_axis_bounds: Dict[str, Tuple[float, float, float]],
) -> Location:
    return varLib.models.normalizeLocation(
        design_space_location, design_space_axis_bounds
    )


def collect_info_masters(
    designspace, axis_bounds
) -> List[Tuple[Location, FontMathObject]]:
    """Return master Info objects wrapped by MathInfo."""
    locations_and_masters = []
    for source in designspace.sources:
        if source.layerName is not None:
            continue
        normalized_location = normalize_design_location(source.location, axis_bounds)
        locations_and_masters.append(
            (normalized_location, fontMath.MathInfo(source.font.info))
        )

    return locations_and_masters


def collect_kerning_masters(
    designspace, axis_bounds
) -> List[Tuple[Location, FontMathObject]]:
    """Return master kerning objects wrapped by MathKerning."""
    locations_and_masters = []
    for source in designspace.sources:
        if source.layerName is not None:
            continue  # No kerning in source layers.
        if not source.muteKerning:
            # This assumes that groups of all sources are the same.
            normalized_location = normalize_design_location(
                source.location, axis_bounds
            )
            locations_and_masters.append(
                (
                    normalized_location,
                    fontMath.MathKerning(source.font.kerning, source.font.groups),
                )
            )

    return locations_and_masters


def collect_glyph_masters(
    designspace, glyph_name, axis_bounds
) -> List[Tuple[Location, FontMathObject]]:
    """Return master glyph objects for glyph_name wrapped by MathGlyph."""
    locations_and_masters = []
    for source in designspace.sources:
        if glyph_name in source.mutedGlyphNames:
            continue

        if source.layerName is None:
            # Source font.
            source_layer = source.font.layers.defaultLayer
        else:
            # Source layer.
            source_layer = source.font.layers[source.layerName]
            if glyph_name not in source_layer:
                # Sparse source layer, skip for this glyph.
                continue

        if glyph_name not in source_layer:
            continue

        source_glyph = source_layer[glyph_name]

        # XXX: What to do about a glyphs lib key? Any useful data that should be
        # copied from master to all instances? `public.verticalOrigin`, does it
        # interpolate? `public.postscript.hints`?
        source_glyph.lib.clear()

        normalized_location = normalize_design_location(source.location, axis_bounds)
        locations_and_masters.append(
            (normalized_location, fontMath.MathGlyph(source_glyph))
        )

    return locations_and_masters


def swapGlyphNames(font, oldName, newName, swapNameExtension="_______________swap"):
    # In font swap the glyphs oldName and newName.
    # Also swap the names in components in order to preserve appearance.
    # Also swap the names in font groups.
    if oldName not in font or newName not in font:
        return
    swapName = oldName + swapNameExtension
    # park the old glyph
    if not swapName in font:
        font.newGlyph(swapName)
    # swap the outlines
    font[swapName].clear()
    p = font[swapName].getPointPen()
    font[oldName].drawPoints(p)
    font[swapName].width = font[oldName].width
    # lib?
    font[oldName].clear()
    p = font[oldName].getPointPen()
    font[newName].drawPoints(p)
    font[oldName].width = font[newName].width

    font[newName].clear()
    p = font[newName].getPointPen()
    font[swapName].drawPoints(p)
    font[newName].width = font[swapName].width

    # remap the components
    for g in font:
        for c in g.components:
            if c.baseGlyph == oldName:
                c.baseGlyph = swapName
            continue
    for g in font:
        for c in g.components:
            if c.baseGlyph == newName:
                c.baseGlyph = oldName
            continue
    for g in font:
        for c in g.components:
            if c.baseGlyph == swapName:
                c.baseGlyph = newName

    # change the names in groups
    # the shapes will swap, that will invalidate the kerning
    # so the names need to swap in the kerning as well.
    newKerning = {}
    for first, second in font.kerning.keys():
        value = font.kerning[(first, second)]
        if first == oldName:
            first = newName
        elif first == newName:
            first = oldName
        if second == oldName:
            second = newName
        elif second == newName:
            second = oldName
        newKerning[(first, second)] = value
    font.kerning.clear()
    font.kerning.update(newKerning)

    for groupName, members in font.groups.items():
        newMembers = []
        for name in members:
            if name == oldName:
                newMembers.append(newName)
            elif name == newName:
                newMembers.append(oldName)
            else:
                newMembers.append(name)
        font.groups[groupName] = newMembers

    remove = []
    for g in font:
        if g.name.find(swapNameExtension) != -1:
            remove.append(g.name)
    for r in remove:
        del font[r]


@attr.s(auto_attribs=True, frozen=True, slots=True)
class Variator:
    """A middle-man class that ingests a mapping of normalized locations to
    masters plus axis definitions and uses varLib to spit out interpolated
    instances at specified normalized locations.

    fontMath objects stand in for the actual master objects from the
    UFO. Upon generating an instance, these objects have to be extracted
    into an actual UFO object.
    """

    masters: List[FontMathObject]
    model: varLib.models.VariationModel

    @classmethod
    def from_masters(
        cls, items: List[Tuple[Location, FontMathObject]], axis_order: List[str]
    ):
        masters = []
        master_locations = []
        for normalized_location, master in items:
            master_locations.append(normalized_location)
            masters.append(master)
        model = varLib.models.VariationModel(master_locations, axis_order)

        return cls(masters, model)

    def instance_at(self, normalized_location: Location) -> FontMathObject:
        return self.model.interpolateFromMasters(normalized_location, self.masters)
