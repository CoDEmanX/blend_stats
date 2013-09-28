@echo off

"C:\Program Files\Blender Foundation\Blender\blender.exe" ^
 -noaudio --disable-autoexec --background test.blend ^
 --python ..\blend_stats.py -- foobar script_param_2 1337

pause