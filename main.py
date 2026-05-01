from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.toast import toast
from kivy.network.urlrequest import UrlRequest
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import StringProperty
import urllib.parse
import json
from kivy.loader import Loader

# CRITICAL: Speed up image loading significantly
Loader.num_workers = 4           # Download up to 4 images in parallel (default is 2)
Loader.max_upload_per_frame = 4  # Send up to 4 images to the GPU per frame

# Local LAN URL so your phone can reach your PC on the same Wi-Fi
API_BASE = "http://192.168.29.215:8000"

KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex

<AuthScreen>:
    name: 'auth'
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: get_color_from_hex("#000000")
        padding: dp(30)
        spacing: dp(20)
        
        Widget:
            size_hint_y: 0.2
            
        MDIcon:
            icon: "album"
            font_size: "100sp"
            halign: "center"
            theme_text_color: "Custom"
            text_color: get_color_from_hex("#FFD700")
            
        MDLabel:
            text: "SleeveNotes"
            font_style: "H3"
            bold: True
            halign: "center"
            theme_text_color: "Custom"
            text_color: get_color_from_hex("#FFD700")
            adaptive_height: True
            
        MDLabel:
            text: "Your Musical Diary"
            font_style: "Subtitle1"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 0.6, 0.6, 0.6, 1
            adaptive_height: True
            
        Widget:
            size_hint_y: 0.1
            
        MDTextField:
            id: username
            hint_text: "Username"
            mode: "round"
            icon_left: "account"
            text_color_normal: 1, 1, 1, 1
            fill_color_normal: get_color_from_hex("#1A1A1A")
            
        MDTextField:
            id: password
            hint_text: "Password"
            password: True
            mode: "round"
            icon_left: "lock"
            text_color_normal: 1, 1, 1, 1
            fill_color_normal: get_color_from_hex("#1A1A1A")
            
        Widget:
            size_hint_y: 0.1
            
        MDRaisedButton:
            text: "SIGN IN"
            font_style: "Button"
            bold: True
            size_hint_x: 1
            height: dp(50)
            md_bg_color: get_color_from_hex("#FFD700")
            text_color: 0, 0, 0, 1
            elevation: 2
            on_release: app.login()
            
        MDFlatButton:
            text: "Don't have an account? Sign Up"
            size_hint_x: 1
            theme_text_color: "Custom"
            text_color: get_color_from_hex("#FFD700")
            on_release: app.signup()
            
        Widget:
            size_hint_y: 0.2

<FeedCard@MDCard>:
    orientation: "vertical"
    adaptive_height: True
    padding: dp(16)
    spacing: dp(12)
    md_bg_color: get_color_from_hex("#111111")
    radius: [dp(16)]
    elevation: 2
    
    cover_url: ""
    album_title: ""
    album_artist: ""
    username: ""
    rating: ""
    review_text: ""
    
    # Header: User Info
    MDBoxLayout:
        adaptive_height: True
        spacing: dp(10)
        MDIcon:
            icon: "account-circle"
            theme_text_color: "Custom"
            text_color: get_color_from_hex("#FFD700")
            font_size: "36sp"
            size_hint: None, None
            size: dp(36), dp(36)
        MDBoxLayout:
            orientation: "vertical"
            adaptive_height: True
            MDLabel:
                text: root.username
                font_style: "Subtitle2"
                bold: True
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                adaptive_height: True
            MDLabel:
                text: "logged a review"
                font_style: "Caption"
                theme_text_color: "Custom"
                text_color: 0.6, 0.6, 0.6, 1
                adaptive_height: True
                
    # Middle: Album Cover & Details
    MDBoxLayout:
        adaptive_height: True
        spacing: dp(16)
        # Cover image with rounded corners
        MDCard:
            size_hint: None, None
            size: dp(90), dp(90)
            radius: [dp(8)]
            elevation: 2
            FitImage:
                source: root.cover_url
                radius: [dp(8)]
                
        # Info & Rating
        MDBoxLayout:
            orientation: "vertical"
            adaptive_height: True
            spacing: dp(4)
            pos_hint: {"center_y": .5}
            MDLabel:
                text: root.album_title
                font_style: "H6"
                bold: True
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                adaptive_height: True
            MDLabel:
                text: root.album_artist
                font_style: "Caption"
                theme_text_color: "Custom"
                text_color: 0.7, 0.7, 0.7, 1
                adaptive_height: True
            MDLabel:
                text: root.rating
                font_style: "Subtitle2"
                theme_text_color: "Custom"
                text_color: get_color_from_hex("#FFD700")
                adaptive_height: True
                
    # Bottom: Review Text
    MDLabel:
        text: root.review_text
        font_style: "Body2"
        theme_text_color: "Custom"
        text_color: 0.9, 0.9, 0.9, 1
        adaptive_height: True
        padding: [0, dp(8), 0, 0]

