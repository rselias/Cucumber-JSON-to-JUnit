import sys
import json

if len(sys.argv) < 2 or not sys.argv[1].endswith(".json"):
    print("No JSON file path received. Usage:")
    print("\tpython cucumber-json-to-junit.py source-report.json target-report.xml")
    sys.exit()
if len(sys.argv) < 3 or not sys.argv[2].endswith(".xml"):
    print("No XML file path received. Usage:")
    print("\tpython cucumber-json-to-junit.py source-report.json target-report.xml")
    sys.exit()

with open(sys.argv[1], "r") as jsonFile:
    print("Opening file " + sys.argv[1] + " in read-only")
    jsonData = json.load(jsonFile)

testcases = ""
header = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n"

testsuiteTime = 0.0
numFailures = 0
numScenarios = 0

for feature in jsonData:
    
    featureName = feature["name"]
    scenarios = feature["elements"]
    featureTime = 0.0
    
    
    for scenario in scenarios:

        numScenarios += 1
        
        scenarioName = scenario["name"]
        stepsBlob = "<![CDATA["
        errBlob = ""
        scenarioStatus = "passed"
        scenarioTime = 0.0
        
        for step in scenario["steps"]:
            
            description = step["name"]
            results = step["result"]
            status = results["status"]
            keyword = step["keyword"]
            
            if status != "skipped":
                scenarioTime += float(results["duration"]) / 1000000000
                
            numDots = 83 - len(keyword) - len(description) - len(status)
            if numDots <= 0: numDots = 1
                
            stepsBlob += keyword + description
            for i in range(numDots): stepsBlob += "."
            stepsBlob += status + "\n"
            if status == "failed":
                errBlob = results["error_message"]
                scenarioStatus = "failed"
                numFailures += 1

        featureTime += scenarioTime
        
        stepsBlob += "]]>"
        
        testcase = "<testcase "
        testcase += "classname=\"" + featureName + "\" "
        testcase += "name=\"" + scenarioName + "\" "
        testcase += "time=\"" + str(scenarioTime) + "\">"
        if scenarioStatus == "passed":
            testcase += "<system-out>" + stepsBlob + "</system-out>\n</testcase>"
        else:
            testcase += "<failure message=\"" + errBlob + "\">"
            testcase += stepsBlob + "</failure>\n"
        testcase += "</testcase>\n"
                 
    testcases += testcase
    testsuiteTime += featureTime
    
testsuite = "<testsuite "
testsuite += "failures=\"" + str(numFailures) + "\" "
testsuite += "name=\"Cucumber JSON to JUnit\" "
testsuite += "skipped=\"0\" "
testsuite += "tests=\"" + str(numScenarios) + "\" "
testsuite += "time=\"" + str(testsuiteTime) + "\">\n"
for testcase in testcases: testsuite += testcase
testsuite += "</testsuite>"


with open(sys.argv[2], "w") as junitFile:
    print("Writing to file " + sys.argv[2] + "...")
    junitFile.write(header)
    junitFile.write(testsuite)

print("Done.")
