import sys
from glob import glob


def split_tests(number_of_files, CI_NODE_TOTAL, CI_NODE_INDEX, test_files_list):
    test_files_sublist = []

    for file_index in range(number_of_files):
        file_number = file_index % CI_NODE_TOTAL
        if file_number == CI_NODE_INDEX:
            test_files_sublist.append(test_files_list[file_index])

    tests_to_run_string = ' '.join(test_files_sublist)

    return tests_to_run_string


if __name__ == '__main__':
    CI_NODE_TOTAL, CI_NODE_INDEX = int(sys.argv[1]), int(sys.argv[2])
    test_files_list = glob('tests/**/*.yaml', recursive=True) + glob('tests/**/*.yml', recursive=True)
    number_of_files = len(test_files_list)
    sys.stdout.write(split_tests(number_of_files, CI_NODE_TOTAL, CI_NODE_INDEX, test_files_list))
