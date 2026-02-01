
def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("Exactly one argument expected: filename")
        return 1
    
    try:
        with open(argv[0], "r") as file:
            parsedLogLines: list[tuple[str, ...]] = []

            counter: int = 0
            for line in file:
                parsedLine: tuple[str, ...] | None = parse_log_line(line)
                if parsedLine:
                    parsedLogLines.append(parsedLine)
                else:
                    counter += 1
            
            print(str(counter) + " Lines could not be parsed")

            top_users: list[tuple[str, int]] = get_top_users(count_requests_per_user(parsedLogLines), 10)

            print("These are the top users:")
            for user in top_users:
                print(user[0]  + " " + str(user[1]))

            for i, (user, count) in enumerate(top_users, start=1):
                print(f"{i}. {user} - {count}")

            print()

    except OSError:
        print("Could not open file.")
        return 1

    return 0

def parse_log_line(line: str) -> tuple[str, ...] | None:
    #2025-11-28T10:03:05Z frank GET /api/items 200

    parts: list[str] = line.strip().split()
    if len(parts) != 5:
        return None
    
    if not parts[2].isalpha():
        return None
    
    if parts[2] not in {"GET", "POST", "DELETE", "UPDATE"}:
        return None

    return tuple(parts)

def count_requests_per_user(lines: list[tuple[str, ...]]) -> dict[str, int]:
    names: dict[str, int] = {}
    for line in lines:
        name = line[1]
        names[name] = names.get(name, 0) + 1

    return names


def get_top_users(counts: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    sortedNames: list[tuple[str,int]]= sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return sortedNames[:n]

if __name__ == "__main__":
    import sys
    raise SystemExit(main(sys.argv[1:]))