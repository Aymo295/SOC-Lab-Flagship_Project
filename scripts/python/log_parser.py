from pathlib import Path


def count_failed_logons(log_file: Path) -> int:
    count = 0

    with log_file.open(encoding="utf-8") as file:
        for line in file:
            if "4625" in line:
                count += 1

    return count


if __name__ == "__main__":
    path = Path("logs/windows_events.txt")
    print(f"Failed logons found: {count_failed_logons(path)}")