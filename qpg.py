import csv, json, random, sys
from pathlib import Path

SUBJECT_ALIASES = {
    "DSA":  ["dsa", "data structures", "data structures & algorithms"],
    "DBMS": ["dbms", "database", "database systems"],
    "CN":   ["cn", "computer networks", "network"],
    "SE":   ["se", "software engineering", "swe"],
}

TYPE_ALIASES = {
    "MCQ": ["mcq", "objective", "multiple choice"],
    "SA1": ["sa1", "short", "short answer"],
    "LA":  ["la", "long", "long answer"],
}

def normalize_subject(s):
    s = (s or "").strip().lower()
    for key, values in SUBJECT_ALIASES.items():
        if s == key.lower() or s in values:
            return key
    return None

def normalize_type(t):
    t = (t or "").strip().lower()
    for key, values in TYPE_ALIASES.items():
        if t == key.lower() or t in values:
            return key
    if t == "short":
        return "SA1"
    if t == "long":
        return "LA"
    return None

def load_bank(csv_path="bank.csv"):
    p = Path(csv_path)
    if not p.exists():
        sys.exit("bank.csv not found!")
    with p.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))

def filter_questions(bank, subject, qtype):
    subj = subject.upper()
    qtp  = qtype.upper()
    return [
        r for r in bank
        if (r.get("subject","").strip().upper() == subj) and
           (r.get("type","").strip().upper() == qtp)
    ]

def display_questions(rows):
    n = min(5, len(rows))
    if n == 0:
        print("\nNo questions found.\n")
        return
    print("\n=== QUESTIONS ===\n")
    for i, q in enumerate(rows[:n], start=1):
        print(f"{i}. ({q.get('marks','').strip()} marks) {q.get('question','').strip()}")
        if (q.get("type","").strip().upper() == "MCQ"):
            opts_raw = (q.get("options","") or "").strip()
            if opts_raw:
                try:
                    opts = json.loads(opts_raw)
                except Exception:
                    opts = [x.strip() for x in opts_raw.split("|")]
                for j, opt in enumerate(opts, start=1):
                    print(f"   {chr(96+j)}) {opt}")
        unit = q.get("unit","-")
        diff = (q.get("difficulty","") or "-").upper()
        topic = q.get("topic","-")
        print(f"   [Unit {unit} | Difficulty {diff} | {topic}]")

def main():
    print("\nAvailable subjects: DSA, DBMS, CN, SE")

    subject = normalize_subject(input("\nEnter subject: "))
    if not subject:
        print("Invalid subject!")
        return

    print("\nQuestion types: MCQ, Short, Long")
    qtype = normalize_type(input("\nEnter question type: "))
    if not qtype:
        print("Invalid question type!")
        return

    bank = load_bank("bank.csv")
    random.shuffle(bank)  # variety across runs

    rows = filter_questions(bank, subject, qtype)

    print(f"\nSelected Subject = {subject}   Type = {qtype}")
    print("Showing up to 5 questions:\n")

    display_questions(rows)

if __name__ == "__main__":
    main()
