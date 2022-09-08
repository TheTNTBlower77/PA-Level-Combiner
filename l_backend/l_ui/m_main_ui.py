"""Contains the full UI."""


import tkinter as tk
import tkinter.ttk as ttk

import l_tkinter_utils

from .. import l_library
from . import m_simple, m_advanced


class MainWindow(tk.Toplevel):
    """The main window."""
    def __init__(self, parent: tk.Widget, combine_job: l_library.CombineJob = None):
        if combine_job is None:
            combine_job = l_library.CombineJob()

        super().__init__(parent)
        l_tkinter_utils.set_weights(self, y = (1 for _ in range(4)))
        l_tkinter_utils.window_set_size(self, 1280, 720)
        l_tkinter_utils.window_center_to_screen(self)
        l_tkinter_utils.window_set_title(self, "PA Level Combiner")

        self.w_title = self.Title(self)
        self.w_view_manager = self.ViewManager(self, self)
        self.w_combine_controls = self.CombineControls(self)
        self.w_misc_buttons = self.MiscButtons(self)


        self.w_simple = self.w_view_manager.w_simple
        self.w_advanced = self.w_view_manager.w_advanced

        self.w_requires_version = [
            self.w_simple.w_level_select,
            self.w_simple.w_output,

            self.w_advanced.w_base_level,
            self.w_advanced.w_current_source_level
        ]

        self.w_view_manager.w_simple.w_version_select.on_change = self.set_requires_version_update
        self.set_requires_version_update()


        self.combine_job = combine_job

    class Title(l_tkinter_utils.Title):
        """The title."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, title = "PA Level Combiner")
            l_tkinter_utils.place_on_grid(self)

    class ViewManager(ttk.Notebook):
        """The view manager."""
        def __init__(self, parent: tk.Widget, main_window: tk.Toplevel):
            super().__init__(parent)
            l_tkinter_utils.place_on_grid(self, coords = (0, 1))
            l_tkinter_utils.notebook_set_style(self)

            self.w_main_window = main_window

            self.w_simple = m_simple.SimpleView(self, main_window)
            self.w_advanced = m_advanced.AdvancedView(self)

            frames = [
                l_tkinter_utils.NotebookFrameInfo("Simple", self.w_simple),
                l_tkinter_utils.NotebookFrameInfo("Advanced", self.w_advanced)
            ]
            l_tkinter_utils.notebook_add_frames(self, frames)

    class CombineControls(tk.Frame):
        """Contains the combining controls."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, **l_tkinter_utils.FRAME_BORDER)
            l_tkinter_utils.place_on_grid(self, coords = (0, 2))
            l_tkinter_utils.set_weights(self, x = (1, 1))

            self.w_options = self.Options(self)
            self.w_button = self.Button(self)

        class Options(tk.Button):
            """Contains all combine options."""
            def __init__(self, parent: tk.Widget):
                super().__init__(parent, text = "Combining Options...")
                l_tkinter_utils.place_on_grid(self)
                l_tkinter_utils.set_font(self, font = l_tkinter_utils.make_font(size_mult = 1.2))

        class Button(tk.Button):
            """The combine button."""
            def __init__(self, parent: tk.Widget):
                super().__init__(parent, text = "Combine!")
                l_tkinter_utils.place_on_grid(self, coords = (1, 0))
                l_tkinter_utils.set_font(self, font = l_tkinter_utils.make_font(size_mult = 1.2, bold = True))

    class MiscButtons(tk.Frame):
        """Contains all the miscellaneous buttons."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, **l_tkinter_utils.FRAME_BORDER)
            l_tkinter_utils.place_on_grid(self, coords = (0, 3))
            l_tkinter_utils.set_weights(self, x = (1, 1, 1))

            self.w_instructions = self.Instructions(self)
            self.w_about = self.About(self)
            self.w_github = self.Github(self)

        class Instructions(tk.Button):
            """Shows the instructions on how to use."""
            def __init__(self, parent: tk.Widget):
                super().__init__(parent, text = "Instructions...")
                l_tkinter_utils.place_on_grid(self)
                l_tkinter_utils.set_font(self)

        class About(tk.Button):
            """The about button."""
            def __init__(self, parent: tk.Widget):
                super().__init__(parent, text = "About...")
                l_tkinter_utils.place_on_grid(self, coords = (1, 0))
                l_tkinter_utils.set_font(self)

        class Github(tk.Button):
            """Opens the Github page."""
            def __init__(self, parent: tk.Widget):
                super().__init__(parent, text = "Open Github Page...")
                l_tkinter_utils.place_on_grid(self, coords = (2, 0))
                l_tkinter_utils.set_font(self)


    def set_active_requires_version(self, active: bool):
        """Sets the activity of the widgets that requires the version field to be filled."""
        for widget in self.w_requires_version:
            l_tkinter_utils.set_active(widget, active)

    def set_requires_version_update(self):
        """Updates the widgets that requires the version field to be filled."""
        self.set_active_requires_version(self.w_view_manager.w_simple.w_version_select.is_filled())