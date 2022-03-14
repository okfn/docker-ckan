import ckan.plugins as p
import ckan.plugins.toolkit as tk
from ckanext.report.interfaces import IReport

from ckanext.qa import tasks, reports
from ckanext.qa.cli import get_commands
from ckanext.qa.qa import QaTaskRunner

class QAPlugin(p.SingletonPlugin, tk.DefaultDatasetForm):
    p.implements(p.IClick)
    p.implements(p.IConfigurer)
    p.implements(p.IPackageController, inherit=True)
    p.implements(IReport)
        
    # ------- IClick method implementations ------- #
    def get_commands(self):
        return get_commands()

    # ------- IConfigurer method implementations ------- #
    def update_config(self, config):
        tk.add_template_directory(config, 'templates')
        
    # ------- IPackageController method implementations ------- #
    def after_create(self, context, pkg_dict):
        runner = QaTaskRunner(tasks)
        runner.run_on_single_package(pkg_dict)
        
    def after_update(self, context, pkg_dict):
        runner = QaTaskRunner(tasks)
        runner.run_on_single_package(pkg_dict)
        
    # ------- IReport method implementations ------- #
    def register_reports(self):
        return reports
