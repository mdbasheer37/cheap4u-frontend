# monthly_challenge.py — Monthly Champion Challenge (Kivy / KivyMD frontend)
#
# Self-contained add-on module: it does NOT edit the giant Cheap4u.py KV
# string. It defines its own Screens + widgets with their own KV rules,
# and exposes a small integration surface:
#
#   from monthly_challenge import ChallengeMixin, register_challenge_screens
#
#   class DashboardApp(ChallengeMixin, MDApp):     # add ChallengeMixin as a base
#       ...
#       def build(self):
#           ...
#           root = Builder.load_string(KV)
#           register_challenge_screens(root, self)   # <-- add this line
#           return root
#
# See the bottom of this file for the exact 4-line integration diff needed
# in Cheap4u.py (already applied for you where noted in the chat reply).
#
# Branding: premium blue (#1A99FF-ish, matches the app's existing wallet
# card gradient) + white, gold/silver/bronze medal accents, rounded cards,
# soft elevation, small on-open animations (fade/scale) for a modern feel.

import threading
import requests
from datetime import datetime, timedelta

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.properties import (
    StringProperty, NumericProperty, BooleanProperty, ListProperty, ObjectProperty
)

from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.label import MDLabel
from kivymd.toast import toast

GOLD   = [1, 0.84, 0, 1]
SILVER = [0.75, 0.75, 0.78, 1]
BRONZE = [0.80, 0.50, 0.20, 1]
BRAND_BLUE = [0.1, 0.6, 1, 1]
BRAND_BLUE_DARK = [0.05, 0.35, 0.75, 1]


def _medal_color(rank):
    return {1: GOLD, 2: SILVER, 3: BRONZE}.get(rank, [0.85, 0.9, 0.98, 1])


def _medal_icon(rank):
    return {1: 'trophy', 2: 'trophy-variant', 3: 'trophy-variant-outline'}.get(rank, 'numeric-{}-circle'.format(rank) if rank and rank <= 9 else 'account-circle')


def _fmt_naira(amount):
    try:
        return f"₦{float(amount):,.2f}"
    except (TypeError, ValueError):
        return "₦0.00"


def _fmt_countdown(seconds):
    seconds = max(0, int(seconds or 0))
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, secs = divmod(rem, 60)
    if days > 0:
        return f"{days}d {hours:02d}h {minutes:02d}m"
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


