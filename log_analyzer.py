import re
import os
from collections import Counter
from datetime import datetime

# ============================================================
# SERVER LOG ANALYZER
# Single-file Python Project
# ============================================================

APP_NAME = "SERVER LOG ANALYZER"
VERSION = "1.0"


# ------------------------------------------------------------
# Display Utilities
# ------------------------------------------------------------

def line(char="=", length=65):
    print(char * length)


def header():
    print()
    line()
    print(f"{APP_NAME:^65}")
    print(f"{'Version ' + VERSION:^65}")
    line()


def section(title):
    print()
    print(title)
    print("-" * 65)


# ------------------------------------------------------------
# Log Analyzer Class
# ------------------------------------------------------------

class LogAnalyzer:

    def __init__(self, filename):
        self.filename = filename
        self.logs = []

        self.levels = Counter()
        self.ip_addresses = Counter()
        self.status_codes = Counter()
        self.errors = Counter()
        self.failed_logins = Counter()

        self.total_requests = 0
        self.total_lines = 0

    # --------------------------------------------------------
    # Load Log File
    # --------------------------------------------------------

    def load_file(self):

        if not os.path.exists(self.filename):
            print(f"\n[ERROR] File not found: {self.filename}")
            return False

        try:
            with open(self.filename, "r", encoding="utf-8") as file:

                for line_text in file:
                    self.total_lines += 1

                    line_text = line_text.strip()

                    if line_text:
                        self.logs.append(line_text)

            print(f"\n[OK] Loaded {len(self.logs)} log entries.")
            return True

        except PermissionError:
            print("[ERROR] Permission denied.")
            return False

        except Exception as error:
            print(f"[ERROR] Could not read file: {error}")
            return False

    # --------------------------------------------------------
    # Analyze Logs
    # --------------------------------------------------------

    def analyze(self):

        for log in self.logs:

            # Count log levels
            level_match = re.search(
                r"\b(INFO|WARNING|WARN|ERROR|DEBUG|CRITICAL)\b",
                log,
                re.IGNORECASE
            )

            if level_match:
                level = level_match.group(1).upper()

                if level == "WARN":
                    level = "WARNING"

                self.levels[level] += 1

            # Extract IP addresses
            ip_matches = re.findall(
                r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
                log
            )

            for ip in ip_matches:
                self.ip_addresses[ip] += 1

            # Extract HTTP status codes
            status_match = re.search(
                r"\b([1-5]\d{2})\b",
                log
            )

            if status_match:
                status = status_match.group(1)
                self.status_codes[status] += 1
                self.total_requests += 1

            # Detect error messages
            if re.search(
                r"\b(ERROR|CRITICAL|EXCEPTION|FAILED)\b",
                log,
                re.IGNORECASE
            ):

                cleaned_error = self.extract_error(log)

                if cleaned_error:
                    self.errors[cleaned_error] += 1

            # Detect failed login attempts
            if re.search(
                r"(failed login|login failed|authentication failed|invalid password)",
                log,
                re.IGNORECASE
            ):

                ip_match = re.search(
                    r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
                    log
                )

                if ip_match:
                    self.failed_logins[ip_match.group()] += 1
                else:
                    self.failed_logins["Unknown IP"] += 1

    # --------------------------------------------------------
    # Extract Error Description
    # --------------------------------------------------------

    def extract_error(self, log):

        patterns = [
            r"(?:ERROR|CRITICAL|EXCEPTION)\s*[:\-]\s*(.*)",
            r"(?:error|exception|failed)\s*[:\-]\s*(.*)"
        ]

        for pattern in patterns:

            match = re.search(pattern, log, re.IGNORECASE)

            if match:

                message = match.group(1).strip()

                if len(message) > 70:
                    message = message[:70] + "..."

                return message

        return "Unknown Error"

    # --------------------------------------------------------
    # Display Summary
    # --------------------------------------------------------

    def show_summary(self):

        section("GENERAL SUMMARY")

        print(f"Log File              : {self.filename}")
        print(f"Total Lines           : {self.total_lines}")
        print(f"Valid Log Entries     : {len(self.logs)}")
        print(f"Total Requests        : {self.total_requests}")

        section("LOG LEVELS")

        levels = [
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL"
        ]

        for level in levels:
            print(f"{level:<20}: {self.levels.get(level, 0)}")

    # --------------------------------------------------------
    # Display HTTP Statistics
    # --------------------------------------------------------

    def show_status_codes(self):

        section("HTTP STATUS CODES")

        if not self.status_codes:
            print("No HTTP status codes detected.")
            return

        status_names = {
            "200": "OK",
            "201": "Created",
            "204": "No Content",
            "301": "Moved Permanently",
            "302": "Found",
            "400": "Bad Request",
            "401": "Unauthorized",
            "403": "Forbidden",
            "404": "Not Found",
            "500": "Internal Server Error",
            "502": "Bad Gateway",
            "503": "Service Unavailable"
        }

        for status, count in self.status_codes.most_common():

            name = status_names.get(status, "Unknown")

            print(
                f"{status:<8} {name:<30} {count} requests"
            )

    # --------------------------------------------------------
    # Display IP Statistics
    # --------------------------------------------------------

    def show_ips(self):

        section("TOP IP ADDRESSES")

        if not self.ip_addresses:
            print("No IP addresses detected.")
            return

        for ip, count in self.ip_addresses.most_common(10):

            print(
                f"{ip:<25} {count:>6} requests"
            )

    # --------------------------------------------------------
    # Security Analysis
    # --------------------------------------------------------

    def show_security(self):

        section("SECURITY ANALYSIS")

        total_failed = sum(self.failed_logins.values())

        print(
            f"Failed Login Attempts : {total_failed}"
        )

        print(
            f"Unique IP Addresses   : {len(self.ip_addresses)}"
        )

        suspicious = [
            ip for ip, count in self.failed_logins.items()
            if count >= 3
        ]

        print(
            f"Suspicious IPs        : {len(suspicious)}"
        )

        if suspicious:

            print("\nPotentially Suspicious IPs:")

            for ip in suspicious:
                print(
                    f"  ⚠ {ip} "
                    f"({self.failed_logins[ip]} failed attempts)"
                )

    # --------------------------------------------------------
    # Display Top Errors
    # --------------------------------------------------------

    def show_errors(self):

        section("TOP ERRORS")

        if not self.errors:
            print("No errors detected.")
            return

        for error, count in self.errors.most_common(10):

            print(
                f"{count:>4} occurrences  |  {error}"
            )

    # --------------------------------------------------------
    # Generate Report
    # --------------------------------------------------------

    def generate_report(self):

        report_file = "log_analysis_report.txt"

        try:

            with open(
                report_file,
                "w",
                encoding="utf-8"
            ) as report:

                report.write("=" * 65 + "\n")
                report.write(
                    f"{APP_NAME:^65}\n"
                )
                report.write("=" * 65 + "\n\n")

                report.write("GENERAL SUMMARY\n")
                report.write("-" * 65 + "\n")

                report.write(
                    f"File: {self.filename}\n"
                )

                report.write(
                    f"Total Lines: {self.total_lines}\n"
                )

                report.write(
                    f"Log Entries: {len(self.logs)}\n"
                )

                report.write(
                    f"Total Requests: {self.total_requests}\n\n"
                )

                report.write("LOG LEVELS\n")
                report.write("-" * 65 + "\n")

                for level, count in self.levels.most_common():

                    report.write(
                        f"{level}: {count}\n"
                    )

                report.write("\nHTTP STATUS CODES\n")
                report.write("-" * 65 + "\n")

                for status, count in self.status_codes.most_common():

                    report.write(
                        f"{status}: {count}\n"
                    )

                report.write("\nTOP IP ADDRESSES\n")
                report.write("-" * 65 + "\n")

                for ip, count in self.ip_addresses.most_common(10):

                    report.write(
                        f"{ip}: {count} requests\n"
                    )

                report.write("\nSECURITY ANALYSIS\n")
                report.write("-" * 65 + "\n")

                report.write(
                    f"Failed Login Attempts: "
                    f"{sum(self.failed_logins.values())}\n"
                )

                report.write(
                    f"Unique IP Addresses: "
                    f"{len(self.ip_addresses)}\n"
                )

                report.write("\nTOP ERRORS\n")
                report.write("-" * 65 + "\n")

                for error, count in self.errors.most_common(10):

                    report.write(
                        f"{count} occurrences | {error}\n"
                    )

                report.write(
                    "\nGenerated: "
                    + datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    + "\n"
                )

            print(
                f"\n[OK] Report generated: {report_file}"
            )

        except Exception as error:

            print(
                f"\n[ERROR] Could not generate report: {error}"
            )


# ------------------------------------------------------------
# Create Sample Log
# ------------------------------------------------------------

def create_sample_log():

    filename = "sample_server.log"

    sample_data = [
        "2026-08-08 09:10:01 192.168.1.10 INFO 200 User dashboard loaded",
        "2026-08-08 09:10:05 192.168.1.11 INFO 200 Login successful",
        "2026-08-08 09:11:10 192.168.1.15 WARNING 404 Page not found",
        "2026-08-08 09:11:22 192.168.1.15 ERROR 500 Database connection failed",
        "2026-08-08 09:12:05 192.168.1.20 INFO 200 Product loaded",
        "2026-08-08 09:13:18 192.168.1.15 ERROR 500 Database connection failed",
        "2026-08-08 09:14:11 10.10.20.5 ERROR 401 Failed login attempt",
        "2026-08-08 09:14:16 10.10.20.5 ERROR 401 Failed login attempt",
        "2026-08-08 09:14:20 10.10.20.5 ERROR 401 Failed login attempt",
        "2026-08-08 09:15:00 192.168.1.21 INFO 200 Request completed",
        "2026-08-08 09:16:10 192.168.1.22 WARNING 403 Unauthorized access",
        "2026-08-08 09:17:02 192.168.1.23 INFO 201 Account created",
        "2026-08-08 09:18:42 192.168.1.24 ERROR 500 File not found",
        "2026-08-08 09:19:15 192.168.1.25 INFO 200 API request completed",
        "2026-08-08 09:20:10 172.16.0.8 ERROR 401 Authentication failed",
        "2026-08-08 09:20:14 172.16.0.8 ERROR 401 Authentication failed",
        "2026-08-08 09:20:18 172.16.0.8 ERROR 401 Authentication failed",
        "2026-08-08 09:21:30 192.168.1.30 INFO 200 Server response successful",
        "2026-08-08 09:22:45 192.168.1.31 WARNING 404 Resource not found",
        "2026-08-08 09:23:50 192.168.1.32 CRITICAL 503 Service unavailable"
    ]

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        for entry in sample_data:
            file.write(entry + "\n")

    return filename


