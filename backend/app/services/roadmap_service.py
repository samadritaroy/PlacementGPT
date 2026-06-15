from app.services.llm_service import ask_llama


def generate_dsa_roadmap(
    target_role="Software Engineer"
):

    prompt = """
You are an expert DSA mentor.

Create a complete 8-week Data Structures and Algorithms roadmap for placement preparation.

Requirements:

- Week-wise roadmap
- Cover beginner to advanced topics
- Include Arrays, Strings, Linked Lists, Stacks, Queues
- Include Trees, BST, Heaps, Hashing
- Include Recursion, Backtracking, Greedy
- Include Graphs and Dynamic Programming
- Mention the number of questions to practice each week
- Mention important concepts to focus on
- Keep the roadmap concise and structured

Format:

Week 1:
Topics:
Practice Goal:

Week 2:
Topics:
Practice Goal:

...

Week 8:
Topics:
Practice Goal:

Return only the roadmap.
"""

    roadmap = ask_llama(prompt)

    return roadmap