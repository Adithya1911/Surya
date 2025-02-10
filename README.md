import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from add_map import Debug_New_Map, User_New_Map


class Application(Gtk.Window):
    def __init__(self):
        super().__init__(title="Location Management")
        self.fullscreen()
        self.set_keep_above(True)
        self.set_titlebar(self.create_header_bar())

        # Mode flag: False = User Mode, True = Debug Mode
        self.debugger_mode = False

        # Apply custom CSS styles
        self.apply_css()

        # Main layout
        self.main_layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.main_layout)

        # Centering container
        self.center_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=20,
            margin=40
        )
        self.center_box.set_valign(Gtk.Align.CENTER)  # Center vertically
        self.center_box.set_halign(Gtk.Align.CENTER)  # Center horizontally
        self.main_layout.pack_start(self.center_box, True, True, 0)

        # Mode Switch (Better visual toggle)
        mode_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        mode_label = Gtk.Label(label="Mode:")
        self.mode_switch = Gtk.Switch()
        self.mode_switch.set_active(False)  # Default to User Mode
        self.mode_switch.connect("state-set", self.on_mode_switch)

        mode_box.pack_start(mode_label, False, False, 0)
        mode_box.pack_start(self.mode_switch, False, False, 0)
        self.center_box.pack_start(mode_box, False, False, 0)

        # 'Add Map' button
        add_location_button = Gtk.Button(label="Add Map")
        add_location_button.get_style_context().add_class("custom-button")
        add_location_button.connect("clicked", self.on_add_location)
        self.center_box.pack_start(add_location_button, False, False, 0)

        # 'Load Map' button
        records_button = Gtk.Button(label="Load Map")
        records_button.get_style_context().add_class("custom-button")
        records_button.connect("clicked", self.on_previous_records)
        self.center_box.pack_start(records_button, False, False, 0)

    def create_header_bar(self):
        """Creates a custom header bar with a title."""
        header_bar = Gtk.HeaderBar(title="Digital Heritage")
        header_bar.set_show_close_button(True)
        return header_bar

    def apply_css(self):
        """Applies custom CSS styles for buttons and switch."""
        css = """
        .custom-button {
            background-color: #007bff;
            color: white;
            font-size: 16px;
            padding: 10px;
            border-radius: 10px;
        }
        .custom-button:hover {
            background-color: #0056b3;
        }
        switch {
            background: #ccc;
            border-radius: 15px;
            padding: 3px;
        }
        switch slider {
            background: #fff;
            border-radius: 50%;
        }
        switch:checked {
            background: #007bff;
        }
        """

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css.encode("utf-8"))

        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def on_mode_switch(self, switch, state):
        """
        Handles the switch toggle between User Mode and Debugger Mode.
        Authentication is required for Debugger Mode.
        """
        if state:
            # Switching to Debugger Mode
            if self.authenticate_debugger():
                self.debugger_mode = True
                print("Switched to Debugger Mode")
            else:
                switch.set_active(False)  # Revert if authentication fails
                print("Authentication failed, staying in User Mode.")
        else:
            # Switching back to User Mode
            self.debugger_mode = False
            print("Switched to User Mode")

    def authenticate_debugger(self):
        """
        Displays an authentication dialog when switching to Debugger Mode.
        Returns True if authentication is successful, otherwise False.
        """
        dialog = Gtk.Dialog(
            title="Debugger Authentication",
            transient_for=self,
            flags=0,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        dialog.set_default_size(300, 150)

        grid = Gtk.Grid(margin=10, row_spacing=10, column_spacing=10)
        dialog.get_content_area().add(grid)

        username_label = Gtk.Label(label="Username:")
        grid.attach(username_label, 0, 0, 1, 1)
        username_entry = Gtk.Entry()
        grid.attach(username_entry, 1, 0, 1, 1)

        password_label = Gtk.Label(label="Password:")
        grid.attach(password_label, 0, 1, 1, 1)
        password_entry = Gtk.Entry()
        password_entry.set_visibility(False)
        grid.attach(password_entry, 1, 1, 1, 1)

        dialog.show_all()
        response = dialog.run()

        authenticated = False
        if response == Gtk.ResponseType.OK:
            username = username_entry.get_text()
            password = password_entry.get_text()
            if username == "debug" and password == "password":
                authenticated = True
            else:
                self.show_error_message("Incorrect username or password.")
        dialog.destroy()
        return authenticated

    def show_error_message(self, message):
        """
        Displays an error message dialog.
        """
        error_dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text="Authentication Error",
        )
        error_dialog.format_secondary_text(message)
        error_dialog.run()
        error_dialog.destroy()

    def on_add_location(self, button):
        """Handles adding a new map based on the current mode."""
        print("Add Map clicked.")
        self.hide()  # Hide the main window before opening a new one

        if self.debugger_mode:
            print("Opening Debugger Mode Map")
            new_map = Debug_New_Map(self)
        else:
            print("Opening User Mode Map")
            new_map = User_New_Map(self)

        new_map.show_all()

    def on_previous_records(self, button):
        """Handles viewing previous maps."""
        print("Load Map clicked.")
        self.set_keep_above(False)  # Allow new window to be above

        if self.debugger_mode:
            print("Loading records in Debugger Mode")
        else:
            print("Loading records in User Mode")

        from load_map import LoadMap
        records_window = LoadMap(self)
        records_window.show_all()
        self.hide()


# Run the application
if __name__ == "__main__":
    win = Application()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
