from app.orchestrator import run_research

def main():
    idea = input("Enter your idea/project: ").strip()

    if not idea:
        print("Please enter a valid idea.")
        return

    result = run_research(idea)

    print("\n\n===== RESEARCH OUTPUT =====\n")
    print(result)


if __name__ == "__main__":
    main()