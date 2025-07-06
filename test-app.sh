docker run -dit --name test-app ubuntu bash
docker exec -d test-app bash -c "while true; do :; done"