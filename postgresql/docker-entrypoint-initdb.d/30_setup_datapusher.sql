\set datapusher_password '\'' `echo $DATAPUSHER_PASSWORD` '\''
\set datapusher_jobs_password '\'' `echo $DATAPUSHER_JOBS_PASSWORD` '\''

-- based on https://github.com/dathere/datapusher-plus#datapusher-database-setup
CREATE ROLE datapusher LOGIN PASSWORD :datapusher_password;
GRANT CREATE, CONNECT, TEMPORARY ON DATABASE datastore TO datapusher;
GRANT USAGE ON SCHEMA public to datapusher;
ALTER ROLE datapusher WITH SUPERUSER; -- todo: see if there's a less permissive way to handle this.

CREATE ROLE datapusher_jobs NOSUPERUSER NOCREATEDB NOCREATEROLE LOGIN PASSWORD :datapusher_jobs_password;
CREATE DATABASE datapusher_jobs WITH OWNER datapusher_jobs ENCODING UTF8;
