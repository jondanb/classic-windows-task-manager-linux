import gi
import os
import time
import dbus
import shlex
import shutil
import psutil
import subprocess

gi.require_version("Gtk", "3.0")
gi.require_version("Gio", "2.0")
gi.require_version("AccountsService", "1.0")

from gi.repository import Gio, Gtk, AccountsService, GLib

from PyQt5.QtGui import QIcon, QImage, QPixmap


SYSTEM_NETWORK_INTERFACE_TYPE_MAP = {
    "lo": "Local Area Connection",
    "eth": "Ethernet Connection",
    "en": "Ethernet Connection",
    "eno": "Ethernet Onboard Connection",
    "ens": "Ethernet Slot Connection",
    "enp": "Ethernet Port Connection",
    "enx": "Ethernet MAC Address Connection",
    "ib": "InfiniBand Connection",
    "sl": "Serial Line IP (SLIP) Connection",
    "wlan": "Wireless Local Area Connection",
    "wl": "Wireless Local Area Connection",
    "ww": "Wireless Wide Area Connection",
    "docker": "Docker Bridge Connection",
    "br": "Docker Bridge Connection",
    "veth": "Virtual Ethernet Connection",
}


def get_all_running_processes_info():
    """
    Retreives all the system's current running procceses' information which includes their:
        - PID (Process Identification)
        - Process name
        - User/group the process is running on
        - Process CPU usage
        - Process memory usage
        - Process command
        - Process executable path
    """
    for proc in psutil.process_iter(
        ["pid", "name", "username", "cpu_percent", "memory_info", "cmdline"]):
        try:
            process_exe_path = proc.exe()
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            process_exe_path = ""
        yield (proc.info["name"], proc.info["pid"], proc.info["username"],
               proc.info["cpu_percent"], proc.info["memory_info"], proc.info["cmdline"],
               process_exe_path) # get the executable path for properties window
        

def get_all_running_applications_names():
    """
    Retreives all the system's current running applications' information which includes their:
        - PID
        - Name
        - Executable path
        - Application command

    This function is not 100% accurate and may skip certain running applications on the system(to be fixed)
    """
    running_apps = []
    processes = [proc.info for proc in psutil.process_iter(["pid", "name", "exe", "cmdline"])]
    desktop_files = Gio.AppInfo.get_all()

    desktop_execs = {}
    for app in desktop_files:
        app_info = Gio.DesktopAppInfo.new(app.get_id())
        if app_info:
            exec_line = app_info.get_executable()
            desktop_execs[exec_line] = app_info
    
    for proc in processes:
        exec_name = os.path.basename(
            proc["exe"]
        ) if proc["exe"] else proc["name"]
        cmdlines = [os.path.basename(cmd) for cmd in proc["cmdline"]] if proc["cmdline"] else []

        if exec_name in desktop_execs:
            running_apps.append((desktop_execs[exec_name], proc["pid"]))
        else:
            for cmd in cmdlines:
                if cmd in desktop_execs:
                    running_apps.append((desktop_execs[cmd], proc["pid"]))
                    break

    return running_apps

def get_all_running_applications(running_apps):
    """
    Retreives full details about each running application on the system. This function expects the output
    of `get_all_running_applications_names` in order to find the icons for the apps.
    """
    app_details = []
    for app_info, app_pid in running_apps:
        app_name = app_info.get_name()
        icon = app_info.get_icon()
        if icon:
            icon_theme = Gtk.IconTheme.get_default()
            icon_info = icon_theme.lookup_by_gicon(icon, 48, Gtk.IconLookupFlags.FORCE_SIZE)
            if icon_info:
                pixbuf = icon_info.load_icon()
                image = Gtk.Image.new_from_pixbuf(pixbuf)
                app_details.append((app_name, app_pid, image))
            else:
                app_details.append((app_name, app_pid, None))
        else:
            app_details.append((app_name, app_pid, None))
    return app_details

def execute_system_uri_command(command):
    if shutil.which(command) is not None:
        return subprocess.call(shlex.split(command))
    return subprocess.call(["xdg-open"] + shlex.split(command))

def show_file_properties(filepath):
    session_bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)

    proxy = Gio.DBusProxy.new_sync(
        session_bus, Gio.DBusProxyFlags.NONE,
        None,
        "org.freedesktop.FileManager1",
        "/org/freedesktop/FileManager1",
        "org.freedesktop.FileManager1",
        None
    )

    proxy.call_sync(
        "ShowItemProperties",
        GLib.Variant("(ass)", ([filepath], filepath)),
        Gio.DBusCallFlags.NONE, -1, None
    )

def gtk_image_to_qicon(gtk_image):
    gtk_image_pixbuf = gtk_image.get_pixbuf()
    raw_gtk_image = gtk_image_pixbuf.get_pixels()
    width, height, rowstride, n_channels = (
        gtk_image_pixbuf.get_width(), gtk_image_pixbuf.get_height(),
        gtk_image_pixbuf.get_rowstride(), gtk_image_pixbuf.get_n_channels()
    )
    image_format = QImage.Format_RGB888 if n_channels == 3 else QImage.Format_RGBA8888
    qimage = QImage(raw_gtk_image, width, height, rowstride, image_format)
    qpixmap = QPixmap.fromImage(qimage)
    qicon = QIcon(qpixmap)
    return qicon

