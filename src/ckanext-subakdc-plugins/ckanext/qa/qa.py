import json
import logging

import ckan.plugins.toolkit as tk

from ckanext.qa.utils import get_all_pkgs, get_qa_properties

log = logging.getLogger(__name__)

class QaTaskRunner():
    tasks = []
    def __init__(self, tasks):
        self.tasks = tasks
        
    def run(self):
        """
        Runs QA tasks over all entities (triggers a job as this will be a long running process)
        """
        func = self.run_tasks_as_job
        tk.enqueue_job(func, rq_kwargs={ 'timeout': 3600 })
        
    def run_tasks_as_job(self):
        """
        Runs an empty patch request on the package - this will trigger run_on_single_package to 
        be be run in CKAN's post-create/update hook which does the actual work of adding/updating 
        QA properties on the package
        """
         # Get all packages and associated resources
        pkgs = get_all_pkgs()
    
        for pkg in pkgs:
            self.run_on_single_package(pkg)
    
    def run_on_single_package(self, pkg):
        """
        Runs whenever a package is created/updated. Runs all QA tasks against the package
        and sets the qa property in the subak_qa dict on the model
        """
        # Get the required API actions
        show_package = tk.get_action('package_show')
        patch_package = tk.get_action('package_patch')
        
        # Get the full package
        pkg = show_package({ 'ignore_auth': True, 'user': None }, 
                           { 'id': pkg['id'] })
        
        # Get the current QA properties
        qa = get_qa_properties(pkg)
        
        # Clone qa properties and evaluate the package against all the qa tasks,
        new_qa = qa.copy()
        try:
            for task in self.tasks:
                new_qa[task.qa_property_name] = task.evaluate(pkg)
        except:
            log.error(f"Could not evaluate package against all tasks in run_on_single_package: {pkg['name']}, {e}")
        
        # Only patch the package if the qa properties have changed
        if qa != new_qa:
            try:
                patch_package({ 'ignore_auth': True, 'user': None }, 
                              { 'id': pkg['id'], 'subak_qa': json.dumps(new_qa) })
            except Exception as e:
                log.error(f"Could not patch package in run_on_single_package: {pkg['name']}, {e}")
