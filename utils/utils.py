import csv


def save_csv(data_list, path, header=None):
    if len(data_list) == 0:
        return

    if header is None:
        header = data_list[0].keys()

    with open(path, 'w+', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for data in data_list:
            row = []
            for h in header:
                row.append(data[h])
            writer.writerow(row)


def load_csv(path):
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        data_list = []

        for row in reader:
            if reader.line_num == 1:
                header = row
                continue

            data = {}
            for i, h in enumerate(header):
                data[h] = row[i]
            data_list.append(data)

        return data_list

def dictList2List(data_list, header):
    out_list = []
    for data in data_list:
        row = []
        for h in header:
            row.append(data[h])
        out_list.append(row)
    return out_list
