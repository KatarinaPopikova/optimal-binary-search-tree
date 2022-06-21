import numpy as np


def read_txt_and_split_data(path):
    keys = dict()
    dummy_keys = dict()
    frequency_count = 0
    with open(path) as file:
        line = file.readline()
        while line:
            splitted_line = line.split()
            frequency = int(splitted_line[0])
            if frequency > 50_000:
                keys[splitted_line[1]] = int(splitted_line[0])
            else:
                dummy_keys[splitted_line[1]] = int(splitted_line[0])
            frequency_count += frequency
            line = file.readline()
    return keys, dummy_keys, frequency_count


def sort_keys(keys):
    return {k: keys[k] for k in sorted(keys)}


def sort_keys_and_add_zero_element(keys):
    keys = sort_keys(keys)
    new_keys = {None: 0}
    new_keys.update(keys)
    return new_keys


def compute_probabilities(keys, dummy_keys, frequency_count):
    q = []
    for key in keys:
        keys[key] /= frequency_count

    i = 0
    keys_index = 1
    dummy_keys_q_sum = 0
    keys_list = list(keys.keys())
    dummies_list = list(dummy_keys.keys())
    while True:
        if i == len(dummy_keys):
            q.append(dummy_keys_q_sum / frequency_count)
            break

        if keys_index == len(keys_list) or dummies_list[i] < keys_list[keys_index]:
            dummy_keys_q_sum += dummy_keys[dummies_list[i]]
            i += 1
        else:
            keys_index += 1
            q.append(dummy_keys_q_sum / frequency_count)
            dummy_keys_q_sum = 0

    return keys, q


def manage_keys(keys, dummy_keys, frequency_count):
    dummy_keys = sort_keys(dummy_keys)
    keys = sort_keys_and_add_zero_element(keys)
    keys, q = compute_probabilities(keys, dummy_keys, frequency_count)
    p = list(keys.values())
    return keys, p, q


def array_filled_with_zeros(cols, rows):
    return [[0] * cols for _ in range(rows)]


def optimal_bst(p, q, n):
    e = array_filled_with_zeros(n, n + 1)
    w = array_filled_with_zeros(n, n + 1)
    root = array_filled_with_zeros(n, n)

    for i in range(1, n + 1):
        e[i][i - 1] = q[i - 1]
        w[i][i - 1] = q[i - 1]

    for l in range(1, n):
        for i in range(1, n - l + 1):
            j = l + i - 1
            e[i][j] = np.inf
            w[i][j] = w[i][j - 1] + p[j] + q[j]
            for r in range(i, j + 1):
                t = e[i][r - 1] + e[r + 1][j] + w[i][j]
                if t < e[i][j]:
                    e[i][j] = t
                    root[i][j] = r

    return root


def comparisons_count(search_word, keys, root):
    keys_list = list(keys.keys())
    root_index = root[1][-1]
    count = 1
    right = len(keys_list) - 1
    left = 1
    while keys_list[root_index] != search_word:
        print("compared word: " + keys_list[root_index])
        count += 1
        if keys_list[root_index] < search_word:
            print("--->")
            left = root_index + 1
            if left > right:
                return -1 * count
            root_index = root[left][right]
        elif keys_list[root_index] > search_word:
            print("<---")
            right = root_index - 1
            if left > right:
                return -1 * count
            root_index = root[left][right]

    return count


def main():
    while True:
        search_word = input("Write the word and click ENTER: ")
        keys, dummy_keys, frequency_count = read_txt_and_split_data('data/dictionary.txt')
        keys, p, q = manage_keys(keys, dummy_keys, frequency_count)
        root = optimal_bst(p, q, len(keys))
        comparisons = comparisons_count(search_word, keys, root)
        if comparisons < 0:
            print(
                f"Program made {abs(comparisons)} comparisons for the \"{search_word}\", but this word does not"
                f" belong to keys of our binary search tree. ")
        else:
            print(f"Program made {comparisons} comparisons for the \"{search_word}\".")


if __name__ == "__main__":
    main()
