from analyzer import analyze_business_idea
from colorama import init, Fore, Style
import csv
import os
import json
import matplotlib.pyplot as plt
from collections import Counter

init(autoreset=True)

def main():
    try:
        idea = input(f"{Fore.YELLOW}💡 Enter your business idea: {Style.RESET_ALL}").strip()
        if not idea:
            print(f"{Fore.RED}⚠ Please enter a non-empty idea.")
            return

        print(f"\n{Fore.CYAN}Analyzing your hustle...\n")
        result = analyze_business_idea(idea)

        if 'error' in result:
            print(f"{Fore.RED}❌ Failed to analyze idea: {result['error']}")
            return

        # Hustle Score
        score = result.get('hustle_score', 0)
        print(f"{Fore.GREEN}✅ Hustle Score: {score} / 100")
        bar = '█' * (score // 5)
        print(f"{Fore.GREEN}📈 Score Bar: {bar}")

        # Viral Factor
        if 'viral_factor' in result:
            print(f"{Fore.MAGENTA}🔥 Viral Factor: {result['viral_factor']} / 10")

        # SWOT
        print(f"\n{Fore.CYAN}🧠 SWOT Analysis:")
        emoji_map = {
            'Strengths': '💪',
            'Weaknesses': '⚠',
            'Opportunities': '🚀',
            'Threats': '⚔'
        }
        for key, val in result['swot'].items():
            emoji = emoji_map.get(key, '🔹')
            print(f"{Fore.YELLOW}  {emoji} {key}:{Style.RESET_ALL} {val}")

        # Keywords
        if 'keywords' in result:
            print(f"\n{Fore.CYAN}🔑 Keywords: {Fore.RESET}{', '.join(result['keywords'])}")

        # Domain suggestions
        if 'domain_suggestions' in result:
            print(f"\n{Fore.CYAN}🌐 Domain Name Ideas:")
            for d, status in result['domain_suggestions'].items():
                symbol = "✅" if "Available" in status else "❌"
                print(f"{Fore.GREEN}  - {d}: {symbol} {status}")

        # Competitors
        if 'competitors' in result:
            print(f"\n{Fore.CYAN}🏢 Potential Competitors:")
            for comp in result['competitors']:
                print(f"{Fore.YELLOW}  - {comp}")

        # Save results
        save_to_csv(idea, result)
        save_to_json(idea, result)

    except Exception as e:
        print(f"{Fore.RED}❌ Unexpected error: {e}")

def save_to_csv(idea, result):
    file_exists = os.path.isfile("results.csv")
    with open("results.csv", mode="a", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow([
                "Idea", "Hustle Score", "Viral Factor",
                "Strengths", "Weaknesses", "Opportunities", "Threats",
                "Keywords", "Domain Suggestions", "Competitors"
            ])
        swot = result['swot']
        writer.writerow([
            idea,
            result.get('hustle_score', 0),
            result.get('viral_factor', 0),
            ', '.join(swot.get('Strengths', [])),
            ', '.join(swot.get('Weaknesses', [])),
            ', '.join(swot.get('Opportunities', [])),
            ', '.join(swot.get('Threats', [])),
            ', '.join(result.get('keywords', [])),
            ', '.join([f"{d} ({s})" for d, s in result.get('domain_suggestions', {}).items()]),
            ', '.join(result.get('competitors', []))
        ])
    print(f"{Fore.MAGENTA}💾 Result saved to 'results.csv'")

def save_to_json(idea, result):
    filename = "results.json"
    data = {
        "idea": idea,
        "hustle_score": result.get('hustle_score', 0),
        "viral_factor": result.get('viral_factor', 0),
        "swot": result.get('swot', {}),
        "keywords": result.get('keywords', []),
        "domain_suggestions": result.get('domain_suggestions', {}),
        "competitors": result.get('competitors', [])
    }

    try:
        if os.path.isfile(filename):
            with open(filename, 'r+', encoding='utf-8') as f:
                existing = json.load(f)
                existing.append(data)
                f.seek(0)
                json.dump(existing, f, indent=4)
        else:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump([data], f, indent=4)
        print(f"{Fore.MAGENTA}💾 Result also saved to '{filename}'")
    except Exception as e:
        print(f"{Fore.RED}❌ Failed to save JSON: {e}")

def visualize_results():
    if not os.path.isfile("results.csv"):
        print(f"{Fore.RED}❌ No 'results.csv' file found to visualize. Please analyze some ideas first.")
        return

    hustle_scores = []
    viral_factors = []
    strengths = []
    weaknesses = []
    opportunities = []
    threats = []

    with open("results.csv", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                hustle_scores.append(int(row.get("Hustle Score", 0)))
                viral_factors.append(int(row.get("Viral Factor", 0)))
            except ValueError:
                hustle_scores.append(0)
                viral_factors.append(0)

            strengths.extend(row.get("Strengths", "").split(", "))
            weaknesses.extend(row.get("Weaknesses", "").split(", "))
            opportunities.extend(row.get("Opportunities", "").split(", "))
            threats.extend(row.get("Threats", "").split(", "))

    # Plot
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.hist(hustle_scores, bins=range(0, 105, 5), color='green', edgecolor='black')
    plt.title("Hustle Score Distribution")
    plt.xlabel("Score")
    plt.ylabel("Count")

    plt.subplot(1, 2, 2)
    plt.hist(viral_factors, bins=range(0, 12), color='magenta', edgecolor='black')
    plt.title("Viral Factor Distribution")
    plt.xlabel("Viral Factor")
    plt.ylabel("Count")

    plt.tight_layout()
    plt.show()

    # Print top SWOT insights
    print(f"\n{Fore.CYAN}Top Strengths: {Counter(strengths).most_common(5)}")
    print(f"{Fore.CYAN}Top Weaknesses: {Counter(weaknesses).most_common(5)}")
    print(f"{Fore.CYAN}Top Opportunities: {Counter(opportunities).most_common(5)}")
    print(f"{Fore.CYAN}Top Threats: {Counter(threats).most_common(5)}")

if __name__ == "__main__":
    print(f"{Fore.MAGENTA}🚀 Welcome to HustleAnalyzer X!\n")

    while True:
        print("\nChoose an option:")
        print("1. Analyze new idea")
        print("2. Visualize saved results")
        print("3. Exit")

        choice = input(f"{Fore.BLUE}Enter choice (1/2/3): {Style.RESET_ALL}").strip()
        if choice == '1':
            main()
        elif choice == '2':
            visualize_results()
        elif choice == '3':
            print(f"{Fore.LIGHTMAGENTA_EX}👋 Thanks for using HustleAnalyzer X! Goodbye!")
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please select 1, 2 or 3.")