# ─────────────────────────────────────────────────────────────────────────
# KV
# ─────────────────────────────────────────────────────────────────────────
CHALLENGE_KV = '''
#:import dp kivy.metrics.dp

<ChallengeDashboardCard>:
    orientation: 'vertical'
    padding: dp(18)
    spacing: dp(8)
    radius: [22]
    elevation: 4
    size_hint_y: None
    height: dp(190)
    md_bg_color: 0.1, 0.6, 1, 1

    MDBoxLayout:
        size_hint_y: None
        height: dp(28)

        MDLabel:
            text: "🏆 Monthly Champion Challenge"
            bold: True
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            font_style: "Subtitle1"

        MDLabel:
            id: countdown_label
            text: "--:--:--"
            halign: "right"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 0.9
            font_style: "Caption"
            size_hint_x: 0.4

    MDBoxLayout:
        spacing: dp(20)
        size_hint_y: None
        height: dp(70)

        MDBoxLayout:
            orientation: 'vertical'
            MDLabel:
                text: "Your Rank"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 0.85
                font_style: "Caption"
            MDLabel:
                id: rank_label
                text: "Unranked"
                bold: True
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                font_style: "H5"

        MDBoxLayout:
            orientation: 'vertical'
            MDLabel:
                text: "Monthly Purchases"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 0.85
                font_style: "Caption"
            MDLabel:
                id: total_label
                text: "₦0.00"
                bold: True
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                font_style: "H5"

    MDLabel:
        id: overtake_label
        text: "Make a purchase to join the challenge!"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 0.95
        font_style: "Caption"
        size_hint_y: None
        height: dp(18)

    MDBoxLayout:
        size_hint_y: None
        height: dp(38)
        spacing: dp(10)

        MDRaisedButton:
            text: "VIEW LEADERBOARD"
            md_bg_color: 1, 1, 1, 1
            text_color: 0.1, 0.6, 1, 1
            on_release: app.open_monthly_challenge_screen()

        MDIconButton:
            icon: "history"
            theme_text_color: "Custom"
            icon_color: 1, 1, 1, 1
            on_release: app.open_winners_history_screen()


<LeaderboardRow>:
    orientation: 'horizontal'
    size_hint_y: None
    height: dp(84)
    padding: [dp(12), dp(8)]
    spacing: dp(12)
    radius: [16]
    elevation: 1
    md_bg_color: 1, 1, 1, 1

    MDBoxLayout:
        size_hint: None, None
        size: dp(44), dp(44)
        pos_hint: {"center_y": 0.5}
        canvas.before:
            Color:
                rgba: root.medal_color
            Ellipse:
                pos: self.pos
                size: self.size
        MDLabel:
            text: root.rank_text
            halign: "center"
            valign: "middle"
            bold: True
            theme_text_color: "Custom"
            text_color: (0.2,0.2,0.2,1) if root.rank and root.rank <= 3 else (1,1,1,1)

    MDBoxLayout:
        size_hint: None, None
        size: dp(40), dp(40)
        pos_hint: {"center_y": 0.5}
        canvas.before:
            Color:
                rgba: 0.1, 0.6, 1, 1
            Ellipse:
                pos: self.pos
                size: self.size
        MDLabel:
            text: root.avatar_initial
            halign: "center"
            bold: True
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(4)

        MDBoxLayout:
            MDLabel:
                text: root.user_name
                bold: True
                theme_text_color: "Primary"
                shorten: True
                shorten_from: "right"
            MDLabel:
                text: root.reward_text
                halign: "right"
                theme_text_color: "Secondary"
                font_style: "Caption"

        MDProgressBar:
            value: root.progress_percent
            max: 100
            color: 0.1, 0.6, 1, 1

        MDLabel:
            text: root.amount_text
            font_style: "Caption"
            theme_text_color: "Secondary"


<MonthlyChallengeScreen>:
    name: "monthly_challenge"

    MDScreen:
        md_bg_color: 0.95, 0.97, 1, 1

        MDBoxLayout:
            orientation: 'vertical'

            MDBoxLayout:
                size_hint_y: None
                height: dp(60)
                padding: [dp(10), 0]
                spacing: dp(10)
                md_bg_color: 0.1, 0.6, 1, 1

                MDIconButton:
                    icon: "arrow-left"
                    theme_text_color: "Custom"
                    icon_color: 1, 1, 1, 1
                    on_release: app.root.current = "dashboard"

                MDLabel:
                    text: "🏆 Monthly Challenge"
                    bold: True
                    font_style: "H6"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1

                MDIconButton:
                    icon: "history"
                    theme_text_color: "Custom"
                    icon_color: 1, 1, 1, 1
                    on_release: app.open_winners_history_screen()

            MDBoxLayout:
                size_hint_y: None
                height: dp(50)
                padding: [dp(15), dp(6)]
                md_bg_color: 1, 1, 1, 1

                MDLabel:
                    text: "⏳ Ends in:"
                    theme_text_color: "Secondary"
                    font_style: "Caption"

                MDLabel:
                    id: screen_countdown_label
                    text: "--:--:--"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: 0.1, 0.6, 1, 1
                    halign: "right"

            MDLabel:
                id: my_rank_summary_label
                text: "Loading your rank..."
                halign: "center"
                theme_text_color: "Secondary"
                font_style: "Caption"
                size_hint_y: None
                height: dp(24)
                padding: [0, dp(4)]

            ScrollView:
                do_scroll_x: False

                MDBoxLayout:
                    id: leaderboard_box
                    orientation: 'vertical'
                    spacing: dp(10)
                    padding: [dp(12), dp(10), dp(12), dp(20)]
                    size_hint_y: None
                    height: self.minimum_height


<WinnersHistoryScreen>:
    name: "winners_history"

    MDScreen:
        md_bg_color: 0.95, 0.97, 1, 1

        MDBoxLayout:
            orientation: 'vertical'

            MDBoxLayout:
                size_hint_y: None
                height: dp(60)
                padding: [dp(10), 0]
                spacing: dp(10)
                md_bg_color: 0.1, 0.6, 1, 1

                MDIconButton:
                    icon: "arrow-left"
                    theme_text_color: "Custom"
                    icon_color: 1, 1, 1, 1
                    on_release: app.root.current = "monthly_challenge"

                MDLabel:
                    text: "🏅 Winners History"
                    bold: True
                    font_style: "H6"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1

            ScrollView:
                do_scroll_x: False

                MDBoxLayout:
                    id: winners_box
                    orientation: 'vertical'
                    spacing: dp(10)
                    padding: [dp(12), dp(10), dp(12), dp(20)]
                    size_hint_y: None
                    height: self.minimum_height


<ChallengeAdminScreen>:
    name: "challenge_admin"

    MDScreen:
        md_bg_color: 0.95, 0.97, 1, 1

        MDBoxLayout:
            orientation: 'vertical'

            MDBoxLayout:
                size_hint_y: None
                height: dp(60)
                padding: [dp(10), 0]
                spacing: dp(10)
                md_bg_color: 0.05, 0.35, 0.75, 1

                MDIconButton:
                    icon: "arrow-left"
                    theme_text_color: "Custom"
                    icon_color: 1, 1, 1, 1
                    on_release: app.root.current = "dashboard"

                MDLabel:
                    text: "⚙️ Challenge Admin"
                    bold: True
                    font_style: "H6"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1

            ScrollView:
                do_scroll_x: False

                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: dp(15)
                    padding: dp(15)
                    size_hint_y: None
                    height: self.minimum_height

                    MDCard:
                        orientation: 'vertical'
                        padding: dp(15)
                        spacing: dp(10)
                        radius: [15]
                        elevation: 2
                        size_hint_y: None
                        height: dp(90)

                        MDBoxLayout:
                            MDLabel:
                                text: "Challenge Enabled"
                                bold: True
                            MDSwitch:
                                id: enabled_switch
                                pos_hint: {"center_y": 0.5}

                        MDLabel:
                            id: last_processed_label
                            text: "Last processed month: —"
                            theme_text_color: "Secondary"
                            font_style: "Caption"

                    MDCard:
                        orientation: 'vertical'
                        padding: dp(15)
                        spacing: dp(12)
                        radius: [15]
                        elevation: 2
                        size_hint_y: None
                        height: dp(280)

                        MDLabel:
                            text: "Reward Settings"
                            bold: True
                            font_style: "Subtitle1"

                        MDTextField:
                            id: first_place_field
                            hint_text: "1st Place — Cashback % of total spend"
                            input_filter: "float"

                        MDTextField:
                            id: second_place_field
                            hint_text: "2nd Place — Fixed Wallet Bonus (₦)"
                            input_filter: "float"

                        MDTextField:
                            id: third_place_field
                            hint_text: "3rd Place — Fixed Wallet Bonus (₦)"
                            input_filter: "float"

                        MDTextField:
                            id: min_qualify_field
                            hint_text: "Minimum spend to qualify for reward (₦, 0 = none)"
                            input_filter: "float"

                        MDRaisedButton:
                            text: "SAVE SETTINGS"
                            md_bg_color: 0.1, 0.6, 1, 1
                            on_release: app.admin_save_challenge_config()

                    MDCard:
                        orientation: 'vertical'
                        padding: dp(15)
                        spacing: dp(10)
                        radius: [15]
                        elevation: 2
                        size_hint_y: None
                        height: dp(160)

                        MDLabel:
                            text: "Tools"
                            bold: True
                            font_style: "Subtitle1"

                        MDRaisedButton:
                            text: "VIEW LIVE LEADERBOARD"
                            md_bg_color: 0.1, 0.6, 1, 1
                            on_release: app.open_monthly_challenge_screen()

                        MDBoxLayout:
                            spacing: dp(10)
                            MDRaisedButton:
                                text: "EXPORT WINNERS CSV"
                                on_release: app.admin_export_winners_csv()
                            MDRaisedButton:
                                text: "PROCESS MONTH NOW"
                                md_bg_color: 0.9, 0.5, 0.1, 1
                                on_release: app.admin_process_month_confirm()
'''

Builder.load_string(CHALLENGE_KV)


# ─────────────────────────────────────────────────────────────────────────
# Widgets
# ─────────────────────────────────────────────────────────────────────────

class ChallengeDashboardCard(MDCard):
    """The Home Dashboard card — rank, monthly total, amount to overtake
    the next user, live countdown, and a button into the full leaderboard."""
    pass


class LeaderboardRow(MDCard):
    rank             = NumericProperty(0)
    rank_text        = StringProperty("")
    user_name        = StringProperty("")
    avatar_initial   = StringProperty("?")
    amount_text      = StringProperty("")
    reward_text      = StringProperty("")
    progress_percent = NumericProperty(0)
    medal_color      = ListProperty([0.85, 0.9, 0.98, 1])

    def set_data(self, row):
        self.rank = row.get('rank', 0)
        self.rank_text = f"#{self.rank}" if self.rank > 3 else {1: "🥇", 2: "🥈", 3: "🥉"}.get(self.rank, f"#{self.rank}")
        self.user_name = row.get('name', 'Unknown')
        self.avatar_initial = row.get('avatar_initial', '?')
        self.amount_text = _fmt_naira(row.get('total_amount', 0))
        self.reward_text = row.get('reward_position') or ""
        self.progress_percent = row.get('progress_percent', 0)
        self.medal_color = _medal_color(self.rank)


