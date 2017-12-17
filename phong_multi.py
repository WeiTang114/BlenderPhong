# WARNING:
# Blender might not release memory even if you delete an object,
# so rendering a large number of object in one run may occupy a lot of memory.
# If this happens, it is better to split the list into multiple runs..
from phong import *

def main():
    argv = sys.argv
    argv = argv[argv.index('--') + 1:]

    if len(argv) != 2:
        print('phong.py args: <3d mesh list file> <image dir>')
        exit(-1)

    models_list = argv[0]
    image_dir = argv[1]

    # blender has no native support for off files
    install_off_addon()

    init_camera()
    fix_camera_to_origin()

    with open(models_list) as f:
        models = f.read().splitlines()

    for model in models:
        do_model(model, image_dir)


if __name__ == '__main__':
    main()
