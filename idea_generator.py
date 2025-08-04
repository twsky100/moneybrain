import subprocess

def generate_ideas(memory_log):
    context = "\n".join(memory_log)
    prompt = open("prompts/idea_generation_prompt.txt").read()
    full_prompt = f"{prompt}\n\nPreviously tested ideas:\n{context}"

    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=full_prompt.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    output = result.stdout.decode("utf-8")
    return output
