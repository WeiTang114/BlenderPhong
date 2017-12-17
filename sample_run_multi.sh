mkdir -p tmp
blender phong.blend --background --python phong_multi.py -- models.txt ./tmp
