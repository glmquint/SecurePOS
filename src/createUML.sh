#!/bin/bash
find . -type d -exec sh -c 'ls -p "{}"/*.py 2>/dev/null | grep -q . && echo "Executing pyreverse in directory: {}" && pyreverse "{}" -d "{}" --colorized' \;

