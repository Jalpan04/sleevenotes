from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.toast import toast
from datetime import datetime
import db

KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex

<AlbumCover@MDFloatLayout>:
    album_color: 0.5, 0.5, 0.5, 1
    size_hint: None, None
    size: dp(100), dp(100)
    canvas.before:
        Color:
            rgba: self.album_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [dp(4)]

MDScreen:
    md_bg_color: get_color_from_hex("#1A1A1A")
    
    MDBottomNavigation:
        panel_color: get_color_from_hex("#251F1C")
        text_color_active: get_color_from_hex("#FFD700")
        text_color_normal: get_color_from_hex("#888888")
        
        # 1. HOME TAB
        MDBottomNavigationItem:
            name: 'home'
            text: 'Home'
            icon: 'home'
            
            MDScrollView:
                MDBoxLayout:
                    orientation: 'vertical'
                    adaptive_height: True
                    padding: dp(16)
                    spacing: dp(16)
                    
                    MDLabel:
                        text: "Popular This Week"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        font_style: "H6"
                        size_hint_y: None
                        height: self.texture_size[1]
                        
                    MDScrollView:
                        do_scroll_x: True
                        do_scroll_y: False
                        size_hint_y: None
                        height: dp(120)
                        
                        MDBoxLayout:
                            id: popular_albums
                            orientation: 'horizontal'
                            adaptive_width: True
                            spacing: dp(10)
                            
        # 2. SEARCH TAB
        MDBottomNavigationItem:
            name: 'search'
            text: 'Search'
            icon: 'magnify'
            
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(16)
                spacing: dp(16)
                
                MDTextField:
                    hint_text: "Search albums, artists..."
                    mode: "fill"
                    fill_color_normal: get_color_from_hex("#251F1C")
                    text_color_normal: 1, 1, 1, 1
                    
                MDScrollView:
                    MDList:
                        id: search_categories

        # 3. LOG ALBUM TAB
        MDBottomNavigationItem:
            name: 'log'
            text: 'Log'
            icon: 'plus-circle'
            
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(16)
                spacing: dp(16)
                
                MDLabel:
                    text: "Log Review for Echoes of Silence"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    font_style: "H6"
                    size_hint_y: None
                    height: self.texture_size[1]
                    
                MDBoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(60)
                    spacing: dp(10)
                    
                    MDIconButton:
                        id: star_1
                        icon: "star-outline"
                        theme_text_color: "Custom"
                        text_color: get_color_from_hex("#555555")
                        on_release: app.set_rating(1)
                    MDIconButton:
                        id: star_2
                        icon: "star-outline"
                        theme_text_color: "Custom"
                        text_color: get_color_from_hex("#555555")
                        on_release: app.set_rating(2)
                    MDIconButton:
                        id: star_3
                        icon: "star-outline"
                        theme_text_color: "Custom"
                        text_color: get_color_from_hex("#555555")
                        on_release: app.set_rating(3)
                    MDIconButton:
                        id: star_4
                        icon: "star-outline"
                        theme_text_color: "Custom"
                        text_color: get_color_from_hex("#555555")
                        on_release: app.set_rating(4)
                    MDIconButton:
                        id: star_5
                        icon: "star-outline"
                        theme_text_color: "Custom"
                        text_color: get_color_from_hex("#555555")
                        on_release: app.set_rating(5)
                    Widget:
                    MDIconButton:
                        id: heart_btn
                        icon: "heart-outline"
                        theme_text_color: "Custom"
                        text_color: get_color_from_hex("#555555")
                        on_release: app.toggle_heart()
                        
                MDSeparator:
                    color: get_color_from_hex("#251F1C")
                    
                MDTextField:
                    id: review_input
                    hint_text: "Add review..."
                    mode: "rectangle"
                    multiline: True
                    fill_color_normal: get_color_from_hex("#1A1A1A")
                    text_color_normal: 1, 1, 1, 1
                    size_hint_y: 1
                    
                MDRaisedButton:
                    text: "SAVE"
                    md_bg_color: get_color_from_hex("#FFD700")
                    text_color: 0, 0, 0, 1
                    pos_hint: {"center_x": .5}
                    on_release: app.save_review()

        # 4. PROFILE TAB (DIARY)
        MDBottomNavigationItem:
            name: 'profile'
            text: 'Profile'
            icon: 'account'
            
            MDScrollView:
                MDBoxLayout:
                    orientation: 'vertical'
                    adaptive_height: True
                    padding: dp(16)
                    spacing: dp(20)
                    
                    MDBoxLayout:
                        orientation: 'vertical'
                        adaptive_height: True
                        MDIcon:
                            icon: "account-circle"
                            font_size: "64sp"
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#FFD700")
                        MDLabel:
                            text: "Jax"
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 1
                            font_style: "H5"
                            
                    MDLabel:
                        text: "My Diary"
                        theme_text_color: "Custom"
                        text_color: 0.6, 0.6, 0.6, 1
                        
                    MDBoxLayout:
                        orientation: 'vertical'
                        adaptive_height: True
                        spacing: dp(5)
                        id: diary_list