def set_nice_of_process(pid: int, nice: int):
    """
    Sets the niceness of a process by its PID

    Arguments:
        - pid (int): The process ID of the process to set niceness
        - nice (int): The niceness to set the process
    """
    process = psutil.Process(pid)
    process.set_nice(nice)

def get_all_system_services():
    l_bus = dbus.SystemBus()
    l_systemd = l_bus.get_object(
        "org.freedesktop.systemd1", "/org/freedesktop/systemd1"
    )
    l_manager = dbus.Interface(
        l_systemd, "org.freedesktop.systemd1.Manager"
    )

    service_units = l_manager.ListUnits()

    for (svc_name, svc_desc, svc_load_status, svc_running_status,
         _, _, svc_path, _, _ , _) in service_units:
        if svc_name.endswith(".service"):
            svc_pid = get_pid_from_service_obj_path(l_bus, svc_path)
            yield (svc_name, svc_pid, svc_desc, svc_running_status)

def get_all_user_accounts_details():
    manager = AccountsService.UserManager.get_default()
    for user in manager.list_users():
        yield (user.get_user_name(), user.get_uid(),
               user.is_logged_in(), user.get_real_name(),
               user.get_home_dir())

def get_user_account_type_icon(all_user_info):
    icon_theme = Gtk.IconTheme.get_default()

    user_uids = [user_uid for (_, user_uid, *_) in all_user_info]
    main_user_uid = min(user_uids)

    for user_uid in user_uids:
        icon_name = "user-identity" if user_uid == main_user_uid \
                        else "system-config-users"
        icon_info = icon_theme.lookup_icon(
            icon_name, 48, Gtk.IconLookupFlags.FORCE_SIZE
        )
        
        if icon_info:
            pixbuf = icon_info.load_icon()
            image = Gtk.Image.new_from_pixbuf(pixbuf)
            yield image

def end_process_by_pid(pid, *, end_process_tree=False):
    selected_process = psutil.Process(pid)

    if end_process_tree:
        for child_process in selected_process.children(recursive=True):
            child_process.kill()

    selected_process.terminate()

def check_if_network_interface_is_connected(interface_name):
    interface_stats = psutil.net_if_stats()

    if interface_name in interface_stats:
        return interface_stats[interface_name].isup
    else:
        return False 

def get_pid_from_service_obj_path(bus, service_obj_path):
    dbus_unit_obj = bus.get_object(
        "org.freedesktop.systemd1", service_obj_path
    )
    dbus_unit_props = dbus.Interface(
        dbus_unit_obj, dbus.PROPERTIES_IFACE
    )
    service_pid = dbus_unit_props.Get(
        "org.freedesktop.systemd1.Service", "MainPID"
    )

    return service_pid

def get_network_interface_link_speed(network_interface: str) -> str:
    nmcli_interface_output = subprocess.check_output(
        ["nmcli",  "-f", "CAPABILITIES.SPEED", "dev", "show", network_interface])
    nmcli_interface_output = b" ".join(nmcli_interface_output.strip().split()[1:]).decode()
    return "-" if nmcli_interface_output == "unknown" else nmcli_interface_output

def get_interface_type_full_name(interface):
    for prefix, iface_type in SYSTEM_NETWORK_INTERFACE_TYPE_MAP.items():
        if interface.startswith(prefix):
            return iface_type
    return "Unknown Network Interface"

def get_number_of_handle_file_descriptors():
    return len(os.listdir("/proc/self/fd"))

def get_number_of_total_threads(total_processes):
    number_of_threads = 0
    for proc in total_processes:
        try:
            number_of_threads += proc.num_threads()
        except psutil.NoSuchProcess:
            pass
    return number_of_threads

def get_total_uptime_in_seconds():
    return time.time() - psutil.boot_time()

def get_total_system_commit_memory(mem):
    return mem.total, mem.total - mem.available

def format_seconds_to_timestamp(seconds):
    mins, secs = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)
    days, hours = divmod(hours, 24)
    return f"{int(days)}:{int(hours):02}:{int(mins):02}:{int(secs):02}"

def convert_proc_mem_b_to_mb(mem_info, *, include_unit_label=True):
    return f"{mem_info / 1024 / 1024:.0f}" + ("MB" if include_unit_label else "")

def get_memory_size_info(size_bytes):
    if size_bytes < 1024:
        return size_bytes, 'B'
    elif size_bytes < 1024**2:
        return round(size_bytes / 1024, 2), 'KB'
    elif size_bytes < 1024**3:
        return round(size_bytes / (1024**2), 2), 'MB'
    elif size_bytes < 1024**4:
        return round(size_bytes / (1024**3), 2), 'GB'
    else:
        return round(size_bytes / (1024**4), 2), 'TB'