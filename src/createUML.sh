#!/bin/bash
# Start from OBthe root directory
root_dir="."
echo "********** Executing pyreverse **********"
find "$root_dir" -type d -exec sh -c 'ls -p "{}"/*.py 2>/dev/null | grep -q . && echo "Executing pyreverse in directory: {}" && pyreverse "{}" -d "{}" -o svg --colorized' \;
echo "********** Now converting svg to EMF **********"
# Convert all SVG files to EMF
find "$root_dir" -type f -name "*.svg" -exec sh -c 'dir=$(dirname "{}"); file=$(basename "{}"); inkscape --export-type=emf "$dir/$file"' \;
echo "Done!"