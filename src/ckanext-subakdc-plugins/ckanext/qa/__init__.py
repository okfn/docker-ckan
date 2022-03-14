from ckanext.qa.qa_no_resources import QaNoResourcesTask, qa_no_resources_report_info
from ckanext.qa.qa_stale import QaStaleTask, qa_stale_report_info

tasks = [ QaNoResourcesTask,
          QaStaleTask ]

reports = [ qa_no_resources_report_info,
            qa_stale_report_info ]
