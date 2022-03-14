# QA Plugin

The QA CKAN plugin defines several tasks that report on the quality of datasets in the data catalogue.

# Defining a new QA task
- Copy an existing qa file (e.g. qa_no_resources.py) to a new python file named `qa_{task_name}.py` in this directory
- Update the `QA_PROPERTY_NAME`
- Rename classes and the `{task_name}_report_info variable` as per your new task's name
- Update the information in the `{task_name}_report_info` dict
- Update the `evaluate` and `should_show_in_report` methods (these of the conditions for setting the qa property on the model and whether a dataset should appear in the report respectively)

For the report template:
- Copy an existing report in `template/report` (e.g. qa_no_resources.html) to a new file and name it `qa_{task_name}.html`
- Update this new file as required

Finally:
- Import and add your new task to the `tasks` list in `__init__.py`
- Import and add you task report to `reports` list in `__init__.py`