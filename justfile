set dotenv-load := true
image_name := 'pyspark-sa:dev'
aws_access_key_id := 'AKIA6HAOBWUXEZNJIN5V'
aws_secret_access_key := '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'
postgres_user := ''
postgres_password := ''
postgres_host := ''
postgres_port := ''
postgres_db_name := ''
table_name := ''

build:
    docker build -t {{image_name}} .

set positional-arguments
@run *args='':
    docker run --mount type=bind,source="$(pwd)",target=/opt/application \
         --mount type=tmpfs,destination=/tmp \
        {{image_name}} driver local:///opt/application/site-packages/main.py "$@"

shell:
    docker run -it \
    -e AWS_ACCESS_KEY_ID={{aws_access_key_id}} -e AWS_SECRET_ACCESS_KEY={{aws_secret_access_key}} \
    {{image_name}} /opt/spark/bin/pyspark --packages com.amazonaws:aws-java-sdk-bundle:1.11.375,org.apache.hadoop:hadoop-aws:3.2.0