<MainScreen>:
    name: 'main'
    MDBottomNavigation:
        id: bottom_nav
        panel_color: get_color_from_hex("#0A0A0A")
        text_color_active: get_color_from_hex("#FFD700")
        text_color_normal: get_color_from_hex("#555555")
        
        MDBottomNavigationItem:
            name: 'feed'
            text: 'Feed'
            icon: 'timeline-text'
            on_tab_press: app.load_feed()
            
            MDBoxLayout:
                orientation: 'vertical'
                md_bg_color: get_color_from_hex("#000000")
                MDTopAppBar:
                    title: "Live Feed"
                    md_bg_color: get_color_from_hex("#0A0A0A")
                    specific_text_color: get_color_from_hex("#FFD700")
                    elevation: 0
                MDScrollView:
                    MDBoxLayout:
                        id: feed_list
                        orientation: 'vertical'
                        adaptive_height: True
                        padding: dp(16)
                        spacing: dp(16)
                        
        MDBottomNavigationItem:
            name: 'search'
            text: 'Search'
            icon: 'magnify'
            
            MDBoxLayout:
                orientation: 'vertical'
                md_bg_color: get_color_from_hex("#000000")
                
                MDBoxLayout:
                    size_hint_y: None
                    height: dp(80)
                    padding: dp(16)
                    md_bg_color: get_color_from_hex("#0A0A0A")
                    MDTextField:
                        id: search_input
                        hint_text: "Find albums..."
                        mode: "fill"
                        radius: [dp(12)]
                        icon_left: "magnify"
                        fill_color_normal: get_color_from_hex("#1A1A1A")
                        text_color_normal: 1, 1, 1, 1
                        on_text: app.on_search_text(self.text)
                        
                MDScrollView:
                    MDList:
                        id: search_results
                        padding: [dp(8), dp(8)]

        MDBottomNavigationItem:
            name: 'profile'
            text: 'Profile'
            icon: 'account-circle'
            on_tab_press: app.load_profile()
            
            MDBoxLayout:
                orientation: 'vertical'
                md_bg_color: get_color_from_hex("#000000")
                MDTopAppBar:
                    title: "Your Profile"
                    md_bg_color: get_color_from_hex("#0A0A0A")
                    specific_text_color: get_color_from_hex("#FFD700")
                    elevation: 0
                    right_action_items: [["logout", lambda x: app.logout()]]
                    
                MDScrollView:
                    MDBoxLayout:
                        orientation: "vertical"
                        adaptive_height: True
                        padding: dp(16)
                        spacing: dp(24)
                        
                        MDBoxLayout:
                            orientation: "vertical"
                            adaptive_height: True
                            spacing: dp(8)
                            MDIcon:
                                icon: "account-circle"
                                font_size: "90sp"
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: get_color_from_hex("#FFD700")
                            MDLabel:
                                id: profile_username
                                text: ""
                                font_style: "H5"
                                bold: True
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: 1, 1, 1, 1
                                adaptive_height: True
                                
                        MDLabel:
                            text: "Your Logs"
                            font_style: "H6"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#FFD700")
                            adaptive_height: True
                            
                        MDGridLayout:
                            id: profile_grid
                            cols: 3
                            spacing: dp(12)
                            adaptive_height: True

