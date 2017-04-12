import bpy
import os.path
import math
from glob import glob
import datetime
import sys

C = bpy.context
D = bpy.data
scene = D.scenes['Scene']

cameras = [
    (60,0), (60,90), (60, 180), (60, 270),
    (0, 0)
]


render_setting = scene.render

# output image size = (W, H)
w = 500
h = 500
render_setting.resolution_x = w
render_setting.resolution_y = h

def center_at_origin():
    bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')


def delect_all(name_prefix):
    candidate_list = [item.name for item in bpy.data.objects if item.type == "MESH"]

    # select them only.
    for object_name in candidate_list:
        if object_name.startswith(name_prefix):
            bpy.data.objects[object_name].select = True

    # remove all selected.
    bpy.ops.object.delete()

def main():
    
    from_thingid = int(argv[0])
    to_thingid = int(argv[1])

    # TODO
    #rl = create_second_renderlayer()
    #enable_linesets(rl)
    #disable_default_renderlayer()
    
    init_camera()
    fix_camera_to_origin()
    
    start =0
    stls = glob('/home/weitang114/Dev/hog_demo/data/stl/*.stl') 
    image_dir = '/home/weitang114/Dev/hog_demo/data/phong/'
    ignore_list = [
            'T3565_0.stl', #TOO long
            'T9404_0.stl', # too long
            'T9115_0.stl', # unknown fail
            ]
 
    def thingid_of_path(stl):
        return int(os.path.basename(stl)[1:].split('_')[0])

    stls = sorted(stls, key=thingid_of_path)
    stls = filter(lambda stl: 
                         from_thingid <= thingid_of_path(stl) <= to_thingid,
                  stls)

    for i,stl in enumerate(stls):
        if i < start:
            continue
        if os.path.basename(stl) in ignore_list:
            continue

        print('start ' + str(i) + ' ' + stl)
        log('start ' + str(i) + ' ' + stl)
        try:
            do_model(stl, image_dir)
            log('done:' + stl)
        except Exception:
            errlog('Fail:' + stl)

def log(msg, error=False):
    now = datetime.datetime.now()
    logfile = 'ok.log' if not error else 'fail.log'

    with open(logfile, 'a+') as f:
        msg = '[' + now.strftime("%Y-%m-%d %H:%M") + '] ' + msg
        print(msg, file=f)
    
def errlog(msg):
    log(msg, error=True)

    
def init_camera():
    cam = D.objects['Camera']
    # select the camera object
    scene.objects.active = cam
    cam.select = True
    
    # set the rendering mode to orthogonal and scale
    C.object.data.type = 'ORTHO'
    C.object.data.ortho_scale = 2.

def fix_camera_to_origin():
    origin_name = 'Origin'
    
    # create origin
    try: 
        origin = D.objects[origin_name]
    except KeyError:
        bpy.ops.object.empty_add(type='SPHERE')
        D.objects['Empty'].name = origin_name
        origin = D.objects[origin_name]
    
    origin.location = (0, 0, 0)
    
    cam = D.objects['Camera']
    scene.objects.active = cam
    cam.select = True
    
    if not 'Track To' in cam.constraints:
        bpy.ops.object.constraint_add(type='TRACK_TO')
    
    cam.constraints['Track To'].target = origin
    cam.constraints['Track To'].track_axis = 'TRACK_NEGATIVE_Z'
    cam.constraints['Track To'].up_axis = 'UP_Y'


def do_model(stl, image_dir):
#    stl = '/Users/weitang114/Downloads/388.stl'
#    image_dir = '/tmp/image/'

    name = load_model(stl)
    center_model(name)
    normalize_model(name)
    image_subdir = os.path.join(image_dir, name)     
    for i,c in enumerate(cameras):
        move_camera(c)
        render()
        save(image_subdir, '%s.%d' % (name, i)) 
    
    delete_model(name)

def load_model(stl):
    dir = os.path.dirname(stl)
    name = os.path.basename(stl).split('.')[0]
    name = name.title().replace('_', ' ')
    if not name in D.objects:
        print('loading :' + name)
        bpy.ops.import_mesh.stl(filepath=stl, directory=dir, filter_glob='*.stl')
    return name

def delete_model(name):
    for ob in scene.objects:
        if ob.type == 'MESH' and ob.name.startswith(name):
            ob.select = True
        else: 
            ob.select = False
    bpy.ops.object.delete()

def center_model(name):
    bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
    D.objects[name].location = (0,0,0)

def normalize_model(name):
    obj = D.objects[name]
    dim = obj.dimensions
    print('original dim:' + str(dim))
    if max(dim) > 0:
        dim = dim / max(dim)
    obj.dimensions = dim
    
    print('new dim:' + str(dim))



def move_camera(coord):
    def deg2rad(deg):
        return deg * math.pi / 180.
    
    r = 3.
    theta, phi = deg2rad(coord[0]), deg2rad(coord[1])
    loc_x = r * math.sin(theta) * math.cos(phi)
    loc_y = r * math.sin(theta) * math.sin(phi)
    loc_z = r * math.cos(theta)
    
    D.objects['Camera'].location = (loc_x, loc_y, loc_z)

def render():
    bpy.ops.render.render()

def save(image_dir, name):
    path = os.path.join(image_dir, name + '.png')
    D.images['Render Result'].save_render(filepath=path)
    print('save to ' + path)
    # log('save to ' + path)
    
#normalize_model('Buesi')  
#fix_camera_to_origin()
#move_camera((60, 270))
  
#bpy.ops.render.render()

argv = sys.argv
argv = argv[argv.index('--') + 1:]

main()
