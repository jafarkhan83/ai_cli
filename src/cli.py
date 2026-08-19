from llm import get_response
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
import re

console = Console()

def take_input():
    console.print(Panel("[bold blue]How may I assist you?[/bold blue]"))
    return console.input("[bold blue]❯ [/bold blue]")

def call_llm_and_get_response(prompt):
    return get_response(prompt)

def get_content_reasoning(response):
    pattern = r"<think>(.*?)</think>"
    match = re.search(pattern, response.content, flags=re.DOTALL)
    if match:
        reasoning = match.group(1).strip()
    else:
        reasoning = ""
    content = re.sub(pattern, '', response.content, flags=re.DOTALL).strip()
    return reasoning, content

def run_cli():
    prompt = take_input()
    console.print("\n[italic yellow]Thinking...[/italic yellow]\n")
    response = call_llm_and_get_response(prompt)
    reasoning, content = get_content_reasoning(response)

    reasoning = Markdown(reasoning)
    content = Markdown(content)

    print("Reasoning: ")
    console.print(Panel(reasoning, border_style="green", title="AI Reasoning"))
    console.print(Panel(content, border_style="blue", title="AI response"))

if __name__ == "__main__":
    while True:
        run_cli()