'''

class SleeveNotesApp(MDApp):
    current_rating = 0
    current_liked = False
    active_album_id = 1 # Hardcoded to "Echoes of Silence" for demo

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)
        
    def on_start(self):
        from kivy.factory import Factory
        from kivymd.uix.list import OneLineListItem
        
        albums = db.get_albums()
        
        # Populate Popular Albums
        popular = self.root.ids.popular_albums
        for album in albums:
            cover = Factory.AlbumCover()
            cover.album_color = album["color"] + (1,)
            popular.add_widget(cover)
            
        # Populate Search Categories
        for cat in ["Release Date", "Genre & Style", "Highest Rated", "Decades"]:
            item = OneLineListItem(text=cat, theme_text_color="Custom", text_color=(1,1,1,1))
            self.root.ids.search_categories.add_widget(item)
            
        self.refresh_diary()

    def set_rating(self, rating):
        self.current_rating = rating
        for i in range(1, 6):
            btn = self.root.ids[f'star_{i}']
            if i <= rating:
                btn.icon = "star"
                btn.text_color = (1, 0.84, 0, 1) # Yellow
            else:
                btn.icon = "star-outline"
                btn.text_color = (0.3, 0.3, 0.3, 1)

    def toggle_heart(self):
        self.current_liked = not self.current_liked
        btn = self.root.ids.heart_btn
        if self.current_liked:
            btn.icon = "heart"
            btn.text_color = (1, 0.84, 0, 1)
        else:
            btn.icon = "heart-outline"
            btn.text_color = (0.3, 0.3, 0.3, 1)

    def save_review(self):
        review_text = self.root.ids.review_input.text
        if self.current_rating == 0 and not review_text:
            toast("Please provide a rating or review.")
            return
            
        # Log to local SQLite Database (user_id 1 is Jax)
        db.log_review(1, self.active_album_id, self.current_rating, review_text, self.current_liked)
        
        # Reset form
        self.root.ids.review_input.text = ""
        self.set_rating(0)
        if self.current_liked:
            self.toggle_heart()
            
        toast("Review saved to diary!")
        self.refresh_diary()

    def refresh_diary(self):
        from kivymd.uix.list import TwoLineListItem
        diary = self.root.ids.diary_list
        diary.clear_widgets()
        
        entries = db.get_diary(1)
        for entry in entries:
            text = f"{entry['date']} - {entry['title']}"
            stars = "★" * int(entry["rating"]) if entry["rating"] else "No rating"
            item = TwoLineListItem(text=text, secondary_text=f"Rating: {stars} | {entry['review']}", theme_text_color="Custom", text_color=(1,1,1,1), secondary_theme_text_color="Custom", secondary_text_color=(1, 0.84, 0, 1))
            diary.add_widget(item)

if __name__ == '__main__':
    SleeveNotesApp().run()
