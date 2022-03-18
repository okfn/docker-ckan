from abc import ABC, abstractmethod
import logging

import ckan.plugins.toolkit as tk

from ckanext.qa.utils import get_all_pkgs

log = logging.getLogger(__name__)


class IQaTask(ABC):
    """
    A task that operates over all or a subset of entities and produces a QA property for each entity e.g. A “broken links” task to test all links associated with a dataset
    """
    qa_property_name = ""
    qa_actions = []
    
    @classmethod
    @abstractmethod
    def evaluate(cls, pkg):
        """
        Runs an evaluation over the entity and sets the QA property based on the result
        """
        pass


class IQaReport(ABC):
    """
    A tabular report generated with the ckanext-report plugin that gathers the QA property for all entities for a 
    given QA task. e.g. Details a summary of all entities with 'Broken links'
    """
    qa_property_name = ""
    qa_actions = []
    
    @classmethod
    def get_qa_actions(cls):
        return [ action.get_action() for action in cls.qa_actions ]
    
    @classmethod
    def build(cls, fields=None, computed_fields=None, action_is_running=False):
        """
        Builds the report table

        Args:
            fields (list, optional): The fields within each pkg to display in the report. Defaults to None.
            computed_fields (dict, optional): Extra fields that are computed when the report is run - dict key is field title/label, dict value is callable (which is passed a pkg dict). Defaults to None.
            action_is_running (boolean, optional): Indicates whether an action is running in the background which will affect the results of this report

        Returns:
            dict: report table dict
        """
        # Get all packages
        pkgs = get_all_pkgs()
        
        # Build report table detailing packages with no resources
        report_table = []
        if fields is None:
            fields = ['id', 'title']
            
        for pkg in pkgs:
            if 'subak_qa' in pkg:
                if cls.qa_property_name in pkg['subak_qa'] and cls.should_show_in_report(pkg['subak_qa'][cls.qa_property_name]):
                    report_fields = { k: pkg[k] for k in fields}
                    if computed_fields is not None:
                        for title, field in computed_fields.items():
                            report_fields[title] = field(pkg)
                        
                    report_table.append(report_fields)
                
        return {
            'table': list(report_table),
            'total_num_packages': len(pkgs),
            'qa_actions': cls.get_qa_actions(),
            'action_is_running': action_is_running
        }
        
    @classmethod
    def run_action(cls):
        """
        Determine which QA action to run based on the button that was clicked in the 
        report and run the QA action as a background job. This should be called by 
        the generate method in this class before building the report table. 
        """
        actions = list(filter(lambda item: item.startswith('action.'), tk.request.form))
        if len(actions) == 0:
            return False
        
        pkg_ids = tk.request.form.getlist('id')
        if len(pkg_ids) == 0:
            return False
        
        action_name = actions[0].split('.', 1)[1]
        for action in cls.qa_actions:
            if action.name == action_name:
                action.run_job(pkg_ids)
                return True
        
    @classmethod
    @abstractmethod
    def generate(cls):
        """
        This method gets called from ckanext-report when generting report. 
        It should define some fields and call cls.build
        """
        pass

    @classmethod
    @abstractmethod
    def should_show_in_report(cls, value):
        """
        Evaluate value against some condition and return True if item should show 
        in the report, False if not
        """
        pass


class IQaAction(ABC):
    """
    An action that can be taken using information in the QA report to modify the 
    entities for a given QA task. e.g. Remove the links, or mark the datasets as 
    'stale'. A QA action should also be able to be run from the command line as 
    a CKAN command
    """
    name = ""
    form_button_text = ""
    
    @classmethod
    def get_action(cls):
        """
        Returns a dict of the name and form_button_text to be used in the report 
        template
        """
        return { "name": f"action.{cls.name}", 
                 "form_button_text": cls.form_button_text }
    
    @classmethod
    def run_job(cls, pkg_ids):
        func = cls.run
        tk.enqueue_job(func, [ pkg_ids ], rq_kwargs={ 'timeout': 3600 })
    
    @classmethod
    @abstractmethod
    def run(cls, pkg_ids):
        """
        Runs an action over the pkg_ids (e.g. deleting all packages in the list)
        """
        pass
