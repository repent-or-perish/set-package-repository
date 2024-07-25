#!/usr/bin/env python3 

import gi
import os
import sys
import shutil

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3

# Check if the script is run with root privileges
if os.geteuid() != 0:
    print("This script must be run as root. Use 'sudo python3 set_pkg_repo.py'")
    sys.exit(1)

CONFIG_FILE = '/etc/pkg/GhostBSD.conf'
BACKUP_FILE = '/etc/pkg/GhostBSD.conf.bak'

class RepoSelector:
    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new(
            "set-pkg-repo",
            "preferences-system",
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        
        # Create a menu
        self.menu = Gtk.Menu()
        
        # Add title item
        title_item = Gtk.MenuItem(label="Set Package Repository")
        title_item.set_sensitive(False)  # Make it non-clickable
        self.menu.append(title_item)
        
        # Add a separator
        self.menu.append(Gtk.SeparatorMenuItem())

        # Add repo options
        self.repos = {
            "GhostBSD_Unstable": ("http://pkg.ghostbsd.org/unstable/${ABI}/latest", "http://pkg.ghostbsd.org/unstable/${ABI}/base"),
            "GhostBSD_CA": ("https://pkg.ca.ghostbsd.org/stable/${ABI}/latest", "https://pkg.ca.ghostbsd.org/stable/${ABI}/base"),
            "GhostBSD": ("https://pkg.ghostbsd.org/stable/${ABI}/latest", "https://pkg.ghostbsd.org/stable/${ABI}/base"),
            "GhostBSD_FR": ("https://pkg.fr.ghostbsd.org/stable/${ABI}/latest", "https://pkg.fr.ghostbsd.org/stable/${ABI}/base"),
            "GhostBSD_NO": ("http://pkg.no.ghostbsd.org/stable/${ABI}/latest", "http://pkg.no.ghostbsd.org/stable/${ABI}/base"),
            "GhostBSD_ZA": ("https://pkg.za.ghostbsd.org/stable/${ABI}/latest", "https://pkg.za.ghostbsd.org/stable/${ABI}/base")
        }

        for name in self.repos.keys():
            menu_item = Gtk.MenuItem(label=name)
            menu_item.connect("activate", self.on_repo_selected, name)
            self.menu.append(menu_item)

        # Add quit option
        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", self.quit)
        self.menu.append(quit_item)

        self.menu.show_all()
        self.indicator.set_menu(self.menu)

    def on_repo_selected(self, widget, repo_name):
        latest_url, base_url = self.repos[repo_name]
        config = (
            f'{repo_name}: {{\n  url: "{latest_url}",\n  enabled: yes\n}}\n'
            f'{repo_name}_base: {{\n  url: "{base_url}",\n  enabled: yes\n}}\n'
        )
        try:
            # Backup existing configuration file
            if os.path.exists(CONFIG_FILE):
                shutil.copyfile(CONFIG_FILE, BACKUP_FILE)
            
            # Write new configuration
            with open(CONFIG_FILE, 'w') as f:
                f.write(config)
            self.show_message("Success", f'Repository {repo_name} selected and configuration updated.')
        except Exception as e:
            self.show_message("Error", str(e))

    def show_message(self, title, message):
        dialog = Gtk.MessageDialog(
            transient_for=None,
            flags=0,
            message_type=Gtk.MessageType.INFO if title == "Success" else Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=title,
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    def quit(self, widget):
        Gtk.main_quit()

if __name__ == "__main__":
    RepoSelector()
    Gtk.main()
