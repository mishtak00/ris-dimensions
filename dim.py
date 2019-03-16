from q import *
import csv

header = initialize_session()


with open("faculty.csv", mode='r') as fac, open("out.csv", mode='w', newline='') as out:
    reader = csv.reader(fac, delimiter=',')
    writer = csv.writer(out, delimiter=',')
    line = 0

    for row in reader:
        correct_row = []
        full_name = row[5]
        department = row[2]
        employee_id = row[0]
        print('line : {}\n'.format(line))

        if (line == 0):
            correct_row = ['Last Name', 'First Name', 'Dimensions ID', 'Current Affiliation', 'Department', 'Employee ID']
        else:
            last_first = full_name.split(',')

            correct_row.append(last_first[0])
            correct_row.append(last_first[1])

            id_affiliation = query_author(full_name, header)

            correct_row.append(id_affiliation[0])
            correct_row.append(id_affiliation[1])

            correct_row.append(department)
            correct_row.append(employee_id)

        writer.writerow(correct_row)

        # if (line == 100):
        #     break

        time.sleep(.5)
        line += 1

    fac.close()
    out.close()
