from re import DEBUG
from ACIP_logs_monitor import create_app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
