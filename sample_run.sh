mkdir -p tmp
blender phong.blend --background --python phong.py -- ./airplane.off ./tmp
