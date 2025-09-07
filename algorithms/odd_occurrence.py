def find_it(seq):
    count_dict = {}
    for i in seq:
        count_dict[i] = count_dict.get(i, 0) + 1
    for key, value in count_dict.items():
        if value % 2 == 1:
            return key

example = [20,1,1,2,2,3,3,5,5,4,20,4,5]
print(find_it(example))  # expected: 5