import csv
import json
import os

# global variables
INPUT_FILES = {
    'INPUT': 'input_file.txt',
    'DEFINITION': 'standard_definition.json',
    'ERROR': 'error_codes.json'
}
OUTPUT_FILES = {
    'PATH': 'parsed',
    'REPORT': 'parsed/report.csv',
    'SUMMARY': 'parsed/summary.txt'
}

# read the input file and returns a list of input
def getContents(fileName) -> list:
    f = open(fileName, "r")
    content = [line.strip() for line in f if line.strip()]
    content = [x.strip() for x in content]
    f.close()
    return content

# read the standard definition file and returns dictionary
def getDefinitions() -> dict:
    definition = dict()
    f = open(INPUT_FILES['DEFINITION'])
    data = json.load(f)
    for i in data:
        d = dict()
        for s in i['sub_sections']:
            element = s.pop('key')
            d[element] = s
        definition[i['key']] = d
    f.close()
    return definition

# parse error codes information and returns dictionary
def getErrorCodes() -> dict:
    errors = dict()
    f = open(INPUT_FILES['ERROR'])
    data = json.load(f)
    for i in data:
        code = i.pop('code')
        errors[code] = i['message_template']
    f.close()
    return errors

# checks input data type
def checkInputType(input) -> str:
    if input == '':
        return '' 
    if input.isdigit(): 
        return 'digits'
    elif input.replace(' ','').isalpha(): 
        return 'word_characters'
    else:
        return 'others'

# returns an error code 
def checkErrors(inputType, expectedType, inputLength, expectedLength, isMissing) -> str:
    checkType = (inputType == expectedType)
    checkLength = (inputLength != 0) and (inputLength <= expectedLength)
    if isMissing: 
        code = 'E05'
    elif checkType == False:
        code = 'E04' if checkLength == False else 'E02'
    else: 
        code = 'E03' if checkLength == False else 'E01'
    return code

# re-organize the input and definition
def getParsedData(filename) -> list:
    definition = getDefinitions()
    content = getContents(filename)
    parsedData = []
    for line in content:
        count = 0
        inputs = line.split('&')
        key = inputs.pop(0)
        numInputs = len(inputs)
        if key in definition.keys():
            for i in range(numInputs, len(definition[key])): 
                inputs.append('')
            for item in definition[key]:
                inputType = checkInputType(inputs[count])
                expectedType = definition[key][item]['data_type']
                inputLength = len(inputs[count])
                expectedLength = definition[key][item]['max_length']
                isMissing = numInputs <= count
                errorCode = checkErrors(inputType, expectedType, inputLength, expectedLength, isMissing)
                if inputLength == 0: 
                    inputLength = ''
                parsedData.append([key, item, inputType, expectedType, inputLength, expectedLength, errorCode])
                count += 1
    return parsedData

# print result data in a csv file
def printReport(data):
    header = ['Section', 'Sub-Section', 'Given DataType', 'Expected DataType', 'Given Length', 'Expected MaxLength', 'Error Code']
    with open(OUTPUT_FILES['REPORT'], 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in data:
            writer.writerow(row)
            
# returns summary string
def getSummary(data, errors) -> str:
    summary, prevKey = '', ''
    for row in data:
        key, code = row[0], row[-1]
        if prevKey != '' and prevKey != key:
            summary += '\n'
        errorInfo = errors[code].replace("LXY", row[1]).replace("LX", key)
        if code == 'E02' or code == 'E03':
            errorInfo = errorInfo.replace("{data_type}", row[3]).replace("{max_length}", str(row[5]))
        summary += errorInfo + '\n'
        prevKey = key
    return summary    

# print the summary in a text file
def printSummary(data, errors):
    with open(OUTPUT_FILES['SUMMARY'], 'w', encoding='UTF8') as f:
        summary = getSummary(data, errors)
        f.write(summary)
        f.close()
        
def main():
    if not os.path.exists(OUTPUT_FILES['PATH']):
        os.mkdir(OUTPUT_FILES) 
    data = getParsedData(INPUT_FILES['INPUT'])
    errors = getErrorCodes()
    printReport(data)
    printSummary(data, errors)
    print('Parsing completed. The parsed data are stored under the', OUTPUT_FILES['PATH'], 'folder')

if __name__ == "__main__":
    main()
