import subprocess


def export_postgres_db(db_name: str, user: str = "postgres") -> bytes:
    process = subprocess.Popen(
        ["pg_dump", "-U", user, db_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout, stderr = process.communicate()

    if process.returncode != 0:
        raise Exception(stderr.decode())

    return stdout
