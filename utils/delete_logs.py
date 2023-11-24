import argparse
from log_utils import delete_all_logs, delete_logs_older_than_days

if __name__ == "__main__":
    logpath = "logs/"
    parser = argparse.ArgumentParser(description="Delete log files")
    parser.add_argument("--days", type=int, default=None, required=False, help="Delete logs older than the specified number of days (optional)")
    args = parser.parse_args()

    if args.days and args.days > 0:
            delete_logs_older_than_days(logpath, args.days)
    else:
        # If no argument provided, delete all logs
        delete_all_logs(logpath)