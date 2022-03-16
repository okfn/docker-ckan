#!/bin/bash

if [ "$1" = "" ] || [ "$2" = "" ] || [ "$3" = "" ]
then
    echo "Usage: $0 <environment_name> <service_name> <database>..."
    echo "Example: $0 production service_name_postgres dbname"
    exit 1
fi

# https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
set -euxo pipefail

export PATH=/usr/local/bin:/usr/local/sbin:/bin:/sbin:/usr/bin:/usr/sbin

environment=$1
service_name=$2
database_name=$3
date=$(date +%Y-%m-%d"_"%H_%M_%S)
backup_filename="${database_name}_${date}.sql"
backup_filename_zipped="${backup_filename}.gz"
s3_location="s3://subakdc-db-backups/${environment}/"

docker_bin=$(which docker)
aws_bin=$(which aws)

container_id=$($docker_bin ps | grep $service_name | awk '{print $1}')

# create the backup
$docker_bin exec $container_id pg_dump -U ckan -f /tmp/$backup_filename $database_name

# copy file inside contaienr to host
$docker_bin cp $container_id:/tmp/$backup_filename .

# remove file in container
$docker_bin exec $container_id rm /tmp/$backup_filename

# compress
gzip $backup_filename

# upload to s3
$aws_bin s3 cp $backup_filename_zipped $s3_location

rm $backup_filename_zipped

echo "Done."