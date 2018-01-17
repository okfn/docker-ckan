import os
import sys
import subprocess
from sqlalchemy import create_engine
import sqlalchemy.exc


ckan_ini = os.environ.get('CKAN_INI', '/srv/app/production.ini')


def check_db():

    db_url = os.environ.get('CKAN_SQLALCHEMY_URL')
    engine = None
    ok = False

    try:
        engine = create_engine(db_url)

        version = engine.execute('SELECT version FROM migrate_version')
        if version.rowcount:
            version = version.fetchone()
            ok = int(version['version']) >= 76
    except sqlalchemy.exc.ProgrammingError:
        print '[prerun-harvest] Migrate table not ready'
    except Exception, e:
        print '[prerun-harvest] Error connecting to the database: ' + \
              '\n{0}'.format(e)
    finally:
        if engine:
            engine.dispose()

    return ok


def start_harvest_process(name):

    print '[prerun-harvest] Starting {0} consumer'.format(name)
    command = [
        'paster', '--plugin=ckanext-harvest', 'harvester',
        '{0}_consumer'.format(name), '-c', ckan_ini]

    subprocess.call(command)


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print '[prerun-harvest] Wrong arguments'
        sys.exit(1)

    name = sys.argv[1]
    if name not in ('gather', 'fetch'):
        print '[prerun-harvest] Wrong process, must be "gather" or "fetch"'
        sys.exit(1)

    if check_db():
        start_harvest_process(name)
    else:
        print '[prerun-harvest] Database not ready, not starting'
        sys.exit(1)
