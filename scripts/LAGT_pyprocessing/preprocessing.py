import numpy
import pandas

### SCRIPT PARAMETERS ###
input_dir = "./preprocessing_input/"
output_dir = "./preprocessing_output/"
exam_csv = "exam.csv"
answer_csv = "answer.csv"
weight_csv = "weight.csv"
known_threshold = 0.60
missing_thresholds = [0.00, 0.50, 1.00]

### LOAD DATA ###
itemXstIn = pandas.read_csv(f"{input_dir}{exam_csv}", index_col=0)
itemXans = pandas.read_csv(f"{input_dir}{answer_csv}", index_col=0)
itemXnode = pandas.read_csv(f"{input_dir}{weight_csv}", index_col=0)
print(f"Loaded shapes: {[(exam_csv, itemXstIn.shape), (answer_csv, itemXans.shape), (weight_csv, itemXnode.shape)]}")

### CLEAN DATA ###
itemsNullAnswer = itemXans.index[itemXans['correct'].isnull()]  # find all null answers
for df in [itemXstIn, itemXans, itemXnode]: df.drop(index=itemsNullAnswer, inplace=True)  # remove items with null answers for itemXstIn, itemXans, itemXnode
itemXnode.drop(columns=['conti'], inplace=True)  # remove conti column for itemXnode
itemXnode.replace(float('NaN'), 0, inplace=True)  # replace missing node weights by 0
print(f"Number of null answers: {len(itemsNullAnswer)}\nShapes after cleaning: {[(exam_csv, itemXstIn.shape), (answer_csv, itemXans.shape), (weight_csv, itemXnode.shape)]}")

def percentage_converter(column):
    conditionChoiceList = [
        (column.isnull(), None),
        (column >= known_threshold, "Known"),
        (column < known_threshold, "NotKnown")]
    return numpy.select(*zip(*conditionChoiceList))

def generate_dataset(missing_threshold):
    ### FILTER EXAMS BY MISSING ANSWERS THRESHOLD ###
    itemXstInFiltered = itemXstIn.dropna(thresh=int(itemXstIn.shape[0] * missing_threshold), axis='columns')
    print(f"Shape after filter (threshold={missing_threshold}) by missing answers: {itemXstInFiltered.shape}")
    ### CALCULATE PERCENTAGES ###
    tallyNoMissing = itemXstInFiltered.apply(lambda studentInput: (studentInput == itemXans['correct']).astype(int)).transpose().dot(itemXnode)
    totalScore = itemXnode.sum()
    percentagesNoMissing = tallyNoMissing / totalScore
    percentagesWithMissing = tallyNoMissing / (totalScore - itemXstInFiltered.isnull().astype(int).transpose().dot(itemXnode))
    percentagesNoMissing.to_csv(f"{output_dir}percentageNoMissing_threshold-{missing_threshold}.csv")
    percentagesWithMissing.to_csv(f"{output_dir}percentageWithMissing_threshold-{missing_threshold}.csv")
    ### GENERATE DATASETS ###
    datasetNoMissing = percentagesNoMissing.apply(percentage_converter)
    datasetWithMissing = percentagesWithMissing.apply(percentage_converter)
    datasetNoMissing.to_csv(f"{output_dir}datasetNoMissing_threshold-{missing_threshold}.csv")
    datasetWithMissing.to_csv(f"{output_dir}datasetWithMissing_threshold-{missing_threshold}.csv")
    print(f"Written files {output_dir}[percentageNoMissing|percentageWithMissing|datasetNoMissing|datasetWithMissing]_threshold-{missing_threshold}.csv")

for missing_threshold in missing_thresholds: generate_dataset(missing_threshold)
