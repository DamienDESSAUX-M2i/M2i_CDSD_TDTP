# Spark UI

1. Create containers

```bash
docker-compose up -d
```

2. Launch application

```bash
docker exec -it spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 /apps/lab_spark_ui.py
```

3. Watch Spark running

http://localhost:8080 -> Spark Master
http://localhost:4040 -> Application UI (driver)
http://localhost:8081 -> Worker 1
http://localhost:8082 -> Worker 2
http://localhost:8083 -> Worker 3