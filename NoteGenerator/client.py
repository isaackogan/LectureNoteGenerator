import random
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from typing import Optional
import os

from NoteGenerator.PDFGenerator import generator
from NoteGenerator.TkUtils.base_gui import BaseGUI
from NoteGenerator.TkUtils.switch import SwitchSelect


class NoteGenerator(BaseGUI):

    def __init__(self):
        super().__init__(width=800, height=500)

        # Set up GUI
        self.root.title("Lecture Note Generator")
        self.root.iconbitmap()

        # Declarations
        self.file_input_button: Optional[ttk.Button] = None
        self.file_convert_button: Optional[ttk.Button] = None
        self.selected_file_label: Optional[tk.Label] = None
        self.output_path_label: Optional[tk.Label] = None
        self.rule_switch_select: Optional[SwitchSelect] = None

        # Internal Variables
        self._input_path: Optional[str] = None
        self._output_path: Optional[str] = None

        # Set up components
        self.setup_gui_components()

        # center GUI
        self.center()

    @property
    def selected_file_path(self) -> str:
        """
        Generate DISPLAY string for the selected input path
        :return: Selected input path DISPLAY label text

        """

        return self._input_path if self._input_path else 'Not Selected'

    @property
    def output_file_path(self) -> str:
        """
        Generate DISPLAY string for the selected output path
        :return: Selected output path DISPLAY label text

        """

        output_path: Optional[str] = self._set_output_path()
        return output_path if output_path else 'Not Selected'

    def _set_output_path(self) -> Optional[str]:
        """
        Set the output path INTERNAL value
        :return: The output path if one can be generated

        """

        # If no input, we can't have an output
        if not self._input_path:
            self._output_path = None
            return

        # Get the filename and generate an output path
        filename: str = os.path.basename(self.selected_file_path)
        self._output_path = self._input_path.replace(
            filename,
            filename.replace(".pdf", f"-({self.rule_switch_select.value}-{random.randint(11111, 99999)}).pdf")
        )

        return self._output_path

    def on_file_button(self, cached: bool = False) -> None:
        """
        When the file select button is clicked, prompt file select if not cached and set the input, output path

        :param cached: Whether to use the current value when setting paths or prompt for a new one
        :return: None

        """

        # Get the name
        name: Optional[str] = (
            self._input_path if cached else fd.askopenfilename(
                title="Select a File",
                initialdir="./",
                filetypes=(('pdf file', '*.pdf'),)
            )
        )

        # Set the path
        self._input_path = name if name else None

        # Configure labels
        self.selected_file_label.configure(text=self.selected_file_path)
        self.output_path_label.configure(text=self.output_file_path)

        # Disable convert button if invalid
        self.file_convert_button["state"] = "normal" if self._output_path else "disabled"

    def on_file_convert(self) -> None:
        """
        When the convert button is clicked, convert the PDF
        :return: None

        """

        # If the output path is invalid, we can't do anything
        if not self._output_path:
            tk.messagebox.showerror("Failed Generator", "Output path not selected")
            return

        # Disable Buttons
        self.file_convert_button["state"] = "disabled"
        self.file_input_button["state"] = "disabled"
        self.rule_switch_select.state(enabled=False)

        # Do Conversion
        generator.convert_file(self._input_path, self._output_path, self.rule_switch_select.value)
        tk.messagebox.showinfo("Generator Finished", f"File written to {self._output_path}")

        # Set new output path
        self.on_file_button(cached=True)

        # Enable Buttons
        self.file_convert_button["state"] = "normal"
        self.file_input_button["state"] = "normal"
        self.rule_switch_select.state(enabled=True)

    def setup_gui_components(self) -> None:
        """
        Build the GUI with the required components
        :return: None

        """

        # Add Title
        canvas = tk.Canvas(self.root, width=400, height=160)
        canvas.create_text(200, 115, text="Lecture Note Generator", fill="black", font='Helvetica 25 bold')

        # Filepath Label
        filepath_frame = tk.Frame(self.root, width=400)
        label_text = tk.Label(filepath_frame, text="Selected File:", font="Helvetica 12 bold")
        self.selected_file_label = tk.Label(filepath_frame, text=self.selected_file_path, font="Helvetica 12")

        # Output Input
        output_path_frame = tk.Frame(self.root, width=400)
        output_label = tk.Label(output_path_frame, text="Output Path:", font="Helvetica 12 bold")
        self.output_path_label = tk.Label(output_path_frame, text=self.selected_file_path, font="Helvetica 12")

        # Lined Input
        rule_frame = tk.Frame(self.root, width=400)
        rule_label = tk.Label(rule_frame, text="Format:", font="Helvetica 12 bold")
        self.rule_switch_select = SwitchSelect(rule_frame, ["Lined", "Grid", "Neither"], default="Lined")

        # Add Input Button
        self.file_input_button: ttk.Button = ttk.Button(
            self.root,
            text='\nSelect Input File (.pdf)\n',
            command=self.on_file_button,
            width=30
        )

        # Convert Button
        self.file_convert_button: ttk.Button = ttk.Button(
            self.root,
            text='\nGenerate File (.pdf)\n',
            command=self.on_file_convert,
            width=30
        )
        self.file_convert_button["state"] = "disabled"

        # Pack Title
        canvas.pack()

        # Pack Input Label
        label_text.pack(side=tk.LEFT)
        self.selected_file_label.pack(pady=0)
        filepath_frame.pack()

        # Pack Output Location
        output_label.pack(side=tk.LEFT)
        self.output_path_label.pack(side=tk.LEFT)
        output_path_frame.pack()

        # Pack Lined Checkbox
        rule_label.pack(side=tk.LEFT)
        self.rule_switch_select.pack(side=tk.LEFT)
        rule_frame.pack(pady=20)

        # Pack File Button
        self.file_input_button.pack()
        self.file_convert_button.pack()


if __name__ == '__main__':
    app: NoteGenerator = NoteGenerator()
    app.run()
