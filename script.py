import copy, re
import sys, os, json
from adofai_lib import *

for_loop_regex = r"\(.+ in [A-Z0-9]+ *.. *[A-Z0-9]+\)"
with open(sys.argv[1], "r", encoding="utf-8") as scriptFile:
    script = scriptFile.readlines()
    try:
        try:
            adofaiFile = open(script[0][:-1], "r", encoding="utf-8")
            adofaiParser = parser.ADOFAIParser(adofaiFile)
        except IndexError as err:
            print("You need to provide the ADOFAI file path on the first line of the ADOFAIScript file")
            exit(-1)

        parsed = adofaiParser.parse()
        init_parsed = copy.copy(parsed)

        loop_stack = 0
        variables = {"START": 0, "END": len(init_parsed["angleData"])}

        for line_index, line in enumerate(script):
            if line_index == 0: continue
            if line == "RemoveEffect":
                parsed = adofaiParser.getChartData()

            if line == "ResetLevel":
                parsed = init_parsed
            
            if line.startswith("for"):
                loop_stack += 1
                loop_range = re.search(for_loop_regex, line, re.MULTILINE)
                if loop_range:
                    matched = loop_range.group()[1:-1]
                    split_match = matched.split(" ")
                    variables[split_match[0]] = None
                    if split_match[1:].count("..") > 0:
                        
                else:
                    print("For Loops Need Range")
        
        adofaiFile.close()
        adofaiFile = open(script[0][:-1], "w", encoding="utf-8")
        adofaiFile.write(json.dumps(adofaiParser.getDefaultWith(parsed)))
        adofaiFile.close()
    except FileNotFoundError:
        print("The ADOFAI file with the specified file name does not exist")