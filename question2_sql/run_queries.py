
"""Run the three SQL queries against the public Rfam database."""

from pathlib import Path

import pymysql

SQL_FILE = Path(__file__).with_name("answers.sql")


def load_queries():
    """Load SQL statements while ignoring SQL comment lines."""
    lines = [
        line
        for line in SQL_FILE.read_text(encoding="utf-8").splitlines()
        if not line.lstrip().startswith("--")
    ]

    queries = [
        query.strip()
        for query in "\n".join(lines).split(";")
        if query.strip()
    ]

    return queries


def main():
    queries = load_queries()

    if len(queries) != 3:
        print(f"Expected 3 SQL queries, found {len(queries)}.")
        return

    connection = None

    try:
        connection = pymysql.connect(
            host="mysql-rfam-public.ebi.ac.uk",
            port=4497,
            user="rfamro",
            database="Rfam",
            connect_timeout=20,
            read_timeout=120,
            cursorclass=pymysql.cursors.DictCursor,
        )

        print("Connected to Rfam.")

        for number, query in enumerate(queries, start=1):
            print(f"\n{'=' * 10} QUERY {number} {'=' * 10}")

            try:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    rows = cursor.fetchall()

                for row in rows:
                    print(row)

                print(f"Rows returned: {len(rows)}")

            except pymysql.MySQLError as error:
                print(f"Query {number} failed: {error}")

                if number == 3:
                    print(
                        "Query 3 could not be verified against the "
                        "live server. See question2_sql/NOTES.md."
                    )
                    break

                return

    except pymysql.MySQLError as error:
        print(f"Database connection failed: {error}")

    finally:
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    main()
