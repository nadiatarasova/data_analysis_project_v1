import statistics

# Helper functions
def most_common(row):
    return max(set(row), key=row.count)

def get_seconds(row):
    return row.second

def sort_dt(row):
    return sorted(row)

## len = length
def get_td_mean(row):
    td = 0
    if len(row) > 2:
        for i in range (0,len(row)-1):
            td += row[i+1]-row[i]
        return td/(len(row)-1)
    else:
        return 0

def get_td_sd(row):
    sd = 0
    new_list = []
    if len(row) > 2:
        for i in range (0,len(row)-1):
            new_list.append(row[i+1]-row[i])
        return statistics.stdev(new_list)
    else:
        return 0


# Find the number of sensor hit by the attacker
def rem_dups(array):
    myset = set(array)
    return len(list(myset))

# helper function for evaluating predictions
def check(row):
    if row['danger'] == row['predictions']:
        return 'Correct'
    else:
        return 'Incorrect'


