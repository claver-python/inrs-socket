from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
import server 
from kivy.clock import Clock
from kivy.uix.label import Label
from threading import Thread
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
import sys
import re

pattern = re.compile(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")
server_socket = server.Server()
server_connected = False

class ListenScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "listen"

        def on_messsage(msg):
            self.ids.chat_history.text += "\n[Message]-> " + msg

        MainScreen.register_cb(on_messsage)


    def server_start(self):
        server_socket.run()

    def server_stop(self):
        server_connected = False
        server_socket.stop()



class LoginScreen(MDScreen):
    dialog = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.name = "login_server"

        self.ip = None
        self.port = None
        self.server = None
        # self.server_connected = False

    """Method to set up the server and go to the Listen Screen"""
    def server_listen(self):
        self.ip = self.ids.ip.text
        self.port = self.ids.port.text

        """regex validation for ip address, ipv4"""
        if not pattern.match(self.ip): 
            self.set_ip_error_message()

        
            """validating the port number"""
        elif len(self.port) > 4:
            self.set_port_error_message()

        else:

            self.ids.ip.readonly = True
            self.ids.port.readonly = True

            try:
                server_socket.bind(self.ip, int(self.port)).run()
                server_connected = True
                self.manager.current = 'listen'
            except (ValueError, ConnectionRefusedError, OverflowError):
                self.show_alert_dialog()

    def set_ip_error_message(self):
        self.ids.ip.error = True

    def set_port_error_message(self):
        self.ids.port.error = True

    """Dialog to show errors on the login screen"""
    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = "Error!",
                text = "Something is wrong, try to run the software again.",
                buttons = [
                    MDRaisedButton(
                        text = "OK",
                        theme_text_color= "Custom",
                        text_color = "red",
                        on_release = self.close_dialog
                    ),
                ]
            )
        self.dialog.open()

    def close_dialog(self, instance):
        sys.exit()

    """Exit the software on the login screeen"""
    def exit_software(self):
        if server_connected:
            print(True)
            server_socket.stop()
            sys.exit()
        else:
            sys.exit()
        
class MainScreen(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    @staticmethod
    def register_cb(cb):
        server_socket.register_cb(cb)


class ServerKv(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"


if __name__=="__main__":
    server_terminal = ServerKv()
    server_terminal.run()
