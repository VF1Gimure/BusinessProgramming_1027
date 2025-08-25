import sys

if len(sys.argv) == 4:
    print("Your words:", sys.argv[1], sys.argv[2], sys.argv[3])
else:
    print("Give 3 words!")


# run this on terminal: python sample_no_main.py hello world today