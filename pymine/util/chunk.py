# A flexible and fast Minecraft server software written completely in Python.
# Copyright (C) 2021 PyMine

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
            
import numpy

from pymine.util.misc import remove_namespace
from pymine.types.abc import AbstractPalette
from pymine.types.chunk import Chunk


def dump_to_obj(file, pymine_chunk: Chunk, palette: AbstractPalette):
    chunk = numpy.zeros((256, 16, 16), numpy.uint64)

    for y, section in pymine_chunk.sections.items():
        if 0 <= y < 17:
            y *= 16
            chunk[y : y + 16] = section.block_states

    air = palette.encode("minecraft:air")

    points = {}
    rpoints = {}
    faces = {}
    rfaces = {}

    def append_point(*p) -> None:
        if not rpoints.get(p):
            points[len(points) - 1] = p
            rpoints[p] = len(points) - 1

    def append_face(f) -> None:
        if not rfaces.get(f):
            faces[len(faces) - 1] = f
            rfaces[f] = len(faces) - 1

    for y in range(256):
        for z in range(16):
            for x in range(16):
                if chunk[y, z, x] == air:
                    continue

                append_point(x, y, z)
                append_point(x + 1, y, z)
                append_point(x, y + 1, z)
                append_point(x, y, z + 1)
                append_point(x + 1, y + 1, z)
                append_point(x, y + 1, z + 1)
                append_point(x + 1, y, z + 1)
                append_point(x + 1, y + 1, z + 1)

    for y in range(256):
        for z in range(16):
            for x in range(16):
                block = chunk[y, z, x]

                if block == air:
                    continue

                block = remove_namespace(palette.decode(block)["name"])

                i1 = rpoints.get((x, y, z)) + 1
                i2 = rpoints.get((x + 1, y, z)) + 1
                i3 = rpoints.get((x, y + 1, z)) + 1
                i4 = rpoints.get((x, y, z + 1)) + 1
                i5 = rpoints.get((x + 1, y + 1, z)) + 1
                i6 = rpoints.get((x, y + 1, z + 1)) + 1
                i7 = rpoints.get((x + 1, y, z + 1)) + 1
                i8 = rpoints.get((x + 1, y + 1, z + 1)) + 1

                append_face(f"usemtl {block}\nf {i1} {i2} {i7} {i4}")
                append_face(f"usemtl {block}\nf {i1} {i2} {i5} {i3}")
                append_face(f"usemtl {block}\nf {i4} {i7} {i8} {i6}")
                append_face(f"usemtl {block}\nf {i1} {i4} {i6} {i3}")
                append_face(f"usemtl {block}\nf {i2} {i5} {i8} {i7}")
                append_face(f"usemtl {block}\nf {i3} {i5} {i8} {i6}")

    file.write("\n".join([f"v {p[0]} {p[1]} {p[2]}" for p in points.values()]) + "\n" + "\n".join(faces.values()))
