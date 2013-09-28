"""
This file is part of BlendStats.

BlendStats is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

BlendStats is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with BlendStats.  If not, see <http://www.gnu.org/licenses/>.
"""
# <pep8-80 compliant>

############
## CONFIG ##
###################################################################

# Should get absolute basepath from argument params[0]
base_path = "D:\\Webserver\\xampp\\htdocs\\blend_stats\\"

###################################################################

import bpy
import json
import os
import sys

context = bpy.context

# Workaround - ensure object mode, even if scene is actually
# in an invalid state (context manipulated by evil script)
def toggle_object_mode():

    limit = 3  # 3 iterations at most
    while ('OBJECT' != context.mode and limit > 0 and
           bpy.ops.object.editmode_toggle.poll()):

        # mode_set(mode='OBJECT') broken in background mode up to r57205
        bpy.ops.object.editmode_toggle()
        limit -= 1

    if context.mode != 'OBJECT':
        # Should only occur if above poll failed (ever?)
        print("Error: mode still not 'OBJECT'!")
        print("Scene statistics output is going to be incorrect.")


def isabs(filepath):
    #return os.path.isabs(filepath)
    #return not (filepath.startswith("//") or ".." in filepath)
    return not filepath.startswith("//")


def is_valid_path(filepath, basepath):
    # print("basepath", basepath)
    # print("filepath", filepath)
    if not filepath.startswith("//"):
        print("no leading //")
        return False
    realpath = os.path.realpath(bpy.path.abspath(filepath))
    # print("realpath", realpath)
    return (realpath.startswith(basepath) and
            os.path.exists(realpath) and
            os.path.isfile(realpath))

# Vars for holding results
output = {}
scenes = []


for scene in bpy.data.scenes:

    # Setting active scene resets object mode in regular Blender use.
    # Unfortunately, it doesn't switch if running in background mode.
    # However, Scene.statistics() still requires the scene being active!
    context.screen.scene = scene

    # Ensure 'OBJECT' mode
    toggle_object_mode()

    verts = sum(len(ob.data.vertices) \
        for ob in scene.objects if ob.type == 'MESH')

    polygons = sum(len(ob.data.polygons) \
        for ob in scene.objects if ob.type == 'MESH')

    render_engine = scene.render.engine

    objects_mesh = len([ob for ob in scene.objects if ob.type == 'MESH'])

    # Get scene statistics from built-in function (object mode required)
    # It includes modifiers (final meshes)!
    builtin_stats = scene.statistics()

    # Extract relevant information
    for segment in builtin_stats.split(" | "):
        segment_split = segment.split(":")
        if segment_split[0] == "Verts":
            verts_modified = int(segment_split[1])
        elif segment_split[0] == "Faces":
            polygons_modified = int(segment_split[1])
        elif segment_split[0] == "Tris":
            triangles = int(segment_split[1])

    this_scene = {
        'name': scene.name,
        'verts': verts,
        'verts_modified': verts_modified,
        'polygons': polygons,
        'polygons_modified': polygons_modified,
        'triangles': triangles,
        'render_engine': render_engine,
        'objects_mesh': objects_mesh,
    }
    scenes.append(this_scene)

output['scenes'] = scenes


# Get script parameters:
# all list items after the last occurence of "--"
print()
print(sys.argv)
print()

try:
    args = list(reversed(sys.argv))
    idx = args.index("--")

except ValueError:
    params = []

else:
    params = args[:idx][::-1]

print("Script params:", params)


# Check for broken image references
bad_images = []

for image in bpy.data.images:

    if image.name in bad_images:
        continue

    if ((image.users > 0 # image datablock in use (ignores use_fake_user)
         and image.packed_file is None # image not stored inside the .blend
         and image.filepath # filepath string is not empty
         # valid means: blender-style relative path, inside base path,
         # path actually exists and path references a file. Checks for invalid.
         and not is_valid_path(image.filepath, base_path)
        )
        or image.library is not None): # is linked from another .blend

        bad_images.append(image.name)

output['bad_images'] = bad_images

""" pretty useless actually, as it's not about the .blend file
output['version'] = {
    "char": bpy.app.version_char,
    "cycle": bpy.app.version_cycle,
    "number": bpy.app.version,
    "revision": bpy.app.build_revision.decode(),

}
"""

# Dump gathered information to command line
# JSON module safely encodes UTF8/16 chars, as well as escape sequences
print("\n---STATS---BEGIN---")
print(json.dumps(output, indent=4, sort_keys=True))
print("---STATS---END---")
