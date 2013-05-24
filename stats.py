import bpy
import json
import os

context = bpy.context
output = {}
stats = {}

def mode_set_object():

    # Bug? Doesn't change mode if Blender runs in background mode
    #if bpy.ops.object.mode_set.poll():
    #    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    #else:
    #    print("mode_set.poll() failed.")

    if context.mode != 'OBJECT':
        bpy.ops.object.editmode_toggle()

    # If mode was e.g. 'PAINT_WEIGHT', it's now 'EDIT_MESH'. Call again...
    if context.mode != 'OBJECT':
        bpy.ops.object.editmode_toggle()

    if context.mode != 'OBJECT':
        print("Error: mode still not 'OBJECT'!")

def isabs(filepath):
    #return os.path.isabs(filepath)
    #return not (filepath.startswith("//") or ".." in filepath)
    return not filepath.startswith("//")

def is_valid_path(filepath, basepath):
    print("basepath", basepath)
    print("filepath", filepath)

    if not filepath.startswith("//"):
        print("no leading //")
        return False
    realpath = os.path.realpath(bpy.path.abspath(filepath))
    print("realpath", realpath)
    return realpath.startswith(basepath) and os.path.exists(realpath) and os.path.isfile(realpath)


for scene in bpy.data.scenes:

    # Was supposed to reset mode to 'OBJECT', but doesn't work in background mode
    # It's still required, since Scene.statistics() requires the scene being active!
    context.screen.scene = scene

    mode_set_object()


    verts = sum(len(ob.data.vertices) for ob in scene.objects if ob.type == 'MESH')
    polygons = sum(len(ob.data.polygons) for ob in scene.objects if ob.type == 'MESH')
    render_engine = scene.render.engine
    objects_mesh = len([ob for ob in scene.objects if ob.type == 'MESH'])

    builtin_stats = scene.statistics() # includes modifiers!

    for segment in builtin_stats.split(" | "):
        segment_split = segment.split(":")
        if segment_split[0] == "Verts":
           verts_modified = int(segment_split[1])
        elif segment_split[0] == "Faces":
           polygons_modified = int(segment_split[1])
        elif segment_split[0] == "Tris":
           triangles = int(segment_split[1])

    stats[scene.name] = {
        'verts': verts,
        'verts_modified': verts_modified,
        'polygons': polygons,
        'polygons_modified': polygons_modified,
        'triangles': triangles,
        'render_engine': render_engine,
        'objects_mesh': objects_mesh,
    }


# Get script parameters
import sys
try:
    #idx = sys.argv.index("--")

    # all list items after the last occurence of "--"
    #idx = len(sys.argv) - list(reversed(sys.argv)).index("--")

    idx = len(sys.argv)  - 1
    while idx >= 0:
        if sys.argv[idx] == "--":
            idx += 1
            break
        idx -= 1


    # additional sanity check, might decrease lower boundary value
    if idx < 6 or idx >= len(sys.argv):
        raise ValueError
except ValueError:
    params = []
else:
    params = sys.argv[idx:] # if .index -> idx+1
print("Script params:", params)

# Should get absolute basepath from argument params[0]
base_path = "D:\\Webserver\\xampp\\htdocs\\blendswap\\" # absolute server path?



output['stats'] = stats

bad_images = []


for image in bpy.data.images:
    if ((image.users > 0 and image.packed_file is None and image.filepath and not is_valid_path(image.filepath, base_path)) \
       or image.library is not None) \
       and image.name not in bad_images:

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

print("\n---STATS---BEGIN---")
print(json.dumps(output, indent=4, sort_keys=True))
print("---STATS---END---")
