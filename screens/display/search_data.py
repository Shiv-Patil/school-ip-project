def get_rows(_num_results, _std, _id_name, app):
    query = "SELECT * FROM students WHERE"
    values = []
    try:
        id = int(_id_name)
        if id > 0 and id <= 1069420:
            query += " id = ?"
            values.append(id)
        else:
            return app.toast("Invalid ID value (too big)")
    except ValueError:
        names = _id_name.split()
        for col, value in zip(("first_name", "middle_name", "last_name"), names):
            if query[-1] == "?":
                query += " AND"
            query += f" {col} LIKE ?"
            values.append(value)
    query += f" LIMIT {_num_results}"

    students = app.database.execute_query(query, values)
    if not isinstance(students, list) or len(students) == 0:
        return app.toast("No data matching search to display")

    final_rows = []
    for id, fname, mname, lname in students:
        query = (
            "SELECT class, division, year_start FROM academic_year WHERE student = ?"
        )
        values = (id,)
        if len(_std) > 0:
            query += " AND class = ?"
            values = (id, _std)
        query += " LIMIT 14"
        academic_year = app.database.execute_query(query, values)
        if not isinstance(academic_year, list):
            return app.toast("No data matching search to display")
        for std, division, year_start in academic_year:
            final_rows.append(
                (
                    id,
                    fname,
                    mname,
                    lname,
                    std,
                    division,
                    f"{year_start}-{str(year_start+1)[-2:]}",
                )
            )

    return final_rows[:_num_results]
