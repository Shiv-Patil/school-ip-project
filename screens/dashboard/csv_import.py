from pandas_schema import Column, Schema
from pandas_schema.validation import InRangeValidation
import pandas
import numpy
from kivymd.app import MDApp

app = MDApp.get_running_app()

schema = Schema(
    [
        Column("id"),
        Column("f_name"),
        Column("m_name", allow_empty=True),
        Column("l_name", allow_empty=True),
        Column("std", [InRangeValidation(1, 13)]),
        Column("div", allow_empty=True),
        Column("roll_no"),
        Column("year"),
        Column("unit1-math", allow_empty=True),
        Column("unit1-eng", allow_empty=True),
        Column("unit1-phy", allow_empty=True),
        Column("unit1-chem", allow_empty=True),
        Column("unit1-ip", allow_empty=True),
        Column("term1-math", allow_empty=True),
        Column("term1-eng", allow_empty=True),
        Column("term1-phy", allow_empty=True),
        Column("term1-chem", allow_empty=True),
        Column("term1-ip", allow_empty=True),
        Column("unit2-math", allow_empty=True),
        Column("unit2-eng", allow_empty=True),
        Column("unit2-phy", allow_empty=True),
        Column("unit2-chem", allow_empty=True),
        Column("unit2-ip", allow_empty=True),
        Column("term2-math", allow_empty=True),
        Column("term2-eng", allow_empty=True),
        Column("term2-phy", allow_empty=True),
        Column("term2-chem", allow_empty=True),
        Column("term2-ip", allow_empty=True),
    ]
)


def _read_csv_and_validate(filepath):
    df = pandas.read_csv(filepath)
    validated = schema.validate(df)
    if len(validated) == 0:
        return df
    else:
        for error in validated:
            app.logger.error("CSV validator: " + str(error))
        return False


def import_csv_in_database(csv, set_progress):
    df = _read_csv_and_validate(csv)
    if df is False:
        return False
    df.drop_duplicates(inplace=True)
    total_rows = len(df)
    rows_added = 0
    unique_added = numpy.array([])
    for _, data in df.iterrows():
        id = data.at["id"]
        if not numpy.isin(id, unique_added):
            unique_added = numpy.append(unique_added, id)
            app.database.execute_query(
                "INSERT OR REPLACE INTO students VALUES (?, ?, ?, ?)",
                data.loc[:"l_name"],
            )
        app.database.execute_query(
            "INSERT INTO academic_year (student, class, division, rollno, year_start) VALUES (?, ?, ?, ?, ?)",
            data.loc[["id", "std", "div", "roll_no", "year"]],
        )
        academic_year_id = app.database.execute_query(
            "SELECT id from academic_year WHERE student=? AND year_start=?",
            (id, data.at["year"]),
        )[0][0]
        for exam in ["unit1", "unit2", "term1", "term2"]:
            app.database.execute_query(
                "INSERT INTO marks (academic_year, exam, mathematics, english, phyiscs, chemistry, informatics_practices) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (academic_year_id,)
                + (exam,)
                + tuple(data.loc[f"{exam}-math":f"{exam}-ip"]),
            )
        rows_added += 1
        set_progress(round((rows_added / total_rows) * 100))
    return True
