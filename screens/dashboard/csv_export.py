import pandas


def export_csv(app, file):
    students = app.database.execute_query("SELECT * FROM students")
    if not students or not isinstance(students, list):
        return False
    rows = []
    for student in students:
        years = app.database.execute_query(
            "SELECT * FROM academic_year WHERE student = ?", (student[0],)
        )
        if not years or not isinstance(years, list):
            app.logger.error("CSV Export: Student has no academic years")
            continue
        for year in years:
            row = {
                "id": student[0],
                "f_name": student[1],
                "m_name": student[2],
                "l_name": student[3],
                "std": year[2],
                "div": year[3],
                "roll_no": year[4],
                "year": year[5],
            }
            marks = app.database.execute_query(
                "SELECT * FROM marks WHERE academic_year = ?", (year[0],)
            )
            if not years or not isinstance(years, list):
                app.logger.error("CSV Export: Student has no marks in an year")
                continue
            for exam_marks in marks:
                exam = exam_marks[2]
                row.update(
                    {
                        f"{exam}-math": exam_marks[3],
                        f"{exam}-eng": exam_marks[4],
                        f"{exam}-phy": exam_marks[5],
                        f"{exam}-chem": exam_marks[6],
                        f"{exam}-ip": exam_marks[7],
                    }
                )
            rows.append(row)
    if not rows:
        return False
    df = pandas.DataFrame(rows)
    df.to_csv(file, index=False)
    return True
