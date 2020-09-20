def fifo(page_n, mem_array, counter):
    global logs
    for j in range(len(mem_array)):
        if mem_array[j] == 0:
            mem_array[j] = page_n
            logs.write(f'FIFO:   -> {page_n}; ')
            return mem_array, counter
        elif mem_array[j] == page_n:
            logs.write(f'FIFO:   !! {page_n}; ')
            return mem_array, counter
    logs.write(f'FIFO: {mem_array[0]} -> {page_n}; ')
    for j in range(len(mem_array) - 1):
        mem_array[j] = mem_array[j + 1]
    mem_array[len(mem_array) - 1] = page_n
    return mem_array, counter + 1


def lru(page_n, mem_array, counter):
    global logs
    for j in range(len(mem_array)):
        if mem_array[j] == 0:
            for it in range(j, 0, -1):
                mem_array[it] = mem_array[it - 1]
            mem_array[0] = page_n
            logs.write(f'LRU:   -> {page_n}; ')
            return mem_array, counter
        elif mem_array[j] == page_n:
            for it in range(j, 0, -1):
                mem_array[it] = mem_array[it - 1]
            mem_array[0] = page_n
            logs.write(f'LRU:   !! {page_n}; ')
            return mem_array, counter
    logs.write(f'LRU: {mem_array[len(mem_array) - 1]} -> {page_n}; ')
    for j in range(len(mem_array) - 1, 0, -1):
        mem_array[j] = mem_array[j - 1]
    mem_array[0] = page_n
    return mem_array, counter + 1


def opt(page_seq, page_index, mem_array, counter):
    global logs
    oracle = {}
    for j in range(len(mem_array)):
        if mem_array[j] == 0:
            mem_array[j] = page_seq[page_index]
            logs.write(f'OPT:   -> {page_seq[page_index]}; \n')
            return mem_array, counter
        elif mem_array[j] == page_seq[page_index]:
            logs.write(f'OPT:   !! {page_seq[page_index]}; \n')
            return mem_array, counter
        else:
            for it in range(page_index + 1, len(page_seq)):
                if page_seq[it] == mem_array[j]:
                    oracle[mem_array[j]] = it
                    break
            if mem_array[j] not in oracle:
                oracle[mem_array[j]] = len(page_seq)
    max_num = 0
    page_max = 0
    for page_n in oracle:
        if oracle[page_n] > max_num:
            max_num = oracle[page_n]
            page_max = page_n
    for j in range(len(mem_array)):
        if mem_array[j] == page_max:
            logs.write(f'OPT: {mem_array[j]} -> {page_seq[page_index]}; \n')
            mem_array[j] = page_seq[page_index]
            break
    return mem_array, counter + 1


inputf = open('virtualmem_in.txt', 'r')
proc_size = int(inputf.readline().rstrip())
mem_size = int(inputf.readline().rstrip())
logs = open('virtualmem_logs.txt', 'w')
logs.write(f"""Input:
{str(proc_size)}
{str(mem_size)}
""")

memory_FIFO = [0] * mem_size
memory_LRU = [0] * mem_size
memory_OPT = [0] * mem_size
counter_FIFO = 0
counter_LRU = 0
counter_OPT = 0
page_sequence = inputf.readline().rstrip().split()
inputf.close()
for i in range(len(page_sequence)):
    logs.write(page_sequence[i] + ' ')
logs.write('\n\nReplacements made:\n')

for i in range(len(page_sequence)):
    page_num = page_sequence[i]
    memory_FIFO, counter_FIFO = fifo(page_num, memory_FIFO, counter_FIFO)
    memory_LRU, counter_LRU = lru(page_num, memory_LRU, counter_LRU)
    memory_OPT, counter_OPT = opt(page_sequence, i, memory_OPT, counter_OPT)

logs.write(f"""
Output:
FIFO: {counter_FIFO}
LRU: {counter_LRU}
OPT: {counter_OPT}
""")
logs.close()

print(f"""
The FIFO algorithm made {counter_FIFO} page replacements
The LRU algorithm made {counter_LRU} page replacements
The OPT algorithm made {counter_OPT} page replacements
""")
if counter_FIFO > counter_LRU:
    print('The LRU algorithm outdid the FIFO algorithm')
elif counter_FIFO < counter_LRU:
    print('The FIFO algorithm outdid the LRU algorithm')
else:
    print('Friendship wins!!! FIFO and LRU algorithms got the same score!')
