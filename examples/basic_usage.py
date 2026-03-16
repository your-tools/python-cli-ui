#!/usr/bin/env python3
"""
Basic usage examples for cli-ui library
"""

import cli_ui
import time


def basic_colors_demo():
    """Demonstrate basic color and formatting features"""
    cli_ui.info_section("Color and Formatting Demo")
    
    # Basic colors
    cli_ui.info("This is", cli_ui.red, "red", cli_ui.reset, "text")
    cli_ui.info("This is", cli_ui.green, "green", cli_ui.reset, "text")
    cli_ui.info("This is", cli_ui.blue, "blue", cli_ui.reset, "text")
    cli_ui.info("This is", cli_ui.yellow, "yellow", cli_ui.reset, "text")
    
    # Formatting
    cli_ui.info("This is", cli_ui.bold, "bold", cli_ui.reset, "text")
    cli_ui.info("This is", cli_ui.underline, "underlined", cli_ui.reset, "text")
    
    # Special characters
    cli_ui.info("Success", cli_ui.check)
    cli_ui.info("Failed", cli_ui.cross)
    cli_ui.info("Loading", cli_ui.ellipsis)


def message_levels_demo():
    """Demonstrate different message levels"""
    cli_ui.info_section("Message Levels Demo")
    
    cli_ui.info_1("Important information")
    cli_ui.info_2("Secondary information")  
    cli_ui.info_3("Detailed information")
    cli_ui.warning("This is a warning")
    cli_ui.error("This is an error")
    
    # Debug messages (only shown if verbose=True)
    cli_ui.setup(verbose=True)
    cli_ui.debug("This is a debug message")
    cli_ui.setup(verbose=False)


def progress_demo():
    """Demonstrate progress indicators"""
    cli_ui.info_section("Progress Demo")
    
    # Dot progress
    cli_ui.info("Processing", end="")
    for i in range(5):
        time.sleep(0.2)
        cli_ui.dot(last=(i == 4))
    
    # Counter progress
    items = ["item1", "item2", "item3", "item4", "item5"]
    for i, item in enumerate(items):
        cli_ui.info_count(i, len(items), "Processing", item)
        time.sleep(0.1)
    
    # Percentage progress
    for i in range(0, 21, 5):
        cli_ui.info_progress("Downloading", i, 20)
        time.sleep(0.1)
    cli_ui.info()  # New line after progress


def table_demo():
    """Demonstrate table formatting"""
    cli_ui.info_section("Table Demo")
    
    # Simple table with headers
    headers = ["Name", "Age", "Score"]
    data = [
        [(cli_ui.bold, "Alice"), (25,), (cli_ui.green, 95)],
        [(cli_ui.bold, "Bob"), (30,), (cli_ui.yellow, 78)],
        [(cli_ui.bold, "Charlie"), (28,), (cli_ui.red, 65)],
    ]
    cli_ui.info_table(data, headers=headers)
    
    # Dictionary-based table
    cli_ui.info()
    dict_data = {
        (cli_ui.bold, "Product"): [(cli_ui.blue, "Widget A"), (cli_ui.blue, "Widget B")],
        (cli_ui.bold, "Price"): [(cli_ui.green, "$19.99"), (cli_ui.green, "$29.99")],
        (cli_ui.bold, "Stock"): [(50,), (23,)],
    }
    cli_ui.info_table(dict_data, headers="keys")


def user_input_demo():
    """Demonstrate user input functions (interactive)"""
    cli_ui.info_section("User Input Demo")
    
    # Ask for string
    name = cli_ui.ask_string("What's your name?", default="Anonymous")
    cli_ui.info("Hello,", cli_ui.green, name)
    
    # Ask yes/no
    likes_pizza = cli_ui.ask_yes_no("Do you like pizza?", default=True)
    if likes_pizza:
        cli_ui.info("Great! Pizza is awesome", cli_ui.check)
    else:
        cli_ui.info("That's okay, more for us!", cli_ui.cross)
    
    # Ask choice
    colors = ["red", "green", "blue", "yellow"]
    favorite_color = cli_ui.ask_choice("Pick your favorite color", choices=colors)
    if favorite_color:
        cli_ui.info("Your favorite color is", getattr(cli_ui, favorite_color), favorite_color)
    
    # Multiple selection
    fruits = ["apple", "banana", "orange", "grape", "kiwi"]
    selected_fruits = cli_ui.select_choices("Select fruits you like", choices=fruits)
    if selected_fruits:
        cli_ui.info("You selected:", ", ".join(selected_fruits))


def timer_demo():
    """Demonstrate timer functionality"""
    cli_ui.info_section("Timer Demo")
    
    # Timer as context manager
    with cli_ui.Timer("Context manager timer"):
        time.sleep(1)
    
    # Timer as decorator
    @cli_ui.Timer("Decorated function")
    def slow_function():
        time.sleep(0.5)
        return "result"
    
    result = slow_function()
    cli_ui.info("Function returned:", result)


def error_handling_demo():
    """Demonstrate error handling and suggestions"""
    cli_ui.info_section("Error Handling Demo")
    
    # Did you mean functionality
    valid_commands = ["start", "stop", "restart", "status"]
    user_input = "stat"
    
    suggestion = cli_ui.did_you_mean("Invalid command", user_input, valid_commands)
    cli_ui.info(suggestion)
    
    # Exception formatting
    try:
        x = 1 / 0
    except Exception as e:
        tokens = cli_ui.message_for_exception(e, "Mathematical error occurred")
        cli_ui.error(*tokens)


def configuration_demo():
    """Demonstrate configuration options"""
    cli_ui.info_section("Configuration Demo")
    
    # Timestamp
    cli_ui.setup(timestamp=True)
    cli_ui.info("This message has a timestamp")
    cli_ui.setup(timestamp=False)
    
    # Quiet mode
    cli_ui.info("This will be shown")
    cli_ui.setup(quiet=True)
    cli_ui.info("This will be hidden")
    cli_ui.error("But errors are still shown")
    cli_ui.setup(quiet=False)
    
    # Color mode
    cli_ui.setup(color="always")
    cli_ui.info("Colors are", cli_ui.red, "always", cli_ui.reset, "on")
    cli_ui.setup(color="auto")  # Reset to auto


def main():
    """Run all demos"""
    cli_ui.info_section(cli_ui.bold, "CLI-UI Library Demo")
    
    demos = [
        ("Basic Colors and Formatting", basic_colors_demo),
        ("Message Levels", message_levels_demo),
        ("Progress Indicators", progress_demo),
        ("Table Formatting", table_demo),
        ("Timer Functionality", timer_demo),
        ("Error Handling", error_handling_demo),
        ("Configuration Options", configuration_demo),
    ]
    
    for name, demo_func in demos:
        cli_ui.info()
        cli_ui.info_2("Running:", name)
        demo_func()
        time.sleep(0.5)
    
    # Interactive demo (optional)
    cli_ui.info()
    if cli_ui.ask_yes_no("Run interactive user input demo?", default=False):
        user_input_demo()
    
    cli_ui.info()
    cli_ui.info_1("Demo complete!", cli_ui.check)


if __name__ == "__main__":
    main()