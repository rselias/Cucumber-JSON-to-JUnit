# Cucumber JSON to JUnit XML

Quick python script to convert a Cucumber JSON report into JUnit XML format.
For use when using a parallelization plugin that can assemble a JSON report but not XML.
This will overwrite the target report if it already exists.

Note that the overall duration will be incorrect for parallel execution, as it is the sum of the scenario durations.

Usage:

`pip install cucumber-json-to-junit-xml`

`json_to_junit source-report.json target-report.xml`