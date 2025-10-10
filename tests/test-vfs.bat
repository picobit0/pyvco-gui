echo ==== Normal vfs path test ====
py ../console-gui.py --vfs-path test-vfs.xml
echo ==== Wrong vfs path test ====
py ../console-gui.py --vfs-path unknown.file
pause