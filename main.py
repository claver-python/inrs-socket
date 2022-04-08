from kivymd.app import MDApp
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
# from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from client import Client
import re
import sys


pattern = re.compile(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")

class ChatScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MenuScreen(MDScreen):
    dialog = None
    chatroom_dialog = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ip_addr = None
        self.port_num = None
        self.clients = Client()


    """Setting up the account to login to chat screen"""
    def setup_acc(self):
        self.ip_addr = self.ids.ip.text
        self.port_num = self.ids.port.text

        """regex validation for ip address, ipv4"""
        if not pattern.match(self.ip_addr): 
            self.set_ip_error_message()

        
            """validating the port number"""
        elif len(self.port_num) > 4:
            self.set_port_error_message()

        else:

            self.ids.ip.readonly = True
            self.ids.port.readonly = True

        try:

            self.clients.connect(self.ip_addr, int(self.port_num))
            print(self.ip_addr, self.port_num)
            self.manager.current = "chat"
        except (ValueError, ConnectionRefusedError, OverflowError):
            self.show_alert_dialog()

    def set_ip_error_message(self):
        self.ids.ip.error = True

    def set_port_error_message(self):
        self.ids.port.error = True

    """Dialog to show error on the login screen"""
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
        self.dialog.dismiss()

    def send_msg(self, msg):
        try:
            self.clients.send(msg.text)
        except BrokenPipeError:
            self.chatroom_alert_dialog()


    """Dialog to show error on the chat screen"""
    def chatroom_alert_dialog(self):
        if not self.chatroom_dialog:
            self.chatroom_dialog = MDDialog(
                title = "Error!",
                text = "Something is wrong with the connection to the server.",
                buttons = [
                    MDRaisedButton(
                        text = "OK",
                        theme_text_color= "Custom",
                        text_color = "red",
                        on_release = self.chatroom_close_dialog
                    ),
                ]
            )
        self.chatroom_dialog.open()

    def chatroom_close_dialog(self, instance):
        self.ids.ip.readonly = False
        self.ids.port.readonly = False
        self.manager.current = "menu"
        self.chatroom_dialog.dismiss()


class MainScreen(ScreenManager):
    pass


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"


if __name__=="__main__":
    clients = MainApp()
    clients.run()
