# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import src.MovieSearch as ms


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    sample_data = ms.load_sample_data()
    bucket = ms.connect_to_capella()

    ms.insert_into_capella(sample_data, bucket)
    ms.search_movie(bucket)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
