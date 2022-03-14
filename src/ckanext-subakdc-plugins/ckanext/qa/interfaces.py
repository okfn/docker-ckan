from abc import ABC, abstractmethod, abstractproperty

from ckanext.qa.utils import get_all_pkgs


class IQaTask(ABC):
    """
    A task that operates over all or a subset of entities and produces a QA property for each entity e.g. A “broken links” task to test all links associated with a dataset
    """
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
    @classmethod
    def build(cls, qa_property_name, fields=None):
        # Get all packages
        pkgs = get_all_pkgs()
        
        # Build report table detailing packages with no resources
        report_table = []
        if fields is None:
            fields = ['id', 'title']
            
        for pkg in pkgs:
            if 'subak_qa' in pkg:
                if qa_property_name in pkg['subak_qa'] and cls.should_show_in_report(pkg['subak_qa'][qa_property_name]):
                    report_table.append({ k: pkg[k] for k in fields})
                
        return {
            'table': list(report_table),
            'total_num_packages': len(pkgs),
        }
        
    @classmethod
    @abstractmethod
    def generate(cls):
        """
        This method gets called from ckanext-report when generting report. It should define some fields
        and call cls.build
        """
        pass

    @classmethod
    @abstractmethod
    def should_show_in_report(cls, value):
        """
        Evaluate value against some condition and return True if item should show in the report, False if not
        """
        pass
    
    @classmethod
    @abstractmethod
    def get_qa_actions(cls):
        pass


class IQaAction(ABC):
    """
    An action that can be taken using information in the QA report to modify the entities for a given QA task. e.g. Remove the links, or mark the datasets as 'stale'. A QA action should also be able to be run from the command line as a ckan command
    """
    @classmethod
    @abstractmethod
    def run(cls):
        pass