from get_student_data import get_student_data
from get_student_grades import login_and_get_subjects
from helpers import gpa_scale, get_grade, create_folder
from bs4 import BeautifulSoup
import json


def calculate_total(html_path, stud_name, ob_grade):
    with open(html_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "lxml")

    data = {}
    grades = []
    total_score = 0.0
    hours = 0
    points = 0.0

    rows = soup.find_all("tr")
    for row in rows[1:]:
        cols = row.find_all("td")
        if len(cols) < 9:
            continue

        course_code = cols[1].get_text(strip=True)
        if not course_code or course_code == 'MBS001' or not cols[8].get_text(strip=True):
            continue

        course_data = {
            "وصف المقرر": cols[2].get_text(strip=True),
            "عدد الساعات المعتمدة": float(cols[3].get_text(strip=True)),
            "الدرجة": cols[6].get_text(strip=True),
            "التقدير": cols[7].get_text(strip=True),
            "نقاط": cols[8].get_text(strip=True)
        }

        try:
            total_score += float(course_data["الدرجة"])
            hours += float(course_data["عدد الساعات المعتمدة"])
            grades.append(float(course_data['الدرجة']))
            points += float(course_data['نقاط']) * float(course_data["عدد الساعات المعتمدة"])
        except ValueError:
            pass

        data[course_code] = course_data
    
    #######################
    if len(grades) < 48:
        ob_score = 0
        try: 
            ob_score = float(ob_grade)
            ob_grade = get_grade(ob_score)
            points += gpa_scale[ob_grade]['points'] * 2
            total_score += ob_score
        except ValueError:
            points += gpa_scale[ob_grade]['points'] * 2
            ob_score = gpa_scale[ob_grade]['score']
            total_score += ob_score

        ob = {
            "وصف المقرر":  "سلوك تنظيمي",
            "عدد الساعات المعتمدة": 2.0,
            "الدرجة": f"{ob_score:.2f}",
            "التقدير": ob_grade,
            "نقاط": f"{gpa_scale[ob_grade]['points']:.3f}"
        }
        hours+=2
        grades.append(ob_score)
        data['HM121'] = ob
    ########################

    gpa = float(points/hours)

    json_file = f'json/{stud_name}.json'

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    if float(total_score) == int(total_score):
        total_score = int(total_score)

    return data, total_score, grades, hours, gpa


def hier(stud_nid, ob_v):

    create_folder('html')
    create_folder('json')

    stud_data = get_student_data(stud_nid)

    if stud_data:
        keys = list(stud_data.keys())

        stud_code = stud_data[keys[1]]
        stud_name = stud_data[keys[2]]

        results = login_and_get_subjects(stud_code, stud_nid, stud_name) 
        
        if type(results) is tuple:
            html_path, img = results

            data, total_score, grades, hours, gpa = calculate_total(html_path, stud_name, ob_v)
            return len(grades), int(hours), gpa, total_score, stud_name, img
            # print(f'Num of Courses: {len(grades)+1}')
            # print(f"Num of Hours: {hours+2}")
            # print(f"CGPA: {gpa}")
            # print(f"Overall Score: {total}")
        return results