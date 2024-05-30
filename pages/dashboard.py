"""The dashboard page."""

import re
import reflex as rx
from typing import List
from Supabase_frontend.templates import template
import subprocess
import docker
from dotenv import dotenv_values

shell_password = ""
path_to_supabase_env = ""
config_dict = dotenv_values(dotenv_path=path_to_supabase_env) 
config_keys_array = [str(key) for key in config_dict.keys()]

class DynamicFormState(rx.State):
    form_data: dict = {}
    form_fields: list[str] = config_keys_array
    def handle_submit(self, form_data: dict):
        self.form_data = form_data

        # Open the file for reading
        with open(path_to_supabase_env, 'r') as file:
            lines = file.readlines()

        # Iterate through each line
        for i, line in enumerate(lines):
            # Iterate through each key to change
            for key, value in self.form_data.items():
                if value != '':
                # Search for the key in the line
                    if re.search(rf"{re.escape(key)}=(.*)", line):
                        # Replace the old value with the new one
                        lines[i] = f"{key}={value}\n"

        # Open the file for writing
        with open(path_to_supabase_env, 'w') as file:
            # Write the updated lines to the file
            file.writelines(lines)

        print("File updated successfully.")

def display_config_value(config):
    return rx.hstack(
        rx.text(str(config)),
        rx.input(
            # placeholder=str(config[1]),
            name=str(config)
        )
    )
    
def dynamic_form():
    return rx.vstack(
        rx.form(
            rx.vstack(
                rx.foreach(
                    DynamicFormState.form_fields,
                    lambda field, idx: rx.hstack(
                        rx.text(field),
                        rx.input(
                            name=field,
                        )
                    )
                ),
                rx.button("Submit", type="submit"),
            ),
            on_submit=DynamicFormState.handle_submit,
            # reset_on_submit=True,
        ),
        rx.divider(),
        rx.heading("Results"),
        rx.text(DynamicFormState.form_data.to_string()),
    )


# def restart():
#     result = subprocess.Popen(["sudo", "ls", "tokenize"],
#                           stdin=subprocess.PIPE,
#                           stdout=subprocess.PIPE).communicate(input=b"<password>\n")
#     print(result)

@template(route="/dashboard", title="Dashboard")
def dashboard() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """
    return rx.vstack(
        rx.heading("Configuration parameters", size="8"),
        dynamic_form(),
        rx.button(
            "Restart all services",
            color_scheme="grass",
            # on_click=restart()
        )
    )
