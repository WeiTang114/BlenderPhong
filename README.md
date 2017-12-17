# BlenderPhong

A Blender python script to render an 3D model object by Phong Shading from several viewpoints.
We currently support **.obj**, **.stl**, and **.off** files.

This is an output from `airplane.off`:

<img src="https://i.imgur.com/9Vq37vD.png" width="200">

We use [blender-off-addon](https://github.com/alextsui05/blender-off-addon) for off importing support.

## Requirements
 - [Blender](https://www.blender.org/)

## Usage
### Run with Blender
```bash
blender phong.blend --background --python phong.py -- <model file> <output dir>
```

eg. (see `sample_run.sh`)
```bash
# remove "--background" if you want to see the GPI
blender phong.blend --background --python phong.py -- ./airplane.off ./
```

 - `phong.blend` is a scene file that has no default objects. (In a new Blender scene, there is a cube. I just removed it and saved the scene.)
 
### Multiple models
Edit models.txt to build a list of models you want to render.
See `sample_run_multiple.sh`
```
blender phong.blend --background --python phong_multi.py -- models.txt ./tmp
```

### Edit the viewpoints:
Edit `cameras` in phong.py to render from different viewpoints. See the code for more details.

## License
MIT
