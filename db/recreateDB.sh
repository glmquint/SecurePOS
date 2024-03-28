#!/bin/bash

# Specify the directory where your .db files are located
db_directory="."

# Iterate over each .db file in the directory
for db_file in "$db_directory"/*.db; do
    if [ -f "$db_file" ]; then
        # Extract the schema of the existing database
        schema=$(sqlite3 "$db_file" ".schema")

        # Remove the existing .db file
        rm "$db_file"

        # Recreate the .db file with the same schema
        sqlite3 "$db_file" "$schema"
        
        echo "Recreated $db_file with the same schema."
    else
        echo "No .db file found in $db_directory"
    fi
done