<AlbumDetailsScreen>:
    name: 'album_details'
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: get_color_from_hex("#000000")
        
        # Transparent overlay header
        MDFloatLayout:
            size_hint_y: None
            height: dp(280)
            
            # Blurred Background Image (using low opacity)
            FitImage:
                source: root.cover_url
                size_hint: 1, 1
                pos_hint: {"center_x": .5, "center_y": .5}
                opacity: 0.2
                
            # Gradient mask simulation (solid box at bottom)
            MDBoxLayout:
                size_hint: 1, 0.3
                pos_hint: {"x": 0, "y": 0}
                md_bg_color: get_color_from_hex("#000000")
                opacity: 0.8
                
            # Back Button
            MDIconButton:
                icon: "arrow-left"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                pos_hint: {"x": 0.02, "top": 0.98}
                on_release: app.go_back_to_main()
                
            # Main Poster Cover
            MDCard:
                size_hint: None, None
                size: dp(140), dp(140)
                pos_hint: {"center_x": .5, "center_y": .5}
                radius: [dp(8)]
                elevation: 4
                FitImage:
                    source: root.cover_url
                    radius: [dp(8)]
                    
            # Title & Artist
            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                pos_hint: {"center_x": .5, "y": 0}
                padding: [dp(16), 0]
                MDLabel:
                    text: root.album_title
                    font_style: "H5"
                    bold: True
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    adaptive_height: True
                MDLabel:
                    text: root.album_artist
                    font_style: "Subtitle1"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 0.7, 0.7, 0.7, 1
                    adaptive_height: True
                    
        MDScrollView:
            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                padding: dp(20)
                spacing: dp(24)
                
                MDRaisedButton:
                    text: "LOG THIS ALBUM"
                    font_style: "Button"
                    bold: True
                    size_hint_x: 1
                    height: dp(50)
                    md_bg_color: get_color_from_hex("#FFD700")
                    text_color: 0, 0, 0, 1
                    elevation: 2
                    on_release: app.open_log_screen()
                    
                MDBoxLayout:
                    orientation: "vertical"
                    adaptive_height: True
                    spacing: dp(8)
                    MDLabel:
                        text: "Tags"
                        font_style: "Subtitle2"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: get_color_from_hex("#FFD700")
                        adaptive_height: True
                    MDLabel:
                        text: root.album_tags
                        font_style: "Caption"
                        theme_text_color: "Custom"
                        text_color: 0.9, 0.9, 0.9, 1
                        adaptive_height: True
                        
                MDBoxLayout:
                    orientation: "vertical"
                    adaptive_height: True
                    spacing: dp(8)
                    MDLabel:
                        text: "About"
                        font_style: "Subtitle2"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: get_color_from_hex("#FFD700")
                        adaptive_height: True
                    MDLabel:
                        text: root.album_wiki
                        font_style: "Body2"
                        theme_text_color: "Custom"
                        text_color: 0.8, 0.8, 0.8, 1
                        adaptive_height: True
                        
                MDBoxLayout:
                    orientation: "vertical"
                    adaptive_height: True
                    spacing: dp(12)
                    MDLabel:
                        text: "Tracklist"
                        font_style: "Subtitle2"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: get_color_from_hex("#FFD700")
                        adaptive_height: True
                    MDBoxLayout:
                        id: tracklist_container
                        orientation: "vertical"
                        adaptive_height: True
                        spacing: dp(8)

<LogReviewScreen>:
    name: 'log_review'
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: get_color_from_hex("#000000")
        
        MDTopAppBar:
            title: "Write Entry"
            md_bg_color: get_color_from_hex("#0A0A0A")
            specific_text_color: get_color_from_hex("#FFD700")
            elevation: 0
            left_action_items: [["close", lambda x: app.cancel_log()]]
            right_action_items: [["check", lambda x: app.save_review()]]
            
        MDScrollView:
            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                padding: dp(20)
                spacing: dp(24)
                
                MDBoxLayout:
                    adaptive_height: True
                    spacing: dp(16)
                    MDCard:
                        size_hint: None, None
                        size: dp(90), dp(90)
                        radius: [dp(8)]
                        elevation: 2
                        FitImage:
                            source: root.cover_url
                            radius: [dp(8)]
                    MDBoxLayout:
                        orientation: "vertical"
                        adaptive_height: True
                        pos_hint: {"center_y": .5}
                        MDLabel:
                            text: root.album_title
                            font_style: "H6"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 1
                            adaptive_height: True
                        MDLabel:
                            text: root.album_artist
                            font_style: "Subtitle1"
                            theme_text_color: "Custom"
                            text_color: 0.7, 0.7, 0.7, 1
                            adaptive_height: True
                            
                MDBoxLayout:
                    orientation: 'vertical'
                    adaptive_height: True
                    spacing: dp(10)
                    MDLabel:
                        text: "Your Rating"
                        font_style: "Subtitle2"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        adaptive_height: True
                    MDBoxLayout:
                        orientation: 'horizontal'
                        adaptive_height: True
                        spacing: dp(8)
                        MDIconButton:
                            id: star_1
                            icon: "star-outline"
                            icon_size: "36sp"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#555555")
                            on_release: app.set_rating(1)
                        MDIconButton:
                            id: star_2
                            icon: "star-outline"
                            icon_size: "36sp"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#555555")
                            on_release: app.set_rating(2)
                        MDIconButton:
                            id: star_3
                            icon: "star-outline"
                            icon_size: "36sp"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#555555")
                            on_release: app.set_rating(3)
                        MDIconButton:
                            id: star_4
                            icon: "star-outline"
                            icon_size: "36sp"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#555555")
                            on_release: app.set_rating(4)
                        MDIconButton:
                            id: star_5
                            icon: "star-outline"
                            icon_size: "36sp"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#555555")
                            on_release: app.set_rating(5)
                            
                MDTextField:
                    id: review_input
                    hint_text: "Write your thoughts..."
                    mode: "rectangle"
                    multiline: True
                    fill_color_normal: get_color_from_hex("#111111")
                    text_color_normal: 1, 1, 1, 1