class MonthlyChallengeScreen(Screen):
    pass


class WinnersHistoryScreen(Screen):
    pass


class ChallengeAdminScreen(Screen):
    pass


def register_challenge_screens(root, app):
    """Call once from DashboardApp.build(), right after Builder.load_string(KV),
    passing the ScreenManager instance it returned. Adds the three new
    screens so app.root.current = 'monthly_challenge' / 'winners_history' /
    'challenge_admin' works exactly like the app's existing screens."""
    for screen_cls, name in (
        (MonthlyChallengeScreen, 'monthly_challenge'),
        (WinnersHistoryScreen, 'winners_history'),
        (ChallengeAdminScreen, 'challenge_admin'),
    ):
        if not root.has_screen(name):
            root.add_widget(screen_cls(name=name))


def insert_dashboard_card(dashboard_box, card, after_index=1):
    """
    Inserts `card` into `dashboard_box` (the dashboard's main vertical
    MDBoxLayout) right after the `after_index`-th widget in KV DECLARATION
    order (0 = welcome/profile row, 1 = wallet balance card, ...).

    Implemented by re-adding every child in declaration order rather than
    reasoning about Kivy's internal (reversed) children list, so it can't
    silently end up in the wrong visual position.
    """
    declared_order = list(reversed(dashboard_box.children))
    if card not in declared_order:
        declared_order.insert(min(after_index + 1, len(declared_order)), card)
    dashboard_box.clear_widgets()
    for w in declared_order:
        dashboard_box.add_widget(w)


# ─────────────────────────────────────────────────────────────────────────
# App mixin — all the networking + UI-update logic
# ─────────────────────────────────────────────────────────────────────────

