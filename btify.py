import gi
import subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

# Define your CSS styles here
css_data = """
/* Define CSS classes for different states */
.running {
    background-color: #00FF00; /* Green */
}

.stopped {
    background-color: #FF0000; /* Red */
}

.error {
    background-color: #FF0000; /* Red */
}
"""

# Function to start the Bluetooth service
def start_bluetooth(widget):
    try:
        subprocess.run(["sudo", "systemctl", "start", "bluetooth.service"], check=True)
        status_label.set_text("Running")
        status_label.get_style_context().add_class("running")  # Apply CSS class for running
    except subprocess.CalledProcessError:
        status_label.set_text("Error starting")
        status_label.get_style_context().add_class("error")  # Apply CSS class for error

# Function to stop the Bluetooth service
def stop_bluetooth(widget):
    try:
        subprocess.run(["sudo", "systemctl", "stop", "bluetooth.service"], check=True)
        status_label.set_text("Stopped")
        status_label.get_style_context().add_class("stopped")  # Apply CSS class for stopped
    except subprocess.CalledProcessError:
        status_label.set_text("Error stopping")
        status_label.get_style_context().add_class("error")  # Apply CSS class for error

def get_initial_bluetooth_status():
    try:
        result = subprocess.run(["sudo", "systemctl", "is-active", "bluetooth.service"], stdout=subprocess.PIPE)
        return result.stdout.decode().strip()
    except subprocess.CalledProcessError:
        return "Error"
    
# Create the GTK window
window = Gtk.Window(title="Bluetooth Control")
window.connect("destroy", Gtk.main_quit)
window.set_default_size(400, 300)  # Set the window size
window.set_resizable(False)  # Disable window resizing


# Create buttons
start_button = Gtk.Button(label="Start Bluetooth")
start_button.connect("clicked", start_bluetooth)
stop_button = Gtk.Button(label="Stop Bluetooth")
stop_button.connect("clicked", stop_bluetooth)

# Create a label for status and set the initial status
initial_status = get_initial_bluetooth_status()
status_label = Gtk.Label()
status_label.set_text(f"Status: {initial_status}")
status_label.set_margin_start(10)
status_label.set_margin_end(10)

# Create a vertical box to hold the widgets
vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
vbox.pack_start(start_button, False, False, 0)
vbox.pack_start(stop_button, False, False, 0)
vbox.pack_start(status_label, False, False, 0)

# Add the box to the window
window.add(vbox)

# Load CSS styles from the embedded data
css_provider = Gtk.CssProvider()
css_provider.load_from_data(css_data.encode())  # Load the CSS data

screen = Gdk.Screen.get_default()
style_context = Gtk.StyleContext()
style_context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


# Show all widgets
window.show_all()

# Start the GTK main loop
Gtk.main()
