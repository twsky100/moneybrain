from agents.idea_generator import generate_ideas
from agents.executor_agent import simulate_execution
from agents.result_logger import log_result
from agents.research_agent import get_market_signals
import re

memory = []

market_signals = get_market_signals()
ideas_text = generate_ideas(memory + [str(market_signals)])
idea_splits = re.split(r'\n\d+\.\s+Name:', ideas_text)
ideas = [idea.strip() for idea in idea_splits if idea.strip()]

for idea_text in ideas:
    lines = idea_text.splitlines()
    idea_name = lines[0].replace('Name:', '').strip() if lines else "Unnamed Idea"
    idea = {
        "name": idea_name,
        "concept": idea_text,
    }
    result = simulate_execution(idea)
    log_result(idea, result)
    memory.append(f"{idea['name']} - Revenue: ${result['revenue']}")
