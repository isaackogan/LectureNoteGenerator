import tkinter as tk


class BaseGUI:
    """
    Base GUI to build off with centering capabilities

    """

    def __init__(self, width: int, height: int, resizable: bool = True):
        """
        Initialize BaseGUI class

        :param width: Width of application
        :param height: Height of application

        """

        # Set width & height
        self.width: int = width
        self.height: int = height

        # Create GUI
        self.root: tk.Tk = tk.Tk()
        self.root.resizable(resizable, resizable)
        self.root.geometry(f"{self.width}x{self.height}")

    def center(self) -> None:
        """
        Center the GUI horizontally and vertically
        :return: None

        """

        screen_width = self.root.winfo_screenwidth()  # Width of the screen
        screen_height = self.root.winfo_screenheight()  # Height of the screen

        x = (screen_width / 2) - (self.width / 2)
        y = (screen_height / 2) - (self.height / 2)

        self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))

    def run(self) -> None:
        """
        Run the app & block the main thread
        :return: None

        """

        self.center()
        self.root.mainloop()
