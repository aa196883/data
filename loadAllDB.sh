#!/bin/bash

#------Init
user=neo4j
database=neo4j

password_file=.database_password

if [ -f $password_file ]; then
    password=$(cat $password_file)
else
    # Read Password
    echo -n "Database password (will be written to $password_file) :" 
    read -s password

    echo $password > $password_file
fi

#------Generate database
make

#------Populate database
#---Clear the current database
echo "*************************";
echo "Clearing the database ..."
echo "*************************";
docker exec -i skrid-neo4j cypher-shell -u $user -p $password -d $database --format verbose "match (n) detach delete n;"
# docker exec -i skrid-neo4j cypher-shell -u $user -p $password -d $database --format verbose "match (n) return count(distinct n.inputfile);"

#---Load all
for d in */; do
    if [[ "$d" != "Musypher/" ]]; then
        echo "*****************************";
        echo "Loading the database '$d' ..."
        echo "*****************************";

        # Read each cypher file path from load_DB.cql and pipe it to docker exec
        while IFS= read -r cypherfile; do
            if [ -f "$cypherfile" ]; then
                echo "Loading $cypherfile ..."
                docker exec -i skrid-neo4j cypher-shell -u $user -p $password -d $database --format verbose < "$cypherfile"
            fi
        done < "$d/load_DB.cql"

        echo "Done !"
    fi
done