'''

class AuthScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class AlbumDetailsScreen(Screen):
    album_title = StringProperty("")
    album_artist = StringProperty("")
    cover_url = StringProperty("")
    album_tags = StringProperty("")
    album_wiki = StringProperty("Loading details...")

class LogReviewScreen(Screen):
    album_title = StringProperty("")
    album_artist = StringProperty("")
    cover_url = StringProperty("")

class SleeveNotesApp(MDApp):
    current_rating = 0
    active_album = None
    search_event = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.store = JsonStore("session.json")
        self.sm = ScreenManager(transition=SlideTransition())
        
        Builder.load_string(KV)
        self.auth_screen = AuthScreen()
        self.main_screen = MainScreen()
        self.album_details = AlbumDetailsScreen()
        self.log_screen = LogReviewScreen()
        
        self.sm.add_widget(self.auth_screen)
        self.sm.add_widget(self.main_screen)
        self.sm.add_widget(self.album_details)
        self.sm.add_widget(self.log_screen)
        
        if self.store.exists("token"):
            self.sm.current = 'main'
            self.load_feed()
            
        return self.sm

    # === AUTHENTICATION ===
    def login(self):
        username = self.auth_screen.ids.username.text
        password = self.auth_screen.ids.password.text
        if not username or not password:
            toast("Enter username and password")
            return
        data = f"username={username}&password={password}"
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        UrlRequest(f"{API_BASE}/login", req_body=data, req_headers=headers, on_success=self.on_login_success, on_failure=self.on_login_fail, on_error=self.on_login_fail)
        
    def signup(self):
        username = self.auth_screen.ids.username.text
        password = self.auth_screen.ids.password.text
        if not username or not password:
            toast("Enter username and password")
            return
        data = json.dumps({"username": username, "password": password})
        headers = {'Content-type': 'application/json'}
        UrlRequest(f"{API_BASE}/signup", req_body=data, req_headers=headers, on_success=lambda req, res: self.login(), on_failure=self.on_login_fail, on_error=self.on_login_fail)

    def on_login_success(self, req, result):
        self.store.put("token", access_token=result["access_token"])
        self.auth_screen.ids.password.text = ""
        self.sm.current = 'main'
        self.load_feed()
        toast("Logged in!")

    def on_login_fail(self, req, result):
        toast(str(result.get("detail", "Authentication failed")))
        
    def logout(self):
        if self.store.exists("token"):
            self.store.delete("token")
        self.sm.current = 'auth'
        toast("Logged out")

    # === SOCIAL FEED ===
    def load_feed(self):
        UrlRequest(f"{API_BASE}/feed", on_success=self.on_feed_success, on_failure=lambda r, e: toast("Failed to load feed"))

    def on_feed_success(self, req, result):
        from kivy.factory import Factory
        feed_list = self.main_screen.ids.feed_list
        feed_list.clear_widgets()
        for item in result:
            card = Factory.FeedCard()
            card.username = item["username"]
            card.album_title = item["album_title"]
            card.album_artist = item["album_artist"]
            card.cover_url = item["album_cover_url"].replace("http://", "https://")
            card.rating = "★" * int(item["rating"])
            card.review_text = item["review_text"]
            feed_list.add_widget(card)

    # === SEARCH ===
    def on_search_text(self, text):
        from kivy.clock import Clock
        if self.search_event:
            self.search_event.cancel()
        self.search_event = Clock.schedule_once(lambda dt: self.perform_search(text), 0.5)

    def perform_search(self, query):
        if len(query) < 2:
            self.main_screen.ids.search_results.clear_widgets()
            return
        safe_query = urllib.parse.quote(query)
        UrlRequest(f"{API_BASE}/search?q={safe_query}", on_success=self.on_search_success)

    def on_search_success(self, req, result):
        from kivymd.uix.list import TwoLineAvatarListItem, ImageLeftWidget
        results_list = self.main_screen.ids.search_results
        results_list.clear_widgets()
        for album in result:
            item = TwoLineAvatarListItem(
                text=album["title"],
                secondary_text=album["artist"],
                theme_text_color="Custom",
                text_color=(1,1,1,1)
            )
            img_url = album["cover_url"].replace("http://", "https://")
            img = ImageLeftWidget(source=img_url)
            item.add_widget(img)
            item.bind(on_release=lambda x, a=album: self.open_album_details(a))
            results_list.add_widget(item)

    # === ALBUM DETAILS ===
    def open_album_details(self, album):
        self.active_album = album
        self.album_details.album_title = album["title"]
        self.album_details.album_artist = album["artist"]
        self.album_details.cover_url = album["cover_url"].replace("http://", "https://")
        self.album_details.album_tags = ""
        self.album_details.album_wiki = "Loading details from Last.fm..."
        self.album_details.ids.tracklist_container.clear_widgets()
        
        self.sm.transition.direction = "left"
        self.sm.current = 'album_details'
        
        a = urllib.parse.quote(album["artist"])
        al = urllib.parse.quote(album["title"])
        UrlRequest(f"{API_BASE}/album/info?artist={a}&album={al}", on_success=self.on_album_info_success)

    def on_album_info_success(self, req, result):
        from kivymd.uix.label import MDLabel
        self.album_details.album_tags = ", ".join(result.get("tags", []))
        raw_wiki = result.get("wiki", "No description available.")
        import re
        clean_wiki = re.sub('<[^<]+>', '', raw_wiki)
        self.album_details.album_wiki = clean_wiki
        
        tc = self.album_details.ids.tracklist_container
        tc.clear_widgets()
        for idx, track in enumerate(result.get("tracks", [])):
            lbl = MDLabel(
                text=f"{idx+1}. {track['name']}  ({track['duration']})",
                theme_text_color="Custom",
                text_color=(0.8, 0.8, 0.8, 1),
                adaptive_height=True
            )
            tc.add_widget(lbl)

    def go_back_to_main(self):
        self.sm.transition.direction = "right"
        self.sm.current = 'main'

    # === LOGGING ===
    def open_log_screen(self):
        if not self.active_album: return
        self.log_screen.album_title = self.active_album["title"]
        self.log_screen.album_artist = self.active_album["artist"]
        self.log_screen.cover_url = self.active_album["cover_url"].replace("http://", "https://")
        self.log_screen.ids.review_input.text = ""
        self.set_rating(0)
        self.sm.transition.direction = "up"
        self.sm.current = 'log_review'

    def cancel_log(self):
        self.sm.transition.direction = "down"
        self.sm.current = 'album_details'

    def set_rating(self, rating):
        self.current_rating = rating
        for i in range(1, 6):
            btn = self.log_screen.ids[f'star_{i}']
            if i <= rating:
                btn.icon = "star"
                btn.text_color = (1, 0.84, 0, 1)
            else:
                btn.icon = "star-outline"
                btn.text_color = (0.3, 0.3, 0.3, 1)

    def save_review(self):
        review_text = self.log_screen.ids.review_input.text
        if self.current_rating == 0 and not review_text:
            toast("Please provide a rating or review.")
            return
            
        if not self.store.exists("token"):
            self.logout()
            return
            
        token = self.store.get("token")["access_token"]
        headers = {'Content-type': 'application/json', 'Authorization': f'Bearer {token}'}
        payload = {"album": self.active_album, "rating": self.current_rating, "review_text": review_text}
        
        UrlRequest(f"{API_BASE}/reviews", req_body=json.dumps(payload), req_headers=headers, on_success=self.on_review_success, on_failure=lambda r, e: toast("Failed to save review"))

    def on_review_success(self, req, result):
        toast("Review published!")
        self.sm.transition.direction = "down"
        self.sm.current = 'main'
        self.main_screen.children[0].switch_tab("feed")
        self.load_feed()

    # === PROFILE ===
    def load_profile(self):
        if not self.store.exists("token"): return
        token = self.store.get("token")["access_token"]
        headers = {'Authorization': f'Bearer {token}'}
        UrlRequest(f"{API_BASE}/profile", req_headers=headers, on_success=self.on_profile_success)

    def on_profile_success(self, req, result):
        self.main_screen.ids.profile_username.text = result["username"]
        grid = self.main_screen.ids.profile_grid
        grid.clear_widgets()
        
        from kivymd.uix.fitimage import FitImage
        from kivymd.uix.card import MDCard
        
        for rev in result["reviews"]:
            img_url = rev["album_cover_url"].replace("http://", "https://")
            # Wrap image in MDCard to ensure perfectly rounded grid squares
            card = MDCard(size_hint=(None, None), size=(dp(105), dp(105)), radius=[dp(8)], elevation=2)
            img = FitImage(source=img_url, radius=[dp(8)])
            card.add_widget(img)
            grid.add_widget(card)

if __name__ == '__main__':
    SleeveNotesApp().run()
