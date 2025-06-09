import sys, os, json

# Ensure parent directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.pivot import pivot_agent

# Sample articles
articles = [
    {
        "title": "U of A post-graduate student Amir Saeedinia remembered...",
        "link": "https://www.cbc.ca/news/canada/edmonton/iran-flight-crash-u-of-a-phd-engineering-canada-iran-ukrainian-airlines-1.5421560",
        "published": "Jan 10, 2020",
        "snippet": "When Ali Khaledi Nasab found out his close friend was coming to Edmonton, the two made plans to get together this coming summer."
    },
    {
        "title": "I almost sold a kidney to pursue my Ph.D.",
        "link": "https://www.science.org/content/article/almost-sold-kidney-pursue-phd",
        "published": "Mar 16, 2023",
        "snippet": "I placed an advertisement and found a buyer. This is legal in Iran and became my only viable solution to fund my education."
    }
]

if __name__ == "__main__":
    output = pivot_agent(articles, "Ali Khaledi Nasab")
    print("\n🧠 Pivot Agent Output:\n")
    print(output)
