"""
Aplicación móvil para acceso a tablero Power BI
con gestión de autorizaciones mediante CSV en OneDrive
"""

# Configurar Kivy antes de importar para evitar conflictos con argumentos
import os
os.environ['KIVY_NO_ARGS'] = '1'

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationLayout, MDNavigationDrawer
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.utils import platform

import threading
from auth_manager import AuthManager
from powerbi_manager import PowerBIManager
from config_manager import ConfigManager


class LoginScreen(MDScreen):
    """Pantalla de login para autenticación de usuarios"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "login"
        self.auth_manager = AuthManager()
        self.build_ui()

    def build_ui(self):
        """Construye la interfaz de usuario de login"""
        main_layout = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            spacing=dp(20),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        # Logo/Título
        title = MDLabel(
            text="Tablero Móvil Power BI",
            theme_text_color="Primary",
            font_style="H4",
            halign="center",
            size_hint_y=None,
            height=dp(80)
        )

        # Card contenedor
        card = MDCard(
            orientation="vertical",
            spacing=dp(20),
            padding=dp(20),
            size_hint=(0.8, None),
            height=dp(300),
            pos_hint={"center_x": 0.5},
            elevation=3
        )

        # Campo de usuario
        self.username_field = MDTextField(
            hint_text="Usuario",
            icon_left="account",
            size_hint_x=1,
            mode="rectangle"
        )

        # Campo de contraseña
        self.password_field = MDTextField(
            hint_text="Contraseña",
            icon_left="lock",
            password=True,
            size_hint_x=1,
            mode="rectangle"
        )

        # Botón de login
        login_btn = MDRaisedButton(
            text="Iniciar Sesión",
            size_hint=(1, None),
            height=dp(40),
            on_release=self.authenticate
        )

        # Barra de progreso
        self.progress_bar = MDProgressBar(
            size_hint_y=None,
            height=dp(4),
            opacity=0
        )

        # Agregar elementos al card
        card.add_widget(self.username_field)
        card.add_widget(self.password_field)
        card.add_widget(login_btn)
        card.add_widget(self.progress_bar)

        # Agregar al layout principal
        main_layout.add_widget(title)
        main_layout.add_widget(card)

        self.add_widget(main_layout)

    def authenticate(self, instance):
        """Autentica al usuario"""
        username = self.username_field.text.strip()
        password = self.password_field.text.strip()

        if not username or not password:
            self.show_error("Por favor ingrese usuario y contraseña")
            return

        self.show_loading(True)

        # Ejecutar autenticación en hilo separado
        threading.Thread(
            target=self._authenticate_async,
            args=(username, password)
        ).start()

    def _authenticate_async(self, username, password):
        """Proceso de autenticación asíncrono"""
        try:
            success = self.auth_manager.authenticate(username, password)
            Clock.schedule_once(
                lambda dt: self._on_auth_complete(success), 0
            )
        except Exception as e:
            Clock.schedule_once(
                lambda dt: self._on_auth_error(str(e)), 0
            )

    def _on_auth_complete(self, success):
        """Callback cuando la autenticación se completa"""
        self.show_loading(False)

        if success:
            # Cambiar a pantalla principal
            app = MDApp.get_running_app()
            app.root.current = "dashboard"
        else:
            self.show_error("Credenciales inválidas")

    def _on_auth_error(self, error_msg):
        """Callback cuando hay error en autenticación"""
        self.show_loading(False)
        self.show_error(f"Error de autenticación: {error_msg}")

    def show_loading(self, show):
        """Muestra/oculta indicador de carga"""
        self.progress_bar.opacity = 1 if show else 0
        self.username_field.disabled = show
        self.password_field.disabled = show

    def show_error(self, message):
        """Muestra mensaje de error"""
        Snackbar(
            text=message,
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=(1 - (20 / self.width))
        ).open()


class DashboardScreen(MDScreen):
    """Pantalla principal con el tablero Power BI"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "dashboard"
        self.powerbi_manager = PowerBIManager()
        self.build_ui()

    def build_ui(self):
        """Construye la interfaz principal"""
        # Layout principal con navegación
        nav_layout = MDNavigationLayout()

        # Screen manager para contenido principal
        screen_manager = MDScreenManager()

        # Pantalla del tablero
        dashboard_screen = MDScreen()

        # Toolbar
        toolbar = MDTopAppBar(
            title="Tablero Power BI",
            left_action_items=[["menu", lambda x: nav_layout.set_state("open")]],
            right_action_items=[
                ["refresh", self.refresh_dashboard],
                ["logout", self.logout]
            ]
        )

        # Contenedor del tablero
        self.dashboard_container = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(10)
        )

        # Scroll view para el contenido
        scroll = MDScrollView()
        scroll.add_widget(self.dashboard_container)

        # Layout principal de la pantalla
        main_layout = MDBoxLayout(orientation="vertical")
        main_layout.add_widget(toolbar)
        main_layout.add_widget(scroll)

        dashboard_screen.add_widget(main_layout)
        screen_manager.add_widget(dashboard_screen)

        # Drawer de navegación
        nav_drawer = MDNavigationDrawer()
        nav_drawer_content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(20)
        )

        drawer_title = MDLabel(
            text="Menú",
            font_style="H6",
            size_hint_y=None,
            height=dp(40)
        )

        # Botones del drawer
        refresh_btn = MDRaisedButton(
            text="Actualizar Datos",
            size_hint_y=None,
            height=dp(40),
            on_release=self.refresh_data
        )

        settings_btn = MDRaisedButton(
            text="Configuración",
            size_hint_y=None,
            height=dp(40),
            on_release=self.show_settings
        )

        logout_btn = MDRaisedButton(
            text="Cerrar Sesión",
            size_hint_y=None,
            height=dp(40),
            on_release=self.logout
        )

        nav_drawer_content.add_widget(drawer_title)
        nav_drawer_content.add_widget(refresh_btn)
        nav_drawer_content.add_widget(settings_btn)
        nav_drawer_content.add_widget(logout_btn)

        nav_drawer.add_widget(nav_drawer_content)
        nav_layout.add_widget(nav_drawer)
        nav_layout.add_widget(screen_manager)

        self.add_widget(nav_layout)

        # Cargar tablero al inicializar
        Clock.schedule_once(self.load_dashboard, 0.5)

    def load_dashboard(self, dt):
        """Carga el tablero Power BI"""
        self.show_loading_message("Cargando tablero...")

        threading.Thread(target=self._load_dashboard_async).start()

    def _load_dashboard_async(self):
        """Carga el tablero de manera asíncrona"""
        try:
            dashboard_url = self.powerbi_manager.get_dashboard_url()
            if dashboard_url:
                Clock.schedule_once(
                    lambda dt: self._on_dashboard_loaded(dashboard_url), 0
                )
            else:
                Clock.schedule_once(
                    lambda dt: self._on_dashboard_error("No se pudo obtener la URL del tablero"), 0
                )
        except Exception as e:
            Clock.schedule_once(
                lambda dt: self._on_dashboard_error(str(e)), 0
            )

    def _on_dashboard_loaded(self, dashboard_url):
        """Callback cuando el tablero se carga exitosamente"""
        self.dashboard_container.clear_widgets()

        # Crear WebView para mostrar Power BI
        if platform == 'android':
            self._create_webview_android(dashboard_url)
        else:
            self._create_webview_desktop(dashboard_url)

    def _create_webview_android(self, url):
        """Crea WebView para Android"""
        from jnius import autoclass

        # Implementar WebView nativo de Android
        webview_card = MDCard(
            size_hint=(1, 1),
            elevation=2
        )

        info_label = MDLabel(
            text=f"Tablero Power BI cargado\nURL: {url[:50]}...",
            halign="center",
            valign="center"
        )

        webview_card.add_widget(info_label)
        self.dashboard_container.add_widget(webview_card)

    def _create_webview_desktop(self, url):
        """Crea vista del tablero para desktop"""
        dashboard_card = MDCard(
            size_hint=(1, None),
            height=dp(400),
            elevation=2,
            padding=dp(20)
        )

        dashboard_info = MDLabel(
            text=f"Tablero Power BI\n\nURL del tablero cargada correctamente.\nAcceso autorizado para el usuario actual.",
            halign="center",
            valign="center"
        )

        open_browser_btn = MDRaisedButton(
            text="Abrir en Navegador",
            size_hint=(None, None),
            height=dp(40),
            width=dp(200),
            pos_hint={"center_x": 0.5},
            on_release=lambda x: self._open_in_browser(url)
        )

        layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20)
        )
        layout.add_widget(dashboard_info)
        layout.add_widget(open_browser_btn)

        dashboard_card.add_widget(layout)
        self.dashboard_container.add_widget(dashboard_card)

    def _open_in_browser(self, url):
        """Abre la URL en el navegador"""
        import webbrowser
        webbrowser.open(url)

    def _on_dashboard_error(self, error_msg):
        """Callback cuando hay error cargando el tablero"""
        self.show_error(f"Error cargando tablero: {error_msg}")

    def show_loading_message(self, message):
        """Muestra mensaje de carga"""
        self.dashboard_container.clear_widgets()

        loading_card = MDCard(
            size_hint=(1, None),
            height=dp(200),
            elevation=2
        )

        loading_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            adaptive_height=True,
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        progress = MDProgressBar()
        label = MDLabel(
            text=message,
            halign="center",
            size_hint_y=None,
            height=dp(40)
        )

        loading_layout.add_widget(progress)
        loading_layout.add_widget(label)
        loading_card.add_widget(loading_layout)

        self.dashboard_container.add_widget(loading_card)

    def refresh_dashboard(self, instance):
        """Actualiza el tablero"""
        self.load_dashboard(0)

    def refresh_data(self, instance):
        """Actualiza los datos de autenticación"""
        self.show_loading_message("Actualizando datos de autorización...")

        threading.Thread(target=self._refresh_data_async).start()

    def _refresh_data_async(self):
        """Actualiza datos de manera asíncrona"""
        try:
            auth_manager = AuthManager()
            success = auth_manager.refresh_permissions()

            Clock.schedule_once(
                lambda dt: self._on_data_refreshed(success), 0
            )
        except Exception as e:
            Clock.schedule_once(
                lambda dt: self.show_error(f"Error actualizando datos: {str(e)}"), 0
            )

    def _on_data_refreshed(self, success):
        """Callback cuando los datos se actualizan"""
        if success:
            Snackbar(text="Datos actualizados correctamente").open()
            self.load_dashboard(0)
        else:
            self.show_error("No se pudieron actualizar los datos")

    def show_settings(self, instance):
        """Muestra configuración"""
        # Implementar pantalla de configuración
        pass

    def logout(self, instance):
        """Cierra sesión"""
        app = MDApp.get_running_app()
        app.root.current = "login"

    def show_error(self, message):
        """Muestra mensaje de error"""
        Snackbar(text=message).open()


class PowerBIApp(MDApp):
    """Aplicación principal"""

    def build(self):
        """Construye la aplicación"""
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"

        # Screen Manager principal
        sm = MDScreenManager()

        # Agregar pantallas
        sm.add_widget(LoginScreen())
        sm.add_widget(DashboardScreen())

        return sm


if __name__ == "__main__":
    PowerBIApp().run()
