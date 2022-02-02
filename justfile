set dotenv-load := true
image_name := 'pyspark-sa:dev'

build:
    docker build -t {{image_name}} .

set positional-arguments
@run *args='':
    docker run --mount type=bind,source="$(pwd)",target=/opt/application \
         --mount type=tmpfs,destination=/tmp \
        {{image_name}} driver local:///opt/application/site-packages/main.py "$@"

shell:
    docker run -it \
    {{image_name}} /opt/spark/bin/pyspark --packages com.amazonaws:aws-java-sdk-bundle:1.11.375,org.apache.hadoop:hadoop-aws:3.2.0

