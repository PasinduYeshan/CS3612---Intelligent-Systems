import random

def write_random_input_data1(f, possible_values):
    for i in range(3):
        for j in range(3):
            index = random.randint(0, len(possible_values) - 1)
            f.write(f"{possible_values[index]} ")
            del possible_values[index]
        f.write("\n")


def write_random_input_data2(f, possible_values):
    for i in range(3):
        for j in range(3):
            index = random.randint(0, len(possible_values) - 1)
            f.write(f"{possible_values[index]} ")
            del possible_values[index]
        f.write("\n")


def main():
    for i in range(0, 100):
        possible_values1 = ['1', '2', '3', '4', '5', '6', '7', '-', '-']
        random.seed(i + 29)
        if (i % 2 == 1):
            with open(f"./goals/{i}.txt", "w") as f:
                write_random_input_data1(f, possible_values1)
        else:
            with open(f"./inputs/{i + 1}.txt", "w") as f:
                write_random_input_data1(f, possible_values1)

    for i in range(1, 101):
        # possible_values2 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '-', '-']
        possible_values2 = ['1', '2', '3', '4', '5', '6', '7', '-', '-']
        random.seed(i + 29)
        if i % 2 == 0:
            with open(f"./goals/{i}.txt", "w") as f:
                write_random_input_data2(f, possible_values2)
        else:
            with open(f"./inputs/{i + 1}.txt", "w") as f:
                write_random_input_data2(f, possible_values2)


if __name__ == '__main__':
    main()