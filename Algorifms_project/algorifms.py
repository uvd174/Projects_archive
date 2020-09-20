def mark_replacement(string, mark_rep_arr, arr_size):  # Функция, однократно применяющая схему Марковских подстановок
    global logs                                        # mark_rep_arr размера arr_size к строке string
    is_not_over = False
    if string == '':
        string = ' '
    logs.write(f'{string} -> ')
    for j in range(arr_size):
        if string.find(mark_rep_arr[j][0]) != -1:
            is_not_over = True
            string = string.replace(mark_rep_arr[j][0], mark_rep_arr[j][2], 1)
            if mark_rep_arr[j][1] == '->.':
                is_not_over = False
            break
    logs.write(string + '\n')
    return is_not_over, string


def read_rep_array(input_f):                                  # Функция, считывающая и форматирующая массив Марковских
    rep_arr = []                                              # подстановок из файла input_f
    sch_size = int(input_f.readline().rstrip())
    for i in range(sch_size):
        rep_arr.append(input_f.readline().rstrip().split())
        if rep_arr[i][0] == '->' or rep_arr[i][0] == '->.':
            if len(rep_arr[i]) == 1:
                rep_arr[i].append(rep_arr[i][0])
                rep_arr[i][0] = ''
                rep_arr[i].append('')
            else:
                rep_arr[i].append(rep_arr[i][1])
                rep_arr[i][1] = rep_arr[i][0]
                rep_arr[i][0] = ''
        elif len(rep_arr[i]) == 2:
            rep_arr[i].append('')
    input_str = input_f.readline().rstrip()
    return rep_arr, sch_size, input_str


ITERATIONS_LIMIT = 1000000
inputf = open('algorifms_in.txt', 'r')
rep_array, scheme_size, in_str = read_rep_array(inputf)
inputf.close()
logs = open('algorifms_logs.txt', 'w')
logs.write(f'Input:\n{in_str}\n\nReplacements made:\n')
one_more_iteration = True
iterations_counter = 0
while one_more_iteration:
    iterations_counter += 1
    one_more_iteration, in_str = mark_replacement(in_str, rep_array, scheme_size)
    if iterations_counter == ITERATIONS_LIMIT:
        break

if iterations_counter == ITERATIONS_LIMIT:
    logs.write('\nThe program ran into a problem\n')
    print(f"""
Unfortunately, the program either entered an infinite loop
or just got tired after completing 1000000 iterations
Anyway, that's the output: {in_str}
""")
else:
    print(in_str)
logs.write(f'\nOutput:\n{in_str}\n')

if in_str == '' or in_str == ' ':
    print('(Yes, it has just printed an empty line)')
    logs.write('(Yes, it has just printed an empty line)\n')
logs.close()
