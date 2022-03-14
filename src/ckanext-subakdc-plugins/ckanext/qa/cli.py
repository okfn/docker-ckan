import click

from ckanext.qa import tasks
from ckanext.qa.qa import QaTaskRunner

@click.group()
def qa():
    pass

@click.command()
def run():
    """
    Runs all tasks over all packages
    
    Run using `ckan qa run` in the CKAN container
    """
    runner = QaTaskRunner(tasks)
    runner.run()

qa.add_command(run)

def get_commands():
    return [qa]