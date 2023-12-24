import csv
import json

CENSOR_INDEXES = [6, 7, 9, 11]


def censor_feedback(columns: list[str]) -> list[str]:
    ls = []
    for i in range(len(columns)):
        if i not in CENSOR_INDEXES:
            ls.append(columns[i])
    return ls


def get_filename(username: str, classlist_map: dict[str, list[str]]) -> str:
    student_info = classlist_map[username]
    student_id = student_info[2].split("@")[0].upper()
    return f"{student_info[0]}_{student_info[1]}_{student_id}_feedback"


with open('reference/tempread.csv', newline='') as csvfile, \
        open('reference/combined_classlist.json') as classlist_file:
    reader = csv.reader(csvfile)
    classlist: list[list[str]] = json.loads(classlist_file.read())
    classlist_map = {}
    for student in classlist:
        classlist_map[student[2]] = student

    headers = []
    feedback = []
    username = ''
    row_count = 0
    for row in reader:
        if row_count == 0:
            headers = censor_feedback(row)
            row_count += 1
            continue
        if row_count == 1:
            username = row[0]
            row_count += 1

        if row[0] != username:
            # flush to disk
            filename = get_filename(username, classlist_map)
            with open(f'reference/feedback/{filename}.csv', 'w', newline='') as feedback_file:
                feedback_writer = csv.writer(feedback_file)
                feedback_writer.writerow(headers)
                feedback_writer.writerows(feedback)
            # start window at next person
            username = row[0]
            feedback = []
        feedback.append(censor_feedback(row))