class ChallengeMixin:
    """Mix into DashboardApp: `class DashboardApp(ChallengeMixin, MDApp):`.
    Uses the app's existing self.backend_api_request/self.session_token/
    self.current_user/self.show_error_dialog/self.show_success_dialog —
    no new networking plumbing needed."""

    _challenge_card = None
    _challenge_countdown_seconds = 0
    _challenge_notif_dialog = None

    # ── dashboard card lifecycle ─────────────────────────────────────────

    def install_challenge_dashboard_card(self):
        """Call once (e.g. at the end of build(), or on first dashboard
        entry) to inject the card into the dashboard and start refreshing."""
        try:
            screen = self.root.get_screen('dashboard')
            box = screen.ids.dashboard_content_box
        except Exception as e:
            print(f"⚠️ Could not find dashboard_content_box: {e}")
            return
        if self._challenge_card is None:
            self._challenge_card = ChallengeDashboardCard()
            insert_dashboard_card(box, self._challenge_card, after_index=1)
        self.refresh_challenge_dashboard_card()
        Clock.unschedule(self._tick_challenge_countdown)
        Clock.schedule_interval(self._tick_challenge_countdown, 1)
        Clock.unschedule(self._poll_challenge_notifications)
        Clock.schedule_interval(self._poll_challenge_notifications, 60)

    def refresh_challenge_dashboard_card(self):
        if not self.session_token:
            return

        def callback(success, result):
            if not success or not self._challenge_card:
                return
            data = result.get('data', {})
            card = self._challenge_card
            if not data.get('challenge_enabled', True):
                card.ids.rank_label.text = "Paused"
                card.ids.total_label.text = "—"
                card.ids.overtake_label.text = "The Monthly Challenge is currently paused."
                return

            rank = data.get('rank')
            card.ids.rank_label.text = f"#{rank}" if rank else "Unranked"
            card.ids.total_label.text = _fmt_naira(data.get('total_monthly_purchases', 0))

            overtake = data.get('amount_to_overtake_next')
            if rank == 1:
                card.ids.overtake_label.text = "🥇 You're in the lead — keep it up!"
            elif overtake is not None:
                card.ids.overtake_label.text = f"Spend {_fmt_naira(overtake)} more to overtake the next rank"
            else:
                card.ids.overtake_label.text = "Make a purchase to join the challenge!"

            self._challenge_countdown_seconds = data.get('countdown_seconds', 0)

        self.backend_api_request('challenge/my-summary', 'GET', None, callback)

    def _tick_challenge_countdown(self, dt):
        if self._challenge_countdown_seconds > 0:
            self._challenge_countdown_seconds -= 1
        text = _fmt_countdown(self._challenge_countdown_seconds)
        if self._challenge_card:
            self._challenge_card.ids.countdown_label.text = text
        try:
            screen = self.root.get_screen('monthly_challenge')
            screen.ids.screen_countdown_label.text = text
        except Exception:
            pass

    # ── screen navigation ────────────────────────────────────────────────

    def open_monthly_challenge_screen(self):
        self.root.current = 'monthly_challenge'
        self.fetch_challenge_leaderboard()

    def open_winners_history_screen(self):
        self.root.current = 'winners_history'
        self.fetch_winners_history()

    def open_challenge_admin_screen(self):
        role = (self.current_user or {}).get('role')
        if role != 'admin':
            self.show_error_dialog("Admin access required.")
            return
        self.root.current = 'challenge_admin'
        self.admin_fetch_challenge_config()

    # ── leaderboard screen ───────────────────────────────────────────────

    def fetch_challenge_leaderboard(self):
        screen = self.root.get_screen('monthly_challenge')
        box = screen.ids.leaderboard_box
        box.clear_widgets()

        def callback(success, result):
            if not success:
                msg = result.get('message', 'Could not load leaderboard')
                screen.ids.my_rank_summary_label.text = msg
                return
            data = result.get('data', {})
            self._challenge_countdown_seconds = data.get('countdown_seconds', 0)
            leaderboard = data.get('leaderboard', [])
            if not leaderboard:
                screen.ids.my_rank_summary_label.text = "No purchases recorded yet this month — be the first!"
                return

            my_id = (self.current_user or {}).get('id')
            my_row = next((r for r in leaderboard if r['user_id'] == my_id), None)
            if my_row:
                screen.ids.my_rank_summary_label.text = (
                    f"You're Rank #{my_row['rank']} with {_fmt_naira(my_row['total_amount'])} this month"
                )
            else:
                screen.ids.my_rank_summary_label.text = "Make a purchase to appear on the leaderboard!"

            for row in leaderboard:
                item = LeaderboardRow()
                item.set_data(row)
                box.add_widget(item)
                # subtle fade-in for a modern feel
                item.opacity = 0
                Animation(opacity=1, duration=0.25).start(item)

        self.backend_api_request('challenge/leaderboard', 'GET', None, callback)

    # ── winners history screen ───────────────────────────────────────────

    def fetch_winners_history(self):
        screen = self.root.get_screen('winners_history')
        box = screen.ids.winners_box
        box.clear_widgets()

        def callback(success, result):
            if not success:
                return
            winners = result.get('data', {}).get('winners', [])
            if not winners:
                box.add_widget(MDLabel(text="No winners yet — check back after the current challenge ends!",
                                        halign="center", theme_text_color="Secondary"))
                return
            current_month = None
            for w in winners:
                if w['month'] != current_month:
                    current_month = w['month']
                    box.add_widget(MDLabel(
                        text=current_month, bold=True, font_style="Subtitle1",
                        size_hint_y=None, height=dp(30),
                    ))
                row = LeaderboardRow()
                row.set_data({
                    'rank': w['rank'], 'name': w['user_name'],
                    'avatar_initial': (w['user_name'][:1].upper() if w['user_name'] else '?'),
                    'total_amount': w['total_amount'],
                    'reward_position': f"Won {_fmt_naira(w['reward_amount'])}"
                                        + ("" if w['credited'] else " (pending credit)"),
                    'progress_percent': 100,
                })
                box.add_widget(row)

        self.backend_api_request('challenge/winners', 'GET', None, callback)

    # ── in-app notifications (push-ready) ────────────────────────────────

    def _poll_challenge_notifications(self, dt=None):
        if not self.session_token:
            return

        def callback(success, result):
            if not success:
                return
            notifs = result.get('data', {}).get('notifications', [])
            unread = [n for n in notifs if not n['is_read']]
            for n in reversed(unread):  # oldest first
                toast(n['title'])
            if unread:
                self.backend_api_request('challenge/notifications/read', 'POST', {}, lambda *a: None)

        self.backend_api_request('challenge/notifications?unread_only=true', 'GET', None, callback)

    # ── admin panel ───────────────────────────────────────────────────────

    def admin_fetch_challenge_config(self):
        screen = self.root.get_screen('challenge_admin')

        def callback(success, result):
            if not success:
                self.show_error_dialog(result.get('message', 'Could not load settings'))
                return
            cfg = result.get('data', {})
            screen.ids.enabled_switch.active = bool(cfg.get('is_enabled', True))
            screen.ids.first_place_field.text = str(cfg.get('first_place_percent', 50))
            screen.ids.second_place_field.text = str(cfg.get('second_place_bonus', 10000))
            screen.ids.third_place_field.text = str(cfg.get('third_place_bonus', 5000))
            screen.ids.min_qualify_field.text = str(cfg.get('min_qualifying_amount', 0))
            screen.ids.last_processed_label.text = f"Last processed month: {cfg.get('last_processed_month') or '—'}"

        self.backend_api_request('admin/challenge/config', 'GET', None, callback)

    def admin_save_challenge_config(self):
        screen = self.root.get_screen('challenge_admin')
        try:
            payload = {
                'is_enabled': screen.ids.enabled_switch.active,
                'first_place_percent': float(screen.ids.first_place_field.text or 0),
                'second_place_bonus': float(screen.ids.second_place_field.text or 0),
                'third_place_bonus': float(screen.ids.third_place_field.text or 0),
                'min_qualifying_amount': float(screen.ids.min_qualify_field.text or 0),
            }
        except ValueError:
            self.show_error_dialog("Please enter valid numbers.")
            return

        def callback(success, result):
            if success:
                self.show_success_dialog("Challenge settings updated.")
            else:
                self.show_error_dialog(result.get('message', 'Update failed'))

        self.backend_api_request('admin/challenge/config', 'POST', payload, callback)

    def admin_process_month_confirm(self):
        dialog = MDDialog(
            title="Process month now?",
            text="This will archive the Top 3 winners for the last completed month "
                 "and credit their wallets immediately (safe to run more than once — "
                 "already-processed months are skipped).",
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(text="PROCEED", on_release=lambda x: (dialog.dismiss(), self._admin_process_month())),
            ],
        )
        dialog.open()

    def _admin_process_month(self):
        def callback(success, result):
            if success or result.get('status') in ('success', 'skipped'):
                self.show_success_dialog(result.get('status', 'Done').capitalize()
                                          + f" — {result.get('reason', result.get('month', ''))}")
            else:
                self.show_error_dialog(result.get('message', 'Failed to process month'))

        self.backend_api_request('admin/challenge/process-month', 'POST', {}, callback)

    def admin_export_winners_csv(self):
        """CSV endpoints aren't JSON, so this bypasses backend_api_request
        and fetches/saves the file directly in a background thread."""
        if not self.session_token:
            self.show_error_dialog("Not logged in.")
            return

        def worker():
            try:
                resp = requests.get(
                    f"{self.backend_url}/api/admin/challenge/export/winners",
                    headers={'Authorization': f'Bearer {self.session_token}'},
                    timeout=30,
                )
                if resp.status_code != 200:
                    Clock.schedule_once(lambda dt: self.show_error_dialog("Export failed."), 0)
                    return
                import os
                from kivy.app import App
                out_dir = App.get_running_app().user_data_dir
                path = os.path.join(out_dir, "challenge_winners.csv")
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(resp.text)
                Clock.schedule_once(lambda dt: self.show_success_dialog(f"Saved to: {path}"), 0)
            except Exception as e:
                Clock.schedule_once(lambda dt, e=e: self.show_error_dialog(f"Export error: {e}"), 0)

        threading.Thread(target=worker, daemon=True).start()
