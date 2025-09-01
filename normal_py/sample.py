import sys


def print_words():
    if len(sys.argv) == 4:
        print("Your words:", sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Give 3 words!")


if __name__ == "__main__":
    # sys.argv = ["sample.py", "apple", "banana", "cherry"]
    print_words()
    # run on terminal : python sample_no_main.py hello world today
