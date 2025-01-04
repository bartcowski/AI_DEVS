docker run ^
    --publish=7474:7474 --publish=7687:7687 ^
    --volume=neo4j-data:/data ^
    --volume=neo4j-logs:/logs ^
    --name neo4j-db ^
    -d ^
    neo4j
