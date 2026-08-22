from llm import get_response
from rich.console import Console, Group
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live
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

# used for invoke, required modifications inside llm.py to call invoke instead.
def run_cli_invoke():
    prompt = take_input()
    console.print("\n[italic yellow]Thinking...[/italic yellow]\n")
    response = call_llm_and_get_response(prompt)
    reasoning, content = get_content_reasoning(response)

    reasoning = Markdown(reasoning)
    content = Markdown(content)

    print("Reasoning: ")
    console.print(Panel(reasoning, border_style="green", title="AI Reasoning"))
    console.print(Panel(content, border_style="blue", title="AI Response"))

# used for stream, required modifications inside llm.py to call stream instead.
def run_cli_stream():
    prompt = take_input()
    console.print("\n[italic yellow]Thinking...[/italic yellow]\n")
    response = call_llm_and_get_response(prompt)

    OPEN, CLOSE = "<think>", "</think>"
    buffer = ""
    state = "before"

    with Live(console=console, refresh_per_second=20) as live:
        reasoning = ""
        answer = ""
        for chunk in response:
            buffer += chunk.content

            while True:
                if state == "before":
                    index = buffer.find(OPEN)
                    
                    if index != -1:
                        buffer = buffer[index+len(OPEN):]
                        state = "thinking"
                        continue
                    
                    if len(buffer) > len(OPEN)-1:
                        buffer = buffer[1-len(OPEN):]

                    break

                elif state == "thinking":
                    index = buffer.find(CLOSE)
                    if index != -1:
                        reasoning += buffer[:index]
                        buffer = buffer[index+len(CLOSE):]
                        state = "answering"
                        continue

                    if len(buffer) > len(CLOSE)-1:
                        reasoning += buffer[:1-len(CLOSE)]
                        buffer = buffer[1-len(CLOSE):]

                    break

                else:
                    answer += buffer
                    buffer = ""
                    break

            live.update (
                Group (
                Panel(Markdown(reasoning), border_style="green", title="AI Reasoning"),
                Panel(Markdown(answer), border_style="blue", title="AI Response")
                )   
            )

def json_structured_output():
    prompt = take_input()
    response = call_llm_and_get_response(prompt)
    json_response = response["structured_response"].model_dump_json()
    print(json_response)

if __name__ == "__main__":
    while True:
        json_structured_output()