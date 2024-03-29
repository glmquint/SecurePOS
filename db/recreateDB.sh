#!/bin/bash

# Specify the directory where your .db files are located
db_directory="."

# Iterate over each .db file in the directory
for db_file in "$db_directory"/*.db; do
    if [ -f "$db_file" ]; then
        # Get the schema of the current database
        schema=$(sqlite3 "$db_file" .schema)

        # Remove the current .db file
        rm "$db_file"

        # Recreate the .db file with the schema
        sqlite3 "$db_file" <<EOF
$schema
EOF

        echo "Database $db_file recreated with schema."
    else
        echo "No .db files found in the current directory."
        exit 1
    fi
done