# ------------------------------------------------------------
# Main Menu
# ------------------------------------------------------------

def main():

    header()

    print("\nChoose an option:\n")

    print("1. Analyze existing log file")
    print("2. Create and analyze sample log")
    print("3. Exit")

    while True:

        choice = input(
            "\nEnter your choice [1-3]: "
        ).strip()

        if choice == "1":

            filename = input(
                "Enter log file path: "
            ).strip()

            analyzer = LogAnalyzer(filename)

            if analyzer.load_file():

                analyzer.analyze()
                analyzer.show_summary()
                analyzer.show_status_codes()
                analyzer.show_ips()
                analyzer.show_security()
                analyzer.show_errors()

                generate = input(
                    "\nGenerate text report? [y/n]: "
                ).lower().strip()

                if generate == "y":
                    analyzer.generate_report()

            break

        elif choice == "2":

            filename = create_sample_log()

            print(
                f"\n[OK] Sample log created: {filename}"
            )

            analyzer = LogAnalyzer(filename)

            if analyzer.load_file():

                analyzer.analyze()
                analyzer.show_summary()
                analyzer.show_status_codes()
                analyzer.show_ips()
                analyzer.show_security()
                analyzer.show_errors()

                analyzer.generate_report()

            break

        elif choice == "3":

            print("\nGoodbye!")
            break

        else:

            print(
                "[ERROR] Please choose 1, 2 or 3."
            )


# ------------------------------------------------------------
# Program Entry Point
# ------------------------------------------------------------

if __name__ == "__main__":
    main()
