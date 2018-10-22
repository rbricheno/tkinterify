import tkinter
import click
import sys
from io import StringIO


def tkinterify(cli_group, app_name="Tkinterified App"):

    # Create and configure root
    root = tkinter.Tk()
    root.wm_title(app_name)
    tkinter.Grid.rowconfigure(root, 0, weight=1)
    tkinter.Grid.columnconfigure(root, 0, weight=1)

    # Create and configure frame
    frame = tkinter.Frame(root)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(2, weight=1)
    frame.rowconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)

    initial_output = "Valid commands:\n"
    initial_command_name_list = list(cli_group.commands.keys())
    for available_command_name in initial_command_name_list:
        initial_output = initial_output + "  " + available_command_name + "\n"
    initial_output = initial_output + "Ready for input."

    # Some GUI widgets
    run_string = tkinter.StringVar()
    entry_run = tkinter.Entry(root, textvariable=run_string, width=50)
    scrollbar_widget = tkinter.Scrollbar(root)
    text_widget = tkinter.Text(root)

    def clear_callback():
        # Because the text widget is usually disabled, we have to explicitly enable it before we can write to it.
        text_widget.config(state='normal')
        text_widget.delete(1.0, tkinter.END)
        text_widget.insert(tkinter.END, initial_output)
        text_widget.config(state='disabled')

    def run_callback():
        command_args = []
        try:
            command_parts = run_string.get().split()
            command_name = command_parts[0]
        except IndexError:
            return
        if len(command_parts) > 1:
            command_args = command_parts[1:]

        if command_name:
            try:
                # Redirect stdout so we can read the output into a string for display within out GUI
                real_stdout = sys.stdout
                fake_stdout = StringIO()
                sys.stdout.flush()
                sys.stdout = fake_stdout

                # Obtain list of available commands
                available_commands = cli_group.commands
                command_name_list = list(cli_group.commands.keys())
                if command_name in command_name_list:
                    try:
                        # Make a fake context in which to run the command
                        context = available_commands[command_name].make_context("tkinter", command_args)
                        # Invoke the command within the fake context
                        available_commands[command_name].invoke(context)
                    except click.exceptions.UsageError as e:
                        print(e)
                        print(initial_output)
                else:
                    print("Command not found.\n")
                    print(initial_output)

                # Put stdout back
                sys.stdout.flush()
                sys.stdout = real_stdout
                sys.stdout.flush()
                output_string = fake_stdout.getvalue()
                fake_stdout.close()

                # Update the text output widget
                text_widget.config(state='normal')
                text_widget.delete(1.0, tkinter.END)
                text_widget.insert(tkinter.END, output_string)
                text_widget.config(state='disabled')

            except IndexError:
                pass

    # More GUI widgets
    button_run = tkinter.Button(root, text="Run", command=run_callback)
    button_clear = tkinter.Button(root, text="Clear", command=clear_callback)

    text_widget.delete(1.0, tkinter.END)
    text_widget.insert(tkinter.END, initial_output)

    entry_run.grid(row=0, column=0, sticky="new")
    button_run.grid(row=0, column=1, sticky="n")
    button_clear.grid(row=0, column=2, sticky="n")
    text_widget.grid(row=1, column=0, columnspan=2, sticky="nsew")
    scrollbar_widget.grid(row=1, column=2, sticky="ns")

    scrollbar_widget.config(command=text_widget.yview)
    text_widget.config(yscrollcommand=scrollbar_widget.set)
    text_widget.config(state='disabled')

    root.mainloop()
