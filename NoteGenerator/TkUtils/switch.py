import functools
import tkinter as tk
from typing import List, Optional, Literal, Dict


class SwitchSelect(tk.Frame):
    """
    Custom component to manage an array of related Checkbutton elements

    """

    def __init__(
            self,
            master: tk.Frame = None,
            options: List[str] = [],
            side: Literal["left", "right", "top", "bottom"] = tk.LEFT,
            anchor: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"] = tk.W,
            default: Optional[str] = None
    ):

        # Init super
        tk.Frame.__init__(self, master)

        # Initialize Variables
        self._variables: Dict[str, tk.BooleanVar] = dict()
        self._default: Optional[str] = default if default else options[0]
        self._check_buttons: List[tk.Checkbutton] = []

        # Generate the buttons
        for pick in options:
            var = tk.BooleanVar(value=False)
            check_button = tk.Checkbutton(self, font="Helvetica 12", text=pick, variable=var, command=functools.partial(self.on_check, pick=pick))
            check_button.pack(side=side, anchor=anchor, expand=tk.YES)
            self._check_buttons.append(check_button)
            self._variables[pick] = var

        # Set the default variable
        self._variables[default].set(True)

    def state(self, enabled: bool) -> None:
        """
        Set the state of the element (mimics element["state"] in regular Checkbutton)

        :param enabled: Whether enabled or false
        :return: None

        """

        for check_button in self._check_buttons:
            check_button["state"] = "normal" if enabled else "disabled"

    def on_check(self, pick: str) -> None:
        """
        When a check-button is clicked

        :param pick: What choice has been selected
        :return: None

        """

        state = self._variables[pick].get()

        # Set all the variables to false
        for var in self._variables.values():
            var: tk.BooleanVar = var
            var.set(False)

        # Set our variable to the state
        self._variables[pick].set(state)

        # If they're all disabled, set the default to True
        if all(var.get() is False for var in self._variables.values()):
            self._variables[self._default].set(True)

    @property
    def value(self) -> str:
        """
        Get the current value

        :return: The current value, or the default if none are found
        """

        for name, value in self._variables.items():
            if value.get():
                return name

        return self._default
