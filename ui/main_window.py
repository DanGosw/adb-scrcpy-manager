
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ADB Wireless Manager
Interfaz gráfica para descubrir dispositivos en la red,
emparejarlos mediante ADB Wireless Debugging y conectarlos.

Requisitos:
    sudo apt install adb nmap python3-tk scrcpy
"""

import subprocess
import tkinter as tk

from tkinter import ttk, messagebox

from config.settings import (
    APP_NAME,
    CONFIG_DIR,
    get_adb_path,
    get_scrcpy_path,
    get_nmap_path
)

from core.network import (
    get_default_interface,
    get_interfaces
)

from core.device_store import DeviceStore
from core.adb_manager import ADBManager
from core.scrcpy_manager import ScrcpyManager
from core.task_manager import TaskManager
from core.log_manager import LogManager
from core.validators import valid_ip, valid_port

from ui.components.scrollable_frame import ScrollableFrame
from ui.pages.dashboard import DashboardPage
from ui.pages.scan import ScanPage
from ui.pages.devices import DevicesPage
from ui.pages.logs import LogsPage
from ui.pages.settings import SettingsPage
from ui.sidebar import Sidebar
from ui.theme import apply_theme, COLORS

# ============================================================
# Aplicación
# ============================================================

class ADBWirelessManager:

    def __init__(self, root):

        self.root = root
        self.root.title(APP_NAME)

        self.task_manager = TaskManager()
        self.store = DeviceStore()

        self.adb_path = get_adb_path()
        self.scrcpy_path = get_scrcpy_path()
        self.nmap_path = get_nmap_path()

        self.adb = ADBManager(self.adb_path)

        self.scrcpy = ScrcpyManager(
            self.scrcpy_path,
            CONFIG_DIR / "scrcpy.log"
        )

        self.interfaces = []

        self.interface_var = tk.StringVar()
        self.ip_var = tk.StringVar()

        self.pair_port_var = tk.StringVar()
        self.pair_code_var = tk.StringVar()

        self.connect_port_var = tk.StringVar()
        self.device_name_var = tk.StringVar()

        self.status_var = tk.StringVar(value="Preparado")

        self.build_ui()

        self.refresh_interfaces()
        self.refresh_saved_devices()

        self.root.after(120, self.poll_events)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    # --------------------------------------------------------
    # Interfaz
    # --------------------------------------------------------


    def build_ui(self):

        self.root.geometry("1180x800")
        self.root.minsize(950, 680)

        apply_theme(self.root)

       # Contenedor principal
        shell = tk.Frame(
            self.root,
            bg=COLORS["background"]
        )
        shell.pack(
            fill="both",
            expand=True
        )

        # Sidebar
        self.sidebar = Sidebar(
            shell,
            self.show_page
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )
 
        # Área principal
        workspace = tk.Frame(
            shell,
            bg=COLORS["background"]
        )
        workspace.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Encabezado
        header = tk.Frame(
            workspace,
            bg=COLORS["background"],
            bd=0,
            highlightthickness=0
        )
        header.pack(
            fill="x",
            padx=0
        )

        header_content = tk.Frame(
            header,
            bg=COLORS["background"]
        )
        header_content.pack(
            fill="x",
            padx=30,
            pady=22
        )

        self.page_title = tk.Label(
            header_content,
            text="Resumen",
            font=("Poppins", 19, "bold"),
            fg=COLORS["text"],
            bg=COLORS["background"]
        )
        self.page_title.pack(
            anchor="w"
        )

        self.page_subtitle = tk.Label(
            header_content,
            text="Estado general de ADB Wireless Manager",
            font=("Poppins", 9),
            fg=COLORS["text_secondary"],
            bg=COLORS["background"]
        )
        self.page_subtitle.pack(
            anchor="w",
            pady=(3, 0)
        )

        # Contenedor de páginas
        self.page_host = tk.Frame(
            workspace,
            bg=COLORS["background"]
        )
        self.page_host.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        # Registro de páginas
        self.pages = {}
        self.page_canvases = {}
        
        # Página: Dashboard
        self.dashboard_page = DashboardPage(
            self.create_scrollable_page("dashboard"),
            self
        )

        # Página: Escaneo de red
        self.scan_page = ScanPage(
            self.create_scrollable_page("scan"),
            self
        )

        # Página: Dispositivos
        self.devices_page = DevicesPage(
            self.create_scrollable_page("devices"),
            self
        )

        # Página: Registro
        self.logs_page = LogsPage(
            self.create_scrollable_page("logs"),
            self
        )

        # Página: Configuración
        self.settings_page = SettingsPage(
            self.create_scrollable_page("settings"),
            self
        )

        # Sistema centralizado de registros
        self.log_manager = LogManager(
            self.task_manager,
            self.log_text
        )

        # Página inicial
        self.show_page("dashboard")

        # Actualizar indicadores
        self.update_dashboard()
    # --------------------------------------------------------
    # Sistema de páginas
    # --------------------------------------------------------


    def create_scrollable_page(self, page_id):

        container = ScrollableFrame(
            self.page_host,
            root=self.root
        )

        self.pages[page_id] = container
        self.page_canvases[page_id] = container.canvas

        return container.content


    def show_page(self, page_id):

        if page_id not in self.pages:
            return

        for page in self.pages.values():
            page.pack_forget()

        self.pages[page_id].pack(
            fill="both",
            expand=True
        )

        titles = {
            "dashboard": (
                "Resumen",
                "Estado general de ADB Wireless Manager"
            ),
            "scan": (
                "Escanear red",
                "Descubre y conecta dispositivos de tu red local"
            ),
            "devices": (
                "Dispositivos",
                "Administra tus dispositivos guardados y conexiones ADB"
            ),
            "logs": (
                "Registro",
                "Historial de operaciones y diagnóstico"
            ),
            "settings": (
                "Ajustes",
                "Configuración y herramientas del sistema"
            )
        }

        title, subtitle = titles[page_id]

        self.page_title.configure(text=title)
        self.page_subtitle.configure(text=subtitle)

        self.sidebar.set_active(page_id)

    # --------------------------------------------------------
    # Componentes visuales
    # --------------------------------------------------------

    
    def create_card(
        self,
        parent,
        title,
        description,
        accent=None
    ):

        accent = accent or COLORS["accent"]

        card = tk.Frame(
            parent,
            bg=COLORS["surface"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            bd=0
        )

        header = tk.Frame(
            card,
            bg=COLORS["surface"]
        )
        header.pack(
            fill="x",
            padx=18,
            pady=(16, 5)
        )

        indicator = tk.Frame(
            header,
            bg=accent,
            width=3,
            height=18
        )
        indicator.pack(
            side="left",
            padx=(0, 10)
        )
        indicator.pack_propagate(False)

        tk.Label(
            header,
            text=title,
            font=("Poppins", 11, "bold"),
            fg=COLORS["text"],
            bg=COLORS["surface"]
        ).pack(
            side="left",
            anchor="center"
        )

        tk.Label(
            card,
            text=description,
            font=("Poppins", 9),
            fg=COLORS["text_secondary"],
            bg=COLORS["surface"],
            justify="left",
            wraplength=600
        ).pack(
            anchor="w",
            padx=18,
            pady=(5, 17)
        )

        return card


    # --------------------------------------------------------
    # Actualización visual del dashboard
    # --------------------------------------------------------

    def update_dashboard(self):

        checks = [
            ("adb_status_label", "ADB", self.adb_path),
            ("scrcpy_status_label", "scrcpy", self.scrcpy_path),
            ("nmap_status_label", "Nmap", self.nmap_path)
        ]

        for attribute, name, path in checks:

            label = getattr(self, attribute, None)

            if not label:
                continue

            if path:
                label.configure(
                    text=f"{name}\nDisponible",
                    fg=COLORS["green"]
                )
            else:
                label.configure(
                    text=f"{name}\nNo encontrado",
                    fg=COLORS["red"]
                )

        if hasattr(self, "saved_count_label"):
            self.saved_count_label.configure(
                text=f"Dispositivos guardados\n{len(self.store.devices)}"
            )

        if hasattr(self, "dashboard_connection_label"):
            self.dashboard_connection_label.configure(
                text=f"Estado: {self.status_var.get()}"
            )


    # --------------------------------------------------------
    # Registro seguro para Tkinter
    # --------------------------------------------------------

    def log(self, message):
        self.log_manager.log(message)


    def append_log(self, message):
        self.log_manager.append(message)

    # --------------------------------------------------------
    # Trabajos en segundo plano
    # --------------------------------------------------------

    def worker(self, function, callback=None):

        try:
            self.task_manager.submit(function, callback)

        except RuntimeError as error:
            messagebox.showwarning(
                APP_NAME,
                str(error)
            )
            return

        self.status_var.set("Procesando...")


    
    def poll_events(self):

        if self.task_manager.closing:
            return

        try:
            for kind, data, callback in self.task_manager.get_events():

                if kind == "log":
                    self.append_log(data)
                    continue

                self.task_manager.busy = False

                if kind == "success":

                    self.status_var.set("Operación completada")
                    self.update_dashboard()

                    if callback:
                        try:
                            callback(data)

                        except Exception as error:
                            self.log(
                                f"ERROR en callback: {error}"
                            )

                            messagebox.showerror(
                                APP_NAME,
                                f"Error al actualizar la interfaz:\n{error}"
                            )

                elif kind == "error":

                    self.status_var.set("Error en la operación")
                    self.update_dashboard()
                    self.log(f"ERROR: {data}")

                    messagebox.showerror(
                        APP_NAME,
                        data
                    )

        finally:
            if not self.task_manager.closing:
                self.root.after(120, self.poll_events)


    # --------------------------------------------------------
    # ADB
    # --------------------------------------------------------

    def require_adb(self):
        return self.adb.require_adb()


    def adb_command(self, arguments, timeout=30):
        self.log("Ejecutando: adb " + " ".join(arguments))

        result = self.adb.run(
            arguments,
            timeout=timeout
        )

        output = result["stdout"]
        error = result["stderr"]

        if output:
            self.log(output)

        if error:
            self.log(error)

        return output

    # --------------------------------------------------------
    # Interfaces
    # --------------------------------------------------------

    def refresh_interfaces(self):

        def task():

            interfaces = get_interfaces()

            if not interfaces:
                raise RuntimeError(
                    "No se encontraron interfaces IPv4."
                )

            return interfaces

        def done(interfaces):

            self.interfaces = interfaces

            values = [
                item["name"]
                for item in interfaces
            ]

            self.interface_combo["values"] = values

            default = get_default_interface()

            selected = next(
                (
                    item["name"]
                    for item in interfaces
                    if item["name"] == default
                ),
                values[0]
            )

            self.interface_var.set(selected)
            self.update_network_info()

            self.log(
                f"Interfaces detectadas: {', '.join(values)}"
            )

        self.worker(task, done)

    def update_network_info(self):

        selected = self.interface_var.get()

        interface = next(
            (
                item for item in self.interfaces
                if item["name"] == selected
            ),
            None
        )

        if interface:
            self.network_info.configure(
                text=(
                    f"IP local: {interface['ip']} | "
                    f"Red: {interface['address']}"
                )
            )

    # --------------------------------------------------------
    # Escaneo de red
    # --------------------------------------------------------

    def scan_network(self):

        if not self.nmap_path:
            messagebox.showerror(
                APP_NAME,
                "No se encontró nmap.\n"
                "Instálalo con: sudo apt install nmap"
            )
            return

        selected = self.interface_var.get()

        interface = next(
            (
                item for item in self.interfaces
                if item["name"] == selected
            ),
            None
        )

        if not interface:
            messagebox.showerror(
                APP_NAME,
                "Selecciona una interfaz válida."
            )
            return

        network = interface["address"]

        def task():

            self.log(f"Escaneando red {network}...")

            result = subprocess.run(
                [
                    self.nmap_path,
                    "-sn",
                    "-n",
                    network
                ],
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode != 0:
                raise RuntimeError(
                    result.stderr.strip() or "Error de nmap."
                )

            devices = []
            current = None

            for line in result.stdout.splitlines():

                if line.startswith("Nmap scan report for"):

                    if current:
                        devices.append(current)

                    value = line.replace(
                        "Nmap scan report for",
                        ""
                    ).strip()

                    hostname = ""
                    ip = value

                    if "(" in value and ")" in value:
                        hostname = value.split("(")[0].strip()
                        ip = value.split("(")[1].split(")")[0]

                    current = {
                        "ip": ip,
                        "hostname": hostname
                    }

            if current:
                devices.append(current)

            return devices

        def done(devices):

            for item in self.scan_tree.get_children():
                self.scan_tree.delete(item)

            for device in devices:

                self.scan_tree.insert(
                    "",
                    "end",
                    values=(
                        device["ip"],
                        device["hostname"] or "Desconocido",
                        "Detectado"
                    )
                )

            self.log(
                f"Escaneo terminado: {len(devices)} dispositivos."
            )

        self.worker(task, done)

    def on_scan_selection(self, _event=None):

        selected = self.scan_tree.selection()

        if not selected:
            return

        values = self.scan_tree.item(
            selected[0],
            "values"
        )

        if values:
            self.ip_var.set(values[0])

            if not self.device_name_var.get():
                self.device_name_var.set(
                    values[1] if values[1] != "Desconocido" else ""
                )

    # --------------------------------------------------------
    # Validación
    # --------------------------------------------------------

    def get_ip(self):

        ip = self.ip_var.get().strip()

        if not valid_ip(ip):
            raise ValueError(
                "Introduce una dirección IP válida, "
                "sin incluir el puerto."
            )

        return ip

    # --------------------------------------------------------
    # Emparejamiento
    # --------------------------------------------------------

    def pair_device(self):

        try:
            ip = self.get_ip()

            pairing_port = self.pair_port_var.get().strip()
            pairing_code = self.pair_code_var.get().strip()

            if not valid_port(pairing_port):
                raise ValueError(
                    "Puerto de emparejamiento inválido."
                )

            if not pairing_code:
                raise ValueError(
                    "Introduce el código de emparejamiento."
                )

        except ValueError as error:

            messagebox.showwarning(
                APP_NAME,
                str(error)
            )
            return

        # Capturamos los valores antes de iniciar el hilo.
        target = f"{ip}:{int(pairing_port)}"
        code = pairing_code

        self.pair_code_var.set("")

        def task():

            self.log(f"Ejecutando: adb pair {target} [código oculto]")

            result = self.adb.run(
                ["pair", target, code],
                timeout=60
            )

            output = result["stdout"]
            error = result["stderr"]

            if output:
                self.log(output)

            if error:
                self.log(error)

            return output

        def done(output):

            self.log("Emparejamiento finalizado.")

            messagebox.showinfo(
                APP_NAME,
                output or "Emparejamiento completado."
            )

        self.worker(task, done)

    # --------------------------------------------------------
    # Conexión
    # --------------------------------------------------------


    def connect_device(self):

        try:
            ip = self.get_ip()
            port = self.connect_port_var.get().strip()

            if not valid_port(port):
                raise ValueError("Puerto de conexión inválido.")

        except ValueError as error:
            messagebox.showwarning(APP_NAME, str(error))
            return

        target = f"{ip}:{int(port)}"

        def task():

            self.log(f"Conectando con {target}...")

            output = self.adb.connect_and_verify(target)

            self.log(f"ADB reconoce el dispositivo {target}.")

            result = self.scrcpy.launch(target)

            return {
                "target": target,
                "pid": result["pid"],
                "adb_output": output
            }

        def done(result):

            self.log(f"ADB conectado: {result['target']}")

            self.log(
                f"scrcpy iniciado correctamente. PID: {result['pid']}"
            )

            self.status_var.set(
                "Dispositivo conectado y reflejándose"
            )

            messagebox.showinfo(
                APP_NAME,
                f"Dispositivo conectado:\n{result['target']}\n\n"
                "scrcpy se ha iniciado correctamente."
            )

            self.refresh_adb(silent=True)

        self.worker(task, done)

    # --------------------------------------------------------
    # Guardar dispositivos
    # --------------------------------------------------------

    def save_device(self):

        try:

            ip = self.get_ip()
            port = self.connect_port_var.get().strip()

            if not valid_port(port):
                raise ValueError(
                    "Introduce un puerto de conexión válido."
                )

            name = self.device_name_var.get().strip()

            if not name:
                name = ip

            self.store.add(
                name,
                ip,
                int(port)
            )

            self.refresh_saved_devices()

            self.log(f"Dispositivo guardado: {name}")

        except ValueError as error:

            messagebox.showwarning(
                APP_NAME,
                str(error)
            )

        except Exception as error:

            messagebox.showerror(
                APP_NAME,
                str(error)
            )

    def refresh_saved_devices(self):

        for item in self.saved_tree.get_children():
            self.saved_tree.delete(item)

        for index, device in enumerate(self.store.devices):

            self.saved_tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    device["name"],
                    device["ip"],
                    device["port"]
                )
            )

    def get_saved_selection(self):

        selected = self.saved_tree.selection()

        if not selected:
            messagebox.showwarning(
                APP_NAME,
                "Selecciona un dispositivo guardado."
            )
            return None


    def reconnect_saved(self):

        index = self.get_saved_selection()

        if index is None:
            return

        device = self.store.devices[index]

        target = f"{device['ip']}:{device['port']}"

        self.ip_var.set(device["ip"])
        self.connect_port_var.set(str(device["port"]))
        self.device_name_var.set(device["name"])

        def task():

            return self.adb_command(
                ["connect", target],
                timeout=30
            )

        def done(output):

            self.log(
                f"Reconexión ejecutada para {device['name']}."
            )

            messagebox.showinfo(
                APP_NAME,
                output or "Comando de reconexión ejecutado."
            )

            self.refresh_adb(silent=True)

        self.worker(task, done)

    def rename_saved(self):

        index = self.get_saved_selection()

        if index is None:
            return

        current = self.store.devices[index]["name"]

        dialog = tk.Toplevel(self.root)
        dialog.title("Renombrar dispositivo")
        dialog.geometry("320x120")
        dialog.transient(self.root)
        dialog.grab_set()

        value = tk.StringVar(value=current)

        ttk.Label(
            dialog,
            text="Nuevo nombre:"
        ).pack(pady=8)

        entry = ttk.Entry(
            dialog,
            textvariable=value
        )
        entry.pack(fill="x", padx=12)
        entry.focus_set()

        def save():

            name = value.get().strip()

            if not name:
                return

            self.store.rename(index, name)
            self.refresh_saved_devices()
            dialog.destroy()

        ttk.Button(
            dialog,
            text="Guardar",
            command=save
        ).pack(pady=8)

    def delete_saved(self):

        index = self.get_saved_selection()

        if index is None:
            return

        device = self.store.devices[index]

        if not messagebox.askyesno(
            APP_NAME,
            f"¿Eliminar {device['name']}?"
        ):
            return

        self.store.delete(index)
        self.refresh_saved_devices()

        self.log(
            f"Dispositivo eliminado: {device['name']}"
        )

    # --------------------------------------------------------
    # Listar dispositivos ADB
    # --------------------------------------------------------

    def refresh_adb(self, silent=False):

        def task():

            output = self.adb_command(
                ["devices", "-l"],
                timeout=20
            )

            return output

        def done(output):

            if not silent:
                messagebox.showinfo(
                    "Dispositivos ADB",
                    output or "No hay dispositivos."
                )

        self.worker(task, done)

    # --------------------------------------------------------
    # Desconectar
    # --------------------------------------------------------

    def disconnect_device(self):

        try:

            ip = self.get_ip()
            port = self.connect_port_var.get().strip()

            if not valid_port(port):
                raise ValueError(
                    "Puerto de conexión inválido."
                )

        except ValueError as error:

            messagebox.showwarning(
                APP_NAME,
                str(error)
            )
            return

        target = f"{ip}:{int(port)}"

        def task():

            return self.adb_command(
                ["disconnect", target],
                timeout=20
            )

        self.worker(task)

    # --------------------------------------------------------
    # scrcpy
    # --------------------------------------------------------


    def launch_scrcpy(self):

        try:
            ip = self.get_ip()
            port = self.connect_port_var.get().strip()

            if not valid_port(port):
                raise ValueError("Puerto de conexión inválido.")

        except ValueError as error:
            messagebox.showwarning(APP_NAME, str(error))
            return

        target = f"{ip}:{int(port)}"

        def task():

            self.require_adb()

            if not self.adb.is_connected(target):

                available = self.adb.get_connected_devices()

                raise RuntimeError(
                    f"El dispositivo {target} no está conectado.\n\n"
                    "Dispositivos disponibles:\n"
                    + (
                        "\n".join(
                            f"{serial} [{state}]"
                            for serial, state in available.items()
                        )
                        if available else "Ninguno"
                    )
                )

            return self.scrcpy.launch(target)

        def done(result):

            self.log(
                f"scrcpy iniciado para {result['target']} "
                f"(PID: {result['pid']})."
            )

            self.status_var.set("scrcpy iniciado")

        self.worker(task, done)


    # --------------------------------------------------------
    # Cierre
    # --------------------------------------------------------

    def close(self):

        if self.task_manager.busy:

            if not messagebox.askyesno(
                APP_NAME,
                "Hay una operación en ejecución. "
                "¿Deseas cerrar la aplicación?"
            ):
                return

        self.task_manager.closing = True

        # No se ejecuta adb kill-server.
        # No se finalizan procesos scrcpy.
        self.root.destroy()


# ============================================================
# Inicio
# ============================================================

def main():

    root = tk.Tk()

    try:
        ttk.Style().theme_use("clam")
    except tk.TclError:
        pass

    ADBWirelessManager(root)

    root.mainloop()


if __name__ == "__main__":
    main()
