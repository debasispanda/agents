from rich.console import Console


def show(text):
    console = Console()
    console.print(text)

todos, completed = [], []

def get_todo_report() -> str:
    result = ""
    for index, todo in enumerate(todos):
        if completed[index]:
            result += f"Todo #{index + 1}: [green][strike]{todo}[/strike][/green]\n"
        else:
            result += f"Todo #{index + 1}: {todo}\n"
    
    show(result)
    return result

def create_todos(descriptions: list[str]) -> str:
    todos.extend(descriptions)
    completed.extend([False] * len(descriptions))
    return get_todo_report()

def mark_complete(index: int, completion_notes: str) -> str:
    if not (1 <= index <= len(todos)):
        return "Invalid todo index."
    
    completed[index - 1] = True
    Console().print(completion_notes)
    return get_todo_report()

if __name__ == "__main__":
    # Example usage
    todos, completed = [], []
    create_todos(["Buy groceries", "Clean the house", "Finish the project"])

    mark_complete(2, "House cleaning completed successfully")
    
