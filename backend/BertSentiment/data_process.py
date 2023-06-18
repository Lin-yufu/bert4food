import random


def create_dataset():
    #提取前8000个数据作为全部数据
    input_file = "food.txt"
    output_file = "data.txt"
    lines_to_extract = 8000

    with open(input_file, "r",encoding='utf-8') as file:
        lines = file.readlines()

    modified_lines = []
    for line in lines:
        modified_line = line.replace(",", "\t", 1)
        modified_lines.append(modified_line)

    extracted_lines = modified_lines[:lines_to_extract]

    with open(output_file, "w",encoding='utf-8') as file:
        file.writelines(extracted_lines)
def divide_dataset():
    #数据集划分
    input_file = "data.txt"
    train_file = "train.txt"
    eval_file = "dev.txt"
    test_file = "test.txt"
    positive_examples = 4000
    negative_examples = 4000
    train_examples = 3500
    eval_examples = 250
    test_examples = 250

    with open(input_file, "r",encoding='utf-8') as file:
        lines = file.readlines()

    positive_lines = lines[:positive_examples]
    negative_lines = lines[positive_examples:positive_examples + negative_examples]

    train_positive = positive_lines[:train_examples]
    train_negative = negative_lines[:train_examples]
    eval_positive = positive_lines[train_examples:train_examples + eval_examples]
    eval_negative = negative_lines[train_examples:train_examples + eval_examples]
    test_positive = positive_lines[train_examples + eval_examples:train_examples + eval_examples + test_examples]
    test_negative = negative_lines[train_examples + eval_examples:train_examples + eval_examples + test_examples]

    train_lines = train_positive + train_negative
    eval_lines = eval_positive + eval_negative
    test_lines = test_positive + test_negative

    random.shuffle(train_lines)
    random.shuffle(eval_lines)
    random.shuffle(test_lines)

    with open(train_file, "w",encoding='utf-8') as file:
        file.writelines(train_lines)

    with open(eval_file, "w",encoding='utf-8') as file:
        file.writelines(eval_lines)

    with open(test_file, "w",encoding='utf-8') as file:
        file.writelines(test_lines)

if __name__=="__main__":
    create_dataset()
    divide_dataset()