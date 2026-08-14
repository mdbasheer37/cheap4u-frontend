from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import (
    OneLineIconListItem, IconLeftWidget, TwoLineListItem, OneLineAvatarListItem, OneLineListItem, MDList
)
from datetime import datetime, timedelta
import random
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window

# Without this, Android's on-screen keyboard just overlays the window with
# nothing repositioning the field currently being typed into -- on a field
# positioned low on screen, the keyboard can cover it entirely, leaving no
# visible feedback of what's being typed. 'below_target' shifts the window
# content so the focused text field always stays visible directly above the
# keyboard, the same way most other apps behave. Applies to every field in
# the app automatically, no per-screen changes needed.
Window.softinput_mode = 'below_target'
from kivy.metrics import dp, Metrics

# Kivy's sp() unit (used internally by KivyMD for font sizes) multiplies by
# the OS's accessibility font-scale setting on Android by default -- meaning
# a user who bumps their phone's system font size up or down would see the
# whole app's text resize to match, unpredictably breaking layouts that
# were designed around fixed sizes. Locking fontscale to 1 makes sp()
# behave identically to dp() everywhere, so the app's typography is always
# exactly what it was designed to be, independent of the device's system
# font-size setting.
Metrics.fontscale = 1
from kivy.network.urlrequest import UrlRequest
from kivy.properties import (
    StringProperty, ObjectProperty, NumericProperty, ListProperty, BooleanProperty
)
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.factory import Factory

from kivymd.app import MDApp
from kivymd.uix.fitimage import FitImage
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDRectangleFlatButton, MDIconButton
from kivymd.uix.behaviors import BackgroundColorBehavior, RoundedRectangularElevationBehavior
from kivymd.uix.list import (
    OneLineIconListItem, IconLeftWidget, TwoLineListItem, OneLineAvatarListItem, OneLineListItem
)
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.textfield import MDTextField
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.segmentedcontrol import MDSegmentedControl, MDSegmentedControlItem   # idan kana amfani da su a KV
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast

# Standard libs
import os, re, json, hashlib, random, traceback, webbrowser, threading, time
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────
# Legal text (Terms of Service / Privacy Policy)
# ─────────────────────────────────────────────────────────────────────────
# NOTE: This is a solid, genuinely useful starting point covering the main
# things a Nigerian VTU app needs (wallet funding, no-refund policy for
# correctly-entered wrong numbers, provider dependency, referral terms,
# data usage/third parties). It is NOT a substitute for review by a
# Nigerian lawyer, especially regarding NDPR (Nigeria Data Protection
# Regulation) compliance once you have real paying users at scale -
# please have a lawyer review before you scale significantly.

TERMS_OF_SERVICE_TEXT = """Terms of Service

Last updated: July 2026

Welcome to Cheap4U. These Terms of Service ("Terms") govern your use of the Cheap4U mobile application ("App") operated by Cheap4U Technology ("we", "us", "our"). By creating an account or using the App, you agree to these Terms. If you do not agree, please do not use the App.

1. Our Services
Cheap4U lets you purchase airtime, mobile data, cable TV subscriptions, electricity tokens, and examination PINs (WAEC, NECO, NABTEB, JAMB), and to fund and manage an in-app wallet, for yourself or on behalf of another phone number/meter/smartcard that you provide.

2. Account Registration
You must provide accurate, current information when creating an account, including a valid phone number and email address. You are responsible for keeping your login details and OTPs confidential. You must be at least 18 years old, or have the consent of a parent/guardian, to use this App.

3. Wallet & Payments
- Wallet funding is processed through Paystack. We do not store your card details.
- Prices shown in the App include our service margin and may change without prior notice to reflect changes in provider pricing.
- All wallet top-ups and successful purchases are final. We do not offer cash refunds for wallet balance; unused balance remains in your wallet for future purchases.

4. Accuracy of Recipient Details
You are solely responsible for entering the correct phone number, meter number, smartcard number, or exam type before confirming any purchase. Once a transaction is successfully processed by the network/provider, we cannot reverse, cancel, or refund it because of an incorrect number you supplied. Please double-check all details before confirming.

5. Service Availability
Airtime, data, cable, and electricity purchases depend on third-party network providers (MTN, Airtel, Glo, 9Mobile, DSTV, GOTV, StarTimes, and electricity distribution companies) and payment processors. We are not responsible for delays, failures, or downtime caused by these third parties, but we will make reasonable efforts to reverse your wallet debit if a provider confirms a transaction genuinely failed on their end.

6. Referral Program
Referral bonuses are credited according to the terms displayed in the Referral section of the App at the time you earn them. We reserve the right to withhold or reverse referral bonuses obtained through fraud, fake accounts, or abuse of the program, and to change referral terms for future referrals at any time.

7. Prohibited Use
You agree not to use the App for money laundering, fraud, purchasing services for resale without our written permission, or any illegal activity. We may suspend or terminate accounts that violate this section, misuse the referral program, or attempt to abuse wallet funding (e.g. chargebacks after successful purchases).

8. Limitation of Liability
To the maximum extent permitted by law, Cheap4U Technology is not liable for indirect, incidental, or consequential damages arising from your use of the App, including losses from an incorrectly entered recipient number, network provider downtime, or unauthorized access to your account caused by your failure to keep your login details secure.

9. Changes to These Terms
We may update these Terms from time to time. Continued use of the App after changes are posted means you accept the updated Terms.

10. Governing Law
These Terms are governed by the laws of the Federal Republic of Nigeria.

11. Contact Us
For questions about these Terms, contact us through the support option in the App."""

PRIVACY_POLICY_TEXT = """Privacy Policy

Last updated: July 2026

This Privacy Policy explains how Cheap4U Technology we collects, uses, and protects your information when you use the Cheap4U mobile application ("App").

1. Information We Collect
- Account information: your name, email address, phone number, and password (stored securely as a hash, never in plain text).
- Transaction information: purchases you make (airtime, data, cable TV, electricity, exam pins), amounts, timestamps, and recipient details you enter (phone numbers, meter numbers, smartcard numbers).
- Wallet & payment information: wallet balance and funding history. Card/bank details you enter to fund your wallet are handled directly by Paystack, our payment processor - we do not receive or store your full card number, CVV, or PIN.
- Device & usage information: basic technical information such as app version and error logs, used to diagnose and fix problems.

2. How We Use Your Information
- To process your airtime, data, cable TV, electricity, and exam PIN purchases through our provider partners (CheapDataHub, VTpass, and similar VTU providers).
- To fund and manage your in-app wallet, including via Paystack.
- To communicate with you about your transactions, account, or referral earnings (via SMS, email, or in-app notifications).
- To detect and prevent fraud, and to enforce our Terms of Service.
- To improve the App and fix bugs.

3. How We Share Your Information
We share only what's necessary to provide the service:
- With Paystack, to process wallet funding.
- With our VTU provider partners (e.g. CheapDataHub, VTpass), to fulfil the specific airtime/data/cable/electricity/exam-pin purchase you request - this includes the recipient phone number, meter number, or smartcard number you provide.
- With SMS/communication providers, to send you OTPs and transaction notifications.
- We do not sell your personal information to advertisers or other third parties.
- We may disclose information if required by Nigerian law or a valid legal request.

4. Data Retention
We retain your account and transaction data for as long as your account is active, and for a reasonable period afterward as required for accounting, fraud prevention, and legal compliance.

5. Your Rights
You can review and update your profile information in the App at any time. You may request account deletion through the Account Deletion option in your Profile - this will deactivate your account and remove your personal data from our active systems, except where we are required to retain transaction records for legal/accounting purposes.

6. Security
We use industry-standard measures (password hashing, encrypted connections, rate limiting) to protect your data. No method of transmission or storage is 100% secure, but we work to protect your information to the best of our ability.

7. Children's Privacy
The App is not directed at children under 18. We do not knowingly collect data from children under 18.

8. Changes to This Policy
We may update this Privacy Policy from time to time. We will indicate the "Last updated" date above when changes are made. Continued use of the App after changes are posted means you accept the updated Policy.

9. Contact Us
For questions about this Privacy Policy or your data, contact us through the support option in the App."""


# HTTP
import requests

# Python 3.13 replacements for 'cgi'
import html                     # for escaping text
from urllib.parse import parse_qs, urlencode, quote, unquote

# Add these imports at the top of your Kivy file
import traceback
from datetime import datetime, timedelta
import os

import json
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
import webbrowser

# Replace this line in your imports section:
from kivy.properties import (
    StringProperty, ObjectProperty, NumericProperty, ListProperty, BooleanProperty
)

# With this:
from kivy.properties import (
    StringProperty, ObjectProperty, NumericProperty, ListProperty, BooleanProperty, DictProperty
)



class Config:
    """Configuration class matching Flask backend"""
    # VTPass Service IDs
    VTPASS_SERVICE_IDS = {
        'airtime': {
            'MTN': 'mtn',
            'Airtel': 'airtel', 
            'Glo': 'glo',
            '9Mobile': 'etisalat'
        },
        'data': {
            'MTN': 'mtn-data',
            'Airtel': 'airtel-data',
            'Glo': 'glo-data',
            '9Mobile': 'etisalat-data'
        },
        'electricity': {
            'IKEDC': 'ikeja-electric',
            'EKEDC': 'eko-electric',
            'IBEDC': 'ibadan-electric',
            'AEDC': 'abuja-electric',
            'KEDCO': 'kano-electric',
            'PHED': 'portharcourt-electric',
            'JED': 'jos-electric'
        },
        'cable_tv': {
            'DSTV': 'dstv',
            'GOTV': 'gotv',
            'Startimes': 'startimes',
            'Showmax': 'showmax'
        },
        'exam_pins': {
            'WAEC': 'waec',
            'NECO': 'neco',
            'JAMB': 'jamb',
            'NABTEB': 'nabteb'
        }
    }
    
    VTPASS_VARIATION_CODES = {
        'electricity': {
            'prepaid': 'prepaid',
            'postpaid': 'postpaid'
        },
        'exam_pins': {
            'WAEC': 'waec',
            'NECO': 'neco',
            'JAMB': 'jamb',
            'NABTEB': 'nabteb'
        }
    }


# Security and utility functions

def hash_password(password):

    return hashlib.sha256(password.encode()).hexdigest()



def is_valid_email(email):

    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    return re.match(pattern, email)



def is_valid_phone(phone):

    return len(phone) == 11 and phone.isdigit()



def is_valid_meter_number(meter):

    return len(meter) >= 6 and meter.isdigit()



def format_currency(amount):

    return f"₦{amount:,.2f}"

        
        
class ProfileScreen(Screen):

    pass



class NetworkSelectionScreen(Screen):

    pass



class PhoneInputScreen(Screen):

    pass



class DashboardScreen(Screen):

    pass



class LoginScreen(Screen):

    pass



class RegisterScreen(Screen):

    pass



class HistoryScreen(Screen):

    pass



class AirtimeTopupScreen(Screen):

    pass



class CableTVScreen(Screen):

    pass



class ElectricityScreen(Screen):

    pass



class DataPurchaseScreen(Screen):

    pass



class OTPVerificationScreen(Screen):

    pass  

 
class ProfileDetailsScreen(Screen):

    pass  

    

class PaymentScreen(Screen):

    pass    
    
class FundingScreen(Screen):
    pass    

class ExamPinScreen(Screen):
    pass     
                                                                       
class WithdrawScreen(Screen):
    pass 
                                                           
class ProfitScreen(Screen):
    pass
    
class ReferralScreen(Screen):
    pass

class CashbackScreen(Screen):
    pass

class SpinScreen(Screen):
    pass

class CouponScreen(Screen):
    pass

class MerchantScreen(Screen):
    pass

class CardScreen(Screen):
    pass

class BillReminderScreen(Screen):
    pass

class ComparisonScreen(Screen):
    pass

class GamificationScreen(Screen):
    pass

class TermsScreen(Screen):
    pass

class PrivacyScreen(Screen):
    pass

class SplashScreen(Screen):
    pass

class PinLoginScreen(Screen):
    pass

class AirtimeToCashScreen(Screen):
    pass

class SupportScreen(Screen):
    pass

class AIChatScreen(Screen):
    pass

KV = '''

#:import hex kivy.utils.get_color_from_hex

#:import colors kivymd.color_definitions.colors

#:import Window kivy.core.window.Window


# Applies to EVERY MDTextField in the app (both KV-defined and
# Python-instantiated ones pick this up automatically) -- explicitly fixes
# the color of the text actually being TYPED, which previously relied on
# KivyMD's own theme-based default and wasn't rendering reliably on some
# devices, making it look like nothing was appearing while typing.
<MDTextField>:
    text_color_normal: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]
    text_color_focus: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]


<CustomCard@MDCard>

    orientation: 'vertical'

    padding: dp(15)

    spacing: dp(10)

    radius: [15]

    elevation: 2

    size_hint: None, None

    size: dp(150), dp(80)

    md_bg_color: app.theme_cls.bg_light



<ProviderButton@MDRectangleFlatButton>

    size_hint: None, None

    size: dp(90), dp(50)

    font_size: '12sp'

    line_color: self.theme_color

    text_color: self.theme_color



<PackageCard@MDCard>

    orientation: 'vertical'

    size_hint: None, None

    size: dp(150), dp(80)

    elevation: 2

    radius: [15]

    md_bg_color: app.theme_cls.bg_light

    theme_color: [1, 1, 1, 1]

    

<FilterChip@MDSegmentedButtonItem>

    size_hint: None, None

    height: dp(40) if not root.parent else root.parent.height

    width: dp(120)

    line_color: self.theme_cls.disabled_hint_text_color if self.state == "normal" else self.theme_cls.primary_color    



# Screen manager to handle multiple screens

MDScreenManager:

    SplashScreen:

    PinLoginScreen:

    AirtimeToCashScreen:

    LoginScreen:

    RegisterScreen:

    DashboardScreen:

    NetworkSelectionScreen:

    PhoneInputScreen:

    ProfileScreen:

    ProfileDetailsScreen:   

    HistoryScreen:

    AirtimeTopupScreen:

    CableTVScreen:

    ElectricityScreen:
        
    PaymentScreen: 
    
    FundingScreen:         

    DataPurchaseScreen:
    
    ExamPinScreen:    
    
    ProfitScreen:
    
    WithdrawScreen:   
    
    ReferralScreen:

    CashbackScreen:

    SpinScreen:

    CouponScreen:

    MerchantScreen:

    CardScreen:

    BillReminderScreen:

    ComparisonScreen:

    GamificationScreen:

    TermsScreen:

    PrivacyScreen:

    OTPVerificationScreen:

        name: "otp_verification"   

    SupportScreen:

    AIChatScreen:



<TermsScreen>:

    name: "terms"

    MDScreen:

        md_bg_color: app.theme_cls.bg_normal

        MDBoxLayout:

            orientation: 'vertical'

            padding: dp(2)

            spacing: dp(10)

            MDBoxLayout:

                size_hint_y: None

                height: dp(60)

                padding: [dp(10), 0]

                spacing: dp(10)

                md_bg_color: app.theme_cls.primary_color

                radius: [10, 10, 0, 0]

                MDIconButton:

                    icon: "arrow-left"

                    theme_icon_color: "Custom"

                    icon_color: [1, 1, 1, 1]

                    on_release: app.root.current = "profile"

                MDLabel:

                    text: "Terms of Service"

                    font_style: "H5"

                    bold: True

                    theme_text_color: "Custom"

                    text_color: [1, 1, 1, 1]

                    halign: "center"

            ScrollView:

                MDLabel:

                    text: app.terms_text

                    padding: dp(20), dp(20)

                    size_hint_y: None

                    height: self.texture_size[1] + dp(40)

                    text_size: self.width - dp(40), None



<PrivacyScreen>:

    name: "privacy"

    MDScreen:

        md_bg_color: app.theme_cls.bg_normal

        MDBoxLayout:

            orientation: 'vertical'

            padding: dp(2)

            spacing: dp(10)

            MDBoxLayout:

                size_hint_y: None

                height: dp(60)

                padding: [dp(10), 0]

                spacing: dp(10)

                md_bg_color: app.theme_cls.primary_color

                radius: [10, 10, 0, 0]

                MDIconButton:

                    icon: "arrow-left"

                    theme_icon_color: "Custom"

                    icon_color: [1, 1, 1, 1]

                    on_release: app.root.current = "profile"

                MDLabel:

                    text: "Privacy Policy"

                    font_style: "H5"

                    bold: True

                    theme_text_color: "Custom"

                    text_color: [1, 1, 1, 1]

                    halign: "center"

            ScrollView:

                MDLabel:

                    text: app.privacy_text

                    padding: dp(20), dp(20)

                    size_hint_y: None

                    height: self.texture_size[1] + dp(40)

                    text_size: self.width - dp(40), None



<SplashScreen>:

    name: "splash"

    MDScreen:

        FloatLayout:

            id: splash_root

            # Smooth diagonal blue gradient background (see GradientBackground
            # class - built once as a small texture, cheap to render). This
            # is the only "graphic" on the splash screen besides the logo.
            GradientBackground:

                id: splash_gradient

                size: splash_root.size

                pos: splash_root.pos

            # Centered app logo.
            Image:

                id: splash_logo

                source: "data/icon.png"

                size_hint: None, None

                size: dp(150), dp(150)

                pos_hint: {'center_x': 0.5, 'center_y': 0.58}

                opacity: 0

            MDLabel:

                id: splash_welcome

                text: "Welcome to Cheap4U"

                font_style: "H5"

                bold: True

                halign: "center"

                theme_text_color: "Custom"

                text_color: [1, 1, 1, 1]

                size_hint: None, None

                size: dp(320), dp(40)

                pos_hint: {'center_x': 0.5, 'center_y': 0.42}

                opacity: 0

            MDLabel:

                id: splash_subtext

                text: "Fast \u2022 Secure \u2022 Reliable"

                font_style: "Body1"

                halign: "center"

                theme_text_color: "Custom"

                text_color: [0.85, 0.9, 1, 1]

                size_hint: None, None

                size: dp(320), dp(30)

                pos_hint: {'center_x': 0.5, 'center_y': 0.36}

                opacity: 0

            # Small, lightweight loading indicator - just text, no spinner
            # graphics or progress-bar fill animation to wait on.
            MDLabel:

                id: splash_loading

                text: "Loading..."

                font_style: "Caption"

                halign: "center"

                theme_text_color: "Custom"

                text_color: [1, 1, 1, 0.75]

                size_hint: None, None

                size: dp(200), dp(24)

                pos_hint: {'center_x': 0.5, 'center_y': 0.18}

                opacity: 0



<AirtimeToCashScreen>:

    name: "airtime_to_cash"

    MDScreen:

        md_bg_color: app.theme_cls.bg_normal

        MDBoxLayout:

            orientation: 'vertical'

            padding: dp(2)

            spacing: dp(10)

            MDBoxLayout:

                size_hint_y: None

                height: dp(60)

                padding: [dp(10), 0]

                spacing: dp(10)

                md_bg_color: app.theme_cls.primary_color

                radius: [10, 10, 0, 0]

                MDIconButton:

                    icon: "arrow-left"

                    theme_icon_color: "Custom"

                    icon_color: [1, 1, 1, 1]

                    on_release: app.root.current = "dashboard"

                MDLabel:

                    text: "Airtime to Cash"

                    font_style: "H5"

                    bold: True

                    theme_text_color: "Custom"

                    text_color: [1, 1, 1, 1]

                    halign: "center"

                    size_hint_x: 0.8

            ScrollView:

                bar_width: dp(4)

                bar_color: app.theme_cls.primary_color

                MDBoxLayout:

                    orientation: 'vertical'

                    spacing: dp(15)

                    padding: [dp(15), dp(15), dp(15), dp(30)]

                    size_hint_y: None

                    height: self.minimum_height

                    MDCard:

                        orientation: 'vertical'

                        padding: dp(15)

                        spacing: dp(12)

                        radius: [15]

                        elevation: 3

                        size_hint_y: None

                        height: self.minimum_height

                        md_bg_color: app.theme_cls.bg_light

                        MDLabel:

                            text: "Select Network"

                            font_style: "H6"

                            bold: True

                            size_hint_y: None

                            height: dp(35)

                            color: app.theme_cls.primary_color

                        MDBoxLayout:

                            id: a2c_network_grid

                            size_hint_y: None

                            height: dp(85)

                            spacing: dp(8)

                            disabled: app.a2c_step != "input"

                        MDTextField:

                            id: a2c_phone_input

                            hint_text: "Your phone number (the SIM to convert from)"

                            icon_left: "phone-outline"

                            input_filter: "int"

                            max_text_length: 11

                            disabled: app.a2c_step != "input"

                        MDTextField:

                            id: a2c_amount_input

                            hint_text: "Amount of airtime to convert (₦)"

                            icon_left: "cash"

                            input_filter: "int"

                            disabled: app.a2c_step != "input"

                        MDRaisedButton:

                            text: "SEND OTP"

                            size_hint_x: 1

                            height: dp(50)

                            md_bg_color: app.theme_cls.primary_color

                            disabled: app.a2c_step != "input"

                            opacity: 1 if app.a2c_step == "input" else 0.4

                            on_release: app.a2c_send_otp()

                    MDCard:

                        orientation: 'vertical'

                        padding: dp(15)

                        spacing: dp(12)

                        radius: [15]

                        elevation: 3

                        size_hint_y: None

                        height: self.minimum_height if app.a2c_step in ("otp", "confirm") else 0

                        opacity: 1 if app.a2c_step in ("otp", "confirm") else 0

                        md_bg_color: app.theme_cls.bg_light

                        MDLabel:

                            text: "Enter the OTP sent to your phone"

                            font_style: "H6"

                            bold: True

                            size_hint_y: None

                            height: dp(35)

                            color: app.theme_cls.primary_color

                        MDTextField:

                            id: a2c_otp_input

                            hint_text: "6-digit OTP"

                            icon_left: "message-text-outline"

                            input_filter: "int"

                            max_text_length: 6

                            disabled: app.a2c_step != "otp"

                        MDRaisedButton:

                            text: "VERIFY OTP"

                            size_hint_x: 1

                            height: dp(50)

                            md_bg_color: app.theme_cls.primary_color

                            disabled: app.a2c_step != "otp"

                            opacity: 1 if app.a2c_step == "otp" else 0.4

                            on_release: app.a2c_verify_otp()

                    MDCard:

                        orientation: 'vertical'

                        padding: dp(15)

                        spacing: dp(12)

                        radius: [15]

                        elevation: 3

                        size_hint_y: None

                        height: self.minimum_height if app.a2c_step == "confirm" else 0

                        opacity: 1 if app.a2c_step == "confirm" else 0

                        md_bg_color: app.theme_cls.bg_light

                        MDLabel:

                            text: f"Airtime balance on this SIM: {app.a2c_airtime_balance}"

                            font_style: "Subtitle1"

                            size_hint_y: None

                            height: dp(30)

                            theme_text_color: "Secondary"

                        MDTextField:

                            id: a2c_sim_pin_input

                            hint_text: "Your SIM's airtime transfer PIN"

                            icon_left: "shield-key-outline"

                            password: True

                            input_filter: "int"

                            max_text_length: 6

                            disabled: app.a2c_step != "confirm"

                        MDRaisedButton:

                            text: "CONVERT TO CASH"

                            size_hint_x: 1

                            height: dp(50)

                            md_bg_color: [0.2, 0.7, 0.3, 1]

                            disabled: app.a2c_step != "confirm"

                            opacity: 1 if app.a2c_step == "confirm" else 0.4

                            on_release: app.a2c_confirm_transfer()



<OTPVerificationScreen>:

    name: "otp_verification"

    MDScreen:

        md_bg_color: app.theme_cls.bg_normal

        MDBoxLayout:

            orientation: 'vertical'

            padding: dp(10)
           
            spacing: dp(10)
            
            Widget:
                size_hint_y: 0.1 
        
            

            # App logo and title

            MDBoxLayout:

                orientation: 'vertical'

                spacing: dp(10)

                size_hint_y: None

                height: dp(100)

                pos_hint: {'center_x': 0.5}

                

                MDIcon:

                    icon: "shield-check"

                    size_hint: (None, None)

                    size: [dp(60), dp(60)]

                    pos_hint: {'center_x': 0.5}

                    theme_text_color: "Custom"

                    text_color: app.theme_cls.primary_color

                

                MDLabel:

                    text: "Verify Your Account"

                    font_style: "H5"

                    halign: "center"

                    bold: True

                    theme_text_color: "Primary"

            

            # OTP form in a card

            MDCard:

                orientation: 'vertical'

                padding: dp(25)

                spacing: dp(20)

                size_hint: (0.9, None)

                height: dp(200)

                pos_hint: {'center_x': 0.5}

                elevation: 5

                radius: [dp(15),]

                md_bg_color: app.theme_cls.bg_light

                

                MDLabel:

                    text: "Enter the 6-digit OTP sent to:"

                    font_style: "Body1"

                    halign: "center"

                    theme_text_color: "Secondary"

                

                MDLabel:

                    id: otp_email_or_phone

                    text: ""

                    font_style: "Subtitle1"

                    halign: "center"

                    bold: True

                    theme_text_color: "Primary"

                

                MDTextField:

                    id: otp_input

                    hint_text: "OTP Code"

                    icon_left: "message-text-outline"

                    input_type: 'number'

                    max_text_length: 6

                    mode: "rectangle"

                    size_hint_y: None

                    height: dp(76)

                    size_hint_x: 1

                    line_color_focus: app.theme_cls.primary_color

                    helper_text: "Enter 6-digit code"

                    helper_text_mode: "on_focus"

                    required: True

                

                MDBoxLayout:

                    orientation: 'horizontal'

                    spacing: dp(10)

                    size_hint_y: None

                    height: dp(40)

                    

                    MDTextButton:

                        text: "Resend OTP"

                        theme_text_color: "Custom"

                        text_color: app.theme_cls.primary_color

                        on_release: app.resend_otp()

                    

                    Widget:

                        size_hint_x: 0.5

                    

                    MDTextButton:

                        text: "Change Email/Phone"

                        theme_text_color: "Custom"

                        text_color: app.theme_cls.primary_color

                        on_release: app.root.current = "register"

            

            # Verify button

            MDRaisedButton:

                text: "VERIFY"

                on_release: app.verify_otp(otp_input.text)

                pos_hint: {'center_x': 0.5}

                size_hint_x: 0.9

                md_bg_color: app.theme_cls.primary_color

                elevation_normal: 5

                font_size: '16sp'

            Widget:
                size_hint_y: 0.3             

            # Back button

            MDTextButton:

                text: "Back to Login"

                on_release: app.root.current = "login"

                pos_hint: {'center_x': 0.5}

                theme_text_color: "Custom"

                text_color: app.theme_cls.primary_color
            
                

<DataPurchaseScreen>:

    name: "data_purchase"

    MDScreen:

        md_bg_color: app.theme_cls.bg_normal

        MDBoxLayout:

            orientation: 'vertical'

            padding: dp(2)

            spacing: dp(10)

            

            # Header with back button and title

            MDBoxLayout:

                size_hint_y: None

                height: dp(60)

                padding: [dp(10), 0]

                spacing: dp(10)

                md_bg_color: app.theme_cls.primary_color

                radius: [10, 10, 0, 0]



                MDIconButton:

                    icon: "arrow-left"

                    theme_icon_color: "Custom"

                    icon_color: [1, 1, 1, 1]

                    #radius: [dp(12),]

                    on_release: app.root.current = "dashboard"



                MDLabel:

                    text: "Data Purchase"

                    font_style: "H5"

                    bold: True

                    theme_text_color: "Custom"

                    text_color: [1, 1, 1, 1]

                  #  radius: [dp(12),]

                    halign: "center"

                    size_hint_x: 0.8



                MDIconButton:

                    icon: "help-circle"

                    theme_icon_color: "Custom"

                    icon_color: [1, 1, 1, 1]

                  #  radius: [dp(12),]

                    on_release: app.show_data_help()



            # Main scrollable content

            ScrollView:

                bar_width: dp(4)

                bar_color: app.theme_cls.primary_color

                

                MDBoxLayout:

                    orientation: 'vertical'

                    spacing: dp(7)

                    padding: [dp(0), dp(3), dp(0), dp(10)]

                    size_hint_y: None

                    height: self.minimum_height

                    

                    # Main content in a card

                    MDCard:

                        orientation: 'vertical'

                        padding: [dp(10), dp(5), dp(9), dp(50)]

                        spacing: dp(7)

                        radius: [15, 15, 10, 10]

                        elevation: 4

                        size_hint_y: None

                        height: self.minimum_height

                        pos_hint: {'center_x': 0.5}

                        size_hint_x: 0.98

                        md_bg_color: app.theme_cls.bg_light



                        # Network selection section

                        MDLabel:

                            text: "Select Network"

                            font_style: "H6"

                            bold: True

                            size_hint_y: None

                            height: dp(50)

                            theme_text_color: "Primary"

                            color: app.theme_cls.primary_color



                        MDGridLayout:

                            id: data_network_grid

                            cols: 4

                            spacing: dp(10)

                            padding: dp(0)

                            size_hint_y: None

                            height: dp(120)



                        # Selected network display

                        MDCard:

                            id: selected_data_network_box

                            size_hint_y: None

                            height: 0 if not app.selected_data_network else dp(50)

                            opacity: 1 if app.selected_data_network else 0

                            md_bg_color: app.theme_cls.primary_light

                            radius: [10]

                            padding: dp(10)

                            elevation: 0



                            MDBoxLayout:

                                MDLabel:

                                    text: "Selected Network:"

                                    font_style: "Subtitle1"

                                    size_hint_x: 0.7

                                    theme_text_color: "Secondary"



                                MDLabel:

                                    id: selected_data_network_label

                                    text: app.selected_data_network if app.selected_data_network else ""

                                    font_style: "Subtitle1"

                                    bold: True

                                    halign: "right"

                                    theme_text_color: "Primary"

                                    color: app.theme_cls.primary_color



                        # Data type selection (SME, SME2, Gifting, etc.)

                        MDLabel:

                            text: "Select Data Type"

                            font_style: "H6"

                            bold: True

                            size_hint_y: None

                            height: dp(30)

                            theme_text_color: "Primary"

                            color: app.theme_cls.primary_color

                            opacity: 1 if app.selected_data_network else 0



                        MDGridLayout:

                            id: data_type_grid

                            cols: 4

                            spacing: dp(5)

                            padding: dp(5)

                            size_hint_y: None

                            height: dp(60) if app.selected_data_network else 0

                            opacity: 1 if app.selected_data_network else 0



                        # Selected data type display

                        MDCard:

                            id: selected_data_type_box

                            size_hint_y: None

                            height: 0 if not app.selected_data_type else dp(50)

                            opacity: 1 if app.selected_data_type else 0

                            md_bg_color: app.theme_cls.primary_light

                            radius: [10]

                            padding: dp(10)

                            elevation: 0



                            MDBoxLayout:

                                MDLabel:

                                    text: "Selected Type:"

                                    font_style: "Subtitle1"

                                    size_hint_x: 0.7

                                    theme_text_color: "Secondary"



                                MDLabel:

                                    id: selected_data_type_label

                                    text: app.selected_data_type if app.selected_data_type else ""

                                    font_style: "Subtitle1"

                                    bold: True

                                    halign: "right"

                                    theme_text_color: "Primary"

                                    color: app.theme_cls.primary_color



                        # Data plan selection

                        MDLabel:

                            text: "Select Data Plan"

                            font_style: "H6"

                            bold: True

                            size_hint_y: None

                            height: dp(30)

                            theme_text_color: "Primary"

                            color: app.theme_cls.primary_color

                            opacity: 1 if app.selected_data_type else 0



                        ScrollView:

                            size_hint_y: None

                            height: dp(200) if app.selected_data_type else 0

                            bar_width: dp(4)

                            bar_color: app.theme_cls.primary_color

                            opacity: 1 if app.selected_data_type else 0



                            MDGridLayout:

                                id: data_plan_grid

                                cols: 1

                                spacing: dp(10)

                                padding: dp(5)

                                size_hint_y: None

                                height: self.minimum_height

                                adaptive_height: True



                        # Selected plan display

                        MDCard:

                            id: selected_data_plan_box

                            size_hint_y: None

                            height: 0 if not app.selected_data_plan else dp(50)

                            opacity: 1 if app.selected_data_plan else 0

                            md_bg_color: app.theme_cls.primary_light

                            radius: [10]

                            padding: dp(10)

                            elevation: 0



                            MDBoxLayout:

                                MDLabel:

                                    text: "Selected Plan:"

                                    font_style: "Subtitle1"

                                    size_hint_x: 0.7

                                    theme_text_color: "Secondary"



                                MDLabel:

                                    id: selected_data_plan_label

                                    text: f"{app.selected_data_plan} - {app.selected_data_amount}" if app.selected_data_plan else ""

                                    font_style: "Subtitle1"

                                    bold: True

                                    halign: "right"

                                    theme_text_color: "Primary"

                                    color: app.theme_cls.primary_color



                        # Phone number input

                        MDTextField:

                            id: data_phone_input

                            hint_text: "Recipient Phone Number"

                            icon_left: "phone-outline"

                            input_type: 'number'

                            helper_text: "Enter 11-digit phone number"

                            helper_text_mode: "on_focus"

                            size_hint_x: 1

                            max_text_length: 11

                            mode: "rectangle"

                            size_hint_y: None

                            height: dp(76)

                            icon_left: "phone"

                            on_text: app.validate_phone_input(self.text, app.selected_data_network)                            

                            color_active: app.theme_cls.primary_color

                            line_color_focus: app.theme_cls.primary_color

                            opacity: 1 if app.selected_data_plan else 0.5

                            disabled: not app.selected_data_plan



                        MDLabel:

                            id: detected_network_label

                            text: ""

                            theme_text_color: "Custom"

                            text_color: app.theme_cls.primary_color

                            opacity: 0



                        # Action button (For Myself only)

                        MDRectangleFlatButton:

                            id: myself_btn

                            text: "For Myself"

                            size_hint_x: 1

                            on_release: app.fill_my_data_number()

                            line_color: app.theme_cls.primary_color

                            text_color: app.theme_cls.primary_color

                            disabled: not app.current_user

                            opacity: 1 if app.selected_data_plan else 0.5

                            disabled: not app.selected_data_plan



                        # Continue button

                        MDFillRoundFlatButton:

                            id: data_continue_btn

                            text: "CONTINUE"

                            on_release: if app.validate_data_purchase(): app.process_data_purchase()

                            pos_hint: {'center_x': 0.5}

                            size_hint_x: 0.9

                            md_bg_color: app.theme_cls.primary_color

                            disabled: not (app.selected_data_network and app.selected_data_type and app.selected_data_plan and len(data_phone_input.text) == 11 and data_phone_input.text.isdigit())

                            opacity: 1 if (app.selected_data_network and app.selected_data_type and app.selected_data_plan and len(data_phone_input.text) == 11 and data_phone_input.text.isdigit()) else 0.5

                            

<ElectricityScreen>:

    name: "electricity"

    MDScreen:

        md_bg_color: app.theme_cls.bg_normal

        

        MDBoxLayout:

            orientation: 'vertical'

            padding: dp(2)

            spacing: dp(10)

            

            # Simplified header without balance

            MDBoxLayout:

                size_hint_y: None

                height: dp(60)

                padding: [dp(10), 0]

                spacing: dp(10)

                md_bg_color: app.theme_cls.primary_color

                radius: [10, 10, 0, 0]

                

                MDIconButton:

                    icon: "arrow-left"

                    theme_icon_color: "Custom"

                    icon_color: [1, 1, 1, 1]

                 #   radius: [dp(12),]

                    on_release: app.root.current = "dashboard"

                

                MDLabel:

                    text: "Electricity Bill Payment"

                    font_style: "H5"

                    bold: True

                    theme_text_color: "Custom"

                    text_color: [1, 1, 1, 1]

                    halign: "center"

                    size_hint_x: 0.8

                

                MDIconButton:

                    icon: "help-circle"

                    theme_icon_color: "Custom"

                    icon_color: [1, 1, 1, 1]

                    #radius: [dp(12),]

                    on_release: app.show_electricity_help()

            

            # Main scrollable content

            ScrollView:

                bar_width: dp(4)

                bar_color: app.theme_cls.primary_color

                

                MDBoxLayout:

                    orientation: 'vertical'

                    spacing: dp(7)

                    padding: [dp(0), dp(3), dp(0), dp(10)]

                    size_hint_y: None

                    height: self.minimum_height

                    

                    # Main content in a card

                    MDCard:

                        orientation: 'vertical'

                        padding: [dp(15), dp(10), dp(10), dp(20)]

                        spacing: dp(15)

                        radius: [15, 15, 10, 10]

                        elevation: 4

                        size_hint_y: None

                        height: self.minimum_height

                        pos_hint: {'center_x': 0.5}

                        size_hint_x: 0.98

                        md_bg_color: app.theme_cls.bg_light

                        

                        # Disco selection section

                        MDLabel:

                            text: "Select Electricity Company"

                            font_style: "H6"

                            bold: True

                            size_hint_y: None

                            height: dp(30)

                            theme_text_color: "Primary"

                            color: app.theme_cls.primary_color

                        

                        MDGridLayout:

                            id: disco_grid

                            cols: 4

                            spacing: dp(7)

                            padding: [dp(0), dp(10), dp(0), dp(10)]

                            size_hint_y: None

                            height: dp(170)

                        

                        # Selected disco display

                        MDCard:

                            id: selected_disco_box

                            size_hint_y: None

                            height: 0 if not app.selected_electricity_provider else dp(50)

                            opacity: 1 if app.selected_electricity_provider else 0

                            md_bg_color: app.theme_cls.primary_light

                            radius: [10]

                            padding: dp(10)

                            elevation: 0

                            

                            MDBoxLayout:

                                MDLabel:

                                    text: "Selected Company:"

                                    font_style: "Subtitle1"

                                    size_hint_x: 0.7

                                    theme_text_color: "Secondary"

                                MDLabel:

                                    id: selected_disco_label

                                    text: app.selected_electricity_provider if app.selected_electricity_provider else ""

                                    font_style: "Subtitle1"

                                    bold: True

                                    halign: "right"

                                    theme_text_color: "Primary"

                                    color: app.theme_cls.primary_color

                        

                        # Meter type selection

                        MDLabel:

                            text: "Select Meter Type"

                            font_style: "H6"

                            bold: True

                            size_hint_y: None

                            height: dp(30)

                            theme_text_color: "Primary"

                            color: app.theme_cls.primary_color

                        

                        MDGridLayout:

                            id: meter_type_grid

                            cols: 2

                            spacing: dp(10)

                            padding: dp(5)

                            size_hint_y: None

                            height: dp(60)

                        

                        # Selected meter type display

                        MDCard:

                            id: selected_meter_type_box

                            size_hint_y: None

                            height: 0 if not app.selected_meter_type else dp(50)

                            opacity: 1 if app.selected_meter_type else 0

                            md_bg_color: app.theme_cls.primary_light

                            radius: [10]

                            padding: dp(10)

                            elevation: 0

                            

                            MDBoxLayout:

                                MDLabel:

                                    text: "Meter Type:"

                                    font_style: "Subtitle1"

                                    size_hint_x: 0.7

                                    theme_text_color: "Secondary"

                                MDLabel:

                                    id: selected_meter_type_label

                                    text: app.selected_meter_type if app.selected_meter_type else ""

                                    font_style: "Subtitle1"

                                    bold: True

                                    halign: "right"

                                    theme_text_color: "Primary"

                                    color: app.theme_cls.primary_color

                        

                        # Meter number input with verify button

                        MDBoxLayout:

                            orientation: 'horizontal'

                            spacing: dp(10)

                            size_hint_y: None

                            height: dp(70)

                            

                            MDTextField:

                                id: meter_number_input

                                hint_text: "Meter Number"

                                input_type: 'number'

                                helper_text: "Enter your meter number"

                                helper_text_mode: "on_focus"

                                size_hint_x: 0.7

                                mode: "rectangle"

                                size_hint_y: None

                                height: dp(76)

                                icon_left: "flash"

                                on_text: app.validate_meter_number(self.text)

                                color_active: app.theme_cls.primary_color

                                line_color_focus: app.theme_cls.primary_color

                            

                            MDRectangleFlatButton:

                                id: verify_meter_btn

                                text: "Verify"

                                size_hint_x: 0.3

                                on_release: app.verify_meter_number(meter_number_input.text)

                                disabled: not (app.selected_electricity_provider and len(meter_number_input.text) >= 6)

                                opacity: 1 if (app.selected_electricity_provider and len(meter_number_input.text) >= 6) else 0.5

                        

                        # Customer name display (shown after verification)

                        MDLabel:

                            id: customer_name_label

                            text: ""

                            font_style: "Subtitle1"

                            theme_text_color: "Secondary"

                            size_hint_y: None

                            height: 0

                            opacity: 0

                        

                        # Phone number input

                        MDTextField:

                            id: electricity_phone_input

                            hint_text: "Your Phone Number"

                            input_type: 'number'

                            helper_text: "Enter 11-digit phone number for receipt"

                            helper_text_mode: "on_focus"

                            size_hint_x: 1

                            max_text_length: 11

                            mode: "rectangle"

                            size_hint_y: None

                            height: dp(76)

                            icon_left: "phone"

                            on_text: app.validate_phone_input(self.text)

                            color_active: app.theme_cls.primary_color

                            line_color_focus: app.theme_cls.primary_color

                        

                        # For myself button

                        MDRectangleFlatButton:

                            id: myself_btn

                            text: "Use My Number"

                            size_hint_x: 1

                            on_release: app.fill_my_electricity_number()

                            line_color: app.theme_cls.primary_color

                            text_color: app.theme_cls.primary_color

                            disabled: not app.current_user

                            opacity: 1 if app.current_user else 0.5

                        

                        # Amount input with check balance button

                        MDBoxLayout:

                            orientation: 'horizontal'

                            spacing: dp(10)

                            size_hint_y: None

                            height: dp(70)

                            

                            MDTextField:

                                id: electricity_amount_input

                                hint_text: "Amount (₦)"

                                icon_left: "cash"

                                helper_text: "Enter amount to pay (₦50 - ₦100,000)"

                                helper_text_mode: "on_focus"

                                size_hint_x: 0.7

                                mode: "rectangle"

                                size_hint_y: None

                                height: dp(76)

                                input_type: 'number'

                                icon_left: "currency-ngn"

                                on_text: app.validate_electricity_amount(self.text)

                                color_active: app.theme_cls.primary_color

                                line_color_focus: app.theme_cls.primary_color

                            

                            MDRectangleFlatButton:

                                id: check_balance_btn

                                text: "Check Balance"

                                size_hint_x: 0.3

                                on_release: app.check_meter_balance()

                                disabled: not (app.selected_electricity_provider and len(meter_number_input.text) >= 6)

                                opacity: 1 if (app.selected_electricity_provider and len(meter_number_input.text) >= 6) else 0.5

                        

                        # Continue button

                        MDFillRoundFlatButton:

                            id: continue_btn

                            text: "CONTINUE"

                            on_release: app.process_electricity_payment()

                            pos_hint: {'center_x': 0.5}

                            size_hint_x: 0.9

                            md_bg_color: app.theme_cls.primary_color

                            disabled: not (app.selected_electricity_provider and app.selected_meter_type and len(meter_number_input.text) > 5 and len(electricity_amount_input.text) > 1 and len(electricity_phone_input.text) == 11)

                            opacity: 1 if (app.selected_electricity_provider and app.selected_meter_type and len(meter_number_input.text) > 5 and len(electricity_amount_input.text) > 1 and len(electricity_phone_input.text) == 11) else 0.5

                            

<CableTVScreen>:

    name: "cable_tv"

    MDScreen:

        md_bg_color: app.theme_cls.bg_normal

        MDBoxLayout:

            orientation: 'vertical'

            padding: dp(2)

            spacing: dp(10)

            

            # Header

            MDBoxLayout:

                size_hint_y: None

                height: dp(60)

                padding: [dp(10), 0]

                spacing: dp(10)

                md_bg_color: app.theme_cls.primary_color

                radius: [10, 10, 0, 0]



                MDIconButton:

                    icon: "arrow-left"

                    theme_icon_color: "Custom"

                    icon_color: [1, 1, 1, 1]

                    #radius: [dp(12),]

                    on_release: app.root.current = "dashboard"



                MDLabel:

                    text: "Cable TV Subscription"

                    font_style: "H5"

                    bold: True

                    theme_text_color: "Custom"

                    text_color: [1, 1, 1, 1]

                    halign: "center"

                    size_hint_x: 0.8



                MDIconButton:

                    icon: "help-circle"

                    theme_icon_color: "Custom"

                    icon_color: [1, 1, 1, 1]

                    #radius: [dp(12),]

                    on_release: app.show_cable_help()



            # Scrollable content

            ScrollView:

                bar_width: dp(4)

                bar_color: app.theme_cls.primary_color

                

                MDBoxLayout:

                    orientation: 'vertical'

                    spacing: dp(5)

                    padding: [dp(0), dp(3), dp(0), dp(10)]

                    size_hint_y: None

                    height: self.minimum_height

                    

                    # Main card

                    MDCard:

                        orientation: 'vertical'

                        padding: [dp(15), dp(10), dp(5), dp(50)]

                        spacing: dp(7)

                        radius: [15, 15, 15, 15]

                        elevation: 10

                        size_hint_y: None

                        height: self.minimum_height

                        pos_hint: {'center_x': 0.5}

                        size_hint_x: 0.98

                        md_bg_color: app.theme_cls.bg_light



                        # Provider selection

                        MDLabel:

                            text: "Select Provider"

                            font_style: "H6"

                            bold: True

                            size_hint_y: None

                            height: dp(30)

                            theme_text_color: "Primary"

                            color: app.theme_cls.primary_color



                        MDGridLayout:

                            id: provider_grid

                            cols: 4

                            spacing: dp(7)

                            padding: dp(0)

                            size_hint_y: None

                            height: dp(120)



                        # Selected provider

                        MDCard:

                            id: selected_provider_box

                            size_hint_y: None

                            height: 0 if not app.selected_cable_provider else dp(50)

                            opacity: 1 if app.selected_cable_provider else 0

                            md_bg_color: app.theme_cls.primary_light

                            radius: [10]

                            padding: dp(10)

                            elevation: 4



                            MDBoxLayout:

                                MDLabel:

                                    text: "Selected Provider:"

                                    font_style: "Subtitle1"

                                    size_hint_x: 0.7

                                    theme_text_color: "Secondary"



                                MDLabel:

                                    id: selected_provider_label

                                    text: app.selected_cable_provider if app.selected_cable_provider else ""

                                    font_style: "Subtitle1"

                                    bold: True

                                    halign: "right"

                                    theme_text_color: "Primary"

                                    color: app.theme_cls.primary_color



                        # Package selection

                        MDLabel:

                            text: "Select Package"

                            font_style: "H6"

                            bold: True

                            size_hint_y: None

                            height: dp(30)

                            theme_text_color: "Primary"

                            color: app.theme_cls.primary_color



                        ScrollView:

                            size_hint_y: None

                            height: dp(200)

                            bar_width: dp(4)

                            bar_color: app.theme_cls.primary_color



                            MDGridLayout:

                                id: package_grid

                                cols: 1

                                spacing: dp(10)

                                padding: dp(5)

                                size_hint_y: None

                                height: self.minimum_height

                                adaptive_height: True



                        # Selected package

                        MDCard:

                            id: selected_package_box

                            size_hint_y: None

                            height: 0 if not app.selected_cable_package else dp(50)

                            opacity: 1 if app.selected_cable_package else 0

                            md_bg_color: app.theme_cls.primary_light

                            radius: [10]

                            padding: dp(10)

                            elevation: 4



                            MDBoxLayout:

                                MDLabel:

                                    text: "Selected Package:"

                                    font_style: "Subtitle1"

                                    size_hint_x: 0.7

                                    theme_text_color: "Secondary"



                                MDLabel:

                                    id: selected_package_label

                                    text: f"{app.selected_cable_package} - ₦{app.selected_cable_amount:,}" if app.selected_cable_package else ""

                                    font_style: "Subtitle1"

                                    bold: True

                                    halign: "right"

                                    theme_text_color: "Primary"

                                    color: app.theme_cls.primary_color



                        # Smartcard input

                        MDTextField:

                            id: smartcard_input

                            hint_text: "Smartcard/IUC Number"

                            helper_text: "Enter your decoder number"

                            helper_text_mode: "on_focus"

                            size_hint_x: 1

                            mode: "rectangle"

                            size_hint_y: None

                            height: dp(76)

                            icon_left: "television"

                            on_text: app.validate_smartcard_input(self.text)

                            color_active: app.theme_cls.primary_color

                            line_color_focus: app.theme_cls.primary_color



                        # For myself button

                        MDRectangleFlatButton:

                            id: myself_btn

                            text: "For Myself"

                            size_hint_x: 1

                            on_release: app.fill_my_smartcard()

                            line_color: app.theme_cls.primary_color

                            text_color: app.theme_cls.primary_color

                            disabled: not app.current_user



                        # Continue button

                        MDFillRoundFlatButton:

                            id: continue_btn

                            text: "CONTINUE"

                            on_release: app.process_cable_subscription()

                            pos_hint: {'center_x': 0.5}

                            size_hint_x: 0.9

                            md_bg_color: app.theme_cls.primary_color

                            disabled: not (app.selected_cable_provider and app.selected_cable_package and len(smartcard_input.text) > 5)

                            opacity: 1 if (app.selected_cable_provider and app.selected_cable_package and len(smartcard_input.text) > 5) else 0.5



<AirtimeTopupScreen>:

    name: "airtime_topup"

    MDScreen:

        md_bg_color: app.theme_cls.bg_normal

        MDBoxLayout:

            orientation: 'vertical'

            padding: dp(2)

            spacing: dp(10)

            

            # Header

            MDBoxLayout:

                size_hint_y: None

                height: dp(60)

                padding: [dp(10), 0]

                spacing: dp(10)

                md_bg_color: app.theme_cls.primary_color

                radius: [10, 10, 0, 0]



                MDIconButton:

                    icon: "arrow-left"

                    theme_icon_color: "Custom"

                    icon_color: [1, 1, 1, 1]

                    #radius: [dp(12),]

                    on_release: app.root.current = "dashboard"



                MDLabel:

                    text: "Airtime Top-Up"

                    font_style: "H5"

                    bold: True

                    theme_text_color: "Custom"

                    text_color: [1, 1, 1, 1]

                    halign: "center"

                    size_hint_x: 0.8



                MDIconButton:

                    icon: "help-circle"

                    theme_icon_color: "Custom"

                    icon_color: [1, 1, 1, 1]

                    #radius: [dp(12),]

                    on_release: app.show_airtime_help()



            # Scrollable content

            ScrollView:

                bar_width: dp(4)

                bar_color: app.theme_cls.primary_color

                

                MDBoxLayout:

                    orientation: 'vertical'

                    spacing: dp(7)

                    padding: [dp(0), dp(3), dp(0), dp(10)]

                    size_hint_y: None

                    height: self.minimum_height

                    

                    # Main card

                    MDCard:

                        orientation: 'vertical'

                        padding: [dp(15), dp(10), dp(5), dp(50)]

                        spacing: dp(10)

                        radius: [15, 15, 15, 15]

                        elevation: 4

                        size_hint_y: None

                        height: self.minimum_height

                        pos_hint: {'center_x': 0.5}

                        size_hint_x: 0.98

                        md_bg_color: app.theme_cls.bg_light



                        # Network selection

                        MDLabel:

                            text: "Select Network"

                            font_style: "H6"

                            bold: True

                            size_hint_y: None

                            height: dp(50)

                            theme_text_color: "Primary"

                            color: app.theme_cls.primary_color



                        MDGridLayout:

                            id: network_grid

                            cols: 4

                            spacing: dp(7)

                            padding: [dp(0), dp(15), dp(0), dp(5)]

                            size_hint_y: None

                            height: dp(120)



                        # Selected network

                        MDCard:

                            id: selected_network_box

                            size_hint_y: None

                            height: 0 if not app.selected_airtime_network else dp(50)

                            opacity: 1 if app.selected_airtime_network else 0

                            md_bg_color: app.theme_cls.primary_light

                            radius: [10]

                            padding: dp(10)

                            elevation: 0



                            MDBoxLayout:

                                MDLabel:

                                    text: "Selected Network:"

                                    font_style: "Subtitle1"

                                    size_hint_x: 0.7

                                    theme_text_color: "Secondary"



                                MDLabel:

                                    id: selected_network_label

                                    text: app.selected_airtime_network if app.selected_airtime_network else ""

                                    font_style: "Subtitle1"

                                    bold: True

                                    halign: "right"

                                    theme_text_color: "Primary"

                                    color: app.theme_cls.primary_color



                        # Amount selection

                        MDLabel:

                            text: "Select Amount"

                            font_style: "H6"

                            bold: True

                            size_hint_y: None

                            height: dp(30)

                            theme_text_color: "Primary"

                            color: app.theme_cls.primary_color



                        ScrollView:

                            size_hint_y: None

                            height: dp(200)

                            bar_width: dp(4)

                            bar_color: app.theme_cls.primary_color



                            MDGridLayout:

                                id: amount_grid

                                cols: 1

                                spacing: dp(5)

                                padding: dp(20)

                                size_hint_y: None

                                height: self.minimum_height

                                adaptive_height: True



                        # Selected amount

                        MDCard:

                            id: selected_amount_box

                            size_hint_y: None

                            height: 0 if not app.selected_airtime_amount else dp(50)

                            opacity: 1 if app.selected_airtime_amount else 0

                            md_bg_color: app.theme_cls.primary_light

                            radius: [10]

                            padding: dp(5)

                            elevation: 0



                            MDBoxLayout:

                                MDLabel:

                                    text: "Selected Amount:"

                                    font_style: "Subtitle1"

                                    size_hint_x: 0.7

                                    theme_text_color: "Secondary"



                                MDLabel:

                                    id: selected_amount_label

                                    text: f"₦{app.selected_airtime_amount:,}" if app.selected_airtime_amount else ""

                                    font_style: "Subtitle1"

                                    bold: True

                                    halign: "right"

                                    theme_text_color: "Primary"

                                    color: app.theme_cls.primary_color



                        # Custom amount

                        MDTextField:

                            id: custom_amount

                            hint_text: "Or enter custom amount"

                            input_type: 'number'

                            helper_text: "Enter amount between ₦100 and ₦50,000"

                            helper_text_mode: "on_focus"

                            size_hint_x: 1

                            mode: "rectangle"

                            size_hint_y: None

                            height: dp(76)

                            icon_left: "currency-ngn"

                            on_text: app.validate_custom_amount(self.text)

                            color_active: app.theme_cls.primary_color

                            line_color_focus: app.theme_cls.primary_color



                        # Phone number

                        MDTextField:

                            id: phone_input

                            hint_text: "Recipient Phone Number"

                            input_type: 'number'

                            helper_text: "Enter 11-digit phone number"

                            helper_text_mode: "on_focus"

                            size_hint_x: 1

                            max_text_length: 11

                            mode: "rectangle"

                            size_hint_y: None

                            height: dp(76)

                            icon_left: "phone"

                            on_text: app.validate_phone_input(self.text)

                            color_active: app.theme_cls.primary_color

                            line_color_focus: app.theme_cls.primary_color



                        # For myself button

                        MDRectangleFlatButton:

                            id: myself_btn

                            text: "For Myself"

                            size_hint_x: 1

                            on_release: app.fill_my_number()

                            line_color: app.theme_cls.primary_color

                            text_color: app.theme_cls.primary_color

                            disabled: not app.current_user



                        # Continue button

                        MDFillRoundFlatButton:

                            id: continue_btn

                            text: "CONTINUE"

                            on_release: app.process_airtime_topup()

                            pos_hint: {'center_x': 0.5}

                            size_hint_x: 0.9

                            md_bg_color: app.theme_cls.primary_color

                            disabled: not (app.selected_airtime_network and app.selected_airtime_amount and len(phone_input.text) == 11)

                            opacity: 1 if (app.selected_airtime_network and app.selected_airtime_amount and len(phone_input.text) == 11) else 0.5

<HistoryScreen>:
    name: "history"
    MDScreen:
        md_bg_color: app.theme_cls.bg_normal
        MDBoxLayout:
            orientation: 'vertical'
            spacing: dp(0)

            # Header
            MDBoxLayout:
                size_hint_y: None
                height: dp(60)
                padding: [dp(10), 0]
                spacing: dp(10)
                md_bg_color: app.theme_cls.primary_color
                radius: [0, 0, 15, 15]
                MDIconButton:
                    icon: "arrow-left"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    #radius: [dp(12),]
                    on_release: app.root.current = "dashboard"
                MDLabel:
                    text: "Transaction History"
                    font_style: "H5"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: [1, 1, 1, 1]
                    halign: "center"
                    size_hint_x: 0.8
                MDIconButton:
                    icon: "filter"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    #radius: [dp(12),]
                    on_release: app.show_history_filters()

            # Loading indicator - FIXED: use size_hint_y instead of fixed height
            MDBoxLayout:
                id: loading_indicator
                orientation: 'vertical'
                spacing: dp(10)
                padding: dp(20)
                size_hint_y: None
                height: dp(2)
                opacity: 0
                MDSpinner:
                    id: history_spinner
                    size_hint: None, None
                    size: dp(40), dp(40)
                    pos_hint: {"center_x": 0.5}
                    active: False
                MDLabel:
                    text: "Loading..."
                    halign: "center"
                    font_style: "Caption"
                    size_hint_y: None
                    height: dp(20)

            # Skeleton placeholders — shown briefly while the real list loads
            MDBoxLayout:
                id: history_skeleton_box
                orientation: 'vertical'
                spacing: dp(8)
                padding: [dp(8), dp(8)]
                size_hint_y: None
                height: 0
                opacity: 0

            # Main transaction list
            ScrollView:
                id: history_scroll
                do_scroll_x: False
                MDList:
                    id: history_list
                    spacing: dp(8)
                    padding: [dp(8), dp(8)]
                    size_hint_y: None
                    height: self.minimum_height

            # Shown when we fall back to locally-cached data after a network failure
            MDLabel:
                id: history_offline_banner
                text: ""
                font_style: "Caption"
                halign: "center"
                theme_text_color: "Secondary"
                size_hint_y: None
                height: 0
                opacity: 0

            # Empty state - FIXED: no conflicting size props
            MDBoxLayout:
                id: empty_state
                orientation: 'vertical'
                spacing: dp(20)
                padding: dp(40)
                size_hint_y: None
                height: dp(2)
                pos_hint: {"center_x": 0.5}
                opacity: 0
                MDIcon:
                    icon: "history"
                    size_hint: None, None
                    size: dp(60), dp(60)
                    pos_hint: {"center_x": 0.5}
                    theme_text_color: "Secondary"
                MDLabel:
                    text: "No transactions yet"
                    font_style: "H6"
                    halign: "center"
                    theme_text_color: "Secondary"
                    size_hint_y: None
                    height: dp(30)
                MDRectangleFlatButton:
                    text: "Go to Dashboard"
                    pos_hint: {"center_x": 0.5}
                    size_hint_x: 0.7
                    on_release: app.root.current = "dashboard"


<ProfileScreen>:

    name: "profile"

    MDScreen:

        md_bg_color: app.theme_cls.bg_normal

        MDBoxLayout:

            orientation: 'vertical'

            padding: dp(0)

            spacing: dp(0)

            



            # Header with back button and title

            MDBoxLayout:

                size_hint_y: None

                height: dp(60)

                padding: [dp(10), 0]

                spacing: dp(10)

                md_bg_color: app.theme_cls.primary_color

                radius: [0, 0, 15, 15]



                MDIconButton:

                    icon: "arrow-left"

                    theme_icon_color: "Custom"

                    icon_color: [1, 1, 1, 1]

                    #radius: [dp(12),]

                    on_release: app.root.current = "dashboard"



                MDLabel:

                    text: "Profile"

                    font_style: "H5"

                    bold: True

                    theme_text_color: "Custom"

                    text_color: [1, 1, 1, 1]

                    halign: "center"

                    size_hint_x: 0.8



            ScrollView:

                do_scroll_x: False

                bar_width: dp(4)

                bar_color: app.theme_cls.primary_color

                MDBoxLayout:

                    orientation: 'vertical'

                    spacing: dp(15)

                    padding: dp(10)

                    size_hint_y: None

                    height: self.minimum_height



                    MDCard:

                        id: profile_card

                        orientation: 'vertical'

                        padding: dp(15)

                        spacing: dp(10)

                        radius: [15]

                        elevation: 4

                        size_hint_y: None

                        height: dp(150)

                        md_bg_color: app.theme_cls.bg_light



                        MDBoxLayout:

                            orientation: 'horizontal'

                            spacing: dp(10)

                            size_hint_y: None

                            height: dp(60)



                            MDIconButton:

                                icon: "account-circle"

                                size_hint: None, None

                                size: [dp(48), dp(48)]

                                #radius: [dp(12),]

                                theme_text_color: "Custom"

                                text_color: app.theme_cls.primary_color

                                on_release: app.root.current = "profile_details"



                            MDLabel:

                                id: profile_name

                                text: ""

                                font_style: "H5"

                                bold: True

                                theme_text_color: "Primary"

                                halign: "left"

                                valign: "center"

                                on_touch_down: 

                                    if self.collide_point(*args[1].pos): app.root.current = "profile_details"



                            MDIconButton:

                                icon: "chevron-right"

                                theme_icon_color: "Custom"

                                #radius: [dp(12),]

                                icon_color: app.theme_cls.primary_color

                                on_release: app.root.current = "profile_details"



                    # Menu items as shown in the screenshot

                    OneLineIconListItem:

                        text: "Upgrade account"

                        on_release: app.show_upgrade_options()

                        IconLeftWidget:

                            icon: "account-arrow-up"

                            theme_text_color: "Custom"

                            #radius: [dp(12),]

                            text_color: app.theme_cls.primary_color



                    OneLineIconListItem:

                        text: "Show My Referrals"

                        on_release: app.show_referrals()

                        IconLeftWidget:

                            icon: "account-group"

                            theme_text_color: "Custom"

                            #radius: [dp(12),]

                            text_color: app.theme_cls.primary_color



                    OneLineIconListItem:

                        text: "Monthly Challenge"

                        on_release: app.open_monthly_challenge_screen()

                        IconLeftWidget:

                            icon: "trophy"

                            theme_text_color: "Custom"

                            text_color: app.theme_cls.primary_color



                    OneLineIconListItem:

                        text: "Winners History"

                        on_release: app.open_winners_history_screen()

                        IconLeftWidget:

                            icon: "medal"

                            theme_text_color: "Custom"

                            text_color: app.theme_cls.primary_color



                    OneLineIconListItem:

                        text: "Challenge Admin"

                        opacity: 1 if app.current_user and app.current_user.get('role') == 'admin' else 0
                        disabled: not (app.current_user and app.current_user.get('role') == 'admin')
                        size_hint_y: None
                        height: dp(48) if app.current_user and app.current_user.get('role') == 'admin' else 0

                        on_release: app.open_challenge_admin_screen()

                        IconLeftWidget:

                            icon: "shield-crown"

                            theme_text_color: "Custom"

                            text_color: app.theme_cls.primary_color



                    OneLineIconListItem:

                        text: "Themes"

                        on_release: app.switch_theme()

                        IconLeftWidget:

                            icon: "theme-light-dark"

                            theme_text_color: "Custom"

                            #radius: [dp(12),]

                            text_color: app.theme_cls.primary_color



                    OneLineIconListItem:

                        text: "Settings"

                        on_release: app.show_settings()

                        IconLeftWidget:

                            icon: "cog"

                            theme_text_color: "Custom"

                            #radius: [dp(12),]

                            text_color: app.theme_cls.primary_color



                    OneLineIconListItem:

                        text: "Security"

                        on_release: app.show_security()

                        IconLeftWidget:

                            icon: "shield-lock"

                            theme_text_color: "Custom"

                            #radius: [dp(12),]

                            text_color: app.theme_cls.primary_color

                   
                    OneLineIconListItem:
                        text: "Set Transaction PIN"
                        on_release: app.show_set_pin_dialog()
                        IconLeftWidget:
                            icon: "lock-plus"
                            theme_text_color: "Custom"
                            text_color: app.theme_cls.primary_color

                    OneLineIconListItem:

                        text: "Legal"

                        on_release: app.show_legal()

                        IconLeftWidget:

                            icon: "file-document"

                            theme_text_color: "Custom"

                            #radius: [dp(12),]

                            text_color: app.theme_cls.primary_color



                    OneLineIconListItem:

                        text: "Account Deletion"

                        on_release: app.show_account_deletion()

                        IconLeftWidget:

                            icon: "delete"

                            theme_text_color: "Custom"

                            #radius: [dp(12),]

                            text_color: [0.9, 0.1, 0.1, 1]

                                



                    # Logout button at the bottom

                    MDRaisedButton:

                        text: "LOGOUT"

                        on_release: app.logout_user()

                        pos_hint: {'center_x': 0.5}

                        size_hint_x: 0.9

                        md_bg_color: [0.9, 0.1, 0.1, 1]

                        icon: "logout"

                        spacing: dp(10)
                                                

<ProfileDetailsScreen>:
    name: "profile_details"

    MDScreen:
        md_bg_color: app.theme_cls.bg_normal

        # Background decorative element
        MDBoxLayout:
            size_hint: (1, 0.15)
            pos_hint: {"top": 1}
            md_bg_color: app.theme_cls.primary_color
            radius: [0, 0, dp(30), dp(30)]

        MDBoxLayout:
            orientation: 'vertical'
            spacing: dp(10)

            # Action bar with back button
            MDBoxLayout:
                size_hint_y: None
                height: dp(56)
                padding: [dp(10), dp(10), dp(10), 0]

                MDIconButton:
                    icon: "arrow-left"
                    theme_icon_color: "Custom"
                    icon_color: app.theme_cls.primary_color if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]
                    ripple_scale: 0.8
                    icon_color: [1, 1, 1, 1]
                    #radius: [dp(12),]
                    on_release: 
                        app.root.transition.direction = "right"
                        app.root.current = "profile"

                MDLabel:
                    text: "My Profile"
                    font_style: "H5"
                    bold: True
                    halign: "center"
                    size_hint_x: 0.8

                Widget:  # Spacer

            ScrollView:
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: dp(20)
                    padding: [dp(20), dp(10), dp(20), dp(20)]
                    size_hint_y: None
                    height: self.minimum_height

                    # Profile header card
                    MDCard:
                        id: profile_card
                        orientation: 'vertical'
                        size_hint_y: None
                        height: dp(200)
                        padding: dp(20)
                        spacing: dp(10)
                        radius: [dp(15)]
                        elevation: 2
                        md_bg_color: app.theme_cls.bg_light
                        ripple_behavior: True
                        on_release: app.show_edit_profile()

                        BoxLayout:
                            size_hint_y: None
                            height: dp(80)
                            spacing: dp(15)

                            FitImage:
                                source: "assets/default_avatar.png" if not app.current_user or not app.current_user.get('avatar') else app.current_user['avatar']
                                size_hint: (None, 1)
                                width: dp(100)
                                radius: [dp(40)]

                            MDBoxLayout:
                                orientation: 'vertical'
                                spacing: dp(5)
                                padding: [0, dp(10), 0, 0]

                                MDLabel:
                                    id: profile_name
                                    text: "Guest User" if not app.current_user else app.current_user.get('name', '')
                                    font_style: "H5"
                                    bold: True
                                    theme_text_color: "Primary"
                                    adaptive_height: True

                                MDLabel:
                                    id: user_type
                                    text: "Premium Member" if app.current_user and app.current_user.get('is_premium', False) else "Standard Member"
                                    font_style: "Caption"
                                    theme_text_color: "Secondary"
                                    adaptive_height: True

                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: dp(10)
                            size_hint_y: None
                            height: dp(40)

                            MDIcon:
                                icon: "shield-check" if app.current_user and app.current_user.get('verified', False) else "shield-alert"
                                theme_text_color: "Custom"
                                text_color: app.theme_cls.primary_color if app.current_user and app.current_user.get('verified', False) else [0.9, 0.3, 0.3, 1]
                                size_hint_x: 0.15

                            MDLabel:
                                text: "Verified Account" if app.current_user and app.current_user.get('verified', False) else "Unverified Account"
                                font_style: "Body2"
                                theme_text_color: "Primary"
                                size_hint_x: 0.85

                    # Account Information Section
                    MDLabel:
                        text: "ACCOUNT INFORMATION"
                        font_style: "Overline"
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: dp(20)
                        bold: True
                        padding: [dp(10), 0, dp(10), 0]

                    MDCard:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: dp(330)
                        padding: dp(20)
                        spacing: dp(15)
                        radius: [dp(12)]
                        elevation: 1
                        md_bg_color: app.theme_cls.bg_light

                        # Email
                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: dp(29)
                            size_hint_y: None
                            height: dp(50)

                            MDIcon:
                                icon: "email"
                                text_color: 0.1, 0.6, 1, 1
                                theme_text_color: "Custom"
                                size_hint_x: 0.1

                            MDBoxLayout:
                                orientation: 'vertical'
                                spacing: dp(2)

                                MDLabel:
                                    text: "Email Address"
                                    font_style: "Caption"
                                    theme_text_color: "Secondary"
                                    size_hint_y: None
                                    height: dp(20)

                                MDLabel:
                                    id: user_email
                                    text: "Not set" if not app.current_user else app.current_user.get('email', 'Not set')
                                    font_style: "Body2"
                                    theme_text_color: "Primary"
                                    adaptive_height: True

                        MDSeparator:
                            height: dp(1)

                        # Phone
                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: dp(29)
                            size_hint_y: None
                            height: dp(50)

                            MDIcon:
                                icon: "phone"
                                text_color: 0.1, 0.6, 1, 1
                                theme_text_color: "Custom"
                                size_hint_x: 0.1

                            MDBoxLayout:
                                orientation: 'vertical'
                                spacing: dp(2)

                                MDLabel:
                                    text: "Phone Number"
                                    font_style: "Caption"
                                    theme_text_color: "Secondary"
                                    size_hint_y: None
                                    height: dp(20)

                                MDLabel:
                                    id: user_phone
                                    text: "Not set" if not app.current_user else app.current_user.get('phone', 'Not set')
                                    font_style: "Body2"
                                    theme_text_color: "Primary"
                                    adaptive_height: True

                        MDSeparator:
                            height: dp(1)

                        # Member Since
                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: dp(29)
                            size_hint_y: None
                            height: dp(50)

                            MDIcon:
                                icon: "calendar-star"
                                text_color: 0.1, 0.6, 1, 1
                                theme_text_color: "Custom"
                                size_hint_x: 0.1

                            MDBoxLayout:
                                orientation: 'vertical'
                                spacing: dp(2)

                                MDLabel:
                                    text: "Member Since"
                                    font_style: "Caption"
                                    theme_text_color: "Secondary"
                                    size_hint_y: None
                                    height: dp(20)

                                MDLabel:
                                    id: joined_date
                                    text: app.format_date(app.current_user.get('joined_date')) if app.current_user else "Unknown"
                                    font_style: "Body2"
                                    theme_text_color: "Primary"
                                    adaptive_height: True

                        MDSeparator:
                            height: dp(1)

                        # Last Active
                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: dp(29)
                            size_hint_y: None
                            height: dp(50)

                            MDIcon:
                                icon: "clock-check"
                                text_color: 0.1, 0.6, 1, 1
                                theme_text_color: "Custom"
                                size_hint_x: 0.1

                            MDBoxLayout:
                                orientation: 'vertical'
                                spacing: dp(2)

                                MDLabel:
                                    text: "Last Active"
                                    font_style: "Caption"
                                    theme_text_color: "Secondary"
                                    size_hint_y: None
                                    height: dp(20)

                                MDLabel:
                                    id: last_login
                                    text: app.format_datetime(app.current_user.get('last_login')) if app.current_user else "Never"
                                    font_style: "Body2"
                                    theme_text_color: "Primary"
                                    adaptive_height: True

                    # Action Buttons
                    MDBoxLayout:
                        orientation: 'vertical'
                        spacing: dp(15)
                        size_hint_y: None
                        height: dp(170)
                        padding: [dp(20), 0, dp(20), 0]

                        MDRectangleFlatButton:
                            text: "EDIT PROFILE"
                            theme_text_color: "Custom"
                            text_color: app.theme_cls.primary_color
                            line_color: app.theme_cls.primary_color
                            size_hint_y: None
                            height: dp(50)
                            on_release: app.show_edit_profile()

                        MDRectangleFlatButton:
                            text: "CHANGE PASSWORD"
                            theme_text_color: "Custom"
                            text_color: app.theme_cls.primary_color
                            line_color: app.theme_cls.primary_color
                            size_hint_y: None
                            height: dp(50)
                            on_release: app.show_change_password()

                        MDRectangleFlatButton:
                            text: "PROFIT DASHBOARD"
                            theme_text_color: "Custom"
                            text_color: [0.8, 0.2, 0.8, 1]
                            line_color: [0.8, 0.2, 0.8, 1]
                            size_hint_y: None
                            height: dp(50)
                            on_release: app.show_profit_dashboard()

                            

<NetworkSelectionScreen>:

    name: "network_select"

    MDScreen:

        MDBoxLayout:

            orientation: 'vertical'

            padding: dp(20)

            spacing: dp(15)



            MDLabel:

                text: "Buy Data" if app.service_type == "data" else "Select Network"

                font_style: "H5"

                halign: "center"

                size_hint_y: None

                height: self.texture_size[1]

                bold: True

                theme_text_color: "Custom"

                text_color: 0.1, 0.6, 1, 1



            MDRectangleFlatButton:

                id: balance_btn

                text: "CLICK TO VIEW CODES FOR CHECKING BALANCE"

                pos_hint: {'center_x': 0.5}

                size_hint_x: 0.9

                font_size: '13sp'

                theme_text_color: "Custom"

                text_color: 0.1, 0.6, 1, 1

                line_color: 0.1, 0.6, 1, 1

                on_release: app.show_balance_codes()

                md_bg_color: 0.95, 0.95, 0.95, 1

                padding: dp(15)

                opacity: 1 if app.service_type == "data" else 0

                height: 0 if app.service_type != "data" else dp(50)

                disabled: app.service_type != "data"

                ripple_scale: 0.8

                ripple_color: 0.1, 0.6, 1, 0.2

                icon: "information-outline" if app.theme_cls.theme_style == "Light" else "information"

                icon_color: 0.1, 0.6, 1, 1

                spacing: dp(10)



            ScrollView:

                MDList:

                    id: network_list

                    spacing: dp(10)

                    padding: dp(5)



            MDRaisedButton:

                id: continue_btn

                text: "Continue"

                on_release: app.go_to_phone_input()

                pos_hint: {'center_x': 0.5}

                size_hint_x: 0.8

                disabled: not app.selected_network

                md_bg_color: (0.1, 0.6, 1, 1) if app.selected_network else (0.7, 0.7, 0.7, 1)

                elevation_normal: 4

                ripple_scale: 0.8



            MDFlatButton:

                text: "Back"

                on_release: app.root.current = "dashboard"

                pos_hint: {'center_x': 0.5}

                theme_text_color: "Custom"

                text_color: 0.1, 0.6, 1, 1



<PhoneInputScreen>:

    name: "phone_input"

    MDScreen:

        MDBoxLayout:

            orientation: 'vertical'

            padding: dp(20)

            spacing: dp(20)



            MDLabel:

                text: "Enter Phone Number"

                font_style: "H5"

                halign: "center"

                size_hint_y: None

                height: self.texture_size[1]



            MDTextField:

                id: phone_input

                hint_text: "Phone Number"

                icon_left: "phone-outline"

                input_type: 'number'

                helper_text: "Enter recipient phone number"

                helper_text_mode: "on_focus"

                size_hint_x: 0.8

                pos_hint: {'center_x': 0.5}

                max_text_length: 11



            MDRaisedButton:

                text: "Continue"

                on_release: app.process_phone_input(phone_input.text)

                pos_hint: {'center_x': 0.5}

                size_hint_x: 0.8

                disabled: len(phone_input.text) != 11

                md_bg_color: (0.1, 0.6, 1, 1) if len(phone_input.text) == 11 else (0.7, 0.7, 0.7, 1)



            MDFlatButton:

                text: "Back"

                on_release: app.root.current = "network_select"

                pos_hint: {'center_x': 0.5}



<DashboardScreen>:

    name: "dashboard"

    on_pre_enter: app.install_challenge_dashboard_card()

    MDScreen:

        md_bg_color: [0.95, 0.95, 0.98, 1] if app.theme_cls.theme_style == "Light" else [0.1, 0.1, 0.15, 1]

        MDBoxLayout:

            orientation: 'vertical'

            padding: [dp(0), dp(0), dp(0), dp(0)]

            spacing: dp(0)

            

            ScrollView:

                md_bg_color: [0.95, 0.95, 0.98, 1] if app.theme_cls.theme_style == "Light" else [0.1, 0.1, 0.15, 1]

                size_hint_y: 8

                padding: [dp(5), dp(20), dp(5), dp(5)]

                do_scroll_x: False

                do_scroll_y: True

                bar_width: dp(3)

                bar_height: dp(0)

                bar_color: app.theme_cls.primary_color

                

                MDBoxLayout:

                    id: dashboard_content_box

                    orientation: 'vertical'

                    spacing: dp(15)

                    padding: [dp(10), dp(10), dp(10), dp(15)]

                    size_hint_y: None

                    height: self.minimum_height



                    # Welcome section with profile

                    MDBoxLayout:

                        spacing: dp(2)

                        size_hint_y: None

                        height: dp(60)

                        padding: [dp(0), dp(10), dp(15), dp(0)]

                        

                        MDIconButton:

                            icon: 'account-circle'

                            size_hint: None, None

                            size: [dp(48), dp(48)]

                            theme_text_color: "Custom"

                            #radius: [dp(12),]

                            text_color: app.theme_cls.primary_color

                            on_release: app.root.current = "profile"

                            

                        MDLabel:

                            id: welcome_label

                            text: "Hi Guest" if not app.current_user else f"Hi {app.current_user['name'].split()[0]}"

                            font_style: "H6"

                            bold: True

                            theme_text_color: "Primary"

                            halign: "left"

                            

                        Widget:

                            size_hint_x: 0.5

                            

                        MDIconButton:

                            icon: 'bell-outline'

                            size_hint: None, None

                            size: [dp(35), dp(35)]

                            theme_text_color: "Custom"

                    #        radius: [dp(12),]

                            text_color: app.theme_cls.primary_color



                    # Wallet balance card with gradient

                    MDCard:

                        orientation: 'vertical'

                        padding: dp(20)

                        spacing: dp(10)

                        radius: [25]

                        md_bg_color: [0.1, 0.6, 1, 1]

                        elevation: 4

                        size_hint_y: None

                        height: dp(150)

                        canvas.before:

                            Color:

                                rgba: [0.1, 0.6, 1, 1] if app.theme_cls.theme_style == "Light" else [0.1, 0.3, 0.6, 1]

                            RoundedRectangle:

                                pos: self.pos

                                size: self.size

                                radius: [25, 25, 25, 25]

                            Color:

                                rgba: [0.3, 0.8, 1, 1] if app.theme_cls.theme_style == "Light" else [0.2, 0.5, 0.8, 1]

                            RoundedRectangle:

                                pos: self.pos[0], self.pos[1] - dp(50)

                                size: self.size[0], self.size[1] + dp(50)

                                radius: [25, 25, 25, 25]



                        MDLabel:

                            text: "Wallet Balance"

                            theme_text_color: "Custom"

                            text_color: [1, 1, 1, 0.9]

                            font_style: "Caption"

                            bold: True

                            halign: "left"

                            

                        MDLabel:

                            id: wallet_balance

                            text: "₦0" if not app.current_user else app.format_currency(app.current_user.get('wallet_balance', 0))

                            font_style: "H3"

                            theme_text_color: "Custom"

                            text_color: [1, 1, 1, 1]

                            bold: True

                            halign: "left"



                        MDBoxLayout:

                            orientation: 'horizontal'

                            spacing: dp(15)

                            size_hint_y: None

                            height: dp(40)

                            

                            MDLabel:

                                text: "Referral Balance"

                                theme_text_color: "Custom"

                                text_color: [1, 1, 1, 0.9]

                                font_style: "Caption"

                                halign: "left"

                                size_hint_x: 0.4

                                

                            MDLabel:

                                id: referral_balance

                                text: "₦0" if not app.current_user else app.format_currency(app.current_user.get('referral_balance', 0))

                                font_style: "Subtitle1"

                                theme_text_color: "Custom"

                                text_color: [1, 1, 1, 1]

                                halign: "right"

                                size_hint_x: 0.6



                    # Quick actions with colorful icons
                    # Inside DashboardScreen, after wallet balance card
                    MDCard:
                        orientation: 'vertical'
                        padding: dp(15)
                        spacing: dp(10)
                        radius: [15]
                        elevation: 2
                        size_hint_y: None
                        height: dp(100)
                        md_bg_color: app.theme_cls.bg_light

                        MDLabel:
                            text: "Your account number"
                            font_style: "Subtitle1"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]

                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: dp(10)
                            size_hint_y: None
                            height: dp(40)

                            MDIconButton:
                                icon: "content-copy"
                                theme_text_color: "Custom"
                                text_color: app.theme_cls.primary_color
                                on_release: app.copy_virtual_account()
                                disabled: not app.virtual_account_number

                            MDLabel:
                                id: virtual_account_display
                                text: f"{app. virtual_bank_name} - {app. virtual_account_number}" if app.  virtual_account_number else "Loading  account..."
                                theme_text_color: "Custom"
                                text_color: [0.35, 0.35, 0.35, 1] if app.theme_cls.theme_style == "Light" else [0.85, 0.85, 0.85, 1]
            
            
                    MDLabel:

                        text: "Quick Actions"

                        font_style: "H6"

                        bold: True

                        padding: [dp(10), 0]

                        size_hint_y: None

                        height: self.texture_size[1]

                        theme_text_color: "Custom"

                        text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]

                        halign: "left"

                     

                    MDGridLayout:

                        cols: 4

                        spacing: dp(6)

                        padding: [dp(1), dp(20), dp(0), dp(0)]

                        size_hint_y: None

                        height: self.minimum_height

                        

                        # Funding

                        MDCard:

                            orientation: "vertical"

                            spacing: dp(10)

                            size_hint: [1, None]

                            height: dp(80)

                            radius: [15]

                            elevation: 2

                            md_bg_color: [0.9, 0.95, 1, 1] if app.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.3, 1]

                            on_release: app.show_funding_options()

                            MDBoxLayout:

                                orientation: "vertical"

                                spacing: dp(5)

                                padding: [dp(5), dp(5), dp(5), dp(15)]

                                size_hint_y: None

                                height: dp(60)

                                pos_hint: {"center_x": 0.5}

                                MDIcon:

                                    icon: "credit-card"

                                    size_hint: [None, None]

                                    size: [dp(30), dp(30)]

                                    pos_hint: {"center_x": 0.5}

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.6, 1, 1]

                                MDLabel:

                                    text: "Funding"

                                    font_style: "Caption"

                                    halign: "center"

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]

                                    size_hint_y: None

                                    height: self.texture_size[1]



                        # Transfer to Banks

                        MDCard:

                            orientation: "vertical"

                            spacing: dp(0)

                            size_hint: [1, None]

                            height: dp(80)

                            radius: [15]

                            elevation: 2

                            md_bg_color: [0.9, 0.95, 1, 1] if app.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.3, 1]

                            on_release: app.show_coming_soon("Transfer to Banks")

                            MDBoxLayout:

                                orientation: "vertical"

                                spacing: dp(5)

                                padding: [dp(5), dp(5), dp(5), dp(15)]

                                size_hint_y: None

                                height: dp(60)

                                pos_hint: {"center_x": 0.5}

                                MDIcon:

                                    icon: "bank-transfer"

                                    size_hint: [None, None]

                                    size: [dp(30), dp(30)]

                                    pos_hint: {"center_x": 0.5}

                                    theme_text_color: "Custom" 

                              #      radius: [dp(12),]                                

                                    text_color: [0.1, 0.5, 0.9, 1]

                                MDLabel:

                                    text: "Transfer to Banks"

                                    font_style: "Caption"

                                    halign: "center"

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]

                                    size_hint_y: None

                                    height: self.texture_size[1]



                        # Transfer to Cheap4U

                        MDCard:

                            orientation: "vertical"

                            spacing: dp(0)

                            size_hint: [1, None]

                            height: dp(80)

                            radius: [15]

                            elevation: 2

                            md_bg_color: [0.9, 0.95, 1, 1] if app.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.3, 1]

                            on_release: app.show_coming_soon("Transfer to Cheap4U")

                            MDBoxLayout:

                                orientation: "vertical"

                                spacing: dp(5)

                                padding: [dp(5), dp(5), dp(5), dp(15)]

                                size_hint_y: None

                                height: dp(60)

                                pos_hint: {"center_x": 0.5}

                                MDIcon:

                                    icon: "account-arrow-right"

                                    size_hint: [None, None]

                                    size: [dp(30), dp(30)]

                                    pos_hint: {"center_x": 0.5}

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.6, 1, 1]

                                MDLabel:

                                    text: "Transfer to Cheap4U"

                                    font_style: "Caption"

                                    halign: "center"

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]

                                    size_hint_y: None

                                    height: self.texture_size[1]
                   
            
                        MDCard:

                            orientation: "vertical"

                            spacing: dp(0)

                            size_hint: [1, None]

                            height: dp(80)

                            radius: [15]

                            elevation: 2

                            md_bg_color: [0.9, 0.95, 1, 1] if app.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.3, 1]

                            on_release: app.show_referral_screen()

                            MDBoxLayout:

                                orientation: "vertical"

                                spacing: dp(5)

                                padding: [dp(5), dp(5), dp(5), dp(15)]

                                size_hint_y: None

                                height: dp(60)

                                pos_hint: {"center_x": 0.5}

                                MDIcon:

                                    icon: "account-plus"

                                    size_hint: [None, None]

                                    size: [dp(30), dp(30)]

                                    pos_hint: {"center_x": 0.5}

                                    theme_text_color: "Custom"

                                    text_color: [0.6, 0.2, 0.8, 1]

                                MDLabel:

                                    text: "Refer"

                                    font_style: "Caption"

                                    halign: "center"

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]

                                    size_hint_y: None

                                    height: self.texture_size[1]

                        MDCard:

                            orientation: "vertical"

                            spacing: dp(0)

                            size_hint: [1, None]

                            height: dp(80)

                            radius: [15]

                            elevation: 2

                            md_bg_color: [0.9, 0.95, 1, 1] if app.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.3, 1]

                            on_release: app.show_cashback_screen()

                            MDBoxLayout:

                                orientation: "vertical"

                                spacing: dp(5)

                                padding: [dp(5), dp(5), dp(5), dp(15)]

                                size_hint_y: None

                                height: dp(60)

                                pos_hint: {"center_x": 0.5}

                                MDIcon:

                                    icon: "cash-refund"

                                    size_hint: [None, None]

                                    size: [dp(30), dp(30)]

                                    pos_hint: {"center_x": 0.5}

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.75, 0.35, 1]

                                MDLabel:

                                    text: "Cashback"

                                    font_style: "Caption"

                                    halign: "center"

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]

                                    size_hint_y: None

                                    height: self.texture_size[1]

                        MDCard:

                            orientation: "vertical"

                            spacing: dp(0)

                            size_hint: [1, None]

                            height: dp(80)

                            radius: [15]

                            elevation: 2

                            md_bg_color: [1, 0.95, 0.9, 1] if app.theme_cls.theme_style == "Light" else [0.3, 0.22, 0.15, 1]

                            on_release: app.show_spin_screen()

                            MDBoxLayout:

                                orientation: "vertical"

                                spacing: dp(5)

                                padding: [dp(5), dp(5), dp(5), dp(15)]

                                size_hint_y: None

                                height: dp(60)

                                pos_hint: {"center_x": 0.5}

                                MDIcon:

                                    icon: "dharmachakra"

                                    size_hint: [None, None]

                                    size: [dp(30), dp(30)]

                                    pos_hint: {"center_x": 0.5}

                                    theme_text_color: "Custom"

                                    text_color: [0.95, 0.55, 0.1, 1]

                                MDLabel:

                                    text: "Spin & Win"

                                    font_style: "Caption"

                                    halign: "center"

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]

                                    size_hint_y: None

                                    height: self.texture_size[1]

                        MDCard:

                            orientation: "vertical"

                            spacing: dp(0)

                            size_hint: [1, None]

                            height: dp(80)

                            radius: [15]

                            elevation: 2

                            md_bg_color: [0.9, 0.9, 1, 1] if app.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.32, 1]

                            on_release: app.show_coupon_screen()

                            MDBoxLayout:

                                orientation: "vertical"

                                spacing: dp(5)

                                padding: [dp(5), dp(5), dp(5), dp(15)]

                                size_hint_y: None

                                height: dp(60)

                                pos_hint: {"center_x": 0.5}

                                MDIcon:

                                    icon: "ticket-percent"

                                    size_hint: [None, None]

                                    size: [dp(30), dp(30)]

                                    pos_hint: {"center_x": 0.5}

                                    theme_text_color: "Custom"

                                    text_color: [0.35, 0.3, 0.9, 1]

                                MDLabel:

                                    text: "Coupons"

                                    font_style: "Caption"

                                    halign: "center"

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]

                                    size_hint_y: None

                                    height: self.texture_size[1]

                        MDCard:

                            orientation: "vertical"

                            spacing: dp(0)

                            size_hint: [1, None]

                            height: dp(80)

                            radius: [15]

                            elevation: 2

                            md_bg_color: [0.9, 0.95, 0.92, 1] if app.theme_cls.theme_style == "Light" else [0.15, 0.25, 0.2, 1]

                            on_release: app.show_merchant_screen()

                            MDBoxLayout:

                                orientation: "vertical"

                                spacing: dp(5)

                                padding: [dp(5), dp(5), dp(5), dp(15)]

                                size_hint_y: None

                                height: dp(60)

                                pos_hint: {"center_x": 0.5}

                                MDIcon:

                                    icon: "briefcase-outline"

                                    size_hint: [None, None]

                                    size: [dp(30), dp(30)]

                                    pos_hint: {"center_x": 0.5}

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.55, 0.4, 1]

                                MDLabel:

                                    text: "Merchant"

                                    font_style: "Caption"

                                    halign: "center"

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]

                                    size_hint_y: None

                                    height: self.texture_size[1]

                        MDCard:

                            orientation: "vertical"

                            spacing: dp(0)

                            size_hint: [1, None]

                            height: dp(80)

                            radius: [15]

                            elevation: 2

                            md_bg_color: [0.92, 0.92, 0.97, 1] if app.theme_cls.theme_style == "Light" else [0.18, 0.18, 0.28, 1]

                            on_release: app.show_card_screen()

                            MDBoxLayout:

                                orientation: "vertical"

                                spacing: dp(5)

                                padding: [dp(5), dp(5), dp(5), dp(15)]

                                size_hint_y: None

                                height: dp(60)

                                pos_hint: {"center_x": 0.5}

                                MDIcon:

                                    icon: "credit-card-outline"

                                    size_hint: [None, None]

                                    size: [dp(30), dp(30)]

                                    pos_hint: {"center_x": 0.5}

                                    theme_text_color: "Custom"

                                    text_color: [0.3, 0.25, 0.7, 1]

                                MDLabel:

                                    text: "Dollar Card"

                                    font_style: "Caption"

                                    halign: "center"

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]

                                    size_hint_y: None

                                    height: self.texture_size[1]

                        MDCard:

                            orientation: "vertical"

                            spacing: dp(0)

                            size_hint: [1, None]

                            height: dp(80)

                            radius: [15]

                            elevation: 2

                            md_bg_color: [0.95, 0.93, 0.85, 1] if app.theme_cls.theme_style == "Light" else [0.28, 0.24, 0.15, 1]

                            on_release: app.show_reminder_screen()

                            MDBoxLayout:

                                orientation: "vertical"

                                spacing: dp(5)

                                padding: [dp(5), dp(5), dp(5), dp(15)]

                                size_hint_y: None

                                height: dp(60)

                                pos_hint: {"center_x": 0.5}

                                MDIcon:

                                    icon: "bell-ring-outline"

                                    size_hint: [None, None]

                                    size: [dp(30), dp(30)]

                                    pos_hint: {"center_x": 0.5}

                                    theme_text_color: "Custom"

                                    text_color: [0.75, 0.55, 0.1, 1]

                                MDLabel:

                                    text: "Reminders"

                                    font_style: "Caption"

                                    halign: "center"

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]

                                    size_hint_y: None

                                    height: self.texture_size[1]

                        MDCard:

                            orientation: "vertical"

                            spacing: dp(0)

                            size_hint: [1, None]

                            height: dp(80)

                            radius: [15]

                            elevation: 2

                            md_bg_color: [0.88, 0.95, 0.96, 1] if app.theme_cls.theme_style == "Light" else [0.12, 0.24, 0.25, 1]

                            on_release: app.show_comparison_screen()

                            MDBoxLayout:

                                orientation: "vertical"

                                spacing: dp(5)

                                padding: [dp(5), dp(5), dp(5), dp(15)]

                                size_hint_y: None

                                height: dp(60)

                                pos_hint: {"center_x": 0.5}

                                MDIcon:

                                    icon: "chart-bar"

                                    size_hint: [None, None]

                                    size: [dp(30), dp(30)]

                                    pos_hint: {"center_x": 0.5}

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.6, 0.65, 1]

                                MDLabel:

                                    text: "Compare"

                                    font_style: "Caption"

                                    halign: "center"

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]

                                    size_hint_y: None

                                    height: self.texture_size[1]

                        MDCard:

                            orientation: "vertical"

                            spacing: dp(0)

                            size_hint: [1, None]

                            height: dp(80)

                            radius: [15]

                            elevation: 2

                            md_bg_color: [1, 0.96, 0.88, 1] if app.theme_cls.theme_style == "Light" else [0.3, 0.25, 0.1, 1]

                            on_release: app.show_gamification_screen()

                            MDBoxLayout:

                                orientation: "vertical"

                                spacing: dp(5)

                                padding: [dp(5), dp(5), dp(5), dp(15)]

                                size_hint_y: None

                                height: dp(60)

                                pos_hint: {"center_x": 0.5}

                                MDIcon:

                                    icon: "trophy-outline"

                                    size_hint: [None, None]

                                    size: [dp(30), dp(30)]

                                    pos_hint: {"center_x": 0.5}

                                    theme_text_color: "Custom"

                                    text_color: [0.85, 0.6, 0.1, 1]

                                MDLabel:

                                    text: "Rewards"

                                    font_style: "Caption"

                                    halign: "center"

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]

                                    size_hint_y: None

                                    height: self.texture_size[1]



                    # Services section

                    MDLabel:

                        text: "Services"

                        font_style: "H6"

                        bold: True

                        padding: [dp(10), 0]

                        size_hint_y: None

                        height: self.texture_size[1]

                        theme_text_color: "Custom"

                        text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]

                        halign: "left"



                    GridLayout:

                        cols: 3

                        spacing: dp(10)

                        padding: [dp(5), dp(5), dp(5), dp(5)]

                        size_hint_y: None

                        height: self.minimum_height



                        # Airtime

                        MDCard:

                            orientation: 'vertical'

                            size_hint: [1, None]

                            height: dp(105)

                            md_bg_color: [0.95, 0.98, 1, 1] if app.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.3, 1]

                            radius: [15]

                            padding: dp(10)

                            elevation: 2

                            on_release: app.buy_airtime()

                            MDBoxLayout:

                                orientation: 'vertical'

                                spacing: dp(5)

                                size_hint_y: None

                                height: dp(80)

                                pos_hint: {"center_x": 0.5}

                                MDIcon:

                                    icon: "phone"

                                    size_hint: [None, None]

                                    size: [dp(40), dp(40)]

                                    pos_hint: {"center_x": 0.5}

                                    theme_text_color: "Custom"

                                    text_color: [1, 0.4, 0.2, 1]

                                MDLabel:

                                    text: "Airtime"

                                    halign: "center"

                                    font_style: "Subtitle1"

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]



                        # Data

                        MDCard:

                            orientation: 'vertical'

                            size_hint: [1, None]

                            height: dp(105)

                            md_bg_color: [0.95, 0.98, 1, 1] if app.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.3, 1]

                            radius: [15]

                            padding: dp(10)

                            elevation: 2

                            on_release: app.buy_data()

                            MDBoxLayout:

                                orientation: 'vertical'

                                spacing: dp(5)

                                size_hint_y: None

                                height: dp(80)

                                pos_hint: {"center_x": 0.5}

                                MDIcon:

                                    icon: "wifi"

                                    size_hint: [None, None]

                                    size: [dp(40), dp(40)]

                                    pos_hint: {"center_x": 0.5}

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.6, 1, 1]

                                MDLabel:

                                    text: "Data"

                                    halign: "center"

                                    font_style: "Subtitle1"

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]



                        # Smile Voice

                        MDCard:

                            orientation: 'vertical'

                            size_hint: [1, None]

                            height: dp(105)

                            md_bg_color: [0.95, 0.98, 1, 1] if app.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.3, 1]

                            radius: [15]

                            padding: dp(10)

                            elevation: 2

                            on_release: app.show_coming_soon("Smile Voice")

                            MDBoxLayout:

                                orientation: 'vertical'

                                spacing: dp(5)

                                size_hint_y: None

                                height: dp(80)

                                pos_hint: {"center_x": 0.5}

                                MDIcon:

                                    icon: "emoticon-outline"

                                    size_hint: [None, None]

                                    size: [dp(40), dp(40)]

                                    pos_hint: {"center_x": 0.5}

                                    theme_text_color: "Custom"

                                    text_color: [0.2, 0.8, 0.2, 1]

                                MDLabel:

                                    text: "Smile Voice"

                                    halign: "center"

                                    font_style: "Subtitle1"

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]



                        # Electricity

                        MDCard:

                            orientation: 'vertical'

                            size_hint: [1, None]

                            height: dp(105)

                            md_bg_color: [0.95, 0.98, 1, 1] if app.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.3, 1]

                            radius: [15]

                            padding: dp(10)

                            elevation: 2

                            on_release: app.buy_electricity()

                            MDBoxLayout:

                                orientation: 'vertical'

                                spacing: dp(5)

                                size_hint_y: None

                                height: dp(80)

                                pos_hint: {"center_x": 0.5}

                                MDIcon:

                                    icon: "flash"

                                    size_hint: [None, None]

                                    size: [dp(40), dp(40)]

                                    pos_hint: {"center_x": 0.5}

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.8, 0.1, 1]

                                MDLabel:

                                    text: "Electricity"

                                    halign: "center"

                                    font_style: "Subtitle1"

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]



                        # Cable Sub

                        MDCard:

                            orientation: 'vertical'

                            size_hint: [1, None]

                            height: dp(105)

                            md_bg_color: [0.95, 0.98, 1, 1] if app.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.3, 1]

                            radius: [15]

                            padding: dp(10)

                            elevation: 2

                            on_release: app.buy_cable_tv()

                            MDBoxLayout:

                                orientation: 'vertical'

                                spacing: dp(5)

                                size_hint_y: None

                                height: dp(80)

                                pos_hint: {"center_x": 0.5}

                                MDIcon:

                                    icon: "television"

                                    size_hint: [None, None]

                                    size: [dp(40), dp(40)]

                                    pos_hint: {"center_x": 0.5}

                                    theme_text_color: "Custom"

                                    text_color: [0.0, 0.6, 0.0, 1]

                                MDLabel:

                                    text: "Cable Sub"

                                    halign: "center"

                                    font_style: "Subtitle1"

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]



                        # Bulk SMS

                        MDCard:

                            orientation: 'vertical'

                            size_hint: [1, None]

                            height: dp(105)

                            md_bg_color: [0.95, 0.98, 1, 1] if app.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.3, 1]

                            radius: [15]

                            padding: dp(10)

                            elevation: 2

                            on_release: app.show_coming_soon("Bulk SMS")

                            MDBoxLayout:

                                orientation: 'vertical'

                                spacing: dp(5)

                                size_hint_y: None

                                height: dp(80)

                                pos_hint: {"center_x": 0.5}

                                MDIcon:

                                    icon: "message-text"

                                    size_hint: [None, None]

                                    size: [dp(40), dp(40)]

                                    pos_hint: {"center_x": 0.5}

                                    theme_text_color: "Custom"

                                    text_color: [1, 0.6, 0.1, 1]

                                MDLabel:

                                    text: "Bulk SMS"

                                    halign: "center"

                                    font_style: "Subtitle1"

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]



                        # Code4Balance

                        MDCard:

                            orientation: 'vertical'

                            size_hint: [1, None]

                            height: dp(105)

                            md_bg_color: [0.95, 0.98, 1, 1] if app.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.3, 1]

                            radius: [15]

                            padding: dp(10)

                            spacing: dp(0)

                            elevation: 2
                            
                            on_release: app.show_code4balance_dialog()

                            #on_release: app.show_code4balance_dialog(Code4Balance)

                            MDBoxLayout:

                                orientation: 'vertical'

                                spacing: dp(10)

                                padding: dp(1)

                                size_hint_y: None

                                height: dp(80)

                                pos_hint: {"center_x": 0.5}

                                MDIcon:

                                    icon: "code-tags"

                                    size_hint: [None, None]

                                    size: [dp(40), dp(40)]

                                    pos_hint: {"center_x": 0.5}

                                    theme_text_color: "Custom"

                                    text_color: [1, 0, 0, 1]

                                MDLabel:

                                    text: "Code4Balance"

                                    halign: "center"

                                    font_style: "Subtitle1"

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]



                        # Exam PIN

                        MDCard:

                            orientation: 'vertical'

                            size_hint: [1, None]

                            height: dp(105)

                            md_bg_color: [0.95, 0.98, 1, 1] if app.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.3, 1]

                            radius: [15]

                            padding: dp(10)

                            elevation: 2
                            
                            on_release: app.buy_exam_pin()
                           # on_release: app.show_coming_soon("Exam PIN")

                            MDBoxLayout:

                                orientation: 'vertical'

                                spacing: dp(5)

                                size_hint_y: None

                                height: dp(80)

                                pos_hint: {"center_x": 0.5}

                                MDIcon:

                                    icon: "file-document-edit"

                                    size_hint: [None, None]

                                    size: [dp(40), dp(40)]

                                    pos_hint: {"center_x": 0.5}

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.6, 1, 1]

                                MDLabel:

                                    text: "Exam PIN"

                                    halign: "center"

                                    font_style: "Subtitle1"

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]



                        # Beneficiary

                        MDCard:

                            orientation: 'vertical'

                            size_hint: [1, None]

                            height: dp(105)

                            md_bg_color: [0.95, 0.98, 1, 1] if app.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.3, 1]

                            radius: [15]

                            padding: dp(10)

                            elevation: 2

                            on_release: app.show_beneficiaries()

                            MDBoxLayout:

                                orientation: 'vertical'

                                spacing: dp(5)

                                size_hint_y: None

                                height: dp(80)

                                pos_hint: {"center_x": 0.5}

                                MDIcon:

                                    icon: "account-box-multiple"

                                    size_hint: [None, None]

                                    size: [dp(40), dp(40)]

                                    pos_hint: {"center_x": 0.5}

                                    theme_text_color: "Custom"

                                    text_color: [1, 0.6, 0.1, 1]

                                MDLabel:

                                    text: "Beneficiary"

                                    halign: "center"

                                    font_style: "Subtitle1"

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]



                        # Pricing

                        MDCard:

                            orientation: 'vertical'

                            size_hint: [1, None]

                            height: dp(105)

                            md_bg_color: [0.95, 0.98, 1, 1] if app.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.3, 1]

                            radius: [15]

                            padding: dp(10)

                            elevation: 2

                            on_release: app.show_pricing()

                            MDBoxLayout:

                                orientation: 'vertical'

                                spacing: dp(5)

                                size_hint_y: None

                                height: dp(80)

                                pos_hint: {"center_x": 0.5}

                                MDIcon:

                                    icon: "cash"

                                    size_hint: [None, None]

                                    size: [dp(40), dp(40)]

                                    pos_hint: {"center_x": 0.5}

                                    theme_text_color: "Custom"

                                    text_color: [0.2, 0.8, 0.2, 1]

                                MDLabel:

                                    text: "Pricing"

                                    halign: "center"

                                    font_style: "Subtitle1"

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]



                        # Upgrade

                        MDCard:

                            orientation: 'vertical'

                            size_hint: [1, None]

                            height: dp(105)

                            md_bg_color: [0.95, 0.98, 1, 1] if app.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.3, 1]

                            radius: [15]

                            padding: dp(10)

                            elevation: 2

                            on_release: app.show_upgrade_options()

                            MDBoxLayout:

                                orientation: 'vertical'

                                spacing: dp(5)

                                size_hint_y: None

                                height: dp(80)

                                pos_hint: {"center_x": 0.5}

                                MDIcon:

                                    icon: "account-arrow-up"

                                    size_hint: [None, None]

                                    size: [dp(40), dp(40)]

                                    pos_hint: {"center_x": 0.5}

                                    theme_text_color: "Custom"

                                    text_color: [0.8, 0.4, 0.1, 1]

                                MDLabel:

                                    text: "Upgrade"

                                    halign: "center"

                                    font_style: "Subtitle1"

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]



                        # Betting

                        MDCard:

                            orientation: 'vertical'

                            size_hint: [1, None]

                            height: dp(105)

                            md_bg_color: [0.95, 0.98, 1, 1] if app.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.3, 1]

                            radius: [15]

                            padding: dp(10)

                            elevation: 2

                            on_release: app.show_coming_soon("Betting")

                            MDBoxLayout:

                                orientation: 'vertical'

                                spacing: dp(5)

                                size_hint_y: None

                                height: dp(80)

                                pos_hint: {"center_x": 0.5}

                                MDIcon:

                                    icon: "soccer"

                                    size_hint: [None, None]

                                    size: [dp(40), dp(40)]

                                    pos_hint: {"center_x": 0.5}

                                    theme_text_color: "Custom"

                                    text_color: [0.2, 0.7, 0.3, 1]

                                MDLabel:

                                    text: "Betting"

                                    halign: "center"

                                    font_style: "Subtitle1"

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]



                        # Gift Cards

                        MDCard:

                            orientation: 'vertical'

                            size_hint: [1, None]

                            height: dp(105)

                            md_bg_color: [0.95, 0.98, 1, 1] if app.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.3, 1]

                            radius: [15]

                            padding: dp(10)

                            elevation: 2

                            on_release: app.show_coming_soon("Gift Card Trading")

                            MDBoxLayout:

                                orientation: 'vertical'

                                spacing: dp(5)

                                size_hint_y: None

                                height: dp(80)

                                pos_hint: {"center_x": 0.5}

                                MDIcon:

                                    icon: "gift"

                                    size_hint: [None, None]

                                    size: [dp(40), dp(40)]

                                    pos_hint: {"center_x": 0.5}

                                    theme_text_color: "Custom"

                                    text_color: [0.9, 0.3, 0.5, 1]

                                MDLabel:

                                    text: "Gift Cards"

                                    halign: "center"

                                    font_style: "Subtitle1"

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]



                        # Airtime to Cash

                        MDCard:

                            orientation: 'vertical'

                            size_hint: [1, None]

                            height: dp(105)

                            md_bg_color: [0.95, 0.98, 1, 1] if app.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.3, 1]

                            radius: [15]

                            padding: dp(10)

                            elevation: 2

                            on_release: app.a2c_reset_flow(); app.root.current = "airtime_to_cash"

                            MDBoxLayout:

                                orientation: 'vertical'

                                spacing: dp(5)

                                size_hint_y: None

                                height: dp(80)

                                pos_hint: {"center_x": 0.5}

                                MDIcon:

                                    icon: "cash-refund"

                                    size_hint: [None, None]

                                    size: [dp(40), dp(40)]

                                    pos_hint: {"center_x": 0.5}

                                    theme_text_color: "Custom"

                                    text_color: [0.9, 0.5, 0.1, 1]

                                MDLabel:

                                    text: "Airtime to Cash"

                                    halign: "center"

                                    font_style: "Subtitle1"

                                    theme_text_color: "Custom"

                                    text_color: [0.1, 0.1, 0.1, 1] if app.theme_cls.theme_style == "Light" else [1, 1, 1, 1]



            # Bottom navigation
            # Bottom navigation (custom - avoids FBO crash)
            MDBoxLayout:
                size_hint_y: None
                height: dp(70)
                md_bg_color: [1, 1, 1, 1] if app.theme_cls.theme_style == "Light" else [0.15, 0.15, 0.2, 1]

                MDBoxLayout:
                    orientation: 'vertical'
                    on_touch_down:
                        if self.collide_point(*args[1].pos): app.switch_screen('dashboard')
                    Widget:
                        size_hint_y: .20  
                    MDIcon:
                        icon: 'home'
                        halign: 'center'
                        #pos_hint: {"center_x": .5, "center_y": .145}
                        pos_hint: {"center_x": .5}
                        theme_text_color: "Custom"
                        text_color: [0.1, 0.6, 1, 1] if app.current_screen_name == 'dashboard' else [0.5, 0.5, 0.5, 1]
                    MDLabel:
                        text: 'Home'
                        halign: 'center'
                        font_style: 'Caption'
                        theme_text_color: "Custom"
                        text_color: [0.1, 0.6, 1, 1] if app.current_screen_name == 'dashboard' else [0.5, 0.5, 0.5, 1]

                MDBoxLayout:
                    orientation: 'vertical'
                    on_touch_down:
                        if self.collide_point(*args[1].pos): app.switch_screen('history')
                    Widget:
                        size_hint_y: .20  
                    MDIcon:
                        icon: 'history'
                        halign: 'center'
                        pos_hint: {"center_x": .5}
                        theme_text_color: "Custom"
                        text_color: [0.1, 0.6, 1, 1] if app.current_screen_name == 'history' else [0.5, 0.5, 0.5, 1]
                    MDLabel:
                        text: 'History'
                        halign: 'center'
                        font_style: 'Caption'
                        theme_text_color: "Custom"
                        text_color: [0.1, 0.6, 1, 1] if app.current_screen_name == 'history' else [0.5, 0.5, 0.5, 1]

                MDBoxLayout:
                    orientation: 'vertical'
                    on_touch_down:
                        if self.collide_point(*args[1].pos): app.open_support()
                    Widget:
                        size_hint_y: .20  
                       
                    MDIcon:
                        icon: 'headphones'
                        halign: 'center'
                        pos_hint: {"center_x": .5}
                        theme_text_color: "Custom"
                        text_color: [0.1, 0.6, 1, 1] if app.current_screen_name in ('support', 'ai_chat') else [0.5, 0.5, 0.5, 1]
                    MDLabel:
                        text: 'Support'
                        halign: 'center'
                        font_style: 'Caption'
                        theme_text_color: "Custom"
                        text_color: [0.1, 0.6, 1, 1] if app.current_screen_name in ('support', 'ai_chat') else [0.5, 0.5, 0.5, 1]

                MDBoxLayout:
                    orientation: 'vertical'
                    on_touch_down:
                        if self.collide_point(*args[1].pos): app.switch_screen('profile')
                    Widget:
                        size_hint_y: .20   
                    MDIcon:
                        icon: 'account'
                        halign: 'center'
                        pos_hint: {"center_x": .5}
                        theme_text_color: "Custom"
                        text_color: [0.1, 0.6, 1, 1] if app.current_screen_name == 'profile' else [0.5, 0.5, 0.5, 1]
                    MDLabel:
                        text: 'Profile'
                        halign: 'center'
                        font_style: 'Caption'
                        theme_text_color: "Custom"
                        text_color: [0.1, 0.6, 1, 1] if app.current_screen_name == 'profile' else [0.5, 0.5, 0.5, 1]
                        




<LoginScreen>:

    name: "login"

    

    MDScreen:

        md_bg_color: app.theme_cls.bg_normal

        

        # Background decoration

        MDBoxLayout:

            orientation: 'vertical'

            size_hint: (1, 1)

            pos_hint: {'center_x': 0.5, 'center_y': 0.5}

            

            # Top decorative curve

            MDBoxLayout:

                size_hint_y: 0.3

                md_bg_color: app.theme_cls.primary_color

                radius: [0, 0, dp(50), dp(50)]

            

            # Main content area

            MDBoxLayout:

                orientation: 'vertical'

                padding: dp(40)

                spacing: dp(30)

                size_hint_y: 0.7

                

                # App logo and title

                MDBoxLayout:

                    orientation: 'vertical'

                    spacing: dp(10)

                    size_hint_y: None

                    height: dp(100)

                    pos_hint: {'center_x': 0.5}

                    

                    MDIcon:

                        icon: "wallet"

                        size_hint: (None, None)

                        size: [dp(60), dp(60)]

                        pos_hint: {'center_x': 0.5}

                        theme_text_color: "Custom"

                        text_color: app.theme_cls.primary_color

                    

                    MDLabel:

                        text: "[size=54][b]Welcome Back![/b][/size]"

                        font_style: "H4"

                        halign: "center"

                        markup: True

                        theme_text_color: "Primary"

                

                # Login form in a card

                MDCard:

                    orientation: 'vertical'

                    padding: dp(25)

                    spacing: dp(20)

                    size_hint: (0.9, None)

                    height: dp(300)

                    pos_hint: {'center_x': 0.5}

                    elevation: 5

                    radius: [dp(15),]

                    md_bg_color: app.theme_cls.bg_light

                    

                    # Email field

                    MDTextField:

                        id: login_email

                        hint_text: "Email Address"

                        icon_left: "email"

                        mode: "rectangle"

                        size_hint_y: None

                        height: dp(76)

                        size_hint_x: 1

                        line_color_focus: app.theme_cls.primary_color

                        helper_text_mode: "on_focus"

                        helper_text: "Enter your registered email"

                        required: True

                    

                    # Password field

                    MDTextField:

                        id: login_password

                        hint_text: "Password"

                        icon_left: "key"

                        mode: "rectangle"

                        size_hint_y: None

                        height: dp(76)

                        size_hint_x: 1

                        password: True

                        line_color_focus: app.theme_cls.primary_color

                        helper_text_mode: "on_focus"
                        

                        helper_text: "Enter your password"

                        required: True

                    

                    # Forgot password link

                    MDTextButton:

                        text: "[color=#1976D2]Forgot Password?[/color]"

                        markup: True

                        theme_text_color: "Custom"

                        text_color: app.theme_cls.primary_color

                        halign: "right"

                        on_release: app.show_forgot_password()

                    

                    # Login button

                    MDRaisedButton:

                        text: "SIGN IN"

                        on_release: app.login_user(login_email.text, login_password.text)

                        pos_hint: {'center_x': 0.5}

                        size_hint_x: 0.9

                        md_bg_color: app.theme_cls.primary_color

                        elevation_normal: 5

                        font_size: '16sp'

                

                # Register link section with arrow

                MDBoxLayout:

                    orientation: 'vertical'

                    spacing: dp(0)

                    size_hint_y: None

                    height: dp(80)

                    pos_hint: {'center_x': 0.5}

                    size_hint_x: 0.9

                    

                    # Text and button row

                    MDBoxLayout:

                        orientation: 'horizontal'

                        spacing: dp(10)

                        size_hint_y: None

                        height: dp(40)

                        

                        MDLabel:

                            text: "New to our app?"

                            font_style: "Body1"

                            markup: True

                            halign: "center"

                            size_hint_x:5

                            size_hint_y: 1

                            valign: "center"

                            

                    MDIcon:

                        icon: "arrow-down"

                        size_hint: (None, None)

                        size: [dp(24), dp(24)]

                        pos_hint: {'center_x': 0.5}

                        theme_text_color: "Custom"

                        text_color: app.theme_cls.primary_color    

                                                

                    MDBoxLayout:

                        orientation: 'horizontal'

                        spacing: dp(10)

                        size_hint_y: None

                        height: dp(40)

                                     

                        MDTextButton:

                            text: "[b][color=#1976D2]Create Account[/color][/b]"

                            markup: True

                            halign: "left"

                            size_hint_x: 0.5

                            valign: "center"

                            on_release: app.root.current = "register"

                                  

            # Bottom decorative curve

            MDBoxLayout:

                size_hint_y: 0.3

                md_bg_color: app.theme_cls.primary_color

                radius: [dp(50), dp(50), 0, 0]



<PinLoginScreen>:

    name: "pin_login"

    MDScreen:

        md_bg_color: app.theme_cls.bg_normal

        MDBoxLayout:

            orientation: 'vertical'

            size_hint: (1, 1)

            pos_hint: {'center_x': 0.5, 'center_y': 0.5}

            MDBoxLayout:

                size_hint_y: 0.3

                md_bg_color: app.theme_cls.primary_color

                radius: [0, 0, dp(50), dp(50)]

            MDBoxLayout:

                orientation: 'vertical'

                padding: dp(40)

                spacing: dp(25)

                size_hint_y: 0.7

                MDBoxLayout:

                    orientation: 'vertical'

                    spacing: dp(10)

                    size_hint_y: None

                    height: dp(100)

                    pos_hint: {'center_x': 0.5}

                    MDIcon:

                        icon: "lock"

                        size_hint: (None, None)

                        size: [dp(60), dp(60)]

                        pos_hint: {'center_x': 0.5}

                        theme_text_color: "Custom"

                        text_color: app.theme_cls.primary_color

                    MDLabel:

                        id: pin_welcome_label

                        text: "Welcome back!"

                        font_style: "H5"

                        halign: "center"

                        theme_text_color: "Primary"

                MDCard:

                    orientation: 'vertical'

                    padding: dp(25)

                    spacing: dp(20)

                    size_hint: (0.9, None)

                    height: dp(260)

                    pos_hint: {'center_x': 0.5}

                    MDTextField:

                        id: pin_input

                        hint_text: "Enter your PIN"

                        icon_left: "shield-key-outline"

                        password: True

                        input_filter: "int"

                        max_text_length: 6

                        halign: "center"

                        font_size: "24sp"

                        on_text_validate: app.attempt_pin_login()

                    MDRaisedButton:

                        text: "UNLOCK"

                        size_hint_x: 1

                        height: dp(50)

                        md_bg_color: app.theme_cls.primary_color

                        on_release: app.attempt_pin_login()

                    MDFlatButton:

                        text: "Not you? Use email & password"

                        size_hint_x: 1

                        on_release: app.switch_to_full_login()

            MDBoxLayout:

                size_hint_y: 0.3

                md_bg_color: app.theme_cls.primary_color

                radius: [dp(50), dp(50), 0, 0]



<RegisterScreen>:
    name: "register"
    MDScreen:
        md_bg_color: app.theme_cls.bg_normal

        # Background decoration
        MDBoxLayout:
            orientation: 'vertical'
            size_hint: (1, 1)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}

            # Top decorative curve
            MDBoxLayout:
                size_hint_y: 0.25
                md_bg_color: app.theme_cls.primary_color
                radius: [0, 0, dp(50), dp(50)]

            # Main content area
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(30)
                spacing: dp(20)
                size_hint_y: 0.75

                # App logo and title
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: dp(10)
                    size_hint_y: None
                    height: dp(80)
                    pos_hint: {'center_x': 0.5}
                    MDIcon:
                        icon: "account-plus"
                        size_hint: (None, None)
                        size: [dp(50), dp(50)]
                        pos_hint: {'center_x': 0.5}
                        theme_text_color: "Custom"
                        text_color: app.theme_cls.primary_color
                    MDLabel:
                       # text: "[size=54][c]Create Account![/c][/size]"
                        text: "Create Account"
                        font_style: "H5"
                        halign: "center"
                        bold: True
                        theme_text_color: "Primary"

                # Register form in a card
                MDCard:
                    orientation: 'vertical'
                    padding: dp(25)
                    spacing: dp(15)
                    size_hint: (0.9, None)
                    height: dp(380)  # Increased height to accommodate referral field
                    pos_hint: {'center_x': 0.5}
                    elevation: 5
                    radius: [dp(15),]
                    md_bg_color: app.theme_cls.bg_light

                    ScrollView:
                        do_scroll_x: False
                        MDBoxLayout:
                            orientation: 'vertical'
                            spacing: dp(15)
                            size_hint_y: None
                            height: dp(490)  # Increased height

                            # Name field
                            MDTextField:
                                id: reg_name
                                hint_text: "Full Name"
                                icon_left: "account"
                                mode: "rectangle"
                                size_hint_y: None
                                height: dp(76)
                                size_hint_x: 1
                                line_color_focus: app.theme_cls.primary_color
                                helper_text_mode: "on_focus"
                                helper_text: "Enter your full name"
                                required: True

                            # Email field
                            MDTextField:
                                id: reg_email
                                hint_text: "Email"
                                icon_left: "email"
                                mode: "rectangle"
                                size_hint_y: None
                                height: dp(76)
                                size_hint_x: 1
                                line_color_focus: app.theme_cls.primary_color
                                helper_text_mode: "on_focus"
                                helper_text: "Enter a valid email"
                                required: True

                            # Phone field
                            MDTextField:
                                id: reg_phone
                                hint_text: "Phone Number"
                                icon_left: "phone"
                                mode: "rectangle"
                                size_hint_y: None
                                height: dp(76)
                                size_hint_x: 1
                                input_type: 'number'
                                max_text_length: 11
                                line_color_focus: app.theme_cls.primary_color
                                helper_text_mode: "on_focus"
                                helper_text: "Enter your phone number"
                                required: True

                            # Referral Code field (OPTIONAL)
                            MDTextField:
                                id: reg_referral_code
                                hint_text: "Referral Code (Optional)"
                                icon_left: "account-group"
                                mode: "rectangle"
                                size_hint_y: None
                                height: dp(76)
                                size_hint_x: 1
                                line_color_focus: app.theme_cls.primary_color
                                helper_text_mode: "on_focus"
                                helper_text: "Enter referral code if you have one"
                                required: False

                            # Password field
                            MDTextField:
                                id: reg_password
                                hint_text: "Password"
                                icon_left: "key"
                                mode: "rectangle"
                                size_hint_y: None
                                height: dp(76)
                                size_hint_x: 1
                                password: True
                                line_color_focus: app.theme_cls.primary_color
                                helper_text_mode: "on_focus"
                                helper_text: "Create a strong password (min 6 chars)"
                                required: True

                            # Confirm Password field
                            MDTextField:
                                id: reg_confirm_password
                                hint_text: "Confirm Password"
                                icon_left: "key-change"
                                mode: "rectangle"
                                size_hint_y: None
                                height: dp(76)
                                size_hint_x: 1
                                password: True
                                line_color_focus: app.theme_cls.primary_color
                                helper_text_mode: "on_focus"
                                helper_text: "Re-enter your password"
                                required: True

                # Register button
                MDRaisedButton:
                    text: "REGISTER"
                    on_release: app.register_user(reg_name.text, reg_email.text, reg_phone.text, reg_referral_code.text, reg_password.text, reg_confirm_password.text)
                    pos_hint: {'center_x': 0.5}
                    size_hint_x: 0.9
                    md_bg_color: app.theme_cls.primary_color
                    elevation_normal: 5
                    font_size: '16sp'

                # Login link
                MDBoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(5)
                    size_hint_y: None
                    height: dp(15)
                    pos_hint: {'center_x': 0.35}
                    MDLabel:
                        text: "Already have an account?"
                        font_style: "Body1"
                        halign: "right"
                    MDTextButton:
                        text: "Login Here"
                        theme_text_color: "Custom"
                        text_color: app.theme_cls.primary_color
                        bold: True
                        on_release: app.root.current = "login"

            # Bottom decorative curve
            MDBoxLayout:
                size_hint_y: 0.25
                md_bg_color: app.theme_cls.primary_color
                radius: [dp(50), dp(50), 0, 0]

<LoaderWidget>:
    size_hint: None, None
    size: dp(100), dp(100)

    canvas.before:
        Color:
            rgba: 0.16, 0.44, 0.75, self.ripple1_alpha
        Line:
            circle:
                self.center_x, self.center_y, \
                dp(75) * self.ripple1_scale, 0, 360
            width: dp(1.2)

        Color:
            rgba: 0.16, 0.44, 0.75,  self.ripple2_alpha
        Line:
            circle:
                self.center_x, self.center_y, \
                dp(65) * self.ripple2_scale, 0, 360
            width: dp(1.8)

    canvas:
        Color:
            rgba: 1, 1, 1, 0.15
        Ellipse:
            size:
                dp(130) * self.pulse_scale, \
                dp(130) * self.pulse_scale
            pos:
                self.center_x - dp(65) * self.pulse_scale, \
                self.center_y - dp(65) * self.pulse_scale

        Color:
            rgba: 0.16, 0.44, 0.75, 1
        Line:
            circle:
                self.center_x, self.center_y, \
                dp(54), self.arc_start, self.arc_start + 160
            width: dp(3.5)
            cap: "round"

        Color:
            rgba: 0.16, 0.44, 0.75, 1
        Ellipse:
            size:
                dp(83) * self.pulse_scale, \
                dp(83) * self.pulse_scale
            pos:
                self.center_x - dp(42) * self.pulse_scale, \
                self.center_y - dp(42) * self.pulse_scale

        Color:
            rgba: 1, 1, 1, 0.15
        Line:
            circle:
                self.center_x, self.center_y, \
                dp(25) * self.pulse_scale, 0, 360
            width: dp(1)

    MDLabel:
        text: "C"
        font_style: "H4"
        bold: True
        halign: "center"
        valign: "middle"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, root.letter_alpha
        font_size: str(int(dp(15) * root.pulse_scale)) + "sp"
        size: root.size
        pos: root.pos
        

            
<ExamPinScreen>:
    name: "exam_pin"
    
    MDScreen:
        md_bg_color: app.theme_cls.bg_normal
        
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(2)
            spacing: dp(10)
            
            # Header
            MDBoxLayout:
                size_hint_y: None
                height: dp(60)
                padding: [dp(10), 0]
                spacing: dp(10)
                md_bg_color: app.theme_cls.primary_color
                radius: [10, 10, 0, 0]
                
                MDIconButton:
                    icon: "arrow-left"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    #radius: [dp(12),]
                    on_release: app.root.current = "dashboard"
                
                MDLabel:
                    text: "Exam PIN Purchase"
                    font_style: "H5"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: [1, 1, 1, 1]
                    halign: "center"
                    size_hint_x: 0.8
                
                MDIconButton:
                    icon: "help-circle"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    #radius: [dp(12),]
                    on_release: app.show_exam_pin_help()
            
            # Scrollable content
            ScrollView:
                bar_width: dp(4)
                bar_color: app.theme_cls.primary_color
                
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: dp(5)
                    padding: [dp(5), dp(3), dp(0), dp(10)]
                    size_hint_y: None
                    height: self.minimum_height
                    
                    # Main content card
                    MDCard:
                        orientation: 'vertical'
                        padding: [dp(15), dp(10), dp(10), dp(20)]
                        spacing: dp(15)
                        radius: [15, 15, 10, 10]
                        elevation: 4
                        size_hint_y: None
                        height: self.minimum_height
                        pos_hint: {'center_x': 0.5}
                        size_hint_x: 0.98
                        md_bg_color: app.theme_cls.bg_light
                        
                        # Exam type selection
                        MDLabel:
                            text: "Select Exam Type"
                            font_style: "H6"
                            bold: True
                            size_hint_y: None
                            height: dp(30)
                            theme_text_color: "Primary"
                            color: app.theme_cls.primary_color
                        
                        MDGridLayout:
                            id: exam_type_grid
                            cols: 4
                            spacing: dp(5)
                            padding: dp(0)
                            size_hint_y: None
                            height: dp(170)
                        
                        # Selected exam type display
                        MDCard:
                            id: selected_exam_type_box
                            size_hint_y: None
                            height: 0 if not app.selected_exam_type else dp(50)
                            opacity: 1 if app.selected_exam_type else 0
                            md_bg_color: app.theme_cls.primary_light
                            radius: [10]
                            padding: dp(10)
                            elevation: 0
                            
                            MDBoxLayout:
                                MDLabel:
                                    text: "Selected Exam:"
                                    font_style: "Subtitle1"
                                    size_hint_x: 0.7
                                    theme_text_color: "Secondary"
                                
                                MDLabel:
                                    id: selected_exam_type_label
                                    text: app.selected_exam_type if app.selected_exam_type else ""
                                    font_style: "Subtitle1"
                                    bold: True
                                    halign: "right"
                                    theme_text_color: "Primary"
                                    color: app.theme_cls.primary_color
                        
                        # Quantity selection
                        MDLabel:
                            text: "Select Quantity"
                            font_style: "H6"
                            bold: True
                            size_hint_y: None
                            height: dp(30)
                            theme_text_color: "Primary"
                            color: app.theme_cls.primary_color
                            opacity: 1 if app.selected_exam_type else 0
                        
                        # REPLACED quantity_grid WITH quantity_input TEXT FIELD
                        MDTextField:
                            id: quantity_input
                            hint_text: "Enter Quantity (1-10)"
                            input_type: 'number'
                            helper_text: "Enter number of PINs needed"
                            helper_text_mode: "on_focus"
                            size_hint_x: 1
                            mode: "rectangle"
                            size_hint_y: None
                            height: dp(76)
                            icon_left: "numeric"
                            on_text: app.validate_quantity_input(self.text)
                            color_active: app.theme_cls.primary_color
                            line_color_focus: app.theme_cls.primary_color
                            opacity: 1 if app.selected_exam_type else 0.5
                            disabled: not app.selected_exam_type
                        
                        # Selected quantity display
                        MDCard:
                            id: selected_quantity_box
                            size_hint_y: None
                            height: 0 if not app.selected_exam_quantity else dp(50)
                            opacity: 1 if app.selected_exam_quantity else 0
                            md_bg_color: app.theme_cls.primary_light
                            radius: [10]
                            padding: dp(10)
                            elevation: 0
                            
                            MDBoxLayout:
                                MDLabel:
                                    text: "Quantity:"
                                    font_style: "Subtitle1"
                                    size_hint_x: 0.7
                                    theme_text_color: "Secondary"
                                
                                MDLabel:
                                    id: selected_quantity_label
                                    text: str(app.selected_exam_quantity) if app.selected_exam_quantity else ""
                                    font_style: "Subtitle1"
                                    bold: True
                                    halign: "right"
                                    theme_text_color: "Primary"
                                    color: app.theme_cls.primary_color
                        
                        # Total amount display
                        MDCard:
                            id: total_amount_box
                            size_hint_y: None
                            height: 0 if not app.selected_exam_quantity else dp(50)
                            opacity: 1 if app.selected_exam_quantity else 0
                            md_bg_color: app.theme_cls.primary_light
                            radius: [10]
                            padding: dp(10)
                            elevation: 0
                            
                            MDBoxLayout:
                                MDLabel:
                                    text: "Total Amount:"
                                    font_style: "Subtitle1"
                                    size_hint_x: 0.7
                                    theme_text_color: "Secondary"
                                
                                MDLabel:
                                    id: total_amount_label
                                    text: app.format_currency(app.exam_pin_total_amount) if app.exam_pin_total_amount else ""
                                    font_style: "Subtitle1"
                                    bold: True
                                    halign: "right"
                                    theme_text_color: "Primary"
                                    color: app.theme_cls.primary_color
                        
                        # Continue button
                        MDFillRoundFlatButton:
                            id: continue_btn
                            text: "CONTINUE"
                            on_release: app.process_exam_pin_purchase()
                            pos_hint: {'center_x': 0.5}
                            size_hint_x: 0.9
                            md_bg_color: app.theme_cls.primary_color
                            disabled: not (app.selected_exam_type and app.selected_exam_quantity)
                            opacity: 1 if (app.selected_exam_type and app.selected_exam_quantity) else 0.5
                            
<FundingScreen>:
    name: "funding"
    
    MDScreen:
        md_bg_color: app.theme_cls.bg_normal

        # Gradient Background Pattern
        MDBoxLayout:
            size_hint: (1, 0.28)
            pos_hint: {"top": 1}
            canvas.before:
                Color:
                    rgba: [0.1, 0.6, 1, 1] if app.theme_cls.theme_style == "Light" else [0.1, 0.3, 0.6, 1]
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [0, 0, dp(35), dp(35)]
                Color:
                    rgba: [0.3, 0.8, 1, 0.4] if app.theme_cls.theme_style == "Light" else [0.2, 0.5, 0.8, 0.3]
                RoundedRectangle:
                    pos: self.pos[0], self.pos[1] - dp(20)
                    size: self.size[0], self.size[1] + dp(40)
                    radius: [0, 0, dp(50), dp(50)]
            
            MDIcon:
                icon: "wallet-plus"
                theme_text_color: "Custom"
                text_color: [1, 1, 1, 0.08]
                font_size: "140sp"
                pos_hint: {"center_x": 0.5, "center_y": 0.6}

        MDBoxLayout:
            orientation: 'vertical'
            padding: 0
            spacing: 0

            # Modern Header Section
            MDBoxLayout:
                size_hint_y: None
                height: dp(90)
                padding: [dp(20), dp(12), dp(20), dp(8)]
                md_bg_color: [0.1, 0.6, 1, 1] if app.theme_cls.theme_style == "Light" else [0.1, 0.3, 0.6, 1]
                radius: [0, 0, dp(25), dp(25)]
                
                MDBoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(12)
                    
                    MDIconButton:
                        icon: "arrow-left"
                        theme_icon_color: "Custom"
                        icon_color: [1, 1, 1, 1]
                        ripple_scale: 0.8
                        size_hint: None, None
                        size: [dp(44), dp(44)]
                        md_bg_color: [1, 1, 1, 0.2]
                        on_release: app.root.current = "dashboard"
                        radius: [18]
                    
                    MDBoxLayout:
                        orientation: 'vertical'
                        spacing: dp(3)
                        padding: [dp(5), 0, 0, 0]
                        
                        MDLabel:
                            text: "Fund Wallet"
                            font_style: "H5"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: [1, 1, 1, 1]
                            halign: "left"
                            size_hint_y: None
                            height: dp(28)
                        
                        MDLabel:
                            text: "Top up your account balance"
                            font_style: "Body2"
                            theme_text_color: "Custom"
                            text_color: [1, 1, 1, 0.9]
                            halign: "left"
                            size_hint_y: None
                            height: dp(22)
                    
                    Widget:
                        size_hint_x: 0.2

            # Main Content with Smooth Scrolling
            ScrollView:
                always_overscroll: False
                bar_width: dp(5)
                bar_color: app.theme_cls.primary_color
                bar_inactive_color: [app.theme_cls.primary_color[0], app.theme_cls.primary_color[1], app.theme_cls.primary_color[2], 0.3]
                scroll_type: ['bars', 'content']
                do_scroll_x: False
                
                         
                
                MDBoxLayout:
                    id: main_content
                    orientation: 'vertical'
                    spacing: dp(16)
                    padding: [dp(16), dp(12), dp(16), dp(20)]
                    size_hint_y: None
                    height: self.minimum_height
                    adaptive_height: True

                    # Premium Balance Card with Shadow
                    MDCard:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: dp(10)
                        padding: dp(20)
                        spacing: dp(8)
                        radius: [20]
                        elevation: 8
                        shadow_softness: 12
                        shadow_offset: [0, 4]
                        
                        canvas.before:
                            Color:
                                rgba: [0.1, 0.6, 1, 1] if app.theme_cls.theme_style == "Light" else [0.1, 0.3, 0.6, 1]
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [20, 20, 20, 20]
                            Color:
                                rgba: [0.3, 0.8, 1, 0.3] if app.theme_cls.theme_style == "Light" else [0.2, 0.5, 0.8, 0.2]
                            RoundedRectangle:
                                pos: self.pos[0] - dp(2), self.pos[1] - dp(2)
                                size: self.size[0] + dp(4), self.size[1] + dp(4)
                                radius: [22, 22, 22, 22]

                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: dp(15)
                            
                            MDIcon:
                                icon: "wallet"
                                theme_text_color: "Custom"
                                text_color: [1, 1, 1, 1]
                                font_size: "28sp"
                                size_hint_x: None
                                width: dp(35)
                            
                            MDBoxLayout:
                                orientation: 'vertical'
                                spacing: dp(4)
                                
                                MDLabel:
                                    text: "CURRENT BALANCE"
                                    font_style: "Caption"
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 0.8]
                                    halign: "left"
                                    size_hint_y: None
                                    height: dp(18)
                                
                                MDLabel:
                                    id: current_balance_label
                                    text: app.format_currency(app.current_user.get('wallet_balance', 0)) if app.current_user else "₦0.00"
                                    font_style: "H5"
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 1]
                                    bold: True
                                    halign: "left"
                                    size_hint_y: None
                                    height: dp(32)

                            Widget:
                                size_hint_x: 0.3

                    # Amount Section with Modern Design
                    MDCard:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: dp(135)
                        padding: dp(20)
                        spacing: dp(12)
                        radius: [18]
                        elevation: 4
                        md_bg_color: app.theme_cls.bg_light
                        shadow_softness: 8
                        shadow_offset: [0, 2]

                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: dp(10)
                            size_hint_y: None
                            height: dp(30)
                            
                            MDIcon:
                                icon: "cash-plus"
                                theme_text_color: "Custom"
                                text_color: app.theme_cls.primary_color
                                size_hint_x: None
                                width: dp(24)
                            
                            MDLabel:
                                text: "Enter Amount"
                                font_style: "H6"
                                bold: True
                                theme_text_color: "Primary"
                                halign: "left"

                        MDTextField:
                            id: amount_input
                            hint_text: "Enter amount in Naira"
                            
                            input_type: 'number'
                            helper_text: "Minimum: ₦100 • Maximum: ₦500,000"
                            helper_text_mode: "on_focus"
                            size_hint_x: 1
                            size_hint_y: None
                            height: dp(52)
                            mode: "fill"
                            fill_color: app.theme_cls.bg_dark if app.theme_cls.theme_style == "Light" else [0.15, 0.15, 0.15, 1]
                            on_text: app.validate_funding_amount(self.text)
                            line_color_focus: app.theme_cls.primary_color
                            icon_left: "currency-ngn"
                            icon_left_color: app.theme_cls.primary_color

                    # Quick Amount Chips - Modern Design
                    MDCard:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: dp(155)
                        padding: dp(18)
                        spacing: dp(25)
                        radius: [18]
                        elevation: 3
                        md_bg_color: app.theme_cls.bg_light

                        MDLabel:
                            text: "QUICK AMOUNT"
                            font_style: "Subtitle1"
                            bold: True
                            theme_text_color: "Primary"
                            size_hint_y: None
                            height: dp(25)

                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: dp(8)
                            size_hint_y: None
                            height: dp(20)
                            radius: [18]

                            MDRoundFlatButton:
                                text: "₦500"
                                on_release: app.set_funding_amount(500)
                                theme_text_color: "Custom"
                                text_color: app.theme_cls.primary_color
                                line_color: app.theme_cls.primary_color
                                size_hint_x: 0.33
                                size_hint_y: None
                                height: dp(38)
                                

                            MDRoundFlatButton:
                                text: "₦1,000"
                                on_release: app.set_funding_amount(1000)
                                theme_text_color: "Custom"
                                text_color: app.theme_cls.primary_color
                                line_color: app.theme_cls.primary_color
                                size_hint_x: 0.33
                                size_hint_y: None
                                height: dp(38)

                            MDRoundFlatButton:
                                text: "₦2,000"
                                on_release: app.set_funding_amount(2000)
                                theme_text_color: "Custom"
                                text_color: app.theme_cls.primary_color
                                line_color: app.theme_cls.primary_color
                                size_hint_x: 0.33
                                size_hint_y: None
                                height: dp(38)

                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: dp(8)
                            size_hint_y: None
                            height: dp(38)

                            MDRoundFlatButton:
                                text: "₦3,000"
                                on_release: app.set_funding_amount(3000)
                                theme_text_color: "Custom"
                                text_color: app.theme_cls.primary_color
                                line_color: app.theme_cls.primary_color
                                size_hint_x: 0.33
                                size_hint_y: None
                                height: dp(38)

                            MDRoundFlatButton:
                                text: "₦5,000"
                                on_release: app.set_funding_amount(5000)
                                theme_text_color: "Custom"
                                text_color: app.theme_cls.primary_color
                                line_color: app.theme_cls.primary_color
                                size_hint_x: 0.33
                                size_hint_y: None
                                height: dp(38)

                            MDRoundFlatButton:
                                text: "₦10,000"
                                on_release: app.set_funding_amount(10000)
                                theme_text_color: "Custom"
                                text_color: app.theme_cls.primary_color
                                line_color: app.theme_cls.primary_color
                                size_hint_x: 0.33
                                size_hint_y: None
                                height: dp(38)

                    # Payment Methods - Premium Design
                    MDCard:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: dp(305)
                        padding: dp(20)
                        spacing: dp(12)
                        radius: [18]
                        elevation: 4
                        md_bg_color: app.theme_cls.bg_light
                        shadow_softness: 8

                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: dp(10)
                            size_hint_y: None
                            height: dp(30)
                            
                            MDIcon:
                                icon: "credit-card-settings"
                                theme_text_color: "Custom"
                                text_color: app.theme_cls.primary_color
                                size_hint_x: None
                                width: dp(24)
                            
                            MDLabel:
                                text: "PAYMENT METHOD"
                                font_style: "H6"
                                bold: True
                                theme_text_color: "Primary"
                                halign: "left"

                        # Bank Transfer - Premium Card
                        MDCard:
                            orientation: 'horizontal'
                            size_hint_y: None
                            height: dp(70)
                            padding: dp(16)
                            spacing: dp(12)
                            radius: [14]
                            elevation: 2
                            md_bg_color: app.theme_cls.primary_light if app.selected_funding_method == "transfer" else app.theme_cls.bg_light
                            on_release: app.select_payment_method("transfer")
                            ripple_behavior: True

                            MDBoxLayout:
                                orientation: 'horizontal'
                                spacing: dp(12)
                                
                                MDIconButton:
                                    icon: "bank-transfer"
                                    theme_icon_color: "Custom"
                                    icon_color: [0.1, 0.6, 1, 1]
                                    ripple_scale: 0
                                    size_hint_x: None
                                    width: dp(40)
                                    md_bg_color: [0.1, 0.6, 1, 0.1]
                                    radius: [10]
                                
                                MDBoxLayout:
                                    orientation: 'vertical'
                                    spacing: dp(3)
                                    size_hint_x: 0.65
                                    
                                    MDLabel:
                                        text: "Bank Transfer"
                                        font_style: "Subtitle1"
                                        bold: True
                                        theme_text_color: "Primary"
                                        halign: "left"
                                        size_hint_y: None
                                        height: dp(22)
                                    
                                    MDLabel:
                                        text: "Instant virtual account"
                                        font_style: "Caption"
                                        theme_text_color: "Secondary"
                                        halign: "left"
                                        size_hint_y: None
                                        height: dp(18)
                                
                                MDIcon:
                                    icon: "check-circle" if app.selected_funding_method == "transfer" else "circle-outline"
                                    theme_text_color: "Custom"
                                    text_color: app.theme_cls.primary_color if app.selected_funding_method == "transfer" else [0.7, 0.7, 0.7, 1]
                                    size_hint_x: None
                                    width: dp(24)

                        # USSD - Premium Card
                        MDCard:
                            orientation: 'horizontal'
                            size_hint_y: None
                            height: dp(70)
                            padding: dp(16)
                            spacing: dp(12)
                            radius: [14]
                            elevation: 2
                            md_bg_color: app.theme_cls.primary_light if app.selected_funding_method == "ussd" else app.theme_cls.bg_light
                            on_release: app.select_payment_method("ussd")
                            ripple_behavior: True

                            MDBoxLayout:
                                orientation: 'horizontal'
                                spacing: dp(12)
                                
                                MDIconButton:
                                    icon: "cellphone-key"
                                    theme_icon_color: "Custom"
                                    icon_color: [0.2, 0.8, 0.2, 1]
                                    ripple_scale: 0
                                    size_hint_x: None
                                    width: dp(40)
                                    md_bg_color: [0.2, 0.8, 0.2, 0.1]
                                    radius: [10]
                                
                                MDBoxLayout:
                                    orientation: 'vertical'
                                    spacing: dp(3)
                                    size_hint_x: 0.65
                                    
                                    MDLabel:
                                        text: "USSD Payment"
                                        font_style: "Subtitle1"
                                        bold: True
                                        theme_text_color: "Primary"
                                        halign: "left"
                                        size_hint_y: None
                                        height: dp(22)
                                    
                                    MDLabel:
                                        text: "Pay with bank USSD"
                                        font_style: "Caption"
                                        theme_text_color: "Secondary"
                                        halign: "left"
                                        size_hint_y: None
                                        height: dp(18)
                                
                                MDIcon:
                                    icon: "check-circle" if app.selected_funding_method == "ussd" else "circle-outline"
                                    theme_text_color: "Custom"
                                    text_color: app.theme_cls.primary_color if app.selected_funding_method == "ussd" else [0.7, 0.7, 0.7, 1]
                                    size_hint_x: None
                                    width: dp(24)

                        # Card Payment - Premium Card
                        MDCard:
                            orientation: 'horizontal'
                            size_hint_y: None
                            height: dp(70)
                            padding: dp(16)
                            spacing: dp(12)
                            radius: [14]
                            elevation: 2
                            md_bg_color: app.theme_cls.primary_light if app.selected_funding_method == "card" else app.theme_cls.bg_light
                            on_release: app.select_payment_method("card")
                            ripple_behavior: True

                            MDBoxLayout:
                                orientation: 'horizontal'
                                spacing: dp(12)
                                
                                MDIconButton:
                                    icon: "contactless-payment"
                                    theme_icon_color: "Custom"
                                    icon_color: [0.8, 0.4, 0.1, 1]
                                    ripple_scale: 0
                                    size_hint_x: None
                                    width: dp(40)
                                    md_bg_color: [0.8, 0.4, 0.1, 0.1]
                                    radius: [10]
                                
                                MDBoxLayout:
                                    orientation: 'vertical'
                                    spacing: dp(3)
                                    size_hint_x: 0.65
                                    
                                    MDLabel:
                                        text: "Card Payment"
                                        font_style: "Subtitle1"
                                        bold: True
                                        theme_text_color: "Primary"
                                        halign: "left"
                                        size_hint_y: None
                                        height: dp(22)
                                    
                                    MDLabel:
                                        text: "Debit/Credit card"
                                        font_style: "Caption"
                                        theme_text_color: "Secondary"
                                        halign: "left"
                                        size_hint_y: None
                                        height: dp(18)
                                
                                MDIcon:
                                    icon: "check-circle" if app.selected_funding_method == "card" else "circle-outline"
                                    theme_text_color: "Custom"
                                    text_color: app.theme_cls.primary_color if app.selected_funding_method == "card" else [0.7, 0.7, 0.7, 1]
                                    size_hint_x: None
                                    width: dp(24)

                    # Security Badge - Premium Design
                    MDCard:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: dp(75)
                        padding: dp(18)
                        spacing: dp(15)
                        radius: [16]
                        elevation: 2
                        md_bg_color: [0.9, 0.98, 0.95, 1] if app.theme_cls.theme_style == "Light" else [0.1, 0.3, 0.2, 1]

                        MDIcon:
                            icon: "shield-check"
                            theme_text_color: "Custom"
                            text_color: [0.2, 0.7, 0.3, 1]
                            size_hint_x: None
                            width: dp(30)
                            font_size: "24sp"
                        
                        MDBoxLayout:
                            orientation: 'vertical'
                            spacing: dp(2)
                            
                            MDLabel:
                                text: "SECURE & ENCRYPTED"
                                font_style: "Subtitle1"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: [0.2, 0.7, 0.3, 1]
                                size_hint_y: None
                                height: dp(22)
                            
                            MDLabel:
                                text: "Bank-level security • PCI DSS compliant"
                                font_style: "Caption"
                                theme_text_color: "Custom"
                                text_color: [0.2, 0.7, 0.3, 0.8]
                                size_hint_y: None
                                height: dp(18)

                    # Action Buttons - Premium Design
                    MDBoxLayout:
                        orientation: 'vertical'
                        spacing: dp(15)
                        size_hint_y: None
                        height: dp(120)
                        padding: [dp(10), 0, dp(10), 0]

                        MDFillRoundFlatIconButton:
                            id: continue_btn
                            text: "PROCEED TO PAYMENT"
                            icon: "lock-outline"
                            on_release: app.process_funding()
                            pos_hint: {'center_x': 0.5}
                            size_hint_x: 1
                            size_hint_y: None
                            height: dp(55)
                            md_bg_color: app.theme_cls.primary_color
                            disabled: not (app.selected_funding_method and app.funding_amount >= 100)
                            opacity: 1 if (app.selected_funding_method and app.funding_amount >= 100) else 0.5
                            font_size: '15sp'
                            elevation: 4
                            shadow_softness: 8

                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: dp(25)
                            size_hint_y: None
                            height: dp(40)
                            padding: [dp(20), 0, dp(20), 0]

                            MDTextButton:
                                text: "← Back to Dashboard"
                                theme_text_color: "Custom"
                                text_color: app.theme_cls.primary_color
                                font_size: '13sp'
                                on_release: app.root.current = "dashboard"
                                pos_hint: {'center_x': 0.5}

                            MDTextButton:
                                text: "Need Help? 💬"
                                theme_text_color: "Custom"
                                text_color: app.theme_cls.primary_color
                                font_size: '13sp'
                                on_release: app.show_funding_help()
                                pos_hint: {'center_x': 0.5}
                                

<ReferralScreen>:
    name: "referral"
    
    MDScreen:
        md_bg_color: app.theme_cls.bg_normal
        
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(10)
            
            # Header
            MDBoxLayout:
                size_hint_y: None
                height: dp(60)
                padding: [dp(10), 0]
                spacing: dp(10)
                md_bg_color: app.theme_cls.primary_color
                radius: [10, 10, 0, 0]
                
                MDIconButton:
                    icon: "arrow-left"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    on_release: app.root.current = "dashboard"
                    radius: [4, ]
                    
                MDLabel:
                    text: "Refer & Earn"
                    font_style: "H5"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: [1, 1, 1, 1]
                    halign: "center"
                    size_hint_x: 0.8
                    
                MDIconButton:
                    icon: "share-variant"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    on_release: app.share_referral_link()
            
            ScrollView:
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: dp(15)
                    padding: [dp(20), dp(20), dp(20), dp(20)]
                    size_hint_y: None
                    height: self.minimum_height
                    
                    # Referral Code Card
                    MDCard:
                        orientation: 'vertical'
                        padding: dp(20)
                        spacing: dp(15)
                        size_hint_y: None
                        height: dp(180)
                        elevation: 2
                        radius: [15]
                        
                        MDLabel:
                            text: "Your Referral Code"
                            font_style: "H6"
                            bold: True
                            halign: "center"
                            size_hint_y: None
                            height: dp(30)
                            
                        MDLabel:
                            id: referral_code_label
                            text: app.referral_code
                            font_style: "H4"
                            bold: True
                            halign: "center"
                            theme_text_color: "Primary"
                            size_hint_y: None
                            height: dp(40)
                            
                        MDRaisedButton:
                            text: "COPY CODE"
                            on_release: app.copy_referral_code()
                            pos_hint: {"center_x": 0.5}
                            size_hint_x: 0.8
                            
                    # Referral Link Card
                    MDCard:
                        orientation: 'vertical'
                        padding: dp(20)
                        spacing: dp(15)
                        size_hint_y: None
                        height: dp(150)
                        elevation: 2
                        radius: [15]
                        
                        MDLabel:
                            text: "Your Referral Link"
                            font_style: "H6"
                            bold: True
                            halign: "center"
                            
                        MDLabel:
                            id: referral_link_label
                            text: "Loading..."
                            halign: "center"
                            text_size: self.width, None
                            theme_text_color: "Secondary"
                            
                        MDRaisedButton:
                            text: "SHARE LINK"
                            on_release: app.share_referral_link()
                            pos_hint: {"center_x": 0.5}
                            size_hint_x: 0.8
                    
                    # Statistics Card
                    MDCard:
                        orientation: 'vertical'
                        padding: dp(20)
                        spacing: dp(15)
                        size_hint_y: None
                        height: dp(200)
                        elevation: 2
                        radius: [15]
                        
                        MDLabel:
                            text: "Referral Statistics"
                            font_style: "H6"
                            bold: True
                            halign: "center"
                            
                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: dp(10)
                            size_hint_y: None
                            height: dp(40)
                            
                            MDLabel:
                                text: "Total Referrals:"
                                bold: True
                                size_hint_x: 0.6
                                
                            MDLabel:
                                id: total_referrals_label
                                text: "0"
                                halign: "right"
                                theme_text_color: "Primary"
                                
                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: dp(10)
                            size_hint_y: None
                            height: dp(40)
                            
                            MDLabel:
                                text: "Pending Referrals:"
                                bold: True
                                size_hint_x: 0.6
                                
                            MDLabel:
                                id: pending_referrals_label
                                text: "0"
                                halign: "right"
                                theme_text_color: "Secondary"
                                
                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: dp(10)
                            size_hint_y: None
                            height: dp(40)
                            
                            MDLabel:
                                text: "Referral Bonus:"
                                bold: True
                                size_hint_x: 0.6
                                
                            MDLabel:
                                id: referral_earnings_label
                                text: "₦0.00"
                                halign: "right"
                                theme_text_color: "Primary"
                                bold: True
                    
                    # Bonus Usage Card
                    MDCard:
                        orientation: 'vertical'
                        padding: dp(20)
                        spacing: dp(15)
                        size_hint_y: None
                        height: dp(180)
                        elevation: 2
                        radius: [15]
                        md_bg_color: app.theme_cls.primary_light
                        
                        MDLabel:
                            text: "Use Your Bonus"
                            font_style: "H6"
                            bold: True
                            halign: "center"
                            
                        MDLabel:
                            id: bonus_info_label
                            text: "Earn ₦50 for each friend who joins and completes their first transaction"
                            halign: "center"
                            text_size: self.width, None
                            theme_text_color: "Secondary"
                            
                        MDRaisedButton:
                            id: use_bonus_btn
                            text: "USE BONUS FOR PURCHASES"
                            on_release: app.use_referral_bonus()
                            pos_hint: {"center_x": 0.5}
                            size_hint_x: 0.9
                            disabled: True
                            opacity: 0.5
                            
                    # How it Works Card
                    MDCard:
                        orientation: 'vertical'
                        padding: dp(20)
                        spacing: dp(15)
                        size_hint_y: None
                        height: dp(250)
                        elevation: 2
                        radius: [15]
                        
                        MDLabel:
                            text: "How It Works"
                            font_style: "H6"
                            bold: True
                            halign: "center"
                            
                        MDLabel:
                            text: "1. Share your referral link with friends\\n2. They sign up using your link\\n3. When they complete their first transaction\\n4. You get ₦50 referral bonus\\n5. Use bonus when you reach ₦200"
                            halign: "left"
                            text_size: self.width, None
                            theme_text_color: "Secondary"
                    
                          
    
<CashbackScreen>:
    name: "cashback"

    MDScreen:
        md_bg_color: app.theme_cls.bg_normal

        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(10)

            # Header
            MDBoxLayout:
                size_hint_y: None
                height: dp(60)
                padding: [dp(10), 0]
                spacing: dp(10)
                md_bg_color: [0.1, 0.75, 0.35, 1]
                radius: [10, 10, 0, 0]

                MDIconButton:
                    icon: "arrow-left"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    on_release: app.root.current = "dashboard"
                    radius: [4, ]

                MDLabel:
                    text: "Cashback"
                    font_style: "H5"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: [1, 1, 1, 1]
                    halign: "center"
                    size_hint_x: 0.8

                MDIconButton:
                    icon: "refresh"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    on_release: app.load_cashback_data()

            ScrollView:
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: dp(15)
                    padding: [dp(20), dp(20), dp(20), dp(20)]
                    size_hint_y: None
                    height: self.minimum_height

                    # Balance Card
                    MDCard:
                        orientation: 'vertical'
                        padding: dp(20)
                        spacing: dp(10)
                        size_hint_y: None
                        height: dp(160)
                        elevation: 2
                        radius: [15]
                        md_bg_color: [0.1, 0.75, 0.35, 1]

                        MDLabel:
                            text: "Available Cashback"
                            font_style: "Subtitle1"
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: [1, 1, 1, 0.9]
                            size_hint_y: None
                            height: dp(25)

                        MDLabel:
                            id: cashback_balance_label
                            text: "₦0.00"
                            font_style: "H3"
                            bold: True
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: [1, 1, 1, 1]
                            size_hint_y: None
                            height: dp(50)

                        MDLabel:
                            id: cashback_expiring_label
                            text: ""
                            font_style: "Caption"
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: [1, 1, 1, 0.85]
                            size_hint_y: None
                            height: dp(20)

                        MDRaisedButton:
                            id: cashback_redeem_btn
                            text: "MOVE TO MAIN WALLET"
                            md_bg_color: [1, 1, 1, 1]
                            theme_text_color: "Custom"
                            text_color: [0.1, 0.75, 0.35, 1]
                            on_release: app.redeem_cashback()
                            pos_hint: {"center_x": 0.5}
                            size_hint_x: 0.85
                            disabled: True
                            opacity: 0.6

                    # Statistics Card
                    MDCard:
                        orientation: 'vertical'
                        padding: dp(20)
                        spacing: dp(12)
                        size_hint_y: None
                        height: dp(180)
                        elevation: 2
                        radius: [15]

                        MDLabel:
                            text: "Cashback Statistics"
                            font_style: "H6"
                            bold: True
                            halign: "center"
                            size_hint_y: None
                            height: dp(30)

                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: dp(10)
                            size_hint_y: None
                            height: dp(35)

                            MDLabel:
                                text: "Total Earned:"
                                bold: True
                                size_hint_x: 0.6

                            MDLabel:
                                id: cashback_total_earned_label
                                text: "₦0.00"
                                halign: "right"
                                theme_text_color: "Primary"

                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: dp(10)
                            size_hint_y: None
                            height: dp(35)

                            MDLabel:
                                text: "Total Redeemed:"
                                bold: True
                                size_hint_x: 0.6

                            MDLabel:
                                id: cashback_total_redeemed_label
                                text: "₦0.00"
                                halign: "right"
                                theme_text_color: "Secondary"

                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: dp(10)
                            size_hint_y: None
                            height: dp(35)

                            MDLabel:
                                text: "Total Expired:"
                                bold: True
                                size_hint_x: 0.6

                            MDLabel:
                                id: cashback_total_expired_label
                                text: "₦0.00"
                                halign: "right"
                                theme_text_color: "Secondary"

                    # Earn Rates Card
                    MDCard:
                        orientation: 'vertical'
                        padding: dp(20)
                        spacing: dp(10)
                        size_hint_y: None
                        height: dp(150)
                        elevation: 2
                        radius: [15]
                        md_bg_color: app.theme_cls.primary_light

                        MDLabel:
                            text: "How It Works"
                            font_style: "H6"
                            bold: True
                            halign: "center"
                            size_hint_y: None
                            height: dp(30)

                        MDLabel:
                            id: cashback_rates_label
                            text: "Earn automatic cashback every time you buy airtime, data, cable TV, electricity, or exam pins. Cashback lands in this wallet and can be moved to your main wallet at any time."
                            halign: "left"
                            text_size: self.width, None
                            theme_text_color: "Secondary"

                    # History
                    MDBoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: dp(35)

                        MDLabel:
                            text: "Recent Activity"
                            font_style: "H6"
                            bold: True
                            size_hint_x: 0.7

                        MDLabel:
                            id: cashback_history_empty_label
                            text: ""
                            font_style: "Caption"
                            halign: "right"
                            theme_text_color: "Secondary"

                    MDList:
                        id: cashback_history_list
                        spacing: dp(4)

<SpinScreen>:
    name: "spin"

    MDScreen:
        md_bg_color: app.theme_cls.bg_normal

        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(10)

            # Header
            MDBoxLayout:
                size_hint_y: None
                height: dp(60)
                padding: [dp(10), 0]
                spacing: dp(10)
                md_bg_color: [0.95, 0.55, 0.1, 1]
                radius: [10, 10, 0, 0]

                MDIconButton:
                    icon: "arrow-left"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    on_release: app.root.current = "dashboard"
                    radius: [4, ]

                MDLabel:
                    text: "Spin & Win"
                    font_style: "H5"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: [1, 1, 1, 1]
                    halign: "center"
                    size_hint_x: 0.8

                MDIconButton:
                    icon: "history"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    on_release: app.show_spin_history()

            ScrollView:
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: dp(15)
                    padding: [dp(20), dp(20), dp(20), dp(20)]
                    size_hint_y: None
                    height: self.minimum_height

                    MDLabel:
                        id: spin_status_label
                        text: "Loading..."
                        halign: "center"
                        font_style: "Subtitle1"
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: dp(30)

                    # Wheel + fixed pointer
                    FloatLayout:
                        id: spin_wheel_container
                        size_hint_y: None
                        height: dp(300)

                        SpinWheelWidget:
                            id: spin_wheel
                            size_hint: [None, None]
                            size: [dp(280), dp(280)]
                            pos_hint: {"center_x": 0.5, "center_y": 0.5}

                        MDIcon:
                            icon: "menu-down"
                            size_hint: [None, None]
                            size: [dp(40), dp(40)]
                            pos_hint: {"center_x": 0.5, "top": 1.05}
                            theme_text_color: "Custom"
                            text_color: [0.95, 0.55, 0.1, 1]

                    MDRaisedButton:
                        id: spin_button
                        text: "SPIN NOW"
                        md_bg_color: [0.95, 0.55, 0.1, 1]
                        pos_hint: {"center_x": 0.5}
                        size_hint_x: 0.7
                        size_hint_y: None
                        height: dp(50)
                        on_release: app.perform_spin()

                    MDLabel:
                        id: spin_cost_label
                        text: ""
                        halign: "center"
                        font_style: "Caption"
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: dp(20)

                    # Prize legend
                    MDCard:
                        orientation: 'vertical'
                        padding: dp(15)
                        spacing: dp(8)
                        size_hint_y: None
                        height: self.minimum_height
                        elevation: 2
                        radius: [15]

                        MDLabel:
                            text: "Possible Prizes"
                            font_style: "H6"
                            bold: True
                            size_hint_y: None
                            height: dp(30)

                        MDBoxLayout:
                            id: spin_legend_box
                            orientation: 'vertical'
                            spacing: dp(6)
                            size_hint_y: None
                            height: self.minimum_height

                    MDLabel:
                        text: "Recent Wins"
                        font_style: "H6"
                        bold: True
                        size_hint_y: None
                        height: dp(30)

                    MDList:
                        id: spin_history_list
                        spacing: dp(4)

<CouponScreen>:
    name: "coupons"

    MDScreen:
        md_bg_color: app.theme_cls.bg_normal

        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(10)

            # Header
            MDBoxLayout:
                size_hint_y: None
                height: dp(60)
                padding: [dp(10), 0]
                spacing: dp(10)
                md_bg_color: [0.35, 0.3, 0.9, 1]
                radius: [10, 10, 0, 0]

                MDIconButton:
                    icon: "arrow-left"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    on_release: app.root.current = "dashboard"
                    radius: [4, ]

                MDLabel:
                    text: "My Coupons"
                    font_style: "H5"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: [1, 1, 1, 1]
                    halign: "center"
                    size_hint_x: 0.8

                MDIconButton:
                    icon: "refresh"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    on_release: app.load_coupon_data()

            ScrollView:
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: dp(15)
                    padding: [dp(20), dp(20), dp(20), dp(20)]
                    size_hint_y: None
                    height: self.minimum_height

                    MDLabel:
                        text: "Enter a coupon code at checkout on any airtime, data, cable TV, electricity or exam-pin purchase to redeem it."
                        halign: "left"
                        text_size: self.width, None
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDLabel:
                        id: coupon_empty_label
                        text: ""
                        halign: "center"
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: dp(30)

                    MDList:
                        id: coupon_list
                        spacing: dp(6)

<MerchantScreen>:
    name: "merchant"

    MDScreen:
        md_bg_color: app.theme_cls.bg_normal

        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(10)

            # Header
            MDBoxLayout:
                size_hint_y: None
                height: dp(60)
                padding: [dp(10), 0]
                spacing: dp(10)
                md_bg_color: [0.1, 0.55, 0.4, 1]
                radius: [10, 10, 0, 0]

                MDIconButton:
                    icon: "arrow-left"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    on_release: app.root.current = "dashboard"
                    radius: [4, ]

                MDLabel:
                    text: "Merchant Dashboard"
                    font_style: "H5"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: [1, 1, 1, 1]
                    halign: "center"
                    size_hint_x: 0.8

                MDIconButton:
                    icon: "refresh"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    on_release: app.load_merchant_data()

            ScrollView:
                MDBoxLayout:
                    id: merchant_sections_container
                    orientation: 'vertical'
                    spacing: dp(15)
                    padding: [dp(20), dp(20), dp(20), dp(20)]
                    size_hint_y: None
                    height: self.minimum_height

                    # ── Apply form (shown when no profile / rejected) ──
                    MDBoxLayout:
                        id: merchant_apply_box
                        orientation: 'vertical'
                        spacing: dp(12)
                        size_hint_y: None
                        height: self.minimum_height

                        MDLabel:
                            text: "Become a Merchant"
                            font_style: "H6"
                            bold: True
                            size_hint_y: None
                            height: dp(30)

                        MDLabel:
                            id: merchant_rejection_label
                            text: ""
                            theme_text_color: "Error"
                            size_hint_y: None
                            height: self.texture_size[1]
                            text_size: self.width, None

                        MDTextField:
                            id: merchant_business_name
                            hint_text: "Business name"
                            icon_left: "store-outline"
                            mode: "rectangle"

                        MDBoxLayout:
                            spacing: dp(10)
                            size_hint_y: None
                            height: dp(45)

                            MDRaisedButton:
                                id: merchant_type_individual_btn
                                text: "Individual"
                                md_bg_color: app.theme_cls.primary_color
                                on_release: app.set_merchant_business_type("individual")

                            MDFlatButton:
                                id: merchant_type_registered_btn
                                text: "Registered Business"
                                on_release: app.set_merchant_business_type("registered_business")

                        MDTextField:
                            id: merchant_registration_number
                            hint_text: "CAC / Registration number (optional)"
                            icon_left: "file-document-outline"
                            mode: "rectangle"

                        MDTextField:
                            id: merchant_business_address
                            hint_text: "Business address"
                            icon_left: "map-marker-outline"
                            mode: "rectangle"

                        MDTextField:
                            id: merchant_business_phone
                            hint_text: "Business phone"
                            icon_left: "phone-outline"
                            input_type: "number"
                            mode: "rectangle"

                        MDRaisedButton:
                            text: "SUBMIT APPLICATION"
                            md_bg_color: [0.1, 0.55, 0.4, 1]
                            pos_hint: {"center_x": 0.5}
                            size_hint_x: 0.9
                            on_release: app.submit_merchant_application()

                    # ── Status banner (shown when pending / suspended) ──
                    MDCard:
                        id: merchant_status_box
                        orientation: 'vertical'
                        padding: dp(20)
                        spacing: dp(10)
                        size_hint_y: None
                        height: dp(150)
                        elevation: 2
                        radius: [15]

                        MDIcon:
                            icon: "clock-outline"
                            pos_hint: {"center_x": 0.5}
                            size_hint: [None, None]
                            size: [dp(40), dp(40)]

                        MDLabel:
                            id: merchant_status_label
                            text: ""
                            halign: "center"
                            text_size: self.width, None
                            theme_text_color: "Secondary"

                    # ── Dashboard (shown when approved) ──
                    MDBoxLayout:
                        id: merchant_dashboard_box
                        orientation: 'vertical'
                        spacing: dp(15)
                        size_hint_y: None
                        height: self.minimum_height

                        MDCard:
                            orientation: 'vertical'
                            padding: dp(20)
                            spacing: dp(8)
                            size_hint_y: None
                            height: dp(110)
                            elevation: 2
                            radius: [15]
                            md_bg_color: [0.1, 0.55, 0.4, 1]

                            MDLabel:
                                text: "Wallet Balance"
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: [1, 1, 1, 0.9]
                                size_hint_y: None
                                height: dp(25)

                            MDLabel:
                                id: merchant_wallet_label
                                text: "₦0.00"
                                font_style: "H4"
                                bold: True
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: [1, 1, 1, 1]

                        MDCard:
                            orientation: 'vertical'
                            padding: dp(15)
                            spacing: dp(8)
                            size_hint_y: None
                            height: dp(110)
                            elevation: 2
                            radius: [15]

                            MDLabel:
                                text: "Profit Summary"
                                font_style: "H6"
                                bold: True
                                size_hint_y: None
                                height: dp(28)

                            MDLabel:
                                id: merchant_profit_label
                                text: "Total profit: ₦0.00"
                                theme_text_color: "Secondary"
                                size_hint_y: None
                                height: dp(25)

                            MDLabel:
                                id: merchant_profit_breakdown_label
                                text: ""
                                theme_text_color: "Secondary"
                                font_style: "Caption"
                                text_size: self.width, None
                                size_hint_y: None
                                height: self.texture_size[1]

                        MDCard:
                            orientation: 'vertical'
                            padding: dp(15)
                            spacing: dp(10)
                            size_hint_y: None
                            height: self.minimum_height
                            elevation: 2
                            radius: [15]

                            MDLabel:
                                text: "Bulk Purchase"
                                font_style: "H6"
                                bold: True
                                size_hint_y: None
                                height: dp(28)

                            MDBoxLayout:
                                id: merchant_job_type_row
                                spacing: dp(6)
                                size_hint_y: None
                                height: dp(40)

                                MDRaisedButton:
                                    id: merchant_type_airtime_btn
                                    text: "Airtime"
                                    md_bg_color: app.theme_cls.primary_color
                                    on_release: app.set_merchant_job_type("airtime")

                                MDFlatButton:
                                    id: merchant_type_data_btn
                                    text: "Data"
                                    on_release: app.set_merchant_job_type("data")

                                MDFlatButton:
                                    id: merchant_type_cable_btn
                                    text: "Cable"
                                    on_release: app.set_merchant_job_type("cable_tv")

                            MDBoxLayout:
                                spacing: dp(6)
                                size_hint_y: None
                                height: dp(40)

                                MDFlatButton:
                                    id: merchant_type_electricity_btn
                                    text: "Electricity"
                                    on_release: app.set_merchant_job_type("electricity")

                                MDFlatButton:
                                    id: merchant_type_exam_btn
                                    text: "Exam PIN"
                                    on_release: app.set_merchant_job_type("exam_pin")

                            MDLabel:
                                id: merchant_format_hint_label
                                text: "One per line: network,phone,amount"
                                font_style: "Caption"
                                theme_text_color: "Secondary"
                                text_size: self.width, None
                                size_hint_y: None
                                height: self.texture_size[1]

                            MDTextField:
                                id: merchant_bulk_input
                                hint_text: "MTN,08012345678,500"
                                multiline: True
                                mode: "rectangle"
                                size_hint_y: None
                                height: dp(120)

                            MDRaisedButton:
                                text: "SUBMIT BATCH"
                                md_bg_color: [0.1, 0.55, 0.4, 1]
                                pos_hint: {"center_x": 0.5}
                                size_hint_x: 0.9
                                on_release: app.submit_merchant_bulk_job()

                        MDCard:
                            orientation: 'vertical'
                            padding: dp(15)
                            spacing: dp(8)
                            size_hint_y: None
                            height: dp(90)
                            elevation: 2
                            radius: [15]

                            MDLabel:
                                text: "API Access"
                                font_style: "H6"
                                bold: True
                                size_hint_y: None
                                height: dp(28)

                            MDBoxLayout:
                                spacing: dp(10)
                                size_hint_y: None
                                height: dp(35)

                                MDLabel:
                                    text: "Use your API key in the X-API-Key header"
                                    font_style: "Caption"
                                    theme_text_color: "Secondary"

                                MDFlatButton:
                                    text: "Get / Reset Key"
                                    theme_text_color: "Custom"
                                    text_color: [0.1, 0.55, 0.4, 1]
                                    on_release: app.regenerate_merchant_api_key()

                        MDLabel:
                            text: "Recent Bulk Jobs"
                            font_style: "H6"
                            bold: True
                            size_hint_y: None
                            height: dp(30)

                        MDList:
                            id: merchant_job_list
                            spacing: dp(4)

<CardScreen>:
    name: "cards"

    MDScreen:
        md_bg_color: app.theme_cls.bg_normal

        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(10)

            # Header
            MDBoxLayout:
                size_hint_y: None
                height: dp(60)
                padding: [dp(10), 0]
                spacing: dp(10)
                md_bg_color: [0.3, 0.25, 0.7, 1]
                radius: [10, 10, 0, 0]

                MDIconButton:
                    icon: "arrow-left"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    on_release: app.root.current = "dashboard"
                    radius: [4, ]

                MDLabel:
                    text: "Virtual Dollar Cards"
                    font_style: "H5"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: [1, 1, 1, 1]
                    halign: "center"
                    size_hint_x: 0.8

                MDIconButton:
                    icon: "refresh"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    on_release: app.load_card_data()

            ScrollView:
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: dp(15)
                    padding: [dp(20), dp(20), dp(20), dp(20)]
                    size_hint_y: None
                    height: self.minimum_height

                    MDLabel:
                        id: card_rate_label
                        text: ""
                        font_style: "Caption"
                        halign: "center"
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: dp(20)

                    MDRaisedButton:
                        text: "+ CREATE NEW CARD"
                        md_bg_color: [0.3, 0.25, 0.7, 1]
                        pos_hint: {"center_x": 0.5}
                        size_hint_x: 0.9
                        on_release: app.show_create_card_dialog()

                    MDLabel:
                        id: card_empty_label
                        text: ""
                        halign: "center"
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: dp(30)

                    MDBoxLayout:
                        id: card_list_box
                        orientation: 'vertical'
                        spacing: dp(15)
                        size_hint_y: None
                        height: self.minimum_height

<BillReminderScreen>:
    name: "reminders"

    MDScreen:
        md_bg_color: app.theme_cls.bg_normal

        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(10)

            # Header
            MDBoxLayout:
                size_hint_y: None
                height: dp(60)
                padding: [dp(10), 0]
                spacing: dp(10)
                md_bg_color: [0.75, 0.55, 0.1, 1]
                radius: [10, 10, 0, 0]

                MDIconButton:
                    icon: "arrow-left"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    on_release: app.root.current = "dashboard"
                    radius: [4, ]

                MDLabel:
                    text: "Bill Reminders"
                    font_style: "H5"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: [1, 1, 1, 1]
                    halign: "center"
                    size_hint_x: 0.8

                MDIconButton:
                    icon: "refresh"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    on_release: app.load_reminder_data()

            ScrollView:
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: dp(15)
                    padding: [dp(20), dp(20), dp(20), dp(20)]
                    size_hint_y: None
                    height: self.minimum_height

                    MDRaisedButton:
                        text: "+ ADD BILL REMINDER"
                        md_bg_color: [0.75, 0.55, 0.1, 1]
                        pos_hint: {"center_x": 0.5}
                        size_hint_x: 0.9
                        on_release: app.show_add_reminder_dialog()

                    MDLabel:
                        id: reminder_empty_label
                        text: ""
                        halign: "center"
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: dp(30)

                    MDBoxLayout:
                        id: reminder_list_box
                        orientation: 'vertical'
                        spacing: dp(12)
                        size_hint_y: None
                        height: self.minimum_height

<ComparisonScreen>:
    name: "compare"

    MDScreen:
        md_bg_color: app.theme_cls.bg_normal

        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(10)

            # Header
            MDBoxLayout:
                size_hint_y: None
                height: dp(60)
                padding: [dp(10), 0]
                spacing: dp(10)
                md_bg_color: [0.1, 0.6, 0.65, 1]
                radius: [10, 10, 0, 0]

                MDIconButton:
                    icon: "arrow-left"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    on_release: app.root.current = "dashboard"
                    radius: [4, ]

                MDLabel:
                    text: "Price Comparison"
                    font_style: "H5"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: [1, 1, 1, 1]
                    halign: "center"
                    size_hint_x: 0.8

                MDIconButton:
                    icon: "refresh"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    on_release: app.load_comparison_data()

            MDBoxLayout:
                spacing: dp(8)
                size_hint_y: None
                height: dp(45)

                MDRaisedButton:
                    id: compare_data_tab_btn
                    text: "Data Plans"
                    md_bg_color: [0.1, 0.6, 0.65, 1]
                    on_release: app.set_comparison_mode("data")

                MDFlatButton:
                    id: compare_airtime_tab_btn
                    text: "Airtime"
                    on_release: app.set_comparison_mode("airtime")

            ScrollView:
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: dp(15)
                    padding: [dp(20), dp(20), dp(20), dp(20)]
                    size_hint_y: None
                    height: self.minimum_height

                    MDLabel:
                        id: compare_note_label
                        text: ""
                        font_style: "Caption"
                        theme_text_color: "Secondary"
                        text_size: self.width, None
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDBoxLayout:
                        id: compare_badges_box
                        orientation: 'vertical'
                        spacing: dp(8)
                        size_hint_y: None
                        height: self.minimum_height

                    MDBoxLayout:
                        id: compare_promo_box
                        orientation: 'vertical'
                        spacing: dp(8)
                        size_hint_y: None
                        height: self.minimum_height

                    MDLabel:
                        text: "Full Comparison"
                        font_style: "H6"
                        bold: True
                        size_hint_y: None
                        height: dp(30)

                    MDBoxLayout:
                        id: compare_results_box
                        orientation: 'vertical'
                        spacing: dp(8)
                        size_hint_y: None
                        height: self.minimum_height

<GamificationScreen>:
    name: "gamification"

    MDScreen:
        md_bg_color: app.theme_cls.bg_normal

        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(10)

            # Header
            MDBoxLayout:
                size_hint_y: None
                height: dp(60)
                padding: [dp(10), 0]
                spacing: dp(10)
                md_bg_color: [0.85, 0.6, 0.1, 1]
                radius: [10, 10, 0, 0]

                MDIconButton:
                    icon: "arrow-left"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    on_release: app.root.current = "dashboard"
                    radius: [4, ]

                MDLabel:
                    text: "Rewards"
                    font_style: "H5"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: [1, 1, 1, 1]
                    halign: "center"
                    size_hint_x: 0.8

                MDIconButton:
                    icon: "refresh"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    on_release: app.load_gamification_data()

            ScrollView:
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: dp(15)
                    padding: [dp(20), dp(20), dp(20), dp(20)]
                    size_hint_y: None
                    height: self.minimum_height

                    # Level / XP card
                    MDCard:
                        orientation: 'vertical'
                        padding: dp(20)
                        spacing: dp(8)
                        size_hint_y: None
                        height: dp(180)
                        elevation: 2
                        radius: [15]
                        md_bg_color: [0.85, 0.6, 0.1, 1]

                        MDBoxLayout:
                            size_hint_y: None
                            height: dp(40)

                            MDIcon:
                                id: gam_level_icon
                                icon: "star-outline"
                                theme_text_color: "Custom"
                                text_color: [1, 1, 1, 1]
                                size_hint_x: None
                                width: dp(30)

                            MDLabel:
                                id: gam_level_label
                                text: "Level 1 — Bronze"
                                font_style: "H6"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: [1, 1, 1, 1]

                            MDLabel:
                                id: gam_rank_label
                                text: ""
                                halign: "right"
                                theme_text_color: "Custom"
                                text_color: [1, 1, 1, 0.9]

                        MDProgressBar:
                            id: gam_xp_progress
                            value: 0
                            max: 100
                            size_hint_y: None
                            height: dp(10)
                            color: [1, 1, 1, 1]

                        MDLabel:
                            id: gam_xp_label
                            text: "0 XP"
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: [1, 1, 1, 0.9]
                            size_hint_y: None
                            height: dp(25)

                        MDLabel:
                            id: gam_next_level_label
                            text: ""
                            halign: "center"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: [1, 1, 1, 0.8]
                            size_hint_y: None
                            height: dp(20)

                    # Missions
                    MDLabel:
                        text: "Missions"
                        font_style: "H6"
                        bold: True
                        size_hint_y: None
                        height: dp(30)

                    MDBoxLayout:
                        id: gam_missions_box
                        orientation: 'vertical'
                        spacing: dp(10)
                        size_hint_y: None
                        height: self.minimum_height

                    # Badges
                    MDLabel:
                        text: "Badges"
                        font_style: "H6"
                        bold: True
                        size_hint_y: None
                        height: dp(30)

                    MDGridLayout:
                        id: gam_badges_grid
                        cols: 4
                        spacing: dp(10)
                        size_hint_y: None
                        height: self.minimum_height

                    # Leaderboard
                    MDLabel:
                        text: "Leaderboard"
                        font_style: "H6"
                        bold: True
                        size_hint_y: None
                        height: dp(30)

                    MDList:
                        id: gam_leaderboard_list
                        spacing: dp(4)

<ProfitScreen>:
    name: "profit"
    
    MDScreen:
        md_bg_color: app.theme_cls.bg_normal
        
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(10)
            
            # Header
            MDBoxLayout:
                size_hint_y: None
                height: dp(60)
                padding: [dp(10), 0]
                spacing: dp(10)
                md_bg_color: app.theme_cls.primary_color
                radius: [10, 10, 0, 0]
                
                MDIconButton:
                    icon: "arrow-left"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    radius: [18]
                    on_release: app.root.current = "dashboard"
                    
                MDLabel:
                    text: "Admin Profit Dashboard"
                    font_style: "H5"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: [1, 1, 1, 1]
                    halign: "center"
                    size_hint_x: 0.6
                 
                MDIconButton:
                    icon: "bank-transfer"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    radius: [dp(18)]
                    on_release: app.          show_withdraw_dialog()  
                
                    
                MDIconButton:
                    icon: "refresh"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    radius: [18]
                    on_release: app.load_profit_data()
            
            ScrollView:
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: dp(15)
                    padding: dp(10)
                    size_hint_y: None
                    height: self.minimum_height
                    
                    MDCard:
                        orientation: 'vertical'
                        padding: dp(15)
                        spacing: dp(10)
                        size_hint_y: None
                        height: dp(80)

                        MDRaisedButton:
                            text: "VIEW & MANAGE USERS"
                            md_bg_color: app.theme_cls.primary_color
                            on_release: app.show_admin_users()
                            size_hint_x: 1
                            size_hint_y: None
                            height: dp(50)
        
                    # Total Profit Card
                    MDCard:
                        orientation: 'vertical'
                        padding: dp(20)
                        spacing: dp(10)
                        size_hint_y: None
                        height: dp(120)
                        md_bg_color: [0.2, 0.8, 0.2, 1]
                        
                        MDLabel:
                            text: "Available Profit"
                            font_style: "H6"
                            theme_text_color: "Custom"
                            text_color: [1, 1, 1, 0.9]
                            halign: 'center'
                            
                        MDLabel:
                            id: total_profit_label
                            text: "₦0.00"
                            font_style: "H4"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: [1, 1, 1, 1]
                            halign: 'center'
                        
                        MDLabel:
                            id: total_earned_label
                            text: "Total Earned: ₦0.00"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: [1, 1, 1, 0.8]
                            halign: 'center'

                    # Spin & Win extra-spin fee revenue
                    MDCard:
                        orientation: 'horizontal'
                        padding: dp(15)
                        spacing: dp(10)
                        size_hint_y: None
                        height: dp(60)
                        elevation: 1
                        radius: [12]

                        MDIcon:
                            icon: "dharmachakra"
                            theme_text_color: "Custom"
                            text_color: [0.95, 0.55, 0.1, 1]
                            size_hint_x: None
                            width: dp(30)

                        MDLabel:
                            text: "Spin & Win fees"
                            theme_text_color: "Primary"

                        MDLabel:
                            id: spin_fee_profit_label
                            text: "₦0.00"
                            bold: True
                            halign: 'right'
                            theme_text_color: "Primary"
                    
                    # Withdrawal Section
                    MDCard:
                        orientation: 'vertical'
                        padding: dp(15)
                        spacing: dp(10)
                        size_hint_y: None
                        height: dp(100)
                        
                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: dp(10)
                            
                            MDRaisedButton:
                                text: "WITHDRAW PROFIT"
                                md_bg_color: [0.9, 0.3, 0.3, 1]
                              
                                on_release: app.show_withdraw_dialog()
                                size_hint_x: 0.6
                                
                            MDLabel:
                                id: withdrawal_status
                                text: ""
                                theme_text_color: "Secondary"
                                halign: 'center'
                                size_hint_x: 0.4
                    
                    # Profit by Category (keep existing category cards...)
                    # ... [Keep the existing category cards code] ...
                    
                    # Withdrawal History
                    MDLabel:
                        text: "Withdrawal History"
                        font_style: "H6"
                        bold: True
                        size_hint_y: None
                        height: dp(30)
                        
                    MDBoxLayout:
                        id: withdrawal_history_box
                        orientation: 'vertical'
                        spacing: dp(5)
                        size_hint_y: None
                        height: dp(150)
                                        
# Add this to your KV string after ProfitScreen

<WithdrawScreen>:
    name: "withdraw"
    
    MDScreen:
        md_bg_color: app.theme_cls.bg_normal
        
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(10)
            
            # Header
            MDBoxLayout:
                size_hint_y: None
                height: dp(60)
                padding: [dp(10), 0]
                spacing: dp(10)
                md_bg_color: app.theme_cls.primary_color
                radius: [10, 10, 0, 0]
                
                MDIconButton:
                    icon: "arrow-left"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    on_release: app.root.current = "profit"
                    radius: [18]
                    
                MDLabel:
                    text: "Withdraw Profit"
                    font_style: "H5"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: [1, 1, 1, 1]
                    halign: "center"
                    size_hint_x: 0.8
            
            ScrollView:
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: dp(20)
                    padding: [dp(20), dp(20), dp(20), dp(20)]
                    size_hint_y: None
                    height: self.minimum_height
                    
                    # Available Balance Card
                    MDCard:
                        orientation: 'vertical'
                        padding: dp(20)
                        spacing: dp(10)
                        size_hint_y: None
                        height: dp(100)
                        md_bg_color: [0.2, 0.8, 0.2, 1]
                        
                        MDLabel:
                            text: "Available Balance"
                            font_style: "H6"
                            theme_text_color: "Custom"
                            text_color: [1, 1, 1, 0.9]
                            halign: 'center'
                            
                        MDLabel:
                            id: withdraw_balance_label
                            text: "₦0.00"
                            font_style: "H4"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: [1, 1, 1, 1]
                            halign: 'center'
                    
                    # Withdrawal Form
                    MDCard:
                        orientation: 'vertical'
                        padding: dp(20)
                        spacing: dp(15)
                        size_hint_y: None
                        height: dp(330)
                        
                        MDTextField:
                            id: withdraw_amount
                            hint_text: "Amount to withdraw"
                            icon_left: "cash"
                            input_type: 'number'
                            helper_text: "Enter amount between ₦50 and ₦500,000"
                            helper_text_mode: "on_focus"
                            size_hint_x: 1
                            
                        MDTextField:
                            id: bank_name
                            hint_text: "Tap to select bank"
                            icon_left: "bank-outline"
                          #  readonly: True
                            size_hint_x: 1
                            on_focus: if self.focus: app.show_bank_picker()                           

                        MDTextField:
                            id: account_number
                            hint_text: "Account Number (10 digits)"
                            icon_left: "credit-card-outline"
                            input_type: 'number'
                            max_text_length: 10
                            size_hint_x: 1                                                                                                  
                    # Action Buttons
                    MDBoxLayout:
                        orientation: 'vertical'
                        spacing: dp(15)
                        size_hint_y: None
                        height: dp(120)
                        
                        MDRaisedButton:
                            id: withdraw_btn
                            text: "PROCEED WITH WITHDRAWAL"
                            md_bg_color: app.theme_cls.primary_color
                            on_release: app.process_withdrawal()
                            size_hint_x: 1                       
                            size_hint_y: None
                            height: dp(50)
                            
                        MDTextButton:
                            text: "Back to Profit Dashboard"
                            
                            theme_text_color: "Custom"
                            text_color: app.theme_cls.primary_color
                            on_release: app.root.current = "profit"
                            halign: 'center'
                            
                            
               
# ══════════════════════════════════════════════════════════════════
# SUPPORT CENTER
# Replaces the old WhatsApp redirect button. Tapping "Support" in the
# bottom nav opens this screen instead of leaving the app.
# ══════════════════════════════════════════════════════════════════

<ChatBubbleLabel@MDLabel>:
    # Reusable auto-height, word-wrapping label used inside chat bubbles.
    size_hint_y: None
    text_size: self.width, None
    height: self.texture_size[1]
    markup: False
    font_style: "Body1"

<SupportScreen>:
    name: "support"

    MDScreen:
        md_bg_color: [0.9608, 0.9686, 0.9804, 1]

        MDBoxLayout:
            orientation: 'vertical'

            # ── Header: standard AppBar row (matches every other screen)
            # plus the "Need Help?" hero, all on one continuous blue
            # gradient panel (primary -> accent, per the design spec).
            MDCard:
                md_bg_color: app.theme_cls.primary_color
                size_hint_y: None
                height: dp(172)
                radius: [0, 0, dp(24), dp(24)]
                elevation: 6
                padding: 0

                MDBoxLayout:
                    orientation: 'vertical'

                    MDBoxLayout:
                        size_hint_y: None
                        height: dp(56)
                        padding: [dp(4), 0, dp(16), 0]

                        MDIconButton:
                            icon: "arrow-left"
                            theme_icon_color: "Custom"
                            icon_color: [1, 1, 1, 1]
                            on_release: app.switch_screen('dashboard')

                        MDLabel:
                            text: "Support Center"
                            font_style: "H6"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: [1, 1, 1, 1]
                            valign: "middle"

                    MDBoxLayout:
                        orientation: 'vertical'
                        spacing: dp(6)
                        padding: [dp(24), dp(4), dp(24), dp(24)]

                        MDLabel:
                            text: "Need Help?"
                            font_style: "H4"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: [1, 1, 1, 1]
                            size_hint_y: None
                            height: dp(44)

                        MDLabel:
                            text: "We're here to assist you 24/7."
                            font_style: "Subtitle1"
                            theme_text_color: "Custom"
                            text_color: [1, 1, 1, 0.92]
                            size_hint_y: None
                            height: dp(24)

            ScrollView:
                do_scroll_x: False

                MDBoxLayout:
                    orientation: 'vertical'
                    padding: [dp(16), dp(24), dp(16), dp(32)]
                    spacing: dp(16)
                    size_hint_y: None
                    height: self.minimum_height

                    # 1. AI ASSISTANT — main / biggest option
                    MDCard:
                        md_bg_color: app.theme_cls.primary_color
                        size_hint_y: None
                        height: dp(152)
                        radius: [dp(22)]
                        elevation: 6
                        padding: dp(20)
                        on_release: app.open_ai_chat()

                        MDBoxLayout:
                            spacing: dp(18)

                            # Icon square — a FloatLayout guarantees the
                            # icon is perfectly centered no matter what
                            # (MDCard alone does not honor pos_hint).
                            MDCard:
                                size_hint: None, None
                                size: dp(64), dp(64)
                                radius: [dp(18)]
                                md_bg_color: [1, 1, 1, 0.22]
                                pos_hint: {"center_y": 0.5}

                                FloatLayout:
                                    MDIcon:
                                        icon: "robot-happy-outline"
                                        font_size: "42sp"
                                        pos_hint: {"center_x": 0.5, "center_y": 0.5}
                                        theme_text_color: "Custom"
                                        text_color: [1, 1, 1, 1]

                            MDBoxLayout:
                                orientation: 'vertical'
                                spacing: dp(6)
                                pos_hint: {"center_y": 0.5}

                                MDLabel:
                                    text: "AI Assistant"
                                    font_style: "H5"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 1]
                                    size_hint_y: None
                                    height: dp(32)
                                    valign: "middle"

                                MDLabel:
                                    text: "Get instant answers, 24/7"
                                    font_style: "Body2"
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 0.9]
                                    size_hint_y: None
                                    height: dp(22)
                                    valign: "middle"

                                MDBoxLayout:
                                    size_hint_y: None
                                    height: dp(20)
                                    spacing: dp(8)

                                    MDIcon:
                                        icon: "circle"
                                        font_size: "10sp"
                                        theme_text_color: "Custom"
                                        text_color: [0.1333, 0.7725, 0.3686, 1]
                                        size_hint: None, None
                                        size: dp(16), dp(20)
                                        pos_hint: {"center_y": 0.5}
                                        halign: "center"
                                        valign: "middle"

                                    MDLabel:
                                        text: "Online now"
                                        font_style: "Caption"
                                        theme_text_color: "Custom"
                                        text_color: [1, 1, 1, 0.88]
                                        valign: "middle"

                            MDIcon:
                                icon: "chevron-right"
                                theme_text_color: "Custom"
                                text_color: [1, 1, 1, 0.9]
                                size_hint: None, None
                                size: dp(24), dp(24)
                                pos_hint: {"center_y": 0.5}
                                halign: "center"
                                valign: "middle"

                    # 2. PHONE SUPPORT
                    MDCard:
                        size_hint_y: None
                        height: dp(92)
                        radius: [dp(22)]
                        elevation: 3
                        padding: [dp(22), dp(14), dp(18), dp(14)]
                        md_bg_color: [1, 1, 1, 1]
                        on_release: app.call_phone_support()

                        MDBoxLayout:
                            spacing: dp(18)

                            MDCard:
                                size_hint: None, None
                                size: dp(56), dp(56)
                                radius: [dp(16)]
                                md_bg_color: [0.898, 0.945, 1, 1]
                                pos_hint: {"center_y": 0.5}

                                FloatLayout:
                                    MDIcon:
                                        icon: "phone"
                                        font_size: "26sp"
                                        pos_hint: {"center_x": 0.5, "center_y": 0.5}
                                        theme_text_color: "Custom"
                                        text_color: [0.1294, 0.5882, 0.9529, 1]

                            MDBoxLayout:
                                orientation: 'vertical'
                                spacing: dp(4)
                                pos_hint: {"center_y": 0.5}

                                MDLabel:
                                    text: "Phone Support"
                                    font_style: "Subtitle1"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: [0.1216, 0.1608, 0.2157, 1]
                                    size_hint_y: None
                                    height: dp(26)
                                    valign: "middle"

                                MDLabel:
                                    text: "Tap to Call  \u2022  " + app.support_phone
                                    font_style: "Caption"
                                    theme_text_color: "Custom"
                                    text_color: [0.4196, 0.4471, 0.5020, 1]
                                    size_hint_y: None
                                    height: dp(20)
                                    valign: "middle"

                            MDIcon:
                                icon: "chevron-right"
                                theme_text_color: "Custom"
                                text_color: [0.4196, 0.4471, 0.5020, 1]
                                size_hint: None, None
                                size: dp(24), dp(24)
                                pos_hint: {"center_y": 0.5}
                                halign: "center"
                                valign: "middle"

                    # 3. EMAIL SUPPORT
                    MDCard:
                        size_hint_y: None
                        height: dp(92)
                        radius: [dp(22)]
                        elevation: 3
                        padding: [dp(22), dp(14), dp(18), dp(14)]
                        md_bg_color: [1, 1, 1, 1]
                        on_release: app.open_email_support()

                        MDBoxLayout:
                            spacing: dp(18)

                            MDCard:
                                size_hint: None, None
                                size: dp(56), dp(56)
                                radius: [dp(16)]
                                md_bg_color: [0.898, 0.945, 1, 1]
                                pos_hint: {"center_y": 0.5}

                                FloatLayout:
                                    MDIcon:
                                        icon: "email"
                                        font_size: "26sp"
                                        pos_hint: {"center_x": 0.5, "center_y": 0.5}
                                        theme_text_color: "Custom"
                                        text_color: [0.1294, 0.5882, 0.9529, 1]

                            MDBoxLayout:
                                orientation: 'vertical'
                                spacing: dp(4)
                                pos_hint: {"center_y": 0.5}

                                MDLabel:
                                    text: "Email Support"
                                    font_style: "Subtitle1"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: [0.1216, 0.1608, 0.2157, 1]
                                    size_hint_y: None
                                    height: dp(26)
                                    valign: "middle"

                                MDLabel:
                                    text: app.support_email
                                    font_style: "Caption"
                                    theme_text_color: "Custom"
                                    text_color: [0.4196, 0.4471, 0.5020, 1]
                                    size_hint_y: None
                                    height: dp(20)
                                    valign: "middle"

                            MDIcon:
                                icon: "chevron-right"
                                theme_text_color: "Custom"
                                text_color: [0.4196, 0.4471, 0.5020, 1]
                                size_hint: None, None
                                size: dp(24), dp(24)
                                pos_hint: {"center_y": 0.5}
                                halign: "center"
                                valign: "middle"

                    # Business hours + version — centered, compact
                    MDBoxLayout:
                        orientation: 'vertical'
                        spacing: dp(6)
                        size_hint_y: None
                        height: dp(76)
                        padding: [0, dp(10), 0, 0]

                        MDLabel:
                            text: "Business Hours"
                            font_style: "Caption"
                            bold: True
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: [0.4196, 0.4471, 0.5020, 1]
                            size_hint_y: None
                            height: dp(18)

                        MDLabel:
                            text: "Monday - Sunday  \u2022  24 Hours Support"
                            font_style: "Caption"
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: [0.4196, 0.4471, 0.5020, 1]
                            size_hint_y: None
                            height: dp(18)

                        MDLabel:
                            text: "Version " + app.app_version
                            font_style: "Caption"
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: [0.62, 0.64, 0.67, 1]
                            size_hint_y: None
                            height: dp(18)


# ══════════════════════════════════════════════════════════════════
# AI CHAT ASSISTANT — ChatGPT/Claude/Gemini-style mobile chat UI
# ══════════════════════════════════════════════════════════════════

<AIChatScreen>:
    name: "ai_chat"

    MDScreen:
        md_bg_color: [0.9608, 0.9686, 0.9804, 1]

        MDBoxLayout:
            orientation: 'vertical'

            # Top bar — same AppBar convention as every other screen
            MDBoxLayout:
                size_hint_y: None
                height: dp(64)
                padding: [dp(4), 0, dp(14), 0]
                spacing: dp(10)
                md_bg_color: [0.1294, 0.5882, 0.9529, 1]
                radius: [0, 0, dp(18), dp(18)]

                MDIconButton:
                    icon: "arrow-left"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    on_release: app.switch_screen('support')

                MDCard:
                    size_hint: None, None
                    size: dp(38), dp(38)
                    radius: [dp(12)]
                    md_bg_color: [1, 1, 1, 0.2]
                    pos_hint: {"center_y": 0.5}

                    FloatLayout:
                        MDIcon:
                            icon: "robot-happy-outline"
                            font_size: "22sp"
                            pos_hint: {"center_x": 0.5, "center_y": 0.5}
                            theme_text_color: "Custom"
                            text_color: [1, 1, 1, 1]

                MDBoxLayout:
                    orientation: 'vertical'
                    padding: [dp(4), 0]

                    MDLabel:
                        text: "AI Assistant"
                        font_style: "Subtitle1"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: [1, 1, 1, 1]
                        size_hint_y: None
                        height: dp(24)
                        valign: "middle"

                    MDLabel:
                        text: "Typing..." if app.ai_chat_typing else "Online \u2022 Replies instantly"
                        font_style: "Caption"
                        theme_text_color: "Custom"
                        text_color: [1, 1, 1, 0.85]
                        size_hint_y: None
                        height: dp(18)
                        valign: "middle"

                MDIconButton:
                    icon: "magnify"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    on_release: app.toggle_chat_search()

                MDIconButton:
                    icon: "delete-outline"
                    theme_icon_color: "Custom"
                    icon_color: [1, 1, 1, 1]
                    on_release: app.confirm_clear_ai_chat()

            # Rounded search bar — only visible while search is active
            MDBoxLayout:
                size_hint_y: None
                height: dp(58) if app.ai_search_active else 0
                opacity: 1 if app.ai_search_active else 0
                padding: [dp(14), dp(8)]
                md_bg_color: [0.9608, 0.9686, 0.9804, 1]

                MDTextField:
                    id: chat_search_field
                    hint_text: "Search this conversation"
                    icon_left: "magnify"
                    mode: "round"
                    disabled: not app.ai_search_active
                    on_text: app.filter_chat_search(self.text)

            # Chat messages
            ScrollView:
                id: chat_scroll
                do_scroll_x: False
                bar_width: dp(3)
                bar_color: [0.1294, 0.5882, 0.9529, 0.35]

                MDBoxLayout:
                    id: chat_list
                    orientation: 'vertical'
                    spacing: dp(16)
                    padding: [dp(12), dp(18), dp(12), dp(18)]
                    size_hint_y: None
                    height: self.minimum_height

            # Suggested question chips
            ScrollView:
                size_hint_y: None
                height: dp(48) if not app.ai_chat_messages else 0
                opacity: 1 if not app.ai_chat_messages else 0
                do_scroll_y: False
                bar_width: 0

                MDBoxLayout:
                    id: suggestions_box
                    orientation: 'horizontal'
                    spacing: dp(10)
                    padding: [dp(14), dp(4)]
                    size_hint_x: None
                    width: self.minimum_width

            # Input bar — rounded field + circular mic + circular send
            MDBoxLayout:
                size_hint_y: None
                height: dp(78)
                padding: [dp(14), dp(14)]
                spacing: dp(10)
                md_bg_color: [1, 1, 1, 1]

                MDCard:
                    size_hint: None, None
                    size: dp(46), dp(46)
                    radius: [dp(23)]
                    elevation: 0
                    md_bg_color: [0.9608, 0.9686, 0.9804, 1]
                    pos_hint: {"center_y": 0.5}

                    FloatLayout:
                        MDIconButton:
                            icon: "microphone"
                            theme_icon_color: "Custom"
                            icon_color: [0.1294, 0.5882, 0.9529, 1]
                            pos_hint: {"center_x": 0.5, "center_y": 0.5}
                            on_release: app.start_voice_input()

                MDTextField:
                    id: ai_chat_input
                    hint_text: "Type your question..."
                    icon_left: "chat-outline"
                    mode: "round"
                    multiline: False
                    size_hint_x: 1
                    pos_hint: {"center_y": 0.5}
                    on_text_validate: app.send_ai_message()

                MDCard:
                    size_hint: None, None
                    size: dp(48), dp(48)
                    radius: [dp(24)]
                    elevation: 0
                    md_bg_color: [0.1294, 0.5882, 0.9529, 1]
                    pos_hint: {"center_y": 0.5}

                    FloatLayout:
                        MDIconButton:
                            icon: "send"
                            theme_icon_color: "Custom"
                            icon_color: [1, 1, 1, 1]
                            pos_hint: {"center_x": 0.5, "center_y": 0.5}
                            on_release: app.send_ai_message()

'''


# Paste this BEFORE your LoginScreen, RegisterScreen etc.

from kivy.properties import StringProperty, NumericProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse, RoundedRectangle, PushMatrix, PopMatrix, Rotate, Line
import math
from kivy.graphics.texture import Texture
from kivy.properties import NumericProperty


class GradientBackground(Widget):
    """Smooth diagonal blue gradient background for the splash screen.
    Builds a small vertical gradient texture once and stretches it to
    fill the widget - cheap to draw, looks smooth at any screen size."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_texture()
        with self.canvas:
            self._rect = Rectangle(texture=self._texture, pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _build_texture(self):
        # Dark blue (top) -> Cheap4U brand blue (middle) -> lighter blue (bottom)
        stops = [
            (13, 40, 90),      # deep navy
            (21, 101, 192),    # #1565C0 brand blue
            (66, 145, 220),    # soft lighter blue
        ]
        height = 256
        buf = bytearray(height * 4)
        for y in range(height):
            t = y / (height - 1)
            if t < 0.5:
                t2 = t / 0.5
                c0, c1 = stops[0], stops[1]
            else:
                t2 = (t - 0.5) / 0.5
                c0, c1 = stops[1], stops[2]
            r = int(c0[0] + (c1[0] - c0[0]) * t2)
            g = int(c0[1] + (c1[1] - c0[1]) * t2)
            b = int(c0[2] + (c1[2] - c0[2]) * t2)
            idx = y * 4
            buf[idx:idx + 4] = bytes([r, g, b, 255])
        self._texture = Texture.create(size=(1, height), colorfmt="rgba")
        self._texture.blit_buffer(bytes(buf), colorfmt="rgba", bufferfmt="ubyte")
        self._texture.wrap = "clamp_to_edge"

    def _update_rect(self, *_):
        self._rect.pos = self.pos
        self._rect.size = self.size


class SpinWheelWidget(Widget):
    """Custom-drawn prize wheel for the Spin & Win screen.

    Segments (label/color) come from the backend so the wheel always
    matches whatever the admin has configured. Slices are drawn once with
    kivy.graphics.Ellipse's angle_start/angle_end (a true pie-slice, not an
    image), wrapped in a Rotate transform; spinning is just animating the
    `rotation` NumericProperty — cheap, no per-frame redraw of the slices.
    """

    rotation = NumericProperty(0)

    def __init__(self, **kwargs):
        self.segments = kwargs.pop('segments', []) or []
        super().__init__(**kwargs)
        self._rot_instr = None
        self.bind(pos=self._redraw, size=self._redraw)
        self.bind(rotation=self._apply_rotation)
        self.bind(parent=self._on_parent_changed)
        self._redraw()

    def _on_parent_changed(self, *_):
        # pos_hint centering is resolved by the parent FloatLayout AFTER
        # this widget is added to it (not during __init__, when pos/size
        # are still Kivy's defaults) — force a couple of follow-up redraws
        # once actually attached so the wheel never gets stuck showing its
        # very first (wrongly-positioned) draw.
        Clock.schedule_once(self._redraw, 0)
        Clock.schedule_once(self._redraw, 0.3)

    def set_segments(self, segments):
        self.segments = segments or []
        self._redraw()
        Clock.schedule_once(self._redraw, 0.2)

    @staticmethod
    def _hex_to_rgba(hex_color, alpha=1.0):
        try:
            h = (hex_color or '#2196F3').lstrip('#')
            r = int(h[0:2], 16) / 255.0
            g = int(h[2:4], 16) / 255.0
            b = int(h[4:6], 16) / 255.0
            return (r, g, b, alpha)
        except Exception:
            return (0.2, 0.6, 1.0, alpha)

    def _redraw(self, *_):
        self.canvas.clear()
        segs = self.segments
        n = len(segs)
        cx, cy = self.center
        radius = max(0, min(self.width, self.height) / 2 - dp(4))

        with self.canvas:
            PushMatrix()
            self._rot_instr = Rotate(angle=self.rotation, origin=(cx, cy))

            if n > 0 and radius > 0:
                sweep = 360.0 / n
                for i, seg in enumerate(segs):
                    Color(*self._hex_to_rgba(seg.get('color', '#2196F3')))
                    start = i * sweep
                    end = start + sweep
                    Ellipse(
                        pos=(cx - radius, cy - radius),
                        size=(radius * 2, radius * 2),
                        angle_start=start, angle_end=end,
                    )
                # divider lines between slices
                Color(1, 1, 1, 0.9)
                for i in range(n):
                    ang = math.radians(i * sweep)
                    Line(points=[cx, cy, cx + radius * math.cos(ang), cy + radius * math.sin(ang)],
                         width=dp(1))

            # outer rim
            Color(1, 1, 1, 1)
            Line(circle=(cx, cy, radius), width=dp(3))

            PopMatrix()

            # hub (drawn outside the rotate block so it stays fixed/on top)
            Color(1, 1, 1, 1)
            Ellipse(pos=(cx - dp(14), cy - dp(14)), size=(dp(28), dp(28)))
            Color(0.1, 0.75, 0.35, 1)
            Line(circle=(cx, cy, dp(14)), width=dp(2))

    def _apply_rotation(self, *_):
        if self._rot_instr is not None:
            self._rot_instr.angle = self.rotation


class SkeletonCard(MDCard):
    """A shimmering placeholder shaped like a list row (avatar circle +
    two text bars), shown while real content is still loading. Used
    instead of (or alongside) a spinner on screens with list content —
    gives users an immediate sense of the page's shape instead of a blank
    gap, and reads as more "alive" than a static spinner.

    Purely decorative — callers just add/remove instances of this widget
    from a container; it animates itself and needs no other wiring.
    """

    shimmer_alpha = NumericProperty(0.35)

    def __init__(self, **kwargs):
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', dp(72))
        kwargs.setdefault('radius', [12])
        kwargs.setdefault('elevation', 0)
        kwargs.setdefault('padding', dp(12))
        kwargs.setdefault('spacing', dp(12))
        kwargs.setdefault('orientation', 'horizontal')
        super().__init__(**kwargs)

        self.md_bg_color = [0, 0, 0, 0.04]

        avatar = Widget(size_hint=(None, None), size=(dp(40), dp(40)))
        with avatar.canvas:
            self._avatar_color = Color(0, 0, 0, self.shimmer_alpha)
            self._avatar_ellipse = Ellipse(pos=avatar.pos, size=avatar.size)
        avatar.bind(pos=self._sync_avatar, size=self._sync_avatar)
        self.add_widget(avatar)

        bars = BoxLayout(orientation='vertical', spacing=dp(8), padding=[0, dp(4), 0, dp(4)])
        self._bar_widgets = []
        for w_hint in (0.6, 0.35):
            bar = Widget(size_hint=(w_hint, None), height=dp(14))
            with bar.canvas:
                color = Color(0, 0, 0, self.shimmer_alpha)
                rect = RoundedRectangle(pos=bar.pos, size=bar.size, radius=[6])
            bar.bind(pos=lambda w, v, r=rect: setattr(r, 'pos', v),
                      size=lambda w, v, r=rect: setattr(r, 'size', v))
            self._bar_widgets.append(color)
            bars.add_widget(bar)
            bars.add_widget(Widget(size_hint_y=None, height=dp(2)))
        self.add_widget(bars)

        self.bind(shimmer_alpha=self._apply_alpha)
        self._start_shimmer()

    def _sync_avatar(self, widget, *_):
        self._avatar_ellipse.pos = widget.pos
        self._avatar_ellipse.size = widget.size

    def _apply_alpha(self, *_):
        self._avatar_color.a = self.shimmer_alpha
        for color in self._bar_widgets:
            color.a = self.shimmer_alpha

    def _start_shimmer(self, *_):
        grow = Animation(shimmer_alpha=0.12, duration=0.7, t='in_out_sine')
        shrink = Animation(shimmer_alpha=0.35, duration=0.7, t='in_out_sine')
        grow.bind(on_complete=lambda *_: shrink.start(self))
        shrink.bind(on_complete=self._start_shimmer)
        grow.start(self)

    def stop(self):
        Animation.cancel_all(self)


class GradientCard(MDCard):
    """MDCard with a real blue gradient background (instead of a flat
    md_bg_color), used for the Support Center's hero header and its
    big "AI Assistant" card so the screen matches the requested
    modern-fintech / blue-gradient design.

    If texture creation ever fails for any reason (e.g. running
    headless in a build step) it just silently keeps MDCard's normal
    flat md_bg_color instead of crashing the app.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self._gradient_tex = self._build_gradient_texture()
            self.md_bg_color = [0, 0, 0, 0]  # let the gradient show through
            with self.canvas.before:
                Color(1, 1, 1, 1)
                self._grad_rect = RoundedRectangle(
                    texture=self._gradient_tex,
                    pos=self.pos,
                    size=self.size,
                    radius=self.radius or [0],
                )
            self.bind(pos=self._update_gradient, size=self._update_gradient,
                      radius=self._update_gradient)
        except Exception as e:
            print(f"GradientCard texture error (non-fatal): {e}")

    def _build_gradient_texture(self, height=128):
        # Cheap4U primary blue (#2196F3) -> accent blue (#42A5F5), top to bottom
        stops = [(33, 150, 243), (66, 165, 245)]
        buf = bytearray(height * 4)
        for y in range(height):
            t = y / (height - 1)
            r = int(stops[0][0] + (stops[1][0] - stops[0][0]) * t)
            g = int(stops[0][1] + (stops[1][1] - stops[0][1]) * t)
            b = int(stops[0][2] + (stops[1][2] - stops[0][2]) * t)
            idx = y * 4
            buf[idx:idx + 4] = bytes([r, g, b, 255])
        tex = Texture.create(size=(1, height), colorfmt="rgba")
        tex.blit_buffer(bytes(buf), colorfmt="rgba", bufferfmt="ubyte")
        tex.wrap = "clamp_to_edge"
        return tex

    def _update_gradient(self, *_):
        if hasattr(self, '_grad_rect'):
            self._grad_rect.pos = self.pos
            self._grad_rect.size = self.size
            self._grad_rect.radius = self.radius or [0]


class LoaderWidget(FloatLayout):
    pulse_scale   = NumericProperty(1.0)
    arc_start     = NumericProperty(0)
    ripple1_scale = NumericProperty(1.0)
    ripple1_alpha = NumericProperty(0.5)
    ripple2_scale = NumericProperty(1.0)
    ripple2_alpha = NumericProperty(0.4)
    letter_alpha  = NumericProperty(1.0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._start_animations, 0.1)

    def _start_animations(self, *_):
        self._spin_arc()
        self._pulse_loop()
        self._ripple_loop()

    def _spin_arc(self, *_):
        anim = Animation(arc_start=self.arc_start + 360,
                         duration=1.1, t="linear")
        anim.bind(on_complete=self._spin_arc)
        anim.start(self)

    def _pulse_loop(self, *_):
        grow = Animation(pulse_scale=1.08, letter_alpha=1.0,
                         duration=0.75, t="in_out_sine")
        shrink = Animation(pulse_scale=0.94, letter_alpha=0.80,
                           duration=0.75, t="in_out_sine")
        grow.bind(on_complete=lambda *_: shrink.start(self))
        shrink.bind(on_complete=self._pulse_loop)
        grow.start(self)

    def _ripple_loop(self, *_):
        def _start_ring2(*_):
            self.ripple2_scale = 1.0
            self.ripple2_alpha = 0.4
            expand2 = Animation(ripple2_scale=1.30, ripple2_alpha=0.0,
                                duration=1.5, t="out_quad")
            expand2.bind(on_complete=self._ripple_loop)
            expand2.start(self)

        self.ripple1_scale = 1.0
        self.ripple1_alpha = 0.5
        expand1 = Animation(ripple1_scale=1.35, ripple1_alpha=0.0,
                            duration=1.5, t="out_quad")
        expand1.bind(on_complete=_start_ring2)
        expand1.start(self)

    def stop(self):
        Animation.cancel_all(self)
            

from monthly_challenge import ChallengeMixin, register_challenge_screens


class DashboardApp(ChallengeMixin, MDApp):

    selected_payment_method = StringProperty(None)

    selected_network = StringProperty(None)

    service_type = StringProperty(None)

    current_selected_item = ObjectProperty("", allownone=True)

    current_user = ObjectProperty("", allownone=True)

    selected_airtime_amount = NumericProperty(0)

    selected_airtime_network = StringProperty("")

    selected_cable_provider = StringProperty("")

    selected_cable_package = StringProperty("")

    selected_cable_amount = NumericProperty(0)

    selected_electricity_provider = StringProperty("")

    selected_meter_type = StringProperty("")

    selected_data_network = StringProperty("")
    a2c_step = StringProperty("input")
    a2c_network = StringProperty("")
    a2c_session_id = StringProperty("")
    a2c_airtime_balance = StringProperty("")
    terms_text = StringProperty(TERMS_OF_SERVICE_TEXT)
    privacy_text = StringProperty(PRIVACY_POLICY_TEXT)

    selected_data_plan = StringProperty("")

    selected_data_amount = StringProperty("")

    selected_network = StringProperty(None)

    service_type = StringProperty("")

    selected_data_type = StringProperty("")
    
   # new
    selected_funding_method = StringProperty("")
    funding_amount = NumericProperty(0)
    #end

    bg_normal = ListProperty([0.95, 0.95, 0.95, 1])

    bg_light = ListProperty([1, 1, 1, 1])

    primary_light = ListProperty([0.9, 0.95, 1, 1])
    
    
    selected_payment_method = StringProperty("")
    selected_network = StringProperty(None)
   

    # Provider colors

    dstv_color = ListProperty([0.9, 0.3, 0.3, 1])  # Red

    gotv_color = ListProperty([0.1, 0.6, 1, 1])     # Blue

    startimes_color = ListProperty([0.9, 0.8, 0.1, 1])  # Yellow

    showmax_color = ListProperty([0.2, 0.8, 0.5, 1])   # Green

    

    # Disco colors

    ikeja_color = ListProperty([0.9, 0.3, 0.3, 1])  # Red

    eko_color = ListProperty([0.1, 0.6, 1, 1])      # Blue

    ibadan_color = ListProperty([0.9, 0.8, 0.1, 1])  # Yellow

    enugu_color = ListProperty([0.2, 0.8, 0.5, 1])   # Green

    abuja_color = ListProperty([0.6, 0.2, 0.8, 1])   # Purple

    

    # Network colors

    mtn_color = ListProperty([0.9, 0.8, 0.1, 1])    # Yellow

    airtel_color = ListProperty([0.9, 0.3, 0.3, 1])  # Red

    glo_color = ListProperty([0.2, 0.8, 0.5, 1])    # Green

    mobile9_color = ListProperty([0.1, 0.6, 1, 1])  # Blue
    current_screen_name = StringProperty("dashboard")

    # ── Support Center / AI Chat Assistant ──────────────────────────
    support_phone = StringProperty("+2349037663816")
    support_email = StringProperty("supportcheap4u@gmail.com")
    app_version = StringProperty("1.0.0")

    ai_chat_messages = ListProperty([])       # [{'role': 'user'|'assistant', 'content': str}, ...]
    ai_chat_typing = BooleanProperty(False)
    ai_chat_session_id = StringProperty("")
    ai_search_active = BooleanProperty(False)
    ai_last_user_message = StringProperty("")

    AI_SUGGESTED_QUESTIONS = [
        "How do I buy data?",
        "My payment failed, what do I do?",
        "How does the referral program work?",
        "How do I reset my password?",
        "What is a pending transaction?",
        "How do I fund my wallet?",
    ]
    # In DashboardApp class
    virtual_account_number =   StringProperty('')
    virtual_bank_name = StringProperty('')
    virtual_account_name = StringProperty('')

    backend_url = StringProperty("")  # Will be set based on environment
    payment_processing = BooleanProperty(False)
    current_payment_reference = StringProperty("")
    selected_exam_type =  StringProperty("")
    selected_exam_quantity =  NumericProperty(0)
    exam_pin_total_amount =  NumericProperty(0)
    exam_pin_prices = DictProperty({
        "WAEC": 3800,     # Cost: 3450, Profit: 350 (10.1%)
        "NECO": 2600,     # Cost: 2350, Profit: 250 (10.6%)
        "NABTEB": 1000,   # Cost: 900,  Profit: 100 (11.1%)
        "JAMB": 16500     # Cost: 15000, Profit: 1500 (10%)
})



#started
    referral_balance = NumericProperty(0)
    total_referrals = NumericProperty(0)
    referral_code = StringProperty("")
    can_use_bonus = BooleanProperty(False)


    _loader_widget  = None
    _loader_overlay = None
    
    
    def show_loader(self, message="Processing..."):
        self.hide_loader(animated=False)
        scrim = FloatLayout(size=Window.size, pos=(0, 0))
        with scrim.canvas.before:
            Color(rgba=(0, 0, 0, 0.45))
            Rectangle(size=Window.size, pos=(0, 0))
        loader = LoaderWidget(
            size_hint=(None, None),
            pos_hint={"center_x": .5, "center_y": .5},
        )
        scrim.add_widget(loader)
        Window.add_widget(scrim)
        self._loader_widget = loader
        self._loader_overlay = scrim
        scrim.opacity = 0
        Animation(opacity=1, duration=0.25, t="out_quad").start(scrim)
        # Safety net: on a slow/flaky connection, a hung network request can
        # fail to ever call back (neither success, failure, nor error) --
        # leaving hide_loader() never called and this dark overlay stuck on
        # screen indefinitely. That looks exactly like "the app is just
        # dark/broken" on whichever device hits it. Force it away after a
        # generous timeout no matter what caused the hang.
        Clock.schedule_once(lambda dt: self._force_hide_stuck_loader(scrim), 20)

    def _force_hide_stuck_loader(self, scrim):
        if getattr(self, '_loader_overlay', None) is scrim:
            print("Loader force-hidden after 20s timeout — a request likely hung without calling back")
            self.hide_loader(animated=True)

    def hide_loader(self, animated=True):
        scrim = getattr(self, '_loader_overlay', None)
        widget = getattr(self, '_loader_widget', None)
        self._loader_overlay = None
        self._loader_widget = None
        if scrim is None:
            return
        if widget:
            try:
                widget.stop()
            except Exception:
                pass
        if not animated:
            try:
                Window.remove_widget(scrim)
            except Exception:
                pass
            return
        anim = Animation(opacity=0, duration=0.2, t="in_quad")
        anim.bind(on_complete=lambda *_: self._safe_remove(scrim))
        anim.start(scrim)

    def _safe_remove(self, widget):
        try:
            Window.remove_widget(widget)
        except Exception:
            pass

    def show_loading(self, message="Processing..."):
        """Alias so old show_loading() calls still work."""
        self.show_loader(message)
   
   
    def show_set_pin_dialog(self):
        """Show dialog to set or change transaction PIN"""
        if not self.current_user:
            self.show_error_dialog("Please login first")
            return
        
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=dp(20),
            size_hint_y=None,
            height=dp(280)
        )
        
        old_pin_input = MDTextField(
            hint_text="Current PIN leave empty if not set",
            icon_left="shield-key-outline",
            password=True,
            input_type='number',
            max_text_length=6,
            mode="rectangle"
        )
        
        new_pin_input = MDTextField(
            hint_text="New PIN (4-6 digits)",
            icon_left="shield-key-outline",
            password=True,
            input_type='number',
            max_text_length=6,
            mode="rectangle"
        )
        
        confirm_pin_input = MDTextField(
            hint_text="Confirm New PIN",
            icon_left="shield-key-outline",
            password=True,
            input_type='number',
            max_text_length=6,
            mode="rectangle"
        )
        
        content.add_widget(old_pin_input)
        content.add_widget(new_pin_input)
        content.add_widget(confirm_pin_input)
        
        dialog = MDDialog(
            title="Set Transaction PIN",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="SAVE PIN",
                    md_bg_color=self.theme_cls.primary_color,
                    on_release=lambda x: self._save_pin(
                        dialog, 
                        old_pin_input.text, 
                        new_pin_input.text, 
                        confirm_pin_input.text
                    )
                )
            ],
            radius=[20, 7, 20, 7]
        )
        dialog.open()

    def _save_pin(self, dialog, old_pin, new_pin, confirm_pin):
        """Save transaction PIN to backend"""
        dialog.dismiss()
        
        if new_pin != confirm_pin:
            self.show_error_dialog("New PINs do not match")
            return
        
        if not new_pin or len(new_pin) < 4 or len(new_pin) > 6:
            self.show_error_dialog("PIN must be 4-6 digits")
            return
        
        if not new_pin.isdigit():
            self.show_error_dialog("PIN must contain only numbers")
            return
        
        self.show_loader("Setting PIN...")
        
        payload = {'new_pin': new_pin}
        if old_pin:
            payload['old_pin'] = old_pin
        
        def on_response(req, result):
            self.hide_loader()
            if result.get('status') == 'success':
                self.show_success_dialog("Transaction PIN set successfully!")
            else:
                self.show_error_dialog(result.get('message', 'Failed to set PIN'))
        
        self.backend_api_request('auth/set-pin', 'POST', payload, on_response)    
            
   
    def verify_transaction_pin(self, on_success):
        """Show PIN entry dialog and call on_success if PIN verified."""
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=dp(20),
            size_hint_y=None,
            height=dp(150)
        )
        
        self.pin_input = MDTextField(
            hint_text="Enter 4-6 digit PIN",
            icon_left="shield-key-outline",
            password=True,
            input_type='number',
            max_text_length=6,
            mode="rectangle"
        )
        content.add_widget(self.pin_input)
        
        # Add error label
        self.pin_error_label = MDLabel(
            text="",
            theme_text_color="Error",
            size_hint_y=None,
            height=dp(30),
            opacity=0
        )
        content.add_widget(self.pin_error_label)

        self.pin_dialog = MDDialog(
            title="Transaction PIN Required",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: self._cancel_pin_verification()
                ),
                MDRaisedButton(
                    text="VERIFY",
                    md_bg_color=self.theme_cls.primary_color,
                    on_release=lambda x: self._submit_pin_verification(on_success)
                )
            ],
            radius=[20, 7, 20, 7]
        )
        self.pin_dialog.open()

    def _cancel_pin_verification(self):
        """Cancel PIN verification"""
        if hasattr(self, 'pin_dialog'):
            self.pin_dialog.dismiss()
        self.pin_error_label = None
        self.pin_input = None

    def _submit_pin_verification(self, on_success):
        pin = self.pin_input.text if self.pin_input else ""
        if not pin or len(pin) < 4:
            self._show_pin_error("PIN must be 4-6 digits")
            return
        if not pin.isdigit():
            self._show_pin_error("PIN must contain only numbers")
            return

        self.show_loader("Verifying PIN...")

        def on_response(req, result):
            self.hide_loader()
            if result.get('status') == 'success':
                if hasattr(self, 'pin_dialog') and self.pin_dialog:
                    self.pin_dialog.dismiss()
                self.verified_pin = pin
                on_success()
            else:
                self._show_pin_error(result.get('message', 'PIN verification failed'))

        def on_failure(req, error):
            self.hide_loader()
            self._show_pin_error(f"Network error: {error}")

        self.backend_api_request('auth/verify-pin', 'POST', {'pin': pin}, on_response)

    def _show_pin_error(self, message):
        """Show error message in PIN dialog"""
        if hasattr(self, 'pin_error_label'):
            self.pin_error_label.text = message
            self.pin_error_label.opacity = 1
            Clock.schedule_once(lambda dt: setattr(self.pin_error_label, 'opacity', 0), 3)

    def _clear_verified_pin(self):
        """Clear the temporarily stored PIN after transaction"""
        if hasattr(self, 'verified_pin'):
            self.verified_pin = ""

    # ── Coupon System (shared across all purchase flows) ────────────

    def _prompt_coupon_then_pin(self, category, amount, on_ready):
        """Optional 'have a coupon?' step shown before PIN verification.
        Works the same for airtime/data/electricity/cable/exam-pin — pass
        the purchase category + amount so the backend can validate the
        coupon against the right rules before the PIN dialog opens."""
        self.pending_coupon_code = None
        self.pending_coupon_category = category
        self.pending_coupon_amount = amount

        content = MDBoxLayout(
            orientation='vertical', spacing=dp(10),
            size_hint_y=None, height=dp(80), padding=dp(10),
        )
        coupon_input = MDTextField(
            hint_text="Coupon code (optional)",
            icon_left="ticket-percent-outline",
            mode="rectangle",
        )
        content.add_widget(coupon_input)

        def _skip(*_):
            dialog.dismiss()
            self.pending_coupon_code = None
            self.verify_transaction_pin(on_ready)

        def _apply(*_):
            dialog.dismiss()
            code = (coupon_input.text or "").strip()
            if not code:
                self.pending_coupon_code = None
                self.verify_transaction_pin(on_ready)
            else:
                self._validate_and_store_coupon(code, category, amount, on_ready)

        dialog = MDDialog(
            title="Have a coupon code?",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="SKIP",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=_skip,
                ),
                MDRaisedButton(
                    text="APPLY",
                    md_bg_color=self.theme_cls.primary_color,
                    on_release=_apply,
                ),
            ],
            radius=[20, 7, 20, 7],
        )
        dialog.open()

    def _validate_and_store_coupon(self, code, category, amount, on_ready):
        """Validates a coupon against the backend before proceeding to
        PIN verification. On failure, tells the user and still lets them
        continue the purchase without a discount rather than blocking them."""
        if not self.session_token:
            self.pending_coupon_code = None
            self.verify_transaction_pin(on_ready)
            return

        self.show_loader("Checking coupon...")

        def on_success(req, result):
            self.hide_loader()
            if result.get('status') == 'success':
                data = result.get('data', {})
                self.pending_coupon_code = data.get('code')
                discount = data.get('discount_amount', 0)
                self.show_success_dialog(f"Coupon applied — you save {self.format_currency(discount)}")
            else:
                self.pending_coupon_code = None
                self.show_error_dialog(result.get('message', 'Invalid or expired coupon'))
            Clock.schedule_once(lambda dt: self.verify_transaction_pin(on_ready), 0.4)

        def on_failure(req, error):
            self.hide_loader()
            self.pending_coupon_code = None
            self.verify_transaction_pin(on_ready)

        UrlRequest(
            f"{self.backend_url}/api/coupons/validate?code={code}&category={category}&amount={amount}",
            on_success=on_success,
            on_failure=on_failure,
            on_error=on_failure,
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            timeout=15,
        )

    def process_vtpass_transaction_with_referral(self, transaction_data):
        """Process VTU transaction with referral bonus check"""
        try:
            # Your existing transaction processing code...
            
            # After successful transaction, check if it's user's first transaction
            if transaction_data.get('status') == 'success':
                user_email = transaction_data.get('user_email')
                if user_email:
                    # Check if this is user's first transaction
                    user = firebase_client.get_user_by_email(user_email)
                    if user and not user.get('has_completed_first_transaction', False):
                        # Process referral bonus
                        bonus_payload = {
                            'user_email': user_email,
                            'amount': transaction_data.get('amount', 0)
                        }
                        
                        # Call referral bonus endpoint
                        requests.post(
                            f"{self.backend_url}/api/referral/process-first-transaction",
                            json=bonus_payload,
                            timeout=10
                        )
                        
        except Exception as e:
            print(f"⚠️ Referral bonus trigger failed: {str(e)}")
            # Don't fail the main transaction if referral bonus fails
    

    def load_referral_data(self):
        """Load referral data from backend using JWT auth."""
        if not self.current_user or not self.session_token:
            return

        def on_success(req, result):
            if result.get('status') == 'success':
                data = result.get('data', {})
                self.referral_balance = data.get('referral_balance', 0)
                self.referral_code = data.get('referral_code', '')
                self.can_use_bonus = data.get('can_use_bonus', False)

                if self.current_user:
                    self.current_user['referral_balance'] = self.referral_balance
                    self.current_user['referral_code'] = self.referral_code

                self.update_dashboard()

                try:
                    screen = self.root.get_screen('referral')
                    self.update_referral_ui(screen, data)
                except Exception as e:
                    print(f"Referral screen update error: {e}")

        def on_failure(req, error):
            print(f"load_referral_data failed: {error}")

        def on_error(req, error):
            print(f"load_referral_data error: {error}")

        from kivy.network.urlrequest import UrlRequest
        UrlRequest(
            f"{self.backend_url}/api/referral/info",
            on_success=on_success,
            on_failure=on_failure,
            on_error=on_error,
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            timeout=15,
        )


    def update_referral_ui(self, screen, data):
        """Update referral screen with correct bonus calculation."""
        try:
            ids = screen.ids

            # Referral code + link
            code = data.get('referral_code', '')
            if hasattr(ids, 'referral_code_label'):
                ids.referral_code_label.text = code
            if hasattr(ids, 'referral_link_label'):
                ids.referral_link_label.text = (
                    f"https://cheap4u.technology/register?ref={code}"
                )

            # Counts
            total = data.get('total_referrals', 0)
            pending = data.get('pending_referrals_count', 0)
            completed = total - pending

            if hasattr(ids, 'total_referrals_label'):
                ids.total_referrals_label.text = str(total)
            if hasattr(ids, 'pending_referrals_label'):
                ids.pending_referrals_label.text = str(pending)
            if hasattr(ids, 'completed_referrals_label'):
                ids.completed_referrals_label.text = str(completed)

            # Referral balance (actual from backend)
            balance = data.get('referral_balance', 0)
            earnings = data.get('referral_earnings', 0)

            # Show expected bonus: ₦50 × completed referrals
            expected_bonus = completed * 50.0

            if hasattr(ids, 'referral_earnings_label'):
                ids.referral_earnings_label.text = self.format_currency(balance)

            if hasattr(ids, 'expected_bonus_label'):
                ids.expected_bonus_label.text = (
                    f"₦{expected_bonus:,.2f} expected "
                    f"({completed} × ₦50)"
                )

            # Bonus info + button state
            can_use = data.get('can_use_bonus', False)
            needed = data.get('next_bonus_threshold', 0)

            if hasattr(ids, 'use_bonus_btn'):
                ids.use_bonus_btn.disabled = not can_use
                ids.use_bonus_btn.opacity = 1.0 if can_use else 0.5

            if hasattr(ids, 'bonus_info_label'):
                if can_use:
                    ids.bonus_info_label.text = (
                        f"You have ₦{balance:,.2f} referral bonus available to use!"
                    )
                elif pending > 0:
                    ids.bonus_info_label.text = (
                        f"{pending} friend(s) signed up but haven't funded wallet yet.\n"
                        f"They need to fund their wallet for you to earn ₦50 each."
                    )
                elif total == 0:
                    ids.bonus_info_label.text = (
                        "Share your referral code to earn ₦50 per friend who signs up!"
                    )
                else:
                    ids.bonus_info_label.text = (
                        f"You need ₦{needed:,.2f} more to use referral bonus."
                    )

        except Exception as e:
            print(f"update_referral_ui error: {e}")
    def copy_referral_code(self):
        """Copy referral code to clipboard."""
        code = (
            self.referral_code
            or (self.current_user.get('referral_code') if self.current_user else '')
        )
        if code:
            Clipboard.copy(code)
            self.show_success_dialog(f"Referral code copied!\n\nCode: {code}")
        else:
            self.show_error_dialog("Referral code not available. Please try again.")
            self.load_referral_data()            


    def share_referral_link(self):
        """Copy referral link to clipboard."""
        code = (
            self.referral_code
            or (self.current_user.get('referral_code') if self.current_user else '')
        )
        if not code:
            self.show_error_dialog("Referral code not available. Please try again.")
            self.load_referral_data()
            return

        link = f"https://cheap4u.technology/register?ref={code}"
        Clipboard.copy(link)
        self.show_success_dialog(
            f"Referral link copied!\n\n{link}\n\n"
            f"Share this with friends. You earn ₦50 when they sign up and fund their wallet."
        )


    def use_referral_bonus(self):
        """Show dialog to use referral bonus."""
        if not self.current_user or not self.can_use_bonus:
            self.show_error_dialog(
                "You need at least ₦200 referral bonus to use this feature."
            )
            return

        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(15),
            size_hint_y=None,
            height=dp(120),
            padding=dp(10),
        )
        amount_input = MDTextField(
            hint_text=f"Amount (max ₦{self.referral_balance:,.2f})",
            icon_left="cash",
            input_type='number',
            helper_text=f"Minimum ₦200 | Available: ₦{self.referral_balance:,.2f}",
            helper_text_mode="persistent",
            mode="rectangle",
        )
        content.add_widget(amount_input)

        dialog = MDDialog(
            title="Use Referral Bonus",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="USE BONUS",
                    md_bg_color=self.theme_cls.primary_color,
                    on_release=lambda x: self._process_bonus_usage(dialog, amount_input.text)
                )
            ],
            radius=[20, 7, 20, 7]
        )
        dialog.open()

    def _process_bonus_usage(self, dialog, amount_text):
        """Process the bonus usage after user confirms amount."""
        dialog.dismiss()

        try:
            amount = float(amount_text.replace('₦', '').replace(',', '').strip())
        except (ValueError, AttributeError):
            self.show_error_dialog("Invalid amount entered")
            return

        if amount < 200:
            self.show_error_dialog("Minimum bonus usage is ₦200")
            return

        if amount > self.referral_balance:
            self.show_error_dialog(
                f"Amount exceeds available balance (₦{self.referral_balance:,.2f})"
            )
            return

        self.show_loader("Processing bonus...")

        payload = {
            'user_email': self.current_user.get('email'),
            'amount': amount,
        }

        def on_success(req, result):
            self.hide_loader()
            if result.get('status') == 'success':
                data = result.get('data', {})
                # Update local balances
                if self.current_user:
                    self.current_user['wallet_balance'] = data.get('wallet_balance', 0)
                    self.current_user['referral_balance'] = data.get('referral_balance', 0)
                self.referral_balance = data.get('referral_balance', 0)
                self.update_dashboard()
                self.load_referral_data()
                self.show_success_dialog(
                    f"₦{amount:,.2f} added to your wallet from referral bonus!"
                )
            else:
                self.show_error_dialog(result.get('message', 'Failed to use bonus'))

        def on_failure(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Network error: {error}")

        def on_error(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Connection error: {error}")

        UrlRequest(
            f"{self.backend_url}/api/referral/use-bonus",
            on_success=on_success,
            on_failure=on_failure,
            on_error=on_error,
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            req_body=json.dumps(payload),
            timeout=15,
        )

    def show_referral_screen(self):
        """Navigate to referral screen and load fresh data."""
        if not self.current_user or not self.session_token:
            self.show_error_dialog("Please login to access the referral program")
            self.root.current = "login"
            return
        self.root.current = "referral"
        Clock.schedule_once(lambda dt: self.load_referral_data(), 0.3)             
    


    # ── Cashback System ──────────────────────────────────────────────

    def show_cashback_screen(self):
        """Navigate to the cashback screen and load fresh data."""
        if not self.current_user or not self.session_token:
            self.show_error_dialog("Please login to view your cashback")
            self.root.current = "login"
            return
        self.root.current = "cashback"
        Clock.schedule_once(lambda dt: self.load_cashback_data(), 0.3)

    def load_cashback_data(self):
        """Load cashback wallet summary + recent history from backend."""
        if not self.current_user or not self.session_token:
            return

        self.cashback_wallet = getattr(self, 'cashback_wallet', {}) or {}

        def on_wallet_success(req, result):
            if result.get('status') == 'success':
                self.cashback_wallet = result.get('data', {})
                try:
                    screen = self.root.get_screen('cashback')
                    self.update_cashback_ui(screen, self.cashback_wallet)
                except Exception as e:
                    print(f"Cashback screen update error: {e}")

        def on_failure(req, error):
            print(f"load_cashback_data failed: {error}")

        def on_error(req, error):
            print(f"load_cashback_data error: {error}")

        UrlRequest(
            f"{self.backend_url}/api/cashback/wallet",
            on_success=on_wallet_success,
            on_failure=on_failure,
            on_error=on_error,
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            timeout=15,
        )

        def on_history_success(req, result):
            if result.get('status') == 'success':
                entries = result.get('data', {}).get('entries', [])
                try:
                    screen = self.root.get_screen('cashback')
                    self.update_cashback_history_ui(screen, entries)
                except Exception as e:
                    print(f"Cashback history render error: {e}")

        UrlRequest(
            f"{self.backend_url}/api/cashback/history?per_page=20",
            on_success=on_history_success,
            on_failure=lambda req, error: print(f"cashback history failed: {error}"),
            on_error=lambda req, error: print(f"cashback history error: {error}"),
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            timeout=15,
        )

    def update_cashback_ui(self, screen, data):
        """Update the cashback screen's balance/stats/redeem-button state."""
        try:
            ids = screen.ids

            balance = data.get('balance', 0)
            if hasattr(ids, 'cashback_balance_label'):
                ids.cashback_balance_label.text = self.format_currency(balance)

            expiring_soon = data.get('expiring_soon', 0)
            next_expiry = data.get('next_expiry_date')
            if hasattr(ids, 'cashback_expiring_label'):
                if expiring_soon and expiring_soon > 0:
                    when = ""
                    if next_expiry:
                        try:
                            dt = datetime.fromisoformat(next_expiry.replace('Z', ''))
                            when = f" by {dt.strftime('%b %d')}"
                        except Exception:
                            pass
                    ids.cashback_expiring_label.text = (
                        f"₦{expiring_soon:,.2f} expiring soon{when}"
                    )
                else:
                    ids.cashback_expiring_label.text = "Cashback earned on every purchase"

            if hasattr(ids, 'cashback_total_earned_label'):
                ids.cashback_total_earned_label.text = self.format_currency(data.get('total_earned', 0))
            if hasattr(ids, 'cashback_total_redeemed_label'):
                ids.cashback_total_redeemed_label.text = self.format_currency(data.get('total_redeemed', 0))
            if hasattr(ids, 'cashback_total_expired_label'):
                ids.cashback_total_expired_label.text = self.format_currency(data.get('total_expired', 0))

            can_redeem = data.get('can_redeem', False)
            if hasattr(ids, 'cashback_redeem_btn'):
                ids.cashback_redeem_btn.disabled = not can_redeem
                ids.cashback_redeem_btn.opacity = 1.0 if can_redeem else 0.6

        except Exception as e:
            print(f"update_cashback_ui error: {e}")

    def update_cashback_history_ui(self, screen, entries):
        """Populate the cashback screen's recent-activity list."""
        try:
            ids = screen.ids
            if not hasattr(ids, 'cashback_history_list'):
                return

            history_list = ids.cashback_history_list
            history_list.clear_widgets()

            if not entries:
                if hasattr(ids, 'cashback_history_empty_label'):
                    ids.cashback_history_empty_label.text = "No activity yet"
                return

            if hasattr(ids, 'cashback_history_empty_label'):
                ids.cashback_history_empty_label.text = ""

            type_labels = {
                'earned':       ('Cashback earned', [0.1, 0.75, 0.35, 1], '+'),
                'redeemed':     ('Moved to wallet', [0.9, 0.5, 0.1, 1], '-'),
                'expired':      ('Cashback expired', [0.8, 0.2, 0.2, 1], '-'),
                'admin_credit': ('Bonus credit', [0.1, 0.75, 0.35, 1], '+'),
                'admin_debit':  ('Adjustment', [0.8, 0.2, 0.2, 1], '-'),
            }

            for entry in entries:
                etype = entry.get('type', '')
                label, color, sign = type_labels.get(etype, (etype.title(), [0.4, 0.4, 0.4, 1], ''))
                category = entry.get('category')
                subtitle = category.replace('_', ' ').title() if category else (entry.get('note') or '')

                created_at = entry.get('created_at') or ''
                date_str = ''
                if created_at:
                    try:
                        dt = datetime.fromisoformat(created_at.replace('Z', ''))
                        date_str = dt.strftime('%b %d, %Y %I:%M %p')
                    except Exception:
                        date_str = created_at

                item = TwoLineListItem(
                    text=f"{label}   {sign}{self.format_currency(entry.get('amount', 0))}",
                    secondary_text=f"{subtitle} • {date_str}" if subtitle else date_str,
                    theme_text_color="Custom",
                    text_color=color,
                    secondary_text_color=[0.5, 0.5, 0.5, 1],
                )
                history_list.add_widget(item)

        except Exception as e:
            print(f"update_cashback_history_ui error: {e}")

    def redeem_cashback(self):
        """Show a confirm dialog and move the cashback balance into the main wallet."""
        wallet = getattr(self, 'cashback_wallet', {}) or {}
        balance = wallet.get('balance', 0)

        if not balance or balance <= 0:
            self.show_error_dialog("You have no cashback balance to redeem.")
            return

        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(15),
            size_hint_y=None,
            height=dp(120),
            padding=dp(10),
        )
        amount_input = MDTextField(
            hint_text=f"Amount (max {self.format_currency(balance)})",
            icon_left="cash",
            input_type='number',
            text=f"{balance:.2f}",
            helper_text=f"Available: {self.format_currency(balance)}",
            helper_text_mode="persistent",
            mode="rectangle",
        )
        content.add_widget(amount_input)

        dialog = MDDialog(
            title="Move Cashback to Wallet",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="REDEEM",
                    md_bg_color=self.theme_cls.primary_color,
                    on_release=lambda x: self._process_cashback_redeem(dialog, amount_input.text)
                )
            ],
            radius=[20, 7, 20, 7]
        )
        dialog.open()

    def _process_cashback_redeem(self, dialog, amount_text):
        """Send the redeem request after the user confirms the amount."""
        dialog.dismiss()

        try:
            amount = float(str(amount_text).replace('₦', '').replace(',', '').strip())
        except (ValueError, AttributeError):
            self.show_error_dialog("Invalid amount entered")
            return

        if amount <= 0:
            self.show_error_dialog("Amount must be greater than zero")
            return

        self.show_loader("Moving cashback to wallet...")

        def on_success(req, result):
            self.hide_loader()
            if result.get('status') == 'success':
                data = result.get('data', {})
                if self.current_user:
                    self.current_user['wallet_balance'] = data.get('wallet_balance', 0)
                self.update_dashboard()
                self.load_cashback_data()
                self.show_success_dialog(result.get('message', 'Cashback moved to your wallet!'))
            else:
                self.show_error_dialog(result.get('message', 'Failed to redeem cashback'))

        def on_failure(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Network error: {error}")

        def on_error(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Connection error: {error}")

        UrlRequest(
            f"{self.backend_url}/api/cashback/redeem",
            on_success=on_success,
            on_failure=on_failure,
            on_error=on_error,
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            req_body=json.dumps({'amount': amount}),
            timeout=15,
        )


    # ── Spin & Win ────────────────────────────────────────────────────

    def show_spin_screen(self):
        """Navigate to the Spin & Win screen and load fresh data."""
        if not self.current_user or not self.session_token:
            self.show_error_dialog("Please login to play Spin & Win")
            self.root.current = "login"
            return
        self.root.current = "spin"
        self.spin_in_progress = False
        Clock.schedule_once(lambda dt: self.load_spin_data(), 0.3)

    def load_spin_data(self):
        """Load the wheel layout, today's spin status, and recent history."""
        if not self.current_user or not self.session_token:
            return

        self.spin_segments = getattr(self, 'spin_segments', []) or []

        def on_segments_success(req, result):
            if result.get('status') == 'success':
                self.spin_segments = result.get('data', [])
                try:
                    screen = self.root.get_screen('spin')
                    if hasattr(screen.ids, 'spin_wheel'):
                        screen.ids.spin_wheel.set_segments(self.spin_segments)
                    self.update_spin_legend(screen, self.spin_segments)
                except Exception as e:
                    print(f"Spin wheel render error: {e}")

        UrlRequest(
            f"{self.backend_url}/api/spin/segments",
            on_success=on_segments_success,
            on_failure=lambda req, error: print(f"spin segments failed: {error}"),
            on_error=lambda req, error: print(f"spin segments error: {error}"),
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            timeout=15,
        )

        def on_status_success(req, result):
            if result.get('status') == 'success':
                self.spin_status = result.get('data', {})
                try:
                    screen = self.root.get_screen('spin')
                    self.update_spin_status_ui(screen, self.spin_status)
                except Exception as e:
                    print(f"Spin status render error: {e}")

        UrlRequest(
            f"{self.backend_url}/api/spin/status",
            on_success=on_status_success,
            on_failure=lambda req, error: print(f"spin status failed: {error}"),
            on_error=lambda req, error: print(f"spin status error: {error}"),
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            timeout=15,
        )

        self._load_spin_history()

    def _load_spin_history(self):
        def on_success(req, result):
            if result.get('status') == 'success':
                entries = result.get('data', {}).get('entries', [])
                try:
                    screen = self.root.get_screen('spin')
                    self.update_spin_history_ui(screen, entries)
                except Exception as e:
                    print(f"Spin history render error: {e}")

        UrlRequest(
            f"{self.backend_url}/api/spin/history?per_page=15",
            on_success=on_success,
            on_failure=lambda req, error: print(f"spin history failed: {error}"),
            on_error=lambda req, error: print(f"spin history error: {error}"),
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            timeout=15,
        )

    def update_spin_status_ui(self, screen, status_data):
        """Update the free-spins/cost label and enable/disable the button."""
        try:
            ids = screen.ids
            can_spin = status_data.get('can_spin', False)
            free_remaining = status_data.get('free_spins_remaining', 0)
            can_spin_paid = status_data.get('can_spin_paid', False)
            cost = status_data.get('extra_spin_cost', 0)

            if hasattr(ids, 'spin_status_label'):
                if not status_data.get('spin_enabled', True):
                    ids.spin_status_label.text = "Spin & Win is currently unavailable"
                elif free_remaining > 0:
                    ids.spin_status_label.text = f"{free_remaining} free spin(s) left today"
                elif can_spin_paid:
                    ids.spin_status_label.text = "No free spins left — spin again for a fee"
                else:
                    ids.spin_status_label.text = "You've used all your spins today. Come back tomorrow!"

            if hasattr(ids, 'spin_cost_label'):
                if free_remaining <= 0 and can_spin_paid:
                    ids.spin_cost_label.text = f"Extra spin costs {self.format_currency(cost)}"
                else:
                    ids.spin_cost_label.text = ""

            if hasattr(ids, 'spin_button'):
                ids.spin_button.disabled = not can_spin or getattr(self, 'spin_in_progress', False)
                ids.spin_button.opacity = 1.0 if (can_spin and not getattr(self, 'spin_in_progress', False)) else 0.6

        except Exception as e:
            print(f"update_spin_status_ui error: {e}")

    def update_spin_legend(self, screen, segments):
        """Show a colored-dot legend of possible prizes below the wheel."""
        try:
            ids = screen.ids
            if not hasattr(ids, 'spin_legend_box'):
                return
            box = ids.spin_legend_box
            box.clear_widgets()

            for seg in segments:
                row = MDBoxLayout(orientation='horizontal', spacing=dp(10),
                                   size_hint_y=None, height=dp(24))
                dot = MDIcon(icon="circle", size_hint=(None, None), size=(dp(20), dp(20)))
                try:
                    hexc = (seg.get('color') or '#2196F3').lstrip('#')
                    r = int(hexc[0:2], 16) / 255.0
                    g = int(hexc[2:4], 16) / 255.0
                    b = int(hexc[4:6], 16) / 255.0
                    dot.theme_text_color = "Custom"
                    dot.text_color = [r, g, b, 1]
                except Exception:
                    pass
                label = MDLabel(text=seg.get('label', ''), font_style="Body2")
                row.add_widget(dot)
                row.add_widget(label)
                box.add_widget(row)
        except Exception as e:
            print(f"update_spin_legend error: {e}")

    def update_spin_history_ui(self, screen, entries):
        """Populate the Spin & Win screen's recent-wins list."""
        try:
            ids = screen.ids
            if not hasattr(ids, 'spin_history_list'):
                return
            history_list = ids.spin_history_list
            history_list.clear_widgets()

            if not entries:
                history_list.add_widget(TwoLineListItem(
                    text="No spins yet", secondary_text="Spin the wheel to see your wins here",
                ))
                return

            for entry in entries:
                created_at = entry.get('created_at') or ''
                date_str = created_at
                try:
                    dt = datetime.fromisoformat(created_at.replace('Z', ''))
                    date_str = dt.strftime('%b %d, %Y %I:%M %p')
                except Exception:
                    pass

                kind = "Free spin" if entry.get('is_free_spin') else f"Paid spin ({self.format_currency(entry.get('cost_paid', 0))})"
                item = TwoLineListItem(
                    text=entry.get('label', ''),
                    secondary_text=f"{kind} • {date_str}",
                )
                history_list.add_widget(item)
        except Exception as e:
            print(f"update_spin_history_ui error: {e}")

    def show_spin_history(self):
        """Refresh recent wins (the list already lives on the spin screen)."""
        self._load_spin_history()

    def perform_spin(self):
        """Call the backend to resolve a spin, then animate the wheel to
        land on the winning segment before showing the reward dialog."""
        if getattr(self, 'spin_in_progress', False):
            return
        if not self.current_user or not self.session_token:
            self.show_error_dialog("Please login to play Spin & Win")
            return

        self.spin_in_progress = True
        try:
            screen = self.root.get_screen('spin')
            if hasattr(screen.ids, 'spin_button'):
                screen.ids.spin_button.disabled = True
                screen.ids.spin_button.opacity = 0.6
        except Exception:
            pass

        def on_success(req, result):
            if result.get('status') == 'success':
                self._animate_spin_result(result.get('data', {}))
            else:
                self.spin_in_progress = False
                self._restore_spin_button()
                self.show_error_dialog(result.get('message', 'Unable to spin right now'))

        def on_failure(req, error):
            self.spin_in_progress = False
            self._restore_spin_button()
            self.show_error_dialog(f"Network error: {error}")

        def on_error(req, error):
            self.spin_in_progress = False
            self._restore_spin_button()
            self.show_error_dialog(f"Connection error: {error}")

        UrlRequest(
            f"{self.backend_url}/api/spin/spin",
            on_success=on_success,
            on_failure=on_failure,
            on_error=on_error,
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            req_body=json.dumps({}),
            timeout=20,
        )

    def _restore_spin_button(self):
        try:
            screen = self.root.get_screen('spin')
            if hasattr(screen.ids, 'spin_button'):
                screen.ids.spin_button.disabled = False
                screen.ids.spin_button.opacity = 1.0
        except Exception:
            pass

    def _animate_spin_result(self, data):
        """Spins the wheel widget several full rotations and lands exactly
        on the winning segment under the fixed top pointer, then shows the
        reward once the animation finishes."""
        try:
            screen = self.root.get_screen('spin')
            wheel = screen.ids.spin_wheel
        except Exception as e:
            print(f"spin wheel lookup failed: {e}")
            self.spin_in_progress = False
            self._on_spin_animation_done(data)
            return

        segments = data.get('wheel_segments') or self.spin_segments or []
        winning_id = data.get('segment_id')
        index = 0
        for i, seg in enumerate(segments):
            if seg.get('id') == winning_id:
                index = i
                break
        n = max(1, len(segments))
        sweep = 360.0 / n

        # Pointer is fixed at the top (90°). After rotating by R degrees,
        # segment `index`'s center sits at (index*sweep + sweep/2 + R) mod 360.
        # Solve for R so that lands on 90°, then add extra full turns for effect.
        target_offset = (90 - (index * sweep + sweep / 2)) % 360
        current = wheel.rotation % 360
        extra_turns = random.randint(4, 6) * 360
        target_rotation = wheel.rotation - current + extra_turns + target_offset
        if target_rotation <= wheel.rotation:
            target_rotation += 360

        anim = Animation(rotation=target_rotation, duration=3.5, transition='out_quart')
        anim.bind(on_complete=lambda *_: self._on_spin_animation_done(data))
        anim.start(wheel)

    def _on_spin_animation_done(self, data):
        self.spin_in_progress = False
        self._restore_spin_button()

        if self.current_user:
            self.current_user['wallet_balance'] = data.get('wallet_balance', 0)
        self.update_dashboard()
        self.load_spin_data()

        label = data.get('label', 'Prize')
        value = data.get('reward_value', 0)
        reward_type = data.get('reward_type', '')

        if value and value > 0:
            if reward_type == 'coupon' and data.get('coupon_code'):
                message = f"You won {label}!\nCoupon code: {data.get('coupon_code')}"
            else:
                message = f"You won {label}!"
            self.show_success_dialog(message)
        else:
            self.show_success_dialog("Better luck next time! Come back for your next spin.")

    # ── Coupon System ────────────────────────────────────────────────

    def show_coupon_screen(self):
        """Navigate to the My Coupons screen and load fresh data."""
        if not self.current_user or not self.session_token:
            self.show_error_dialog("Please login to view your coupons")
            self.root.current = "login"
            return
        self.root.current = "coupons"
        Clock.schedule_once(lambda dt: self.load_coupon_data(), 0.3)

    def load_coupon_data(self):
        """Load coupons personally awarded to this user (referral rewards,
        spin wins, etc.) from both the coupon system and Spin & Win."""
        if not self.current_user or not self.session_token:
            return

        collected = []

        def render_if_ready():
            try:
                screen = self.root.get_screen('coupons')
                self.update_coupon_list_ui(screen, collected)
            except Exception as e:
                print(f"Coupon list render error: {e}")

        def on_coupons_success(req, result):
            if result.get('status') == 'success':
                for c in result.get('data', []):
                    collected.append({
                        'code': c.get('code'),
                        'discount_type': c.get('discount_type', 'fixed'),
                        'discount_value': c.get('discount_value', 0),
                        'expires_at': c.get('expires_at'),
                        'source': 'Personal offer',
                    })
            render_if_ready()

        UrlRequest(
            f"{self.backend_url}/api/coupons/my-coupons",
            on_success=on_coupons_success,
            on_failure=lambda req, error: render_if_ready(),
            on_error=lambda req, error: render_if_ready(),
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            timeout=15,
        )

        def on_spin_coupons_success(req, result):
            if result.get('status') == 'success':
                for c in result.get('data', []):
                    if not c.get('is_used'):
                        collected.append({
                            'code': c.get('code'),
                            'discount_type': 'fixed',
                            'discount_value': c.get('discount_amount', 0),
                            'expires_at': c.get('expires_at'),
                            'source': 'Spin & Win prize',
                        })
            render_if_ready()

        UrlRequest(
            f"{self.backend_url}/api/spin/coupons",
            on_success=on_spin_coupons_success,
            on_failure=lambda req, error: render_if_ready(),
            on_error=lambda req, error: render_if_ready(),
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            timeout=15,
        )

    def update_coupon_list_ui(self, screen, coupons):
        """Populate the My Coupons list. Called after both sources have
        responded (or failed) so the list only renders once, complete."""
        try:
            ids = screen.ids
            if not hasattr(ids, 'coupon_list'):
                return

            coupon_list = ids.coupon_list
            coupon_list.clear_widgets()

            if not coupons:
                if hasattr(ids, 'coupon_empty_label'):
                    ids.coupon_empty_label.text = "No personal coupons yet — win one from Spin & Win!"
                return

            if hasattr(ids, 'coupon_empty_label'):
                ids.coupon_empty_label.text = ""

            for c in coupons:
                if c.get('discount_type') == 'percentage':
                    discount_text = f"{c.get('discount_value', 0):.0f}% off"
                else:
                    discount_text = f"{self.format_currency(c.get('discount_value', 0))} off"

                expiry_text = ""
                if c.get('expires_at'):
                    try:
                        dt = datetime.fromisoformat(c['expires_at'].replace('Z', ''))
                        expiry_text = f" • Expires {dt.strftime('%b %d, %Y')}"
                    except Exception:
                        pass

                item = TwoLineListItem(
                    text=f"{c.get('code', '')}  —  {discount_text}",
                    secondary_text=f"{c.get('source', '')}{expiry_text}",
                    on_release=lambda x, code=c.get('code'): self._copy_coupon_code(code),
                )
                coupon_list.add_widget(item)
        except Exception as e:
            print(f"update_coupon_list_ui error: {e}")

    def _copy_coupon_code(self, code):
        if not code:
            return
        Clipboard.copy(code)
        self.show_success_dialog(f"Coupon code {code} copied — paste it at checkout")

    # ── Merchant Dashboard ────────────────────────────────────────────

    def show_merchant_screen(self):
        """Navigate to the Merchant Dashboard and load fresh data."""
        if not self.current_user or not self.session_token:
            self.show_error_dialog("Please login to access the Merchant Dashboard")
            self.root.current = "login"
            return
        self.root.current = "merchant"
        self.merchant_business_type = 'individual'
        self.merchant_job_type = 'airtime'

        # The apply/status/dashboard sections are all statically defined in
        # KV (so their MDTextFields etc. exist and can be looked up via
        # ids), which means all three are present in the tree at once
        # until _render_merchant_sections picks the right one. Detach them
        # immediately so nothing overlaps while the profile is loading.
        try:
            screen = self.root.get_screen('merchant')
            for box_id in ('merchant_apply_box', 'merchant_status_box', 'merchant_dashboard_box'):
                box = screen.ids.get(box_id)
                if box and box.parent:
                    box.parent.remove_widget(box)
        except Exception as e:
            print(f"show_merchant_screen cleanup error: {e}")

        Clock.schedule_once(lambda dt: self.load_merchant_data(), 0.3)

    def load_merchant_data(self):
        """Load the merchant profile and, if approved, the dashboard data."""
        if not self.current_user or not self.session_token:
            return

        def on_success(req, result):
            if result.get('status') != 'success':
                return
            self.merchant_profile = result.get('data')
            try:
                screen = self.root.get_screen('merchant')
                self._render_merchant_sections(screen, self.merchant_profile)
            except Exception as e:
                print(f"Merchant screen render error: {e}")

        UrlRequest(
            f"{self.backend_url}/api/merchant/profile",
            on_success=on_success,
            on_failure=lambda req, error: print(f"merchant profile failed: {error}"),
            on_error=lambda req, error: print(f"merchant profile error: {error}"),
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            timeout=15,
        )

    def _render_merchant_sections(self, screen, profile):
        """Show exactly one of: apply form / pending-or-suspended banner /
        full dashboard, based on the merchant profile's current status.

        Sections are added/removed from the container entirely (not just
        collapsed to height 0) — collapsing a box that still contains live
        MDTextFields left their layout/touch targets in an inconsistent
        state on some devices, which is why typing into the apply form
        could silently fail. Fully detaching the inactive sections avoids
        that class of bug altogether."""
        try:
            ids = screen.ids
            container = ids.merchant_sections_container
            apply_box = ids.merchant_apply_box
            status_box = ids.merchant_status_box
            dash_box = ids.merchant_dashboard_box

            for box in (apply_box, status_box, dash_box):
                if box.parent:
                    box.parent.remove_widget(box)

            status = (profile or {}).get('status')

            if not profile or status == 'rejected':
                container.add_widget(apply_box)
                if hasattr(ids, 'merchant_rejection_label'):
                    reason = (profile or {}).get('rejection_reason')
                    ids.merchant_rejection_label.text = (
                        f"Your previous application was declined: {reason}\nYou can re-apply below."
                        if status == 'rejected' else ""
                    )

            elif status == 'pending':
                container.add_widget(status_box)
                if hasattr(ids, 'merchant_status_label'):
                    ids.merchant_status_label.text = (
                        "Your merchant application is under review.\n"
                        "We'll notify you once it's approved."
                    )

            elif status == 'suspended':
                container.add_widget(status_box)
                if hasattr(ids, 'merchant_status_label'):
                    reason = (profile or {}).get('rejection_reason')
                    ids.merchant_status_label.text = (
                        f"Your merchant account is currently suspended.\n{reason or ''}"
                    )

            elif status == 'approved':
                container.add_widget(dash_box)
                self._load_merchant_dashboard_data(screen)

        except Exception as e:
            print(f"_render_merchant_sections error: {e}")

    def set_merchant_business_type(self, business_type):
        self.merchant_business_type = business_type
        try:
            screen = self.root.get_screen('merchant')
            ids = screen.ids
            is_individual = business_type == 'individual'
            ids.merchant_type_individual_btn.md_bg_color = (
                self.theme_cls.primary_color if is_individual else [0, 0, 0, 0])
            ids.merchant_type_registered_btn.md_bg_color = (
                self.theme_cls.primary_color if not is_individual else [0, 0, 0, 0])
        except Exception as e:
            print(f"set_merchant_business_type error: {e}")

    def submit_merchant_application(self):
        try:
            screen = self.root.get_screen('merchant')
            ids = screen.ids
            business_name = ids.merchant_business_name.text.strip()
            if not business_name:
                self.show_error_dialog("Business name is required")
                return

            payload = {
                'business_name': business_name,
                'business_type': getattr(self, 'merchant_business_type', 'individual'),
                'registration_number': ids.merchant_registration_number.text.strip(),
                'business_address': ids.merchant_business_address.text.strip(),
                'business_phone': ids.merchant_business_phone.text.strip(),
            }
        except Exception as e:
            self.show_error_dialog(f"Please check the form: {e}")
            return

        self.show_loader("Submitting application...")

        def on_success(req, result):
            self.hide_loader()
            if result.get('status') == 'success':
                self.show_success_dialog("Application submitted! We'll review it shortly.")
                self.load_merchant_data()
            else:
                self.show_error_dialog(result.get('message', 'Application failed'))

        def on_failure(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Network error: {error}")

        UrlRequest(
            f"{self.backend_url}/api/merchant/apply",
            on_success=on_success,
            on_failure=on_failure,
            on_error=on_failure,
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            req_body=json.dumps(payload),
            timeout=15,
        )

    def _load_merchant_dashboard_data(self, screen):
        # Wallet
        def on_wallet(req, result):
            if result.get('status') == 'success' and hasattr(screen.ids, 'merchant_wallet_label'):
                bal = result.get('data', {}).get('wallet_balance', 0)
                screen.ids.merchant_wallet_label.text = self.format_currency(bal)

        UrlRequest(
            f"{self.backend_url}/api/merchant/wallet",
            on_success=on_wallet,
            on_failure=lambda req, error: None, on_error=lambda req, error: None,
            req_headers={'Authorization': f'Bearer {self.session_token}'}, timeout=15,
        )

        # Profit analytics
        def on_profit(req, result):
            if result.get('status') == 'success':
                data = result.get('data', {})
                if hasattr(screen.ids, 'merchant_profit_label'):
                    screen.ids.merchant_profit_label.text = f"Total profit: {self.format_currency(data.get('total_profit', 0))}"
                if hasattr(screen.ids, 'merchant_profit_breakdown_label'):
                    parts = [f"{c['category']}: {self.format_currency(c['profit'])}" for c in data.get('by_category', [])]
                    screen.ids.merchant_profit_breakdown_label.text = " • ".join(parts)

        UrlRequest(
            f"{self.backend_url}/api/merchant/analytics/profit",
            on_success=on_profit,
            on_failure=lambda req, error: None, on_error=lambda req, error: None,
            req_headers={'Authorization': f'Bearer {self.session_token}'}, timeout=15,
        )

        # Recent bulk jobs
        def on_jobs(req, result):
            if result.get('status') == 'success':
                jobs = result.get('data', {}).get('jobs', [])
                self._render_merchant_job_list(screen, jobs)

        UrlRequest(
            f"{self.backend_url}/api/merchant/bulk/jobs?per_page=15",
            on_success=on_jobs,
            on_failure=lambda req, error: None, on_error=lambda req, error: None,
            req_headers={'Authorization': f'Bearer {self.session_token}'}, timeout=15,
        )

    def _render_merchant_job_list(self, screen, jobs):
        try:
            if not hasattr(screen.ids, 'merchant_job_list'):
                return
            job_list = screen.ids.merchant_job_list
            job_list.clear_widgets()

            if not jobs:
                job_list.add_widget(TwoLineListItem(text="No bulk jobs yet",
                                                      secondary_text="Submit a batch above to get started"))
                return

            for j in jobs:
                status_text = j.get('status', '').replace('_', ' ').title()
                item = TwoLineListItem(
                    text=f"{j.get('job_type', '').title()} — {j.get('success_count', 0)}/{j.get('total_items', 0)} succeeded",
                    secondary_text=f"{status_text} • {self.format_currency(j.get('total_amount_charged', 0))} charged",
                )
                job_list.add_widget(item)
        except Exception as e:
            print(f"_render_merchant_job_list error: {e}")

    MERCHANT_FORMAT_HINTS = {
        'airtime':     "One per line: network,phone,amount",
        'data':        "One per line: plan_id,phone",
        'electricity': "One per line: disco,meter_number,meter_type,amount,phone",
        'cable_tv':    "One per line: plan_id,smartcard",
        'exam_pin':    "One per line: exam_name,quantity,selling_price",
    }

    def set_merchant_job_type(self, job_type):
        self.merchant_job_type = job_type
        try:
            screen = self.root.get_screen('merchant')
            ids = screen.ids
            buttons = {
                'airtime': ids.merchant_type_airtime_btn,
                'data': ids.merchant_type_data_btn,
                'electricity': ids.merchant_type_electricity_btn,
                'cable_tv': ids.merchant_type_cable_btn,
                'exam_pin': ids.merchant_type_exam_btn,
            }
            for key, btn in buttons.items():
                btn.md_bg_color = self.theme_cls.primary_color if key == job_type else [0, 0, 0, 0]
            if hasattr(ids, 'merchant_format_hint_label'):
                ids.merchant_format_hint_label.text = self.MERCHANT_FORMAT_HINTS.get(job_type, "")
        except Exception as e:
            print(f"set_merchant_job_type error: {e}")

    def _parse_merchant_bulk_lines(self, job_type, text):
        """Turns pasted CSV-style lines into the item dicts each bulk
        endpoint expects. Returns (items, errors) — errors are line-level
        so the merchant can fix just the bad rows."""
        items, errors = [], []
        lines = [ln.strip() for ln in (text or "").splitlines() if ln.strip()]

        for i, line in enumerate(lines, start=1):
            parts = [p.strip() for p in line.split(',')]
            try:
                if job_type == 'airtime':
                    network, phone, amount = parts[0], parts[1], parts[2]
                    items.append({'network': network, 'phone': phone, 'amount': float(amount)})
                elif job_type == 'data':
                    plan_id, phone = parts[0], parts[1]
                    items.append({'plan_id': plan_id, 'phone': phone})
                elif job_type == 'electricity':
                    disco, meter_number, meter_type, amount, phone = parts[0], parts[1], parts[2], parts[3], parts[4]
                    items.append({'disco': disco, 'meter_number': meter_number, 'meter_type': meter_type,
                                  'amount': float(amount), 'phone': phone})
                elif job_type == 'cable_tv':
                    plan_id, smartcard = parts[0], parts[1]
                    items.append({'plan_id': plan_id, 'smartcard': smartcard})
                elif job_type == 'exam_pin':
                    exam_name, quantity, selling_price = parts[0], parts[1], parts[2]
                    items.append({'exam_name': exam_name, 'quantity': int(quantity), 'selling_price': float(selling_price)})
            except (IndexError, ValueError):
                errors.append(f"Line {i}: invalid format — {line}")

        return items, errors

    def submit_merchant_bulk_job(self):
        job_type = getattr(self, 'merchant_job_type', 'airtime')
        try:
            screen = self.root.get_screen('merchant')
            raw_text = screen.ids.merchant_bulk_input.text
        except Exception:
            raw_text = ""

        items, errors = self._parse_merchant_bulk_lines(job_type, raw_text)
        if errors:
            self.show_error_dialog("Fix these lines and try again:\n" + "\n".join(errors[:5]))
            return
        if not items:
            self.show_error_dialog("Add at least one line before submitting")
            return

        endpoint_map = {
            'airtime': 'bulk/airtime', 'data': 'bulk/data', 'electricity': 'bulk/electricity',
            'cable_tv': 'bulk/cable-tv', 'exam_pin': 'bulk/exam-pin',
        }
        self.show_loader(f"Processing {len(items)} item(s)...")

        def on_success(req, result):
            self.hide_loader()
            if result.get('status') == 'success':
                job = result.get('data', {})
                self.show_success_dialog(
                    f"Batch complete: {job.get('success_count', 0)}/{job.get('total_items', 0)} succeeded\n"
                    f"Charged: {self.format_currency(job.get('total_amount_charged', 0))}"
                )
                try:
                    screen.ids.merchant_bulk_input.text = ""
                except Exception:
                    pass
                self.load_merchant_data()
            else:
                self.show_error_dialog(result.get('message', 'Bulk job failed'))

        def on_failure(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Network error: {error}")

        UrlRequest(
            f"{self.backend_url}/api/merchant/{endpoint_map[job_type]}",
            on_success=on_success,
            on_failure=on_failure,
            on_error=on_failure,
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            req_body=json.dumps({'items': items}),
            timeout=60,
        )

    def regenerate_merchant_api_key(self):
        self.show_loader("Generating API key...")

        def on_success(req, result):
            self.hide_loader()
            if result.get('status') == 'success':
                key = result.get('data', {}).get('api_key', '')
                Clipboard.copy(key)
                self.show_success_dialog(f"New API key copied to clipboard:\n{key}")
            else:
                self.show_error_dialog(result.get('message', 'Failed to generate API key'))

        def on_failure(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Network error: {error}")

        UrlRequest(
            f"{self.backend_url}/api/merchant/api-key/regenerate",
            on_success=on_success,
            on_failure=on_failure,
            on_error=on_failure,
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            req_body=json.dumps({}),
            timeout=15,
        )

    # ── Virtual Dollar Card ──────────────────────────────────────────

    def show_card_screen(self):
        """Navigate to the Virtual Dollar Card screen and load fresh data."""
        if not self.current_user or not self.session_token:
            self.show_error_dialog("Please login to access Virtual Dollar Cards")
            self.root.current = "login"
            return
        self.root.current = "cards"
        Clock.schedule_once(lambda dt: self.load_card_data(), 0.3)

    def load_card_data(self):
        """Loads the FX/fee config and the user's cards."""
        if not self.current_user or not self.session_token:
            return

        def on_config_success(req, result):
            if result.get('status') == 'success':
                self.card_config = result.get('data', {})
                try:
                    screen = self.root.get_screen('cards')
                    rate = self.card_config.get('usd_to_ngn_rate', 0)
                    fee = self.card_config.get('card_creation_fee_usd', 0)
                    if hasattr(screen.ids, 'card_rate_label'):
                        screen.ids.card_rate_label.text = f"Rate: ₦{rate:,.0f}/$ • Card fee: ${fee:,.2f}"
                except Exception as e:
                    print(f"card config render error: {e}")

        UrlRequest(
            f"{self.backend_url}/api/cards/config",
            on_success=on_config_success,
            on_failure=lambda req, error: None, on_error=lambda req, error: None,
            req_headers={'Authorization': f'Bearer {self.session_token}'}, timeout=15,
        )

        def on_cards_success(req, result):
            if result.get('status') == 'success':
                self.user_cards = result.get('data', [])
                try:
                    screen = self.root.get_screen('cards')
                    self._render_card_list(screen, self.user_cards)
                except Exception as e:
                    print(f"card list render error: {e}")

        UrlRequest(
            f"{self.backend_url}/api/cards",
            on_success=on_cards_success,
            on_failure=lambda req, error: print(f"load cards failed: {error}"),
            on_error=lambda req, error: print(f"load cards error: {error}"),
            req_headers={'Authorization': f'Bearer {self.session_token}'}, timeout=15,
        )

    def _render_card_list(self, screen, cards):
        try:
            ids = screen.ids
            box = ids.card_list_box
            box.clear_widgets()

            if not cards:
                if hasattr(ids, 'card_empty_label'):
                    ids.card_empty_label.text = "No cards yet — create one above"
                return
            if hasattr(ids, 'card_empty_label'):
                ids.card_empty_label.text = ""

            for c in cards:
                box.add_widget(self._build_card_widget(c))
        except Exception as e:
            print(f"_render_card_list error: {e}")

    def _build_card_widget(self, card_data):
        """Builds one bank-card-styled widget with its action buttons."""
        status = card_data.get('status', 'active')
        status_colors = {
            'active': [0.25, 0.2, 0.65, 1],
            'frozen': [0.4, 0.4, 0.45, 1],
            'terminated': [0.6, 0.15, 0.15, 1],
        }
        card_color = status_colors.get(status, [0.25, 0.2, 0.65, 1])

        outer = MDCard(
            orientation='vertical', padding=dp(18), spacing=dp(8),
            size_hint_y=None, height=dp(230), radius=[18], elevation=3,
            md_bg_color=card_color,
        )

        brand_row = MDBoxLayout(size_hint_y=None, height=dp(25))
        brand_row.add_widget(MDLabel(text=card_data.get('card_brand', 'Visa'), bold=True,
                                      theme_text_color="Custom", text_color=[1, 1, 1, 1]))
        brand_row.add_widget(MDLabel(text=status.upper(), halign="right",
                                      theme_text_color="Custom", text_color=[1, 1, 1, 0.85],
                                      font_style="Caption"))
        outer.add_widget(brand_row)

        outer.add_widget(MDLabel(
            text=card_data.get('card_number_masked', '**** **** **** ****'),
            font_style="H6", theme_text_color="Custom", text_color=[1, 1, 1, 1],
            size_hint_y=None, height=dp(35),
        ))

        info_row = MDBoxLayout(size_hint_y=None, height=dp(30))
        info_row.add_widget(MDLabel(
            text=f"Exp {card_data.get('expiry_month', '--')}/{card_data.get('expiry_year', '----')[-2:]}",
            theme_text_color="Custom", text_color=[1, 1, 1, 0.85], font_style="Caption"))
        info_row.add_widget(MDLabel(
            text=f"${card_data.get('balance', 0):,.2f}", halign="right", bold=True,
            theme_text_color="Custom", text_color=[1, 1, 1, 1]))
        outer.add_widget(info_row)

        outer.add_widget(MDLabel(
            text=card_data.get('cardholder_name', ''), font_style="Caption",
            theme_text_color="Custom", text_color=[1, 1, 1, 0.7],
            size_hint_y=None, height=dp(20),
        ))

        card_id = card_data.get('id')
        actions = MDBoxLayout(spacing=dp(8), size_hint_y=None, height=dp(40))

        if status != 'terminated':
            actions.add_widget(MDIconButton(
                icon="cash-plus", theme_icon_color="Custom", icon_color=[1, 1, 1, 1],
                on_release=lambda x, cid=card_id: self.show_fund_card_dialog(cid),
            ))
            freeze_icon = "lock-open-variant" if status == 'frozen' else "lock"
            actions.add_widget(MDIconButton(
                icon=freeze_icon, theme_icon_color="Custom", icon_color=[1, 1, 1, 1],
                on_release=lambda x, cid=card_id, st=status: self.toggle_card_freeze(cid, st),
            ))
            actions.add_widget(MDIconButton(
                icon="delete-outline", theme_icon_color="Custom", icon_color=[1, 1, 1, 1],
                on_release=lambda x, cid=card_id: self.confirm_delete_card(cid),
            ))
        actions.add_widget(MDIconButton(
            icon="history", theme_icon_color="Custom", icon_color=[1, 1, 1, 1],
            on_release=lambda x, cid=card_id: self.show_card_transactions(cid),
        ))
        outer.add_widget(actions)

        return outer

    def show_create_card_dialog(self):
        cfg = getattr(self, 'card_config', {}) or {}
        min_funding = cfg.get('min_funding_usd', 5)
        fee = cfg.get('card_creation_fee_usd', 2)
        rate = cfg.get('usd_to_ngn_rate', 1600)

        content = MDBoxLayout(orientation='vertical', spacing=dp(10),
                               size_hint_y=None, height=dp(120), padding=dp(10))
        amount_input = MDTextField(
            hint_text=f"Funding amount in USD (min ${min_funding:,.2f})",
            icon_left="currency-usd",
            input_type='number', mode="rectangle",
            helper_text=f"+ ${fee:,.2f} card fee, charged at ₦{rate:,.0f}/$ from your wallet",
            helper_text_mode="persistent",
        )
        content.add_widget(amount_input)

        dialog = MDDialog(
            title="Create Virtual Dollar Card",
            type="custom", content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL", theme_text_color="Custom",
                              text_color=self.theme_cls.primary_color,
                              on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(text="CREATE", md_bg_color=self.theme_cls.primary_color,
                                on_release=lambda x: self._process_create_card(dialog, amount_input.text)),
            ],
            radius=[20, 7, 20, 7],
        )
        dialog.open()

    def _process_create_card(self, dialog, amount_text):
        dialog.dismiss()
        try:
            amount = float(str(amount_text).strip())
        except (ValueError, AttributeError):
            self.show_error_dialog("Enter a valid USD amount")
            return
        if amount <= 0:
            self.show_error_dialog("Amount must be greater than zero")
            return

        self.show_loader("Creating your card...")

        def on_success(req, result):
            self.hide_loader()
            if result.get('status') == 'success':
                self.show_success_dialog("Virtual dollar card created!")
                self.update_dashboard()
                self.load_card_data()
            else:
                self.show_error_dialog(result.get('message', 'Failed to create card'))

        def on_failure(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Network error: {error}")

        UrlRequest(
            f"{self.backend_url}/api/cards",
            on_success=on_success, on_failure=on_failure, on_error=on_failure,
            req_headers={'Authorization': f'Bearer {self.session_token}', 'Content-Type': 'application/json'},
            req_body=json.dumps({'funding_amount_usd': amount}),
            timeout=20,
        )

    def show_fund_card_dialog(self, card_id):
        content = MDBoxLayout(orientation='vertical', spacing=dp(10),
                               size_hint_y=None, height=dp(90), padding=dp(10))
        amount_input = MDTextField(hint_text="Amount in USD", icon_left="currency-usd", input_type='number', mode="rectangle")
        content.add_widget(amount_input)

        dialog = MDDialog(
            title="Fund Card", type="custom", content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL", theme_text_color="Custom",
                              text_color=self.theme_cls.primary_color,
                              on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(text="FUND", md_bg_color=self.theme_cls.primary_color,
                                on_release=lambda x: self._process_fund_card(dialog, card_id, amount_input.text)),
            ],
            radius=[20, 7, 20, 7],
        )
        dialog.open()

    def _process_fund_card(self, dialog, card_id, amount_text):
        dialog.dismiss()
        try:
            amount = float(str(amount_text).strip())
        except (ValueError, AttributeError):
            self.show_error_dialog("Enter a valid USD amount")
            return
        if amount <= 0:
            self.show_error_dialog("Amount must be greater than zero")
            return

        self.show_loader("Funding card...")

        def on_success(req, result):
            self.hide_loader()
            if result.get('status') == 'success':
                self.show_success_dialog("Card funded successfully!")
                self.update_dashboard()
                self.load_card_data()
            else:
                self.show_error_dialog(result.get('message', 'Failed to fund card'))

        def on_failure(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Network error: {error}")

        UrlRequest(
            f"{self.backend_url}/api/cards/{card_id}/fund",
            on_success=on_success, on_failure=on_failure, on_error=on_failure,
            req_headers={'Authorization': f'Bearer {self.session_token}', 'Content-Type': 'application/json'},
            req_body=json.dumps({'amount_usd': amount}),
            timeout=20,
        )

    def toggle_card_freeze(self, card_id, current_status):
        action = "unfreeze" if current_status == 'frozen' else "freeze"
        self.show_loader(f"{'Unfreezing' if action == 'unfreeze' else 'Freezing'} card...")

        def on_success(req, result):
            self.hide_loader()
            if result.get('status') == 'success':
                self.load_card_data()
            else:
                self.show_error_dialog(result.get('message', f'Failed to {action} card'))

        def on_failure(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Network error: {error}")

        UrlRequest(
            f"{self.backend_url}/api/cards/{card_id}/{action}",
            on_success=on_success, on_failure=on_failure, on_error=on_failure,
            req_headers={'Authorization': f'Bearer {self.session_token}', 'Content-Type': 'application/json'},
            req_body=json.dumps({}),
            timeout=15,
        )

    def confirm_delete_card(self, card_id):
        dialog = MDDialog(
            title="Delete Card?",
            text="This closes the card permanently and refunds any remaining balance to your wallet. This cannot be undone.",
            buttons=[
                MDFlatButton(text="CANCEL", theme_text_color="Custom",
                              text_color=self.theme_cls.primary_color,
                              on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(text="DELETE", md_bg_color=[0.8, 0.2, 0.2, 1],
                                on_release=lambda x: self._process_delete_card(dialog, card_id)),
            ],
        )
        dialog.open()

    def _process_delete_card(self, dialog, card_id):
        dialog.dismiss()
        self.show_loader("Deleting card...")

        def on_success(req, result):
            self.hide_loader()
            if result.get('status') == 'success':
                self.show_success_dialog("Card deleted — balance refunded to your wallet")
                self.update_dashboard()
                self.load_card_data()
            else:
                self.show_error_dialog(result.get('message', 'Failed to delete card'))

        def on_failure(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Network error: {error}")

        UrlRequest(
            f"{self.backend_url}/api/cards/{card_id}",
            on_success=on_success, on_failure=on_failure, on_error=on_failure,
            req_headers={'Authorization': f'Bearer {self.session_token}', 'Content-Type': 'application/json'},
            req_method='DELETE',
            timeout=15,
        )

    def show_card_transactions(self, card_id):
        self.show_loader("Loading history...")

        def on_success(req, result):
            self.hide_loader()
            if result.get('status') != 'success':
                self.show_error_dialog("Could not load card history")
                return
            entries = result.get('data', {}).get('transactions', [])
            self._show_card_transactions_dialog(entries)

        def on_failure(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Network error: {error}")

        UrlRequest(
            f"{self.backend_url}/api/cards/{card_id}/transactions",
            on_success=on_success, on_failure=on_failure, on_error=on_failure,
            req_headers={'Authorization': f'Bearer {self.session_token}'}, timeout=15,
        )

    def _show_card_transactions_dialog(self, entries):
        scroll = ScrollView(size_hint_y=None, height=dp(300))
        tx_list = MDList(spacing=dp(6))

        if not entries:
            tx_list.add_widget(OneLineListItem(text="No transactions yet"))
        else:
            for e in entries:
                date_str = e.get('created_at', '')
                try:
                    dt = datetime.fromisoformat(date_str.replace('Z', ''))
                    date_str = dt.strftime('%b %d, %Y %I:%M %p')
                except Exception:
                    pass
                tx_list.add_widget(TwoLineListItem(
                    text=f"{e.get('type', '').title()} — ${e.get('amount', 0):,.2f}",
                    secondary_text=f"{e.get('description', '')} • {date_str}",
                ))

        scroll.add_widget(tx_list)

        dialog = MDDialog(
            title="Card Transactions", type="custom", content_cls=scroll,
            buttons=[MDFlatButton(text="CLOSE", theme_text_color="Custom",
                                    text_color=self.theme_cls.primary_color,
                                    on_release=lambda x: dialog.dismiss())],
        )
        dialog.open()

    # ── Bill Reminder ────────────────────────────────────────────────

    BILL_TYPE_LABELS = {
        'dstv': 'DSTV', 'gotv': 'GOtv', 'startimes': 'StarTimes',
        'electricity': 'Electricity', 'internet': 'Internet',
    }

    def show_reminder_screen(self):
        """Navigate to the Bill Reminders screen and load fresh data."""
        if not self.current_user or not self.session_token:
            self.show_error_dialog("Please login to manage bill reminders")
            self.root.current = "login"
            return
        self.root.current = "reminders"
        Clock.schedule_once(lambda dt: self.load_reminder_data(), 0.3)

    def load_reminder_data(self):
        if not self.current_user or not self.session_token:
            return

        def on_success(req, result):
            if result.get('status') == 'success':
                self.bill_reminders = result.get('data', [])
                try:
                    screen = self.root.get_screen('reminders')
                    self._render_reminder_list(screen, self.bill_reminders)
                except Exception as e:
                    print(f"Reminder list render error: {e}")

        UrlRequest(
            f"{self.backend_url}/api/reminders",
            on_success=on_success,
            on_failure=lambda req, error: print(f"load reminders failed: {error}"),
            on_error=lambda req, error: print(f"load reminders error: {error}"),
            req_headers={'Authorization': f'Bearer {self.session_token}'}, timeout=15,
        )

    def _render_reminder_list(self, screen, reminders):
        try:
            ids = screen.ids
            box = ids.reminder_list_box
            box.clear_widgets()

            if not reminders:
                if hasattr(ids, 'reminder_empty_label'):
                    ids.reminder_empty_label.text = "No bill reminders yet — add one above"
                return
            if hasattr(ids, 'reminder_empty_label'):
                ids.reminder_empty_label.text = ""

            for r in reminders:
                box.add_widget(self._build_reminder_widget(r))
        except Exception as e:
            print(f"_render_reminder_list error: {e}")

    def _build_reminder_widget(self, r):
        label = self.BILL_TYPE_LABELS.get(r.get('bill_type'), r.get('bill_type', '').title())
        title = r.get('nickname') or label
        is_active = r.get('is_active', True)

        card = MDCard(
            orientation='vertical', padding=dp(15), spacing=dp(6),
            size_hint_y=None, height=dp(140), radius=[15], elevation=2,
            opacity=1.0 if is_active else 0.55,
        )

        top_row = MDBoxLayout(size_hint_y=None, height=dp(28))
        top_row.add_widget(MDLabel(text=f"{title} ({label})", bold=True))
        top_row.add_widget(MDIconButton(
            icon="pencil-outline", on_release=lambda x, rid=r.get('id'): self.show_edit_reminder_dialog(rid)))
        top_row.add_widget(MDIconButton(
            icon="delete-outline", on_release=lambda x, rid=r.get('id'): self.confirm_delete_reminder(rid)))
        card.add_widget(top_row)

        card.add_widget(MDLabel(
            text=f"Account: {r.get('account_identifier', '')}", font_style="Caption",
            theme_text_color="Secondary", size_hint_y=None, height=dp(20)))

        next_due = r.get('next_due_date', '')
        amount_part = f" • Est. {self.format_currency(r.get('estimated_amount'))}" if r.get('estimated_amount') else ""
        card.add_widget(MDLabel(
            text=f"Next due: {next_due}{amount_part}", font_style="Caption",
            theme_text_color="Secondary", size_hint_y=None, height=dp(20)))

        bottom_row = MDBoxLayout(size_hint_y=None, height=dp(30))
        bottom_row.add_widget(MDLabel(
            text="Active" if is_active else "Paused", font_style="Caption",
            theme_text_color="Secondary"))
        bottom_row.add_widget(MDFlatButton(
            text="PAUSE" if is_active else "RESUME",
            theme_text_color="Custom", text_color=self.theme_cls.primary_color,
            on_release=lambda x, rid=r.get('id'), active=is_active: self.toggle_reminder_active(rid, active),
        ))
        card.add_widget(bottom_row)

        return card

    def show_add_reminder_dialog(self):
        self._reminder_dialog_bill_type = 'dstv'
        self._open_reminder_form_dialog(title="Add Bill Reminder", existing=None)

    def show_edit_reminder_dialog(self, reminder_id):
        existing = next((r for r in getattr(self, 'bill_reminders', []) if r.get('id') == reminder_id), None)
        if not existing:
            return
        self._reminder_dialog_bill_type = existing.get('bill_type', 'dstv')
        self._open_reminder_form_dialog(title="Edit Bill Reminder", existing=existing)

    BILL_TYPE_ICONS = {
        'dstv': 'television-classic', 'gotv': 'television-classic',
        'startimes': 'television-classic', 'electricity': 'flash',
        'internet': 'wifi',
    }

    def _open_reminder_form_dialog(self, title, existing):
        content = MDBoxLayout(orientation='vertical', spacing=dp(16),
                               size_hint_y=None, height=dp(430), padding=[dp(4), dp(6), dp(4), 0])

        content.add_widget(MDLabel(
            text="Bill type", font_style="Caption", theme_text_color="Secondary",
            size_hint_y=None, height=dp(18),
        ))

        # 3-per-row wrapping grid — a single fixed-width row previously let
        # "Internet" (the 5th option) overflow off the dialog with no way
        # to reach it. This always fits all 5 types within two rows.
        type_grid = MDGridLayout(cols=3, spacing=dp(8), size_hint_y=None, height=dp(96))
        type_buttons = {}

        def _chip_colors(selected):
            if selected:
                return self.theme_cls.primary_color, [1, 1, 1, 1]
            light = self.theme_cls.theme_style == "Light"
            return ([0.93, 0.93, 0.96, 1] if light else [0.22, 0.22, 0.28, 1]), \
                   ([0.15, 0.15, 0.15, 1] if light else [0.9, 0.9, 0.9, 1])

        def _select_type(bt):
            self._reminder_dialog_bill_type = bt
            for key, chip in type_buttons.items():
                bg, fg = _chip_colors(key == bt)
                chip.md_bg_color = bg
                chip.ids.chip_icon.text_color = fg
                chip.ids.chip_label.text_color = fg

        for bt, label in self.BILL_TYPE_LABELS.items():
            is_selected = bt == self._reminder_dialog_bill_type
            bg, fg = _chip_colors(is_selected)

            chip = MDCard(
                orientation='vertical', spacing=dp(2), padding=[dp(4), dp(8), dp(4), dp(6)],
                radius=[14], elevation=0, md_bg_color=bg, ripple_behavior=True,
                on_release=lambda x, b=bt: _select_type(b),
            )
            icon = MDIcon(icon=self.BILL_TYPE_ICONS.get(bt, 'file-document-outline'),
                           halign="center", theme_text_color="Custom", text_color=fg)
            label_widget = MDLabel(text=label, font_style="Caption", halign="center",
                                     theme_text_color="Custom", text_color=fg)
            chip.add_widget(icon)
            chip.add_widget(label_widget)
            chip.ids = {'chip_icon': icon, 'chip_label': label_widget}

            type_buttons[bt] = chip
            type_grid.add_widget(chip)

        content.add_widget(type_grid)

        content.add_widget(MDLabel(
            text="Details", font_style="Caption", theme_text_color="Secondary",
            size_hint_y=None, height=dp(18),
        ))

        nickname_input = MDTextField(hint_text="Nickname (optional, e.g. Home DSTV)", icon_left="tag-outline", mode="rectangle",
                                       text=(existing or {}).get('nickname') or '')
        account_input = MDTextField(hint_text="Account / smartcard / meter number", icon_left="card-account-details-outline", mode="rectangle",
                                      text=(existing or {}).get('account_identifier') or '')
        due_day_input = MDTextField(hint_text="Due day of month (1-31)", icon_left="calendar-month-outline", input_type='number', mode="rectangle",
                                      text=str((existing or {}).get('due_day_of_month') or ''),
                                      helper_text="We'll remind you a few days before this date each month",
                                      helper_text_mode="persistent")
        amount_input = MDTextField(hint_text="Estimated amount (optional)", icon_left="cash", input_type='number', mode="rectangle",
                                     text=str((existing or {}).get('estimated_amount') or ''))

        for field in (nickname_input, account_input, due_day_input, amount_input):
            content.add_widget(field)

        def _submit(*_):
            account_value = account_input.text.strip()
            due_day_value = due_day_input.text.strip()

            if not account_value:
                self.show_error_dialog("Account/smartcard/meter number is required")
                return
            if not due_day_value:
                self.show_error_dialog("Due day of month is required")
                return
            try:
                due_day_int = int(due_day_value)
                if not (1 <= due_day_int <= 31):
                    raise ValueError
            except ValueError:
                self.show_error_dialog("Due day of month must be a number from 1 to 31")
                return

            dialog.dismiss()
            payload = {
                'bill_type': self._reminder_dialog_bill_type,
                'nickname': nickname_input.text.strip(),
                'account_identifier': account_value,
                'due_day_of_month': due_day_value,
                'estimated_amount': amount_input.text.strip() or None,
            }
            if existing:
                self._process_update_reminder(existing.get('id'), payload)
            else:
                self._process_create_reminder(payload)

        dialog = MDDialog(
            title=title, type="custom", content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL", theme_text_color="Custom",
                              text_color=self.theme_cls.primary_color,
                              on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(text="SAVE", md_bg_color=self.theme_cls.primary_color, on_release=_submit),
            ],
            radius=[20, 7, 20, 7],
        )
        dialog.open()

    def _process_create_reminder(self, payload):
        self.show_loader("Saving reminder...")

        def on_success(req, result):
            self.hide_loader()
            if result.get('status') == 'success':
                self.show_success_dialog("Bill reminder added!")
                self.load_reminder_data()
            else:
                self.show_error_dialog(result.get('message', 'Failed to add reminder'))

        def on_failure(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Network error: {error}")

        UrlRequest(
            f"{self.backend_url}/api/reminders",
            on_success=on_success, on_failure=on_failure, on_error=on_failure,
            req_headers={'Authorization': f'Bearer {self.session_token}', 'Content-Type': 'application/json'},
            req_body=json.dumps(payload), timeout=15,
        )

    def _process_update_reminder(self, reminder_id, payload):
        self.show_loader("Saving reminder...")

        def on_success(req, result):
            self.hide_loader()
            if result.get('status') == 'success':
                self.show_success_dialog("Bill reminder updated!")
                self.load_reminder_data()
            else:
                self.show_error_dialog(result.get('message', 'Failed to update reminder'))

        def on_failure(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Network error: {error}")

        UrlRequest(
            f"{self.backend_url}/api/reminders/{reminder_id}",
            on_success=on_success, on_failure=on_failure, on_error=on_failure,
            req_headers={'Authorization': f'Bearer {self.session_token}', 'Content-Type': 'application/json'},
            req_body=json.dumps(payload), req_method='PUT', timeout=15,
        )

    def toggle_reminder_active(self, reminder_id, currently_active):
        self._process_update_reminder(reminder_id, {'is_active': not currently_active})

    def confirm_delete_reminder(self, reminder_id):
        dialog = MDDialog(
            title="Delete Reminder?",
            text="You'll stop getting reminders for this bill. This cannot be undone.",
            buttons=[
                MDFlatButton(text="CANCEL", theme_text_color="Custom",
                              text_color=self.theme_cls.primary_color,
                              on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(text="DELETE", md_bg_color=[0.8, 0.2, 0.2, 1],
                                on_release=lambda x: self._process_delete_reminder(dialog, reminder_id)),
            ],
        )
        dialog.open()

    def _process_delete_reminder(self, dialog, reminder_id):
        dialog.dismiss()

        def on_success(req, result):
            if result.get('status') == 'success':
                self.load_reminder_data()
            else:
                self.show_error_dialog(result.get('message', 'Failed to delete reminder'))

        UrlRequest(
            f"{self.backend_url}/api/reminders/{reminder_id}",
            on_success=on_success,
            on_failure=lambda req, error: self.show_error_dialog(f"Network error: {error}"),
            on_error=lambda req, error: self.show_error_dialog(f"Network error: {error}"),
            req_headers={'Authorization': f'Bearer {self.session_token}', 'Content-Type': 'application/json'},
            req_method='DELETE', timeout=15,
        )

    def check_pending_bill_reminders(self):
        """Polls for reminders queued on the push channel and fires a real
        on-device notification via plyer for each, then acknowledges it so
        it isn't shown again. Safe no-op if plyer isn't available (e.g.
        desktop dev environment) or the user isn't logged in."""
        if not self.current_user or not self.session_token:
            return

        def on_success(req, result):
            if result.get('status') != 'success':
                return
            for log in result.get('data', []):
                self._fire_local_notification(
                    title="Bill Reminder",
                    message=log.get('message', 'You have a bill due soon'),
                )
                self._ack_pending_reminder(log.get('id'))

        UrlRequest(
            f"{self.backend_url}/api/reminders/pending",
            on_success=on_success,
            on_failure=lambda req, error: None,
            on_error=lambda req, error: None,
            req_headers={'Authorization': f'Bearer {self.session_token}'}, timeout=15,
        )

    def _fire_local_notification(self, title, message):
        try:
            from plyer import notification as plyer_notification
            plyer_notification.notify(title=title, message=message, app_name="Cheap4U")
        except Exception as e:
            # plyer isn't available on every platform/dev setup — fall back
            # to an in-app banner so the reminder is still seen.
            print(f"Local notification unavailable ({e}); showing in-app instead")
            try:
                self.show_success_dialog(f"{title}: {message}")
            except Exception:
                pass

    def _ack_pending_reminder(self, log_id):
        if not log_id:
            return
        UrlRequest(
            f"{self.backend_url}/api/reminders/pending/{log_id}/ack",
            on_success=lambda req, result: None,
            on_failure=lambda req, error: None,
            on_error=lambda req, error: None,
            req_headers={'Authorization': f'Bearer {self.session_token}', 'Content-Type': 'application/json'},
            req_body=json.dumps({}), timeout=15,
        )

    # ── Smart Price Comparison ───────────────────────────────────────

    def show_comparison_screen(self):
        if not self.current_user or not self.session_token:
            self.show_error_dialog("Please login to compare prices")
            self.root.current = "login"
            return
        self.root.current = "compare"
        self.comparison_mode = 'data'
        Clock.schedule_once(lambda dt: self.load_comparison_data(), 0.3)

    def set_comparison_mode(self, mode):
        self.comparison_mode = mode
        try:
            screen = self.root.get_screen('compare')
            ids = screen.ids
            ids.compare_data_tab_btn.md_bg_color = self.theme_cls.primary_color if mode == 'data' else [0, 0, 0, 0]
            ids.compare_airtime_tab_btn.md_bg_color = self.theme_cls.primary_color if mode == 'airtime' else [0, 0, 0, 0]
        except Exception as e:
            print(f"set_comparison_mode error: {e}")
        self.load_comparison_data()

    def load_comparison_data(self):
        if not self.current_user or not self.session_token:
            return
        mode = getattr(self, 'comparison_mode', 'data')
        endpoint = 'data' if mode == 'data' else 'airtime'

        def on_success(req, result):
            if result.get('status') != 'success':
                return
            try:
                screen = self.root.get_screen('compare')
                if mode == 'data':
                    self._render_data_comparison(screen, result.get('data', {}))
                else:
                    self._render_airtime_comparison(screen, result.get('data', {}))
            except Exception as e:
                print(f"comparison render error: {e}")

        UrlRequest(
            f"{self.backend_url}/api/compare/{endpoint}",
            on_success=on_success,
            on_failure=lambda req, error: print(f"comparison load failed: {error}"),
            on_error=lambda req, error: print(f"comparison load error: {error}"),
            req_headers={'Authorization': f'Bearer {self.session_token}'}, timeout=20,
        )

    def _make_badge(self, icon, title, value, color):
        card = MDCard(orientation='horizontal', padding=dp(12), spacing=dp(10),
                       size_hint_y=None, height=dp(60), radius=[12], elevation=1, md_bg_color=color)
        card.add_widget(MDIcon(icon=icon, theme_text_color="Custom", text_color=[1, 1, 1, 1],
                                 size_hint_x=None, width=dp(30)))
        text_box = MDBoxLayout(orientation='vertical')
        text_box.add_widget(MDLabel(text=title, font_style="Caption", theme_text_color="Custom",
                                      text_color=[1, 1, 1, 0.85], size_hint_y=None, height=dp(18)))
        text_box.add_widget(MDLabel(text=value, bold=True, theme_text_color="Custom", text_color=[1, 1, 1, 1]))
        card.add_widget(text_box)
        return card

    def _render_promotions(self, ids, promotions):
        box = ids.compare_promo_box
        box.clear_widgets()
        if not promotions:
            return
        box.add_widget(MDLabel(text="Active Promotions", font_style="H6", bold=True,
                                 size_hint_y=None, height=dp(28)))
        for p in promotions:
            if p.get('discount_type') == 'percentage':
                desc = f"{p.get('discount_value', 0):.0f}% off"
            else:
                desc = f"{self.format_currency(p.get('discount_value', 0))} off"
            box.add_widget(self._make_badge("ticket-percent", f"Code: {p.get('code')}", desc, [0.85, 0.55, 0.1, 1]))

    def _render_data_comparison(self, screen, data):
        ids = screen.ids
        ids.compare_note_label.text = "Comparing live prices, speed, and reliability across all data providers."

        badges_box = ids.compare_badges_box
        badges_box.clear_widgets()

        cheapest = data.get('cheapest_plan')
        if cheapest:
            badges_box.add_widget(self._make_badge(
                "cash", f"Cheapest — {cheapest.get('provider')} {cheapest.get('size')}",
                f"₦{cheapest.get('price_per_gb', 0):,.2f}/GB", [0.1, 0.6, 0.3, 1]))

        fastest = data.get('fastest_provider')
        if fastest:
            stats = data.get('provider_stats', {}).get(fastest, {})
            time_ms = stats.get('avg_processing_time_ms')
            badges_box.add_widget(self._make_badge(
                "lightning-bolt", f"Fastest — {fastest}",
                f"~{time_ms:,}ms avg" if time_ms else "N/A", [0.85, 0.55, 0.1, 1]))

        best_value = data.get('best_value_plan')
        if best_value:
            badges_box.add_widget(self._make_badge(
                "star", f"Best Value — {best_value.get('provider')} {best_value.get('size')}",
                f"Score {best_value.get('value_score', 0)}/100", [0.3, 0.25, 0.7, 1]))

        self._render_promotions(ids, data.get('promotions', []))

        results_box = ids.compare_results_box
        results_box.clear_widgets()
        for plan in data.get('plans', []):
            item = TwoLineListItem(
                text=f"{plan.get('provider')} — {plan.get('size')} ({plan.get('plan_type')}) — {self.format_currency(plan.get('price', 0))}",
                secondary_text=(
                    f"₦{plan.get('price_per_gb', 0):,.2f}/GB • Value score {plan.get('value_score', 0)}/100 • "
                    f"{plan.get('speed', {}).get('success_rate') or 'N/A'}% success"
                ),
            )
            results_box.add_widget(item)

    def _render_airtime_comparison(self, screen, data):
        ids = screen.ids
        ids.compare_note_label.text = data.get('note', '')

        badges_box = ids.compare_badges_box
        badges_box.clear_widgets()

        fastest = data.get('fastest_network')
        if fastest:
            net_stats = next((n for n in data.get('networks', []) if n.get('network') == fastest), {})
            time_ms = net_stats.get('avg_processing_time_ms')
            badges_box.add_widget(self._make_badge(
                "lightning-bolt", f"Fastest — {fastest}",
                f"~{time_ms:,}ms avg" if time_ms else "N/A", [0.85, 0.55, 0.1, 1]))

        reliable = data.get('most_reliable_network')
        if reliable:
            net_stats = next((n for n in data.get('networks', []) if n.get('network') == reliable), {})
            badges_box.add_widget(self._make_badge(
                "shield-check", f"Most Reliable — {reliable}",
                f"{net_stats.get('success_rate', 0)}% success", [0.1, 0.6, 0.3, 1]))

        self._render_promotions(ids, data.get('promotions', []))

        results_box = ids.compare_results_box
        results_box.clear_widgets()
        for net in data.get('networks', []):
            success = net.get('success_rate')
            time_ms = net.get('avg_processing_time_ms')
            item = TwoLineListItem(
                text=f"{net.get('network')} — Value score {net.get('value_score', 0)}/100",
                secondary_text=(
                    f"{success}% success rate • ~{time_ms:,}ms avg" if (success is not None and time_ms)
                    else "Not enough recent data yet"
                ),
            )
            results_box.add_widget(item)

    # ── Gamification ─────────────────────────────────────────────────

    def show_gamification_screen(self):
        if not self.current_user or not self.session_token:
            self.show_error_dialog("Please login to view your rewards")
            self.root.current = "login"
            return
        self.root.current = "gamification"
        Clock.schedule_once(lambda dt: self.load_gamification_data(), 0.3)

    def load_gamification_data(self):
        if not self.current_user or not self.session_token:
            return

        def on_summary(req, result):
            if result.get('status') == 'success':
                try:
                    screen = self.root.get_screen('gamification')
                    self._render_gamification_summary(screen, result.get('data', {}))
                except Exception as e:
                    print(f"gamification summary render error: {e}")

        UrlRequest(
            f"{self.backend_url}/api/gamification/summary",
            on_success=on_summary,
            on_failure=lambda req, error: print(f"gamification summary failed: {error}"),
            on_error=lambda req, error: print(f"gamification summary error: {error}"),
            req_headers={'Authorization': f'Bearer {self.session_token}'}, timeout=15,
        )

        def on_missions(req, result):
            if result.get('status') == 'success':
                try:
                    screen = self.root.get_screen('gamification')
                    self._render_missions(screen, result.get('data', []))
                except Exception as e:
                    print(f"missions render error: {e}")

        UrlRequest(
            f"{self.backend_url}/api/gamification/missions",
            on_success=on_missions,
            on_failure=lambda req, error: None, on_error=lambda req, error: None,
            req_headers={'Authorization': f'Bearer {self.session_token}'}, timeout=15,
        )

        def on_badges(req, result):
            if result.get('status') == 'success':
                try:
                    screen = self.root.get_screen('gamification')
                    self._render_badges(screen, result.get('data', []))
                except Exception as e:
                    print(f"badges render error: {e}")

        UrlRequest(
            f"{self.backend_url}/api/gamification/badges/all",
            on_success=on_badges,
            on_failure=lambda req, error: None, on_error=lambda req, error: None,
            req_headers={'Authorization': f'Bearer {self.session_token}'}, timeout=15,
        )

        def on_leaderboard(req, result):
            if result.get('status') == 'success':
                try:
                    screen = self.root.get_screen('gamification')
                    self._render_leaderboard(screen, result.get('data', []))
                except Exception as e:
                    print(f"leaderboard render error: {e}")

        UrlRequest(
            f"{self.backend_url}/api/gamification/leaderboard?limit=20",
            on_success=on_leaderboard,
            on_failure=lambda req, error: None, on_error=lambda req, error: None,
            req_headers={'Authorization': f'Bearer {self.session_token}'}, timeout=15,
        )

    def _render_gamification_summary(self, screen, data):
        ids = screen.ids
        current_level = data.get('current_level') or {}
        next_level = data.get('next_level')
        total_xp = data.get('total_xp', 0)

        ids.gam_level_icon.icon = current_level.get('icon', 'star-outline')
        ids.gam_level_label.text = f"Level {current_level.get('level_number', 1)} — {current_level.get('title', 'Bronze')}"
        ids.gam_rank_label.text = f"Rank #{data.get('rank', '-')}"
        ids.gam_xp_label.text = f"{total_xp:,} XP"

        if next_level:
            span = max(1, next_level.get('xp_required', 1) - current_level.get('xp_required', 0))
            progress = max(0, total_xp - current_level.get('xp_required', 0))
            ids.gam_xp_progress.max = span
            ids.gam_xp_progress.value = min(span, progress)
            ids.gam_next_level_label.text = (
                f"{data.get('xp_to_next_level', 0):,} XP to {next_level.get('title')}"
            )
        else:
            ids.gam_xp_progress.max = max(total_xp, 1)
            ids.gam_xp_progress.value = ids.gam_xp_progress.max
            ids.gam_next_level_label.text = "Max level reached!"

    def _render_missions(self, screen, missions):
        box = screen.ids.gam_missions_box
        box.clear_widgets()

        if not missions:
            box.add_widget(MDLabel(text="No active missions right now — check back soon!",
                                     theme_text_color="Secondary", size_hint_y=None, height=dp(30)))
            return

        for m in missions:
            card = MDCard(orientation='vertical', padding=dp(12), spacing=dp(6),
                           size_hint_y=None, height=dp(90), radius=[12], elevation=1)

            top_row = MDBoxLayout(size_hint_y=None, height=dp(22))
            period_tag = "Daily" if m.get('period') == 'daily' else "Weekly"
            top_row.add_widget(MDLabel(text=f"{m.get('title')} ({period_tag})", bold=True, font_style="Body2"))
            if m.get('is_completed'):
                top_row.add_widget(MDIcon(icon="check-circle", theme_text_color="Custom",
                                            text_color=[0.1, 0.7, 0.3, 1], size_hint_x=None, width=dp(24)))
            card.add_widget(top_row)

            progress_bar = MDProgressBar(
                value=min(m.get('progress_value', 0), m.get('target_value', 1)),
                max=max(m.get('target_value', 1), 1),
                size_hint_y=None, height=dp(8),
            )
            card.add_widget(progress_bar)

            reward_text = f"+{m.get('xp_reward', 0)} XP"
            if m.get('points_reward'):
                reward_text += f" • +{m.get('points_reward')} points"
            card.add_widget(MDLabel(text=reward_text, font_style="Caption", theme_text_color="Secondary",
                                      size_hint_y=None, height=dp(20)))

            box.add_widget(card)

    def _render_badges(self, screen, badges):
        grid = screen.ids.gam_badges_grid
        grid.clear_widgets()

        if not badges:
            grid.add_widget(MDLabel(text="No badges available yet", theme_text_color="Secondary"))
            return

        for b in badges:
            earned = b.get('earned', False)
            cell = MDBoxLayout(orientation='vertical', size_hint_y=None, height=dp(90))
            icon = MDIcon(
                icon=b.get('icon', 'medal'), pos_hint={"center_x": 0.5},
                size_hint=(None, None), size=(dp(36), dp(36)),
                theme_text_color="Custom",
                text_color=[0.85, 0.6, 0.1, 1] if earned else [0.6, 0.6, 0.6, 0.4],
            )
            label = MDLabel(
                text=b.get('name', ''), font_style="Caption", halign="center",
                theme_text_color="Primary" if earned else "Secondary",
                opacity=1.0 if earned else 0.5,
            )
            cell.add_widget(icon)
            cell.add_widget(label)
            grid.add_widget(cell)

    def _render_leaderboard(self, screen, rows):
        lb_list = screen.ids.gam_leaderboard_list
        lb_list.clear_widgets()

        if not rows:
            lb_list.add_widget(OneLineListItem(text="No rankings yet"))
            return

        my_id = self.current_user.get('id') if self.current_user else None
        for row in rows:
            is_me = row.get('user_id') == my_id
            item = TwoLineListItem(
                text=f"#{row.get('rank')} {row.get('name', '')}" + ("  (You)" if is_me else ""),
                secondary_text=f"Level {row.get('level', 1)} • {row.get('total_xp', 0):,} XP",
                theme_text_color="Custom" if is_me else "Primary",
                text_color=self.theme_cls.primary_color if is_me else [0, 0, 0, 1],
            )
            lb_list.add_widget(item)


    def load_airtime_networks(self):
        """Load airtime networks from backend"""
        try:
            def on_success(req, result):
                if result.get('status') == 'success':
                    # Networks are hardcoded for now, but could come from API
                    networks = ['MTN', 'Airtel', 'Glo', '9Mobile']
                    self.setup_airtime_networks_ui(networks)
                else:
                    print("Failed to load airtime networks")

            def on_failure(req, error):
                print(f"Failed to load airtime networks: {error}")
                # Use fallback networks
                networks = ['MTN', 'Airtel', 'Glo', '9Mobile']
                self.setup_airtime_networks_ui(networks)

            self.backend_api_request("vtpass/services", "GET", callback=on_success)

        except Exception as e:
            print(f"Error loading airtime networks: {str(e)}")

    def setup_airtime_networks_ui(self, networks):
        """Setup airtime networks in UI"""
        try:
            screen = self.root.get_screen("airtime_topup")
            network_grid = screen.ids.network_grid
            network_grid.clear_widgets()

            network_data = {
                'MTN': {'color': self.mtn_color, 'icon': 'assets/mtn.png'},
                'Airtel': {'color': self.airtel_color, 'icon': 'assets/airtel.png'},
                'Glo': {'color': self.glo_color, 'icon': 'assets/glo.png'},
                '9Mobile': {'color': self.mobile9_color, 'icon': 'assets/9mobile.png'}
            }

            for network in networks:
                net_info = network_data.get(network, {'color': [0.5, 0.5, 0.5, 1], 'icon': 'network'})
                
                card = MDCard(
                    orientation='vertical',
                    size_hint=(None, None),
                    size=(dp(75), dp(75)),
                    elevation=2,
                    on_release=lambda x, n=network: self.select_airtime_network(n),
                    md_bg_color=[0.95, 0.95, 0.95, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1],
                    radius=[15]
                )

                # Try to load logo
                try:
                    logo = FitImage(
                        source=net_info['icon'],
                        size_hint=(1, 0.7),
                        radius=[15, 15, 15, 15]
                    )
                except:
                    logo = MDIcon(
                        icon="network",
                        size_hint=(1, 0.7),
                        theme_text_color="Custom",
                        text_color=net_info['color']
                    )
                card.add_widget(logo)

                label = MDLabel(
                    text=network,
                    size_hint_y=None,
                    height=dp(10),
                    halign="center",
                    font_style="Caption",
                    theme_text_color="Custom",
                    text_color=net_info['color']
                )
                card.add_widget(label)

                network_grid.add_widget(card)

        except Exception as e:
            print(f"Error setting up airtime networks UI: {str(e)}")

    def select_airtime_network(self, network):
        """Handle airtime network selection"""
        try:
            screen = self.root.get_screen("airtime_topup")
            
            # Reset all network cards
            for child in screen.ids.network_grid.children:
                child.md_bg_color = [0.95, 0.95, 0.95, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1]

            # Highlight selected card
            for child in screen.ids.network_grid.children:
                if hasattr(child.children[1], 'text') and child.children[1].text == network:
                    child.md_bg_color = [0.8, 0.8, 0.8, 1] if self.theme_cls.theme_style == "Light" else [0.3, 0.3, 0.3, 1]
                    break

            self.selected_airtime_network = network
            screen.ids.selected_network_label.text = network

            # Show selection box
            selected_box = screen.ids.selected_network_box
            if selected_box.height == 0:
                Animation(height=dp(50), opacity=1, duration=0.2).start(selected_box)

            # Enable amount selection
            screen.ids.amount_grid.parent.height = dp(200)
            screen.ids.amount_grid.parent.opacity = 1

        except Exception as e:
            self.show_error_dialog(f"Error selecting network: {str(e)}")

    
    def on_account_number_change(self, instance, value):
        """Verify bank account when account number is entered"""
        bank_name = self.root.get_screen('withdraw').ids.bank_name.text
        account_number = value
        
        if len(account_number) == 10 and bank_name:
            self.verify_bank_account_backend(account_number, bank_name)

        
    def verify_bank_account_backend(self, account_number, bank_name):
        """Verify bank account via backend"""
        def on_success(req, result):
            if result.get('status') == 'success':
                account_name = result.get('data', {}).get('account_name')
                return account_name
            return None
        
        def on_failure(req, error):
            print(f"❌ Bank verification failed: {error}")
            return None
        
        payload = {
            'account_number': account_number,
            'bank_name': bank_name
        }
        
        UrlRequest(
            f"{self.backend_url}/api/bank/verify",
            on_success=on_success,
            on_failure=on_failure,
            req_headers={'Content-Type': 'application/json'},
            req_body=json.dumps(payload),
            timeout=30
        )
    
   
    def process_airtime_topup(self):
        """Process airtime topup with PIN verification"""
        # Validate inputs
        if not self._validate_airtime_input():
            return
        
        # Ask for PIN
        def on_pin_success():
            self._execute_airtime_purchase()
        
        self._prompt_coupon_then_pin("airtime", self.selected_airtime_amount, on_pin_success)

    def _execute_airtime_purchase(self):
        """Execute airtime purchase after PIN verified"""
        try:
            screen = self.root.get_screen("airtime_topup")
            phone = screen.ids.phone_input.text
            amount = self.selected_airtime_amount
            
            # Check wallet balance
            if self.current_user and amount > self.current_user.get('wallet_balance', 0):
                self.show_error_dialog("Insufficient wallet balance")
                self._clear_verified_pin()
                return
            
            self.show_loader("Processing airtime topup...")
            
            payload = {
                'network': self.selected_airtime_network,
                'phone': phone,
                'amount': amount,
                'pin': self.verified_pin,
                'user_email': self.current_user.get('email'),
                'coupon_code': getattr(self, 'pending_coupon_code', None),
            }
            
            def callback(success, response):
                self.hide_loader()
                self._clear_verified_pin()
                
                if success and response.get('status') == 'success':
                    profit_amount = response.get('data', {}).get('profit_amount', 0)
                    new_balance   = response.get('data', {}).get('new_balance')
                    discount      = response.get('data', {}).get('discount_amount', 0)
                    if new_balance is not None and self.current_user:
                        self.current_user['wallet_balance'] = new_balance
                    msg = f"Airtime topup of ₦{amount:,} successful!\nProfit earned: ₦{profit_amount:,.2f}"
                    if discount:
                        msg += f"\nCoupon savings: {self.format_currency(discount)}"
                    self.show_success_dialog(msg)
                    self.update_dashboard()
                    
                    
                    self.root.current = "dashboard"
                    self.reset_airtime_selections()
                    self.pending_coupon_code = None
                else:
                    error_msg = response.get('message', 'Airtime topup failed')
                    self.show_error_dialog(f"Airtime topup failed: {error_msg}")
            
            self.backend_api_request('vtpass/airtime', 'POST', payload, callback)
            
        except Exception as e:
            self.hide_loader()
            self._clear_verified_pin()
            self.show_error_dialog(f"Airtime topup error: {str(e)}")

    def _validate_airtime_input(self):
        """Validate airtime input fields"""
        if not self.selected_airtime_network:
            self.show_error_dialog("Please select a network")
            return False
        
        if not self.selected_airtime_amount:
            self.show_error_dialog("Please select an amount")
            return False
        
        screen = self.root.get_screen("airtime_topup")
        phone = screen.ids.phone_input.text
        
        if len(phone) != 11 or not phone.isdigit():
            self.show_error_dialog("Please enter a valid 11-digit phone number")
            return False
        
        return True
     

    def reset_airtime_selections(self):
        """Reset airtime purchase selections"""
        self.selected_airtime_network = ""
        self.selected_airtime_amount = 0
        
        try:
            screen = self.root.get_screen("airtime_topup")
            
            # Reset network selection
            for child in screen.ids.network_grid.children:
                child.md_bg_color = [0.95, 0.95, 0.95, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1]

            # Reset amount selection
            for child in screen.ids.amount_grid.children:
                if hasattr(child, 'md_bg_color'):
                    child.md_bg_color = [1, 1, 1, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1]
                    if hasattr(child, 'text_color'):
                        child.text_color = child.line_color

            # Clear input fields
            screen.ids.phone_input.text = ""
            screen.ids.custom_amount.text = ""

            # Hide selection boxes
            screen.ids.selected_network_box.height = 0
            screen.ids.selected_network_box.opacity = 0
            screen.ids.selected_amount_box.height = 0
            screen.ids.selected_amount_box.opacity = 0

            # Hide amount section
            screen.ids.amount_grid.parent.height = 0
            screen.ids.amount_grid.parent.opacity = 0

        except Exception as e:
            print(f"Error resetting airtime selections: {str(e)}")


    def fetch_data_plans(self, network=None, data_type=None):
        """Fetch data plans from backend and display them, optionally filtered by data_type (SME, Gifting, Corporate, etc.)."""
        self.show_loader("Loading data plans...")
        
        def on_success(req, result):
            self.hide_loader()
            if result.get('status') == 'success':
                plans = result.get('data', [])
                # Filter by network if provided
                if network:
                    plans = [p for p in plans if p['provider'].lower() == network.lower()]
                # Filter by data_type - the backend now tags each plan with a real
                # type (SME / Gifting / Corporate) from the provider catalog.
                if data_type:
                    plans = [
                        p for p in plans
                        if str(p.get('type', p.get('category', ''))).strip().lower() == data_type.strip().lower()
                    ]
                self.display_data_plans(plans)
            else:
                self.show_error_dialog("Failed to load data plans")
        
        def on_failure(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Network error: {error}")
        
        self.backend_api_request('plans/data', 'GET', callback=on_success, on_failure=on_failure)

    def display_data_plans(self, plans):
        """Display data plans in the data purchase screen grid."""
        screen = self.root.get_screen("data_purchase")
        plan_grid = screen.ids.data_plan_grid
        plan_grid.clear_widgets()
        
        if not plans:
            no_plan_label = MDLabel(
                text="No plans available in this category yet",
                halign="center",
                theme_text_color="Secondary"
            )
            plan_grid.add_widget(no_plan_label)
            return
        
        for plan in plans:
            card = MDCard(
                orientation='vertical',
                size_hint=(None, None),
                size=(dp(150), dp(80)),
                elevation=2,
                on_release=lambda x, p=plan: self.select_data_plan(p),
                md_bg_color=[1,1,1,1] if self.theme_cls.theme_style=="Light" else [0.2,0.2,0.2,1],
                radius=[15]
            )
            # Plan name (size)
            name_label = MDLabel(
                text=plan['size'],
                font_style='Subtitle1',
                bold=True,
                halign='center',
                theme_text_color="Primary",
                size_hint_y=None,
                height=dp(40)
            )
            card.add_widget(name_label)
            # Price and duration
            details_label = MDLabel(
                text=f"₦{plan['selling_price']:,.0f} | {plan['duration']}",
                font_style='Caption',
                halign='center',
                theme_text_color="Secondary",
                size_hint_y=None,
                height=dp(30)
            )
            card.add_widget(details_label)
            plan_grid.add_widget(card)
        
        # Make the scroll view visible
        plan_grid.parent.height = dp(200)
        plan_grid.parent.opacity = 1

    def select_data_plan(self, plan):
        """Handle data plan selection, store plan_id and selling price."""
        screen = self.root.get_screen("data_purchase")
        
        # Reset all cards highlight
        for child in screen.ids.data_plan_grid.children:
            if hasattr(child, 'md_bg_color'):
                child.md_bg_color = [1,1,1,1] if self.theme_cls.theme_style=="Light" else [0.2,0.2,0.2,1]
        
        # Find the clicked card and highlight it
        for child in screen.ids.data_plan_grid.children:
            if hasattr(child, 'children') and len(child.children) >= 2:
                if child.children[1].text == plan['size']:
                    child.md_bg_color = [0.9,0.9,0.9,1] if self.theme_cls.theme_style=="Light" else [0.3,0.3,0.3,1]
                    break
        
        # Store selection
        self.selected_data_plan = plan['size']
        self.selected_data_amount = str(plan['selling_price'])
        #self.selected_data_amount = plan['selling_price']
        self.selected_plan_id = plan['plan_id']   # Important: store the plan_id for purchase
        
        # Update UI labels
        screen.ids.selected_data_plan_label.text = f"{plan['size']} - ₦{plan['selling_price']:,.0f}"
        
        # Show selection box with animation
        selected_box = screen.ids.selected_data_plan_box
        if selected_box.height == 0:
            anim = Animation(height=dp(50), opacity=1, duration=0.2)
            anim.start(selected_box)
        
        # Enable phone input and buttons
        screen.ids.data_phone_input.disabled = False
        screen.ids.data_phone_input.opacity = 1
        screen.ids.myself_btn.disabled = False
        screen.ids.myself_btn.opacity = 1

    def load_data_plans(self, network, data_type):
        """Called when user selects network and data type. Fetches plans."""
        self.fetch_data_plans(network, data_type)

    def _execute_data_purchase(self):
        """Execute data purchase after PIN verified - uses plan_id."""
        try:
            screen = self.root.get_screen("data_purchase")
            phone = screen.ids.data_phone_input.text
            amount = float(self.selected_data_amount)
            
            # Check wallet balance
            if self.current_user and amount > self.current_user.get('wallet_balance', 0):
                self.show_error_dialog("Insufficient wallet balance")
                self._clear_verified_pin()
                return
            
            self.show_loader("Processing data purchase...")
            
            payload = {
                'plan_id': self.selected_plan_id,   # Send plan_id, not plan_code
                'phone': phone,
                'pin': self.verified_pin,
                'user_email': self.current_user.get('email'),
                'coupon_code': getattr(self, 'pending_coupon_code', None),
            }
            
            def callback(success, response):
                self.hide_loader()
                self._clear_verified_pin()
                if success and response.get('status') == 'success':
                    profit_amount = response.get('data', {}).get('profit_amount', 0)
                    discount = response.get('data', {}).get('discount_amount', 0)
                    msg = f"Data purchase of {self.selected_data_plan} successful!\nProfit earned: ₦{profit_amount:,.2f}"
                    if discount:
                        msg += f"\nCoupon savings: {self.format_currency(discount)}"
                    self.show_success_dialog(msg)
                    self.update_dashboard()
                    self.root.current = "dashboard"
                    self.reset_data_selections()
                    self.pending_coupon_code = None
                else:
                    error_msg = response.get('message', 'Data purchase failed')
                    self.show_error_dialog(f"Data purchase failed: {error_msg}")
            
            self.backend_api_request('vtpass/data', 'POST', payload, callback)
            
        except Exception as e:
            self.hide_loader()
            self._clear_verified_pin()
            self.show_error_dialog(f"Data purchase error: {str(e)}")

    
    def process_data_purchase(self):
        """Process data purchase with PIN verification"""
        # Validate inputs
        if not self._validate_data_input():
            return
        
        # Ask for PIN
        def on_pin_success():
            self._execute_data_purchase()
        
        self._prompt_coupon_then_pin("data", float(self.selected_data_amount), on_pin_success)

    

    def _validate_data_input(self):
        """Validate data purchase input fields"""
        if not self.selected_data_network:
            self.show_error_dialog("Please select a network")
            return False
        
        if not self.selected_data_type:
            self.show_error_dialog("Please select a data type")
            return False
        
        if not self.selected_data_plan:
            self.show_error_dialog("Please select a data plan")
            return False
        
        screen = self.root.get_screen("data_purchase")
        phone = screen.ids.data_phone_input.text
        
        if len(phone) != 11 or not phone.isdigit():
            self.show_error_dialog("Please enter a valid 11-digit phone number")
            return False
        
        return True
        
    def show_admin_users(self):
        """Show all users — safe version that cannot crash the app."""
        if not self.session_token:
            self.show_error_dialog("Please login first")
            return

        self.show_loader("Loading users...")

        def on_success(req, result):
            self.hide_loader()
            try:
                if result.get('status') == 'success':
                    self._display_admin_users(result.get('data', []))
                else:
                    self.show_error_dialog(
                        result.get('message', 'Failed to load users')
                    )
            except Exception as e:
                self.show_error_dialog(f"Display error: {e}")
                print(f"show_admin_users on_success error: {e}")

        def on_failure(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Network error: {error}")

        def on_error(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Connection error: {error}")

        from kivy.network.urlrequest import UrlRequest
        UrlRequest(
            f"{self.backend_url}/api/admin/users",
            on_success=on_success,
            on_failure=on_failure,
            on_error=on_error,
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            timeout=20,
        )

    def _display_admin_users(self, users):
        """Display user list safely — wrapped in try/except."""
        try:
            from kivy.uix.scrollview import ScrollView
            from kivymd.uix.boxlayout import MDBoxLayout
            from kivymd.uix.card import MDCard
            from kivymd.uix.label import MDLabel
            from kivymd.uix.button import MDRaisedButton
            from kivy.metrics import dp

            content = MDBoxLayout(
                orientation='vertical',
                spacing=dp(5),
                padding=dp(10),
                size_hint_y=None,
                height=dp(500),
            )

            scroll = ScrollView()
            user_list = MDBoxLayout(
                orientation='vertical',
                spacing=dp(6),
                size_hint_y=None,
                height=dp(max(len(users) * 85, 80)),
            )

            if not users:
                user_list.add_widget(MDLabel(
                    text="No users found",
                    halign="center",
                    theme_text_color="Secondary",
                    size_hint_y=None,
                    height=dp(40),
                ))
            else:
                for u in users:
                    try:
                        card = MDCard(
                            orientation='vertical',
                            size_hint_y=None,
                            height=dp(78),
                            padding=dp(8),
                            spacing=dp(4),
                            radius=[8],
                            elevation=0,  # avoid shadow-shader crash on some Android GPUs
                        )

                        # Info row
                        info = MDBoxLayout(orientation='horizontal', spacing=dp(5))
                        info.add_widget(MDLabel(
                            text=f"[b]{u.get('name','?')}[/b]",
                            markup=True,
                            font_style="Body2",
                            size_hint_x=0.5,
                            size_hint_y=None,
                            height=dp(24),
                        ))
                        info.add_widget(MDLabel(
                            text=u.get('email', ''),
                            font_style="Caption",
                            theme_text_color="Secondary",
                            size_hint_x=0.5,
                            size_hint_y=None,
                            height=dp(24),
                        ))
                        card.add_widget(info)

                        # Balance + status row
                        row2 = MDBoxLayout(orientation='horizontal', spacing=dp(5))
                        row2.add_widget(MDLabel(
                            text=f"₦{u.get('wallet_balance',0):,.2f}",
                            bold=True,
                            size_hint_x=0.4,
                            size_hint_y=None,
                            height=dp(22),
                        ))
                        is_active = u.get('is_active', True)
                        row2.add_widget(MDLabel(
                            text="✅ Active" if is_active else "🚫 Blocked",
                            font_style="Caption",
                            size_hint_x=0.3,
                            size_hint_y=None,
                            height=dp(22),
                        ))
                        uid = u.get('id')
                        action = 'unblock' if not is_active else 'block'
                        btn = MDRaisedButton(
                            text="UNBLOCK" if not is_active else "BLOCK",
                            md_bg_color=[0.2, 0.7, 0.2, 1] if not is_active else [0.9, 0.3, 0.3, 1],
                            size_hint_x=0.3,
                            size_hint_y=None,
                            height=dp(28),
                            font_size='10sp',
                            on_release=lambda x, i=uid, a=action: self._toggle_user_block(i, a),
                        )
                        row2.add_widget(btn)
                        card.add_widget(row2)
                        user_list.add_widget(card)

                    except Exception as e:
                        print(f"Error creating user card: {e}")
                        continue

            scroll.add_widget(user_list)
            content.add_widget(scroll)

            from kivymd.uix.dialog import MDDialog
            from kivymd.uix.button import MDFlatButton
            dialog = MDDialog(
                title=f"All Users ({len(users)})",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(
                        text="CLOSE",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: dialog.dismiss(),
                    )
                ],
                radius=[20, 7, 20, 7],
            )
            dialog.open()

        except Exception as e:
            self.show_error_dialog(f"Could not display users: {e}")
            print(f"_display_admin_users error: {e}")

    def _toggle_user_block(self, user_id, action):
        """Block or unblock a user."""
        self.show_loader(f"{'Unblocking' if action == 'unblock' else 'Blocking'} user...")

        def on_success(req, result):
            self.hide_loader()
            if result.get('status') == 'success':
                self.show_success_dialog(result.get('message', 'Done'))
                Clock.schedule_once(lambda dt: self.show_admin_users(), 0.5)
            else:
                self.show_error_dialog(result.get('message', 'Action failed'))

        def on_failure(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Network error: {error}")

        from kivy.network.urlrequest import UrlRequest
        UrlRequest(
            f"{self.backend_url}/api/admin/users/{user_id}/{action}",
            on_success=on_success,
            on_failure=on_failure,
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            req_body='{}',
            timeout=15,
        )        
        
               
               
    def show_profit_dashboard(self):
        """Show admin profit dashboard. Checks admin by email."""
        if not self.current_user or not self.session_token:
            self.show_error_dialog("Please login first")
            return

        admin_emails = ['admin@cheap4u.com', 'muhammadibrahim3766@gmail.com']
        if self.current_user.get('email') not in admin_emails \
                and self.current_user.get('role') != 'admin':
            self.show_error_dialog("Admin access required")
            return

        self.root.current = "profit"
        Clock.schedule_once(lambda dt: self._load_admin_data(), 0.3)

    def _load_admin_data(self):
        """Load profit data and withdrawal history together."""
        self.load_profit_data()
        self.load_withdrawal_history()

    def load_profit_data(self):
        """Load profit summary from backend."""
        if not self.current_user or not self.session_token:
            return

        def on_success(req, result):
            self.hide_loader()
            if result.get('status') == 'success':
                self.update_profit_ui(result.get('data', {}))
            else:
                self.show_error_dialog(
                    result.get('message', 'Failed to load profit data')
                )

        def on_failure(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Network error loading profit: {error}")

        def on_error(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Connection error: {error}")

        self.show_loader("Loading profit data...")
        UrlRequest(
            f"{self.backend_url}/api/admin/profit",
            on_success=on_success,
            on_failure=on_failure,
            on_error=on_error,
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            timeout=20,
        )


    def update_profit_ui(self, profit_data):
        """Update profit screen UI. Works with both field name conventions."""
        try:
            screen = self.root.get_screen("profit")

            # Available profit — backend sends both 'available_balance' and 'total_available'
            available = (
                profit_data.get('available_balance')
                or profit_data.get('total_available')
                or 0.0
            )
            total_earned = (
                profit_data.get('total_profit')
                or profit_data.get('total_earned')
                or 0.0
            )

            if hasattr(screen.ids, 'total_profit_label'):
                screen.ids.total_profit_label.text = self.format_currency(available)

            if hasattr(screen.ids, 'total_earned_label'):
                screen.ids.total_earned_label.text = (
                    f"Total Earned: {self.format_currency(total_earned)}"
                )

            # By-category breakdown — backend sends 'by_category' or 'profit_by_category'
            by_cat = (
                profit_data.get('by_category')
                or profit_data.get('profit_by_category')
                or {}
            )

            category_map = {
                'data':        ('data_profit_label',        'data_count_label'),
                'airtime':     ('airtime_profit_label',     'airtime_count_label'),
                'electricity': ('electricity_profit_label', 'electricity_count_label'),
                'cable_tv':    ('tv_profit_label',          'tv_count_label'),
                'exam_pin':    ('exam_profit_label',        'exam_count_label'),
                'spin_fee':    ('spin_fee_profit_label',    None),
            }

            for category, (amount_id, count_id) in category_map.items():
                cat_data = by_cat.get(category, {})
                if isinstance(cat_data, dict):
                    amount = cat_data.get('amount', 0) or cat_data.get('sales', 0)
                    count = cat_data.get('count', 0)
                else:
                    amount = float(cat_data or 0)
                    count = 0

                if hasattr(screen.ids, amount_id):
                    screen.ids[amount_id].text = self.format_currency(amount)
                if count_id and hasattr(screen.ids, count_id):
                    screen.ids[count_id].text = f"{count} transactions"

        except Exception as e:
            print(f"update_profit_ui error: {e}")

    def load_withdrawal_history(self):
        """Load withdrawal history from backend."""
        if not self.current_user or not self.session_token:
            return

        def on_success(req, result):
            if result.get('status') == 'success':
                self.update_withdrawal_history(result.get('data', []))

        def on_failure(req, error):
            print(f"load_withdrawal_history failed: {error}")

        UrlRequest(
            f"{self.backend_url}/api/admin/withdrawals",
            on_success=on_success,
            on_failure=on_failure,
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            timeout=15,
        )


    def update_withdrawal_history(self, withdrawals):
        """Update withdrawal history UI"""
        screen = self.root.get_screen("profit")
        history_box = screen.ids.withdrawal_history_box
        history_box.clear_widgets()
        
        if not withdrawals:
            no_history = MDLabel(
                text="No withdrawal history",
                theme_text_color="Secondary",
                halign="center"
            )
            history_box.add_widget(no_history)
            return
        
        for withdrawal in withdrawals[:5]:  # Show last 5 withdrawals
            card = MDCard(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(50),
                padding=dp(10),
                spacing=dp(10)
            )
            
            # Amount and status
            amount_label = MDLabel(
                text=f"₦{withdrawal.get('amount', 0):,.2f}",
                bold=True,
                size_hint_x=0.4
            )
            
            status = withdrawal.get('status', 'pending')
            status_color = {
                'pending': [0.9, 0.6, 0.1, 1],
                'completed': [0.2, 0.8, 0.2, 1],
                'failed': [0.9, 0.3, 0.3, 1]
            }.get(status, [0.5, 0.5, 0.5, 1])
            
            status_label = MDLabel(
                text=status.upper(),
                theme_text_color="Custom",
                text_color=status_color,
                bold=True,
                size_hint_x=0.3
            )
            
            # Date
            date_str = withdrawal.get('created_at', '')[:10]
            date_label = MDLabel(
                text=date_str,
                theme_text_color="Secondary",
                size_hint_x=0.3
            )
            
            card.add_widget(amount_label)
            card.add_widget(status_label)
            card.add_widget(date_label)
            history_box.add_widget(card)

    def show_withdraw_dialog(self):
        """Navigate to withdraw screen."""
        if not self.current_user or not self.session_token:
            self.show_error_dialog("Please login first")
            return

        admin_emails = ['admin@cheap4u.com', 'muhammadibrahim3766@gmail.com']
        if self.current_user.get('email') not in admin_emails \
                and self.current_user.get('role') != 'admin':
            self.show_error_dialog("Admin access required")
            return

        self.root.current = "withdraw"
        Clock.schedule_once(lambda dt: self.update_withdraw_screen(), 0.3)
  

    def update_withdraw_screen(self):
        """Update withdraw screen with balance and load bank list."""
        if not self.session_token:
            return

        def on_balance_success(req, result):
            if result.get('status') == 'success':
                data = result.get('data', {})
                available = data.get('available_balance') or data.get('total_available') or 0.0
                try:
                    screen = self.root.get_screen("withdraw")
                    screen.ids.withdraw_balance_label.text = self.format_currency(available)
                    screen.ids.withdraw_amount.text = ""
                    screen.ids.account_number.text = ""
                    screen.ids.account_name.text = ""
                except Exception as e:
                    print(f"update_withdraw_screen error: {e}")

        from kivy.network.urlrequest import UrlRequest
        UrlRequest(
            f"{self.backend_url}/api/admin/profit",
            on_success=on_balance_success,
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            timeout=15,
        )

        # Load bank list for dropdown
        self._load_bank_list()

    def _load_bank_list(self):
        """Fetch Nigerian bank list from backend for dropdown selection."""
        def on_success(req, result):
            if result.get('status') == 'success':
                self.bank_list = result.get('data', [])

        from kivy.network.urlrequest import UrlRequest
        UrlRequest(
            f"{self.backend_url}/api/admin/banks",
            on_success=on_success,
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            timeout=20,
        )
        
    def show_bank_picker(self):
        """Show bank selection dialog with correct Paystack bank codes."""
        banks = [
            {"name": "Access Bank",                    "code": "044"},
            {"name": "Citibank",                       "code": "023"},
            {"name": "Ecobank",                        "code": "050"},
            {"name": "Fidelity Bank",                  "code": "070"},
            {"name": "First Bank",                     "code": "011"},
            {"name": "First City Monument Bank (FCMB)","code": "214"},
            {"name": "Guaranty Trust Bank (GTBank)",   "code": "058"},
            {"name": "Heritage Bank",                  "code": "030"},
            {"name": "Keystone Bank",                  "code": "082"},
            {"name": "Kuda Bank",                      "code": "090267"},
            {"name": "Moniepoint MFB",                 "code": "50515"},
            {"name": "OPay",                           "code": "999992"},
            {"name": "PalmPay",                        "code": "100033"},
            {"name": "Polaris Bank",                   "code": "076"},
            {"name": "Providus Bank",                  "code": "101"},
            {"name": "Stanbic IBTC Bank",              "code": "221"},
            {"name": "Standard Chartered",             "code": "068"},
            {"name": "Sterling Bank",                  "code": "232"},
            {"name": "Union Bank",                     "code": "032"},
            {"name": "United Bank for Africa (UBA)",   "code": "033"},
            {"name": "Unity Bank",                     "code": "215"},
            {"name": "VFD MFB",                        "code": "566"},
            {"name": "Wema Bank",                      "code": "035"},
            {"name": "Zenith Bank",                    "code": "057"},
        ]

        self.bank_list = banks

        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivy.uix.scrollview import ScrollView
        from kivy.metrics import dp

        content = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(400),
        )
        scroll = ScrollView()
        bank_list = MDBoxLayout(
            orientation='vertical',
            spacing=dp(2),
            size_hint_y=None,
            height=dp(len(banks) * 46),
        )

        for bank in banks:
            btn = MDFlatButton(
                text=bank["name"],
                size_hint=(1, None),
                height=dp(44),
                on_release=lambda x, b=bank: self._select_bank_and_close(b),
            )
            bank_list.add_widget(btn)

        scroll.add_widget(bank_list)
        content.add_widget(scroll)

        self._bank_dialog = MDDialog(
            title="Select Bank",
            type="custom",
            content_cls=content,
            buttons=[MDFlatButton(
                text="CANCEL",
                on_release=lambda x: self._bank_dialog.dismiss(),
            )],
            radius=[20, 7, 20, 7],
        )
        self._bank_dialog.open()

    def _select_bank_and_close(self, bank):
        """Select bank and update the bank field."""
        self.selected_bank_code = bank['code']
        self.selected_bank_name = bank['name']
        try:
            screen = self.root.get_screen("withdraw")
            if hasattr(screen.ids, 'bank_name_field'):
                screen.ids.bank_name_field.text = bank['name']
            elif hasattr(screen.ids, 'bank_name'):
                screen.ids.bank_name.text = bank['name']
        except Exception as e:
            print(f"_select_bank error: {e}")
        if hasattr(self, '_bank_dialog'):
            self._bank_dialog.dismiss()

    def process_withdrawal(self):
        """Submit withdrawal via Paystack instant transfer."""
        screen = self.root.get_screen("withdraw")

        amount_text = screen.ids.withdraw_amount.text.strip()
        account_number = screen.ids.account_number.text.strip() if hasattr(screen.ids, 'account_number') else ''
        bank_code = getattr(self, 'selected_bank_code', '')
        bank_name = getattr(self, 'selected_bank_name', '')

        # Fallback: try reading from bank_name field if bank_code not set
        if not bank_name:
            if hasattr(screen.ids, 'bank_name_field'):
                bank_name = screen.ids.bank_name_field.text.strip()
            elif hasattr(screen.ids, 'bank_name'):
                bank_name = screen.ids.bank_name.text.strip()

        if not amount_text:
            self.show_error_dialog("Please enter withdrawal amount")
            return
        if not account_number or len(account_number) != 10:
            self.show_error_dialog("Please enter a valid 10-digit account number")
            return
        if not bank_code:
            self.show_error_dialog("Please tap the bank field to select your bank")
            return

        try:
            amount = float(amount_text.replace(',', '').replace('₦', ''))
        except ValueError:
            self.show_error_dialog("Invalid amount — numbers only")
            return

        if amount < 100:
            self.show_error_dialog("Minimum withdrawal is ₦100")
            return

        self.show_loader("Verifying account & sending transfer...")

        import json
        payload = {
            'amount': amount,
            'bank_details': {
                'bank_name': bank_name,
                'bank_code': bank_code,
                'account_number': account_number,
            }
        }

        def on_success(req, result):
            self.hide_loader()
            if result.get('status') == 'success':
                # Reset bank selection
                self.selected_bank_code = ''
                self.selected_bank_name = ''
                self.show_success_dialog(
                    result.get('message', 'Transfer sent successfully!')
                )
                self.root.current = "profit"
                Clock.schedule_once(lambda dt: self._load_admin_data(), 0.5)
            else:
                self.show_error_dialog(
                    result.get('message', 'Transfer failed. Try again.')
                )

        def on_failure(req, result):
            self.hide_loader()
            # result here is a dict from a failed HTTP (4xx/5xx)
            try:
                msg = result.get('message', str(result))
            except Exception:
                msg = str(result)
            self.show_error_dialog(f"Error: {msg}")

        def on_error(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Connection error: {error}")

        from kivy.network.urlrequest import UrlRequest
        UrlRequest(
            f"{self.backend_url}/api/admin/profit/withdraw",
            on_success=on_success,
            on_failure=on_failure,
            on_error=on_error,
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            req_body=json.dumps(payload),
            timeout=45,
        )
    
    
    def handle_payment_completion(self, success, transaction_data=None):
        """Handle payment completion callback"""
        if success:
            amount = transaction_data.get('amount', 0) if transaction_data else 0
            self.show_success_dialog(f"Payment of ₦{amount:,.2f} completed successfully!")
            
            # Update user wallet
            if self.current_user:
                self._credit_wallet_after_payment(amount)
                
            self.update_dashboard()
        else:
            self.show_error_dialog("Payment failed. Please try again.")
            
    
    
    def handle_vtpass_error(self, response):
        """Handle VTPass API errors gracefully"""
        if isinstance(response, dict):
            error_code = response.get('code', '')
            error_message = response.get('response_description', 'Transaction failed')
            
            # Common VTPass error codes
            error_codes = {
                '099': 'Service unavailable. Please try again later.',
                '021': 'Insufficient balance in provider account',
                '022': 'Transaction failed. Please try again.',
                '023': 'Service not available for this network',
                '024': 'Invalid phone number or meter number'
            }
            
            user_message = error_codes.get(error_code, error_message)
            return user_message
        return "Transaction failed. Please try again."
        
   
 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # ---- CRITICAL: Set backend URL first ----
        self.backend_url = "https://cheap4u-backend.onrender.com"
        print(f"📍 Backend URL: {self.backend_url}")
        
        # ---- Window binding ----
        Window.bind(on_keyboard=self.on_keyboard)
        
        # ---- File manager ----
        self.file_manager = MDFileManager(
            exit_manager=self.exit_file_manager,
            select_path=self.select_path,
            preview=True
        )
        
        # ---- State variables ----
        self.session_token = None
        self.pending_user_id = None
        self.pending_user_email = None
        self.pending_user_phone = None
        self.current_user = None
        
        self.payment_processing = False
        self.current_payment_reference = ""
        self.verified_pin = ""
        self.selected_funding_method = ""
        self.funding_amount = 0
        
        self.selected_airtime_network = ""
        self.selected_airtime_amount = 0
        self.selected_cable_provider = ""
        self.selected_cable_package = ""
        self.selected_cable_amount = 0
        self.selected_cable_plan_id = ""
        self.selected_electricity_provider = ""
        self.selected_meter_type = ""
        self.selected_data_network = ""
        self.selected_data_type = ""
        self.selected_data_plan = ""
        self.selected_data_amount = ""
        self.selected_plan_id = ""
        self.selected_exam_type = ""
        self.selected_exam_quantity = 0
        self.exam_pin_total_amount = 0
        self.exam_pin_prices = {
            "WAEC": 3800,
            "NECO": 2600,
            "NABTEB": 1000,
            "JAMB": 16500
        }
        
        self.referral_balance = 0
        self.total_referrals = 0
        self.referral_code = ""
        self.can_use_bonus = False

        self.cashback_wallet = {}

        self.spin_segments = []
        self.spin_status = {}
        self.spin_in_progress = False

        self.pending_coupon_code = None

        self.merchant_profile = {}
        self.merchant_business_type = 'individual'
        self.merchant_job_type = 'airtime'

        self.card_config = {}
        self.user_cards = []

        self.bill_reminders = []
        self._reminder_dialog_bill_type = 'dstv'

        self.comparison_mode = 'data'
        
        self.users = {}
        self.transactions = {}
        self.users_file = "users.json"
        self.transactions_file = "transactions.json"
        
        self.filter_menu = None
        self.pin_dialog = None
        self.pin_input = None
        self.pin_error_label = None
        self.balance_dialog = None
        self.code_grid = None
        self.all_codes = []
        
        # ---- Load local data ----
        self.load_users()
        self.load_transactions()
        
        print("✅ App initialized with backend URL:", self.backend_url)

    
    def payment_callback(self, success, transaction_data=None):
        """Handle payment completion callback"""
        if success:
            amount = transaction_data.get('amount', 0) if transaction_data else 0
            self.show_success_dialog(f"Payment of ₦{amount:,.2f} completed successfully!")
            
            # Update user wallet
            if self.current_user:
                user_id = next((k for k,v in self.users.items() if v == self.current_user), None)
                if user_id:
                    self.users[user_id]['wallet_balance'] += amount
                    self.current_user = self.users[user_id]
                    self.save_users()
                    self.update_dashboard()
        else:
            self.show_error_dialog("Payment failed. Please try again.")
    

    
    def debug_backend_connection(self):
        """Debug method to check backend connection"""
        print("🐛 DEBUG: Checking backend connection...")
        print(f"📍 Backend URL: {getattr(self, 'backend_url', 'NOT SET')}")
        print(f"📍 Current user: {self.current_user}")
        print(f"📍 Funding amount: {getattr(self, 'funding_amount', 'NOT SET')}")
        print(f"📍 Selected method: {getattr(self, 'selected_funding_method', 'NOT SET')}")
        
        # Test the connection directly
        import requests
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            print(f"🔧 Direct test - Status: {response.status_code}")
            print(f"🔧 Direct test - Response: {response.text}")
        except Exception as e:
            print(f"🔧 Direct test - Error: {str(e)}")
                        
    def process_funding(self):
        if not self.selected_funding_method:
            self.show_error_dialog("Please select a payment method")
            return
        if not self.funding_amount or float(self.funding_amount) < 100:
            self.show_error_dialog("Minimum funding amount is ₦100")
            return
        if not self.session_token:
            self.show_error_dialog("Please login first")
            return
        method = self.selected_funding_method
        if method == "transfer":
            self._process_bank_transfer_funding()
        elif method == "card":
            self._process_card_funding()
        elif method == "ussd":
            self._process_ussd_funding()
        else:
            self.show_error_dialog("Invalid payment method selected")
                        
    
    def _process_card_funding(self):
        """Initialize Paystack card payment"""
        if not self.session_token:
            self.show_error_dialog("Please login first")
            return

        amount = float(self.funding_amount)
        if amount < 100:
            self.show_error_dialog("Minimum funding amount is ₦100")
            return

        self.show_loader("Initializing payment...")

        import json
        payload = {'amount': amount}

        def on_success(req, result):
            self.hide_loader()
            if result.get('status') == 'success':
                auth_url = result['data']['authorization_url']
                reference = result['data']['reference']
                self.current_payment_reference = reference
                import webbrowser
                webbrowser.open(auth_url)
                self.show_success_dialog(
                    "Complete your payment in the browser.\n"
                    "Your wallet will be credited automatically."
                )
                from kivy.clock import Clock
                Clock.schedule_once(
                    lambda dt: self._check_payment_status(reference), 15
                )
            else:
                self.show_error_dialog(
                    result.get('message', 'Payment initialization failed')
                )

        def on_failure(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Network error: {error}")

        def on_error(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Connection error: {error}")

        from kivy.network.urlrequest import UrlRequest
        UrlRequest(
            f"{self.backend_url}/api/payment/initialize",
            on_success=on_success,
            on_failure=on_failure,
            on_error=on_error,
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            req_body=json.dumps(payload),
            timeout=30,
        )
        
    

    def _process_bank_transfer_funding(self):
        """Show dedicated virtual account for bank transfer"""
        if not self.session_token:
            self.show_error_dialog("Please login first")
            return

        # If we already have the account number, show it immediately
        if self.virtual_account_number:
            self._show_bank_transfer_details({
                'account_number': self.virtual_account_number,
                'bank_name': self.virtual_bank_name,
                'account_name': self.virtual_account_name,
            })
            return

        self.show_loader("Loading account details...")

        def on_success(req, result):
            self.hide_loader()
            if result.get('status') == 'success':
                data = result['data']
                self.virtual_account_number = data.get('account_number') or ''
                self.virtual_bank_name = data.get('bank_name') or ''
                self.virtual_account_name = data.get('account_name') or ''
                self.update_dashboard_virtual_account()

                if data.get('has_virtual_account') and self.virtual_account_number:
                    self._show_bank_transfer_details(data)
                else:
                    self.show_error_dialog(
                        "Virtual account not available yet.\n"
                        "Please use Card Payment to fund your wallet."
                    )
            else:
                self.show_error_dialog(
                    result.get('message', 'Failed to load account details')
                )

        def on_failure(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Network error: {error}")

        def on_error(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Connection error: {error}")

        from kivy.network.urlrequest import UrlRequest
        UrlRequest(
            f"{self.backend_url}/api/payment/account-details",  # FIXED URL
            on_success=on_success,
            on_failure=on_failure,
            on_error=on_error,
            req_headers={
                'Authorization': f'Bearer {self.session_token}',  # FIXED: auth
                'Content-Type': 'application/json',
            },
            timeout=15,
        )


    def _process_ussd_funding(self):
        """Process USSD funding via backend"""
        print("🔄 Processing USSD funding...")
        self.show_loader("Initializing USSD payment...")

        if not self.current_user:
            email = "guest@example.com"
        else:
            email = self.current_user.get('email', 'guest@example.com')

        try:
            payload = {
                "email": email,
                "amount": self.funding_amount,
                "channel": "ussd"
            }

            def on_success(req, result):
                self.hide_loader()
                print(f"✅ USSD success: {result}")
                
                if result.get('status') == 'success':
                    payment_data = result['data']
                    self._show_ussd_instructions(payment_data)
                    
                    # Record pending transaction
                    self._record_pending_transaction(
                        type="wallet_funding",
                        method="ussd",
                        amount=self.funding_amount,
                        reference=payment_data.get('reference', ''),
                        status="pending"
                    )
                else:
                    error_msg = result.get('message', 'Failed to initialize USSD payment')
                    self.show_error_dialog(f"USSD payment failed: {error_msg}")

            def on_failure(req, error):
                self.hide_loader()
                print(f"❌ USSD failure: {error}")
                self.show_error_dialog(f"Network error: {error}")

            UrlRequest(
                f"{self.backend_url}/api/payment/initialize",
                on_success=on_success,
                on_failure=on_failure,
                req_headers={'Content-Type': 'application/json'},
                req_body=json.dumps(payload),
                timeout=30
            )

        except Exception as e:
            self.hide_loader()
            print(f"💥 Exception in USSD: {str(e)}")
            self.show_error_dialog(f"Error: {str(e)}")

    

    def _record_pending_transaction(self, type, method, amount, reference, status="pending"):
        """Record a pending transaction for tracking"""
        try:
            if not hasattr(self, 'pending_transactions'):
                self.pending_transactions = {}
                
            transaction_id = f"tx_{int(datetime.now().timestamp())}"
            self.pending_transactions[transaction_id] = {
                "type": type,
                "method": method,
                "amount": amount,
                "reference": reference,
                "status": status,
                "timestamp": datetime.now().isoformat()
            }
            print(f"📝 Recorded pending transaction: {transaction_id}")
            
        except Exception as e:
            print(f"❌ Failed to record pending transaction: {str(e)}")

   
    def test_paystack_integration(self):
        """Test Paystack integration"""
        print("🧪 Testing Paystack integration...")
        
        def on_success(req, result):
            print(f"✅ Paystack test result: {result}")
            if result.get('status') == 'success':
                self.show_success_dialog("Paystack integration is working!")
            else:
                self.show_error_dialog(f"Paystack test failed: {result.get('message')}")
        
        def on_failure(req, error):
            print(f"❌ Paystack test failed: {error}")
            self.show_error_dialog(f"Paystack test failed: {error}")
        
        UrlRequest(
            f"{self.backend_url}/health",
            on_success=on_success,
            on_failure=on_failure,
            timeout=10
        )

    def process_payment_safely(self, amount, email, service_type="wallet_funding"):
        """Safe payment processing with comprehensive error handling"""
        try:
            print(f"🔄 Processing payment: {email} - ₦{amount}")
            
            payload = {
                "email": email,
                "amount": amount,
                "service_type": service_type,
                "metadata": {
                    "source": "kivy_app",
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            self.show_loader("Initializing payment...")
            
            def on_success(req, result):
                self.hide_loader()
                print(f"📊 Payment initialization response: {result}")
                
                if result.get('status') == 'success':
                    payment_data = result['data']
                    reference = payment_data.get('reference')
                    
                    # Open payment URL
                    import webbrowser
                    webbrowser.open(payment_data['authorization_url'])
                    
                    self.show_success_dialog("Please complete payment in your browser")
                    
                    # Start status checking
                    self.start_payment_status_check(reference)
                else:
                    self.show_error_dialog(f"Payment failed: {result.get('message')}")
            
            def on_failure(req, error):
                self.hide_loader()
                print(f"❌ Payment initialization failed: {error}")
                self.show_error_dialog(f"Network error: {error}")
            
            UrlRequest(
                f"{self.backend_url}/api/payment/initialize",
                on_success=on_success,
                on_failure=on_failure,
                req_headers={'Content-Type': 'application/json'},
                req_body=json.dumps(payload),
                timeout=30
            )
            
        except Exception as e:
            self.hide_loader()
            print(f"💥 Payment processing error: {str(e)}")
            self.show_error_dialog(f"Payment error: {str(e)}")

    def start_payment_status_check(self, reference, attempt=0):
        """Start checking payment status with retry logic"""
        max_attempts = 20  # 10 minutes total (30 seconds each)
        
        if attempt >= max_attempts:
            print("⏰ Payment status check timeout")
            self.show_error_dialog("Payment verification timeout. Please check your transaction history.")
            return
        
        print(f"🔍 Checking payment status (attempt {attempt + 1}/{max_attempts}): {reference}")
        
        def on_success(req, result):
            print(f"📊 Status check response: {result.get('status')}")
            
            if result.get('status') == 'success':
                print("✅ Payment verified successfully!")
                self.show_success_dialog("Payment verified! Wallet funded successfully.")
                self.update_dashboard()
                self.root.current = "dashboard"
            else:
                # Continue checking
                Clock.schedule_once(
                    lambda dt: self.start_payment_status_check(reference, attempt + 1),
                    30  # Check every 30 seconds
                )
        
        def on_failure(req, error):
            print(f"❌ Status check failed: {error}")
            # Continue checking despite failure
            Clock.schedule_once(
                lambda dt: self.start_payment_status_check(reference, attempt + 1),
                30
            )
        
        UrlRequest(
            f"{self.backend_url}/api/payment/verify/{reference}",
            on_success=on_success,
            on_failure=on_failure,
            timeout=30
        )
    
    def _credit_wallet(txn, amount, channel='unknown', user=None):
        if user is None:
            user = User.query.get(txn.user_id)
        if not user:
            logger.error(f'_credit_wallet: user {txn.user_id} not found')
            return None

        user.wallet_balance = round(user.wallet_balance + amount, 2)
        txn.status = 'success'
        txn.amount = amount
        txn.details = {**(txn.details or {}), 'channel': channel}

        
        if not user.referral_bonus_claimed and user.referred_by_user_id:
            referrer = User.query.get(user.referred_by_user_id)
            if referrer:
                bonus = 50.0
                referrer.referral_balance = round(referrer.referral_balance + bonus, 2)
                referrer.referral_earnings = round(referrer.referral_earnings + bonus, 2)
                user.referral_bonus_claimed = True
                db.session.add(ReferralTransaction(
                    referrer_id=referrer.id,
                    referred_user_id=user.id,
                    amount=bonus,
                    type='signup_bonus',
                ))
                logger.info(
                    f'Referral bonus ₦{bonus} awarded to user {referrer.id} '
                    f'(referred user {user.id} funded wallet)'
                )

        db.session.commit()
        return user    
    
    def _credit_wallet_after_payment(self, amount):
        """Credit user's wallet after successful payment"""
        if not self.current_user:
            print("❌ No user logged in to credit wallet")
            return False
            
        try:
            # Find user in database
            user_id = None
            for uid, user_data in self.users.items():
                if user_data == self.current_user:
                    user_id = uid
                    break
                    
            if user_id:
                # Update wallet balance
                current_balance = self.users[user_id].get('wallet_balance', 0)
                new_balance = current_balance + amount
                
                self.users[user_id]['wallet_balance'] = new_balance
                self.current_user = self.users[user_id]
                
                # Save to storage
                self.save_users()
                
                # Update UI
                self.update_dashboard()
                
                print(f"💰 Wallet credited: ₦{amount:,.2f}. New balance: ₦{new_balance:,.2f}")
                
                # Record transaction
                transaction_id = str(len(self.transactions) + 1)
                transaction = {
                    "user_id": user_id,
                    "type": "Wallet Funding",
                    "amount": f"₦{amount:,.2f}",
                    "status": "Successful",
                    "date": datetime.now().strftime("%B %d, %Y %I:%M:%S %p"),
                    "method": self.selected_funding_method,
                    "reference": getattr(self, 'current_payment_reference', 'N/A')
                }
                self.transactions[transaction_id] = transaction
                self.save_transactions()
                
                return True
            else:
                print("❌ User not found in database")
                return False
                
        except Exception as e:
            print(f"❌ Error crediting wallet: {str(e)}")
            return False
            
            

    def _clear_pending_transaction(self, reference):
        """Clear a pending transaction after successful payment"""
        try:
            if hasattr(self, 'pending_transactions'):
                for tx_id, tx_data in self.pending_transactions.items():
                    if tx_data.get('reference') == reference:
                        del self.pending_transactions[tx_id]
                        print(f"✅ Cleared pending transaction: {tx_id}")
                        break
        except Exception as e:
            print(f"❌ Failed to clear pending transaction: {str(e)}")

    
    def _show_bank_transfer_details(self, account_details):
        """Show bank transfer details with copy functionality"""
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(15),
            size_hint_y=None,
            height=dp(280),
            padding=dp(20)
        )

        # Bank details
        details = [
            f"Bank: {account_details.get('bank', {}).get('name', 'N/A')}",
            f"Account Number: {account_details.get('account_number', 'N/A')}",
            f"Account Name: {account_details.get('account_name', 'N/A')}",
            f"Amount: ₦{self.funding_amount:,.2f}",
            "",
            "Transfer the exact amount to this account.",
            "Your wallet will be credited automatically."
        ]

        for detail in details:
            content.add_widget(MDLabel(
                text=detail,
                size_hint_y=None,
                height=dp(20)
            ))

        # Copy button for account number
        copy_btn = MDRaisedButton(
            text="COPY ACCOUNT NUMBER",
            size_hint_y=None,
            height=dp(50),
            on_release=lambda x: self.copy_to_clipboard(account_details.get('account_number', ''))
        )
        content.add_widget(copy_btn)

        dialog = MDDialog(
            title="Bank Transfer Instructions",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CLOSE",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: dialog.dismiss()
                )
            ],
            radius=[20, 7, 20, 7]
        )
        dialog.open()

        # Start checking payment status
        Clock.schedule_once(
            lambda dt: self._check_payment_status(account_details.get('reference')),
            30
        )

   
    def _show_ussd_instructions(self, ussd_details):
        """Show USSD instructions with copy functionality"""
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(15),
            size_hint_y=None,
            height=dp(250),
            padding=dp(20)
        )

        content.add_widget(MDLabel(
            text="Follow these steps to complete payment:",
            size_hint_y=None,
            height=dp(30),
            bold=True
        ))

        steps = [
            "1. Dial *966*0# on your phone",
            "2. Select 'Pay with USSD'", 
            "3. Enter amount when prompted",
            "4. Follow the instructions to complete payment"
        ]

        for step in steps:
            content.add_widget(MDLabel(
                text=step,
                size_hint_y=None,
                height=dp(25),
                theme_text_color="Secondary"
            ))

        content.add_widget(MDLabel(
            text=f"Reference: {ussd_details.get('reference', 'N/A')}",
            size_hint_y=None,
            height=dp(30),
            bold=True
        ))

        # Copy reference button
        copy_btn = MDRaisedButton(
            text="COPY REFERENCE",
            size_hint_y=None,
            height=dp(50),
            on_release=lambda x: self.copy_to_clipboard(ussd_details.get('reference', ''))
        )
        content.add_widget(copy_btn)

        dialog = MDDialog(
            title="USSD Payment Instructions",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="DONE",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: dialog.dismiss()
                )
            ],
            radius=[20, 7, 20, 7]
        )
        dialog.open()

        # Start checking payment status
        Clock.schedule_once(
            lambda dt: self._check_payment_status(ussd_details.get('reference')),
            30
        )
                
  
    def tvpass_backend_request(self, endpoint, method="POST", data=None, callback=None):
        """Make VTPass requests through backend with enhanced error handling"""
        url = f"{self.backend_url}/api/vtpass/{endpoint}"
        
        print(f"🔧 Backend VTPass Request: {method} {url}")
        print(f"🔧 Request Data: {data}")
        
        def on_success(req, result):
            print(f"🔧 Backend VTPass Success: {result}")
            if callback:
                # Handle both success and error responses from backend
                if isinstance(result, dict):
                    if result.get('status') == 'success':
                        callback(True, result.get('data', result))
                    else:
                        callback(False, result)
                else:
                    callback(True, {'status': 'success', 'data': result})
        
        def on_failure(req, error):
            print(f"🔧 Backend VTPass Failure: {error}")
            if callback:
                callback(False, {"status": "error", "message": str(error)})
        
        def on_error(req, error):
            print(f"🔧 Backend VTPass Error: {error}")
            if callback:
                callback(False, {"status": "error", "message": f"Network error: {str(error)}"})
        
        try:
            if method.upper() == "GET":
                UrlRequest(
                    url,
                    on_success=on_success,
                    on_failure=on_failure,
                    on_error=on_error,
                    timeout=30
                )
            else:
                UrlRequest(
                    url,
                    on_success=on_success,
                    on_failure=on_failure,
                    on_error=on_error,
                    req_headers={'Content-Type': 'application/json'},
                    req_body=json.dumps(data) if data else None,
                    timeout=30
                )
        except Exception as e:
            print(f"🔧 Backend VTPass Exception: {e}")
            if callback:
                callback(False, {"status": "error", "message": f"Request error: {str(e)}"})

    def _display_backend_transactions(self, transactions, filter_type='all'):
        """Display transactions fetched from backend."""
        screen = self.root.get_screen("history")

        if not transactions:
            self._show_empty_state(True)
            return

        self._show_empty_state(False)

        # Apply filter
        filter_map = {
            'airtime': lambda t: t.get('service_type') == 'airtime',
            'data': lambda t: t.get('service_type') == 'data',
            'electricity': lambda t: t.get('service_type') == 'electricity',
            'cable': lambda t: t.get('service_type') == 'cable_tv',
            'success': lambda t: t.get('status') == 'success',
            'failed': lambda t: t.get('status') == 'failed',
        }

        if filter_type in filter_map:
            transactions = [t for t in transactions if filter_map[filter_type](t)]

        history_list = screen.ids.history_list
        history_list.clear_widgets()

        for txn in transactions:
            # Convert backend transaction dict to display format
            display_txn = {
                'type': (txn.get('service_type') or txn.get('type') or 'Transaction').replace('_', ' ').title(),
                'amount': f"₦{txn.get('amount', 0):,.2f}",
                'status': txn.get('status', 'pending').capitalize(),
                'date': txn.get('date') or txn.get('created_at', ''),
                'reference': txn.get('reference', ''),
                'details': txn.get('details', {}),
                'service_type': txn.get('service_type', ''),
            }

            try:
                card = self._create_transaction_item(display_txn)
                history_list.add_widget(card)
            except Exception as e:
                print(f"Transaction card error: {e}")

        history_list.height = history_list.minimum_height                
    
    def backend_api_request(self, endpoint, method="GET", data=None, callback=None, on_failure=None):
        """Threaded request using requests library with extended timeout for Render free tier."""
        if not self.backend_url:
            print("❌ Backend URL not set!")
            if callback:
                Clock.schedule_once(lambda dt: callback(False, {"message": "Backend URL not configured"}), 0)
            return

        url = f"{self.backend_url}/api/{endpoint}"
        print(f"🌐 Requesting: {method} {url}")
        
        if data:
            print(f"📤 Data: {data}")

        def make_request():
            try:
                headers = {'Content-Type': 'application/json'}
                if hasattr(self, 'session_token') and self.session_token:
                    headers['Authorization'] = f'Bearer {self.session_token}'

                # Extended timeout for Render free tier (60 seconds)
                if method.upper() == "GET":
                    response = requests.get(url, headers=headers, timeout=60)
                elif method.upper() == "DELETE":
                    response = requests.delete(url, headers=headers, timeout=60)
                elif method.upper() == "PUT":
                    response = requests.put(url, json=data, headers=headers, timeout=60)
                else:
                    response = requests.post(url, json=data, headers=headers, timeout=60)

                # Handle empty or invalid JSON responses
                try:
                    result = response.json()
                except json.JSONDecodeError as je:
                    print(f"❌ Invalid JSON response: {response.text[:200]}")
                    result = {"status": "error", "message": f"Server error (HTTP {response.status_code})"}
                
                print(f"📦 Response (HTTP {response.status_code}): {result}")

                from kivy.clock import Clock
                if response.status_code == 401:
                    Clock.schedule_once(lambda dt: self.handle_session_expired(), 0)
                    Clock.schedule_once(lambda dt, r=result: callback(False, r) if callback else None, 0)
                    return
                if response.status_code == 200 and result.get('status') == 'success':
                    Clock.schedule_once(lambda dt, r=result: callback(True, r) if callback else None, 0)
                else:
                    Clock.schedule_once(lambda dt, r=result: callback(False, r) if callback else None, 0)
                    
            except requests.exceptions.ConnectionError as err:
                print(f"❌ Connection error: {err}")
                from kivy.clock import Clock
                Clock.schedule_once(lambda dt, e=err: callback(False, {"message": "Cannot connect to server. Check your internet."}) if callback else None, 0)
                
            except requests.exceptions.Timeout as err:
                print(f"❌ Timeout: {err}")
                from kivy.clock import Clock
                Clock.schedule_once(lambda dt, e=err: callback(False, {"message": "Server is waking up. Please try again in 30 seconds."}) if callback else None, 0)
                
            except Exception as err:
                print(f"❌ Request error: {err}")
                from kivy.clock import Clock
                Clock.schedule_once(lambda dt, e=err: callback(False, {"message": str(e)}) if callback else None, 0)

        thread = threading.Thread(target=make_request)
        thread.daemon = True
        thread.start()
    
    
    def process_electricity_payment(self):
        """Process electricity payment with PIN verification"""
        # Validate inputs
        if not self._validate_electricity_input():
            return
        
        # Ask for PIN
        def on_pin_success():
            self._execute_electricity_payment()

        try:
            screen = self.root.get_screen("electricity")
            amount = float(screen.ids.electricity_amount_input.text.replace('₦', '').replace(',', ''))
        except Exception:
            amount = 0
        self._prompt_coupon_then_pin("electricity", amount, on_pin_success)

    def _execute_electricity_payment(self):
        """Execute electricity payment after PIN verified"""
        try:
            screen = self.root.get_screen("electricity")
            meter_number = screen.ids.meter_number_input.text
            amount = float(screen.ids.electricity_amount_input.text.replace('₦', '').replace(',', ''))
            phone = screen.ids.electricity_phone_input.text
            
            # Check wallet balance
            if self.current_user and amount > self.current_user.get('wallet_balance', 0):
                self.show_error_dialog("Insufficient wallet balance")
                self._clear_verified_pin()
                return
            
            self.show_loader("Processing electricity payment...")
            
            payload = {
                'disco': self.selected_electricity_provider,
                'meter_number': meter_number,
                'meter_type': self.selected_meter_type,
                'amount': amount,
                'phone': phone,
                'pin': self.verified_pin,
                'user_email': self.current_user.get('email'),
                'coupon_code': getattr(self, 'pending_coupon_code', None),
            }
            
            def callback(success, response):
                self.hide_loader()
                self._clear_verified_pin()
                
                if success and response.get('status') == 'success':
                    data = response.get('data', {})
                    token = data.get('token', '')
                    profit_amount = data.get('profit_amount', 0)
                    discount = data.get('discount_amount', 0)
                    
                    if token:
                        self._show_electricity_success(token, meter_number, amount, profit_amount)
                    else:
                        msg = f"Electricity payment of ₦{amount:,} successful!\nProfit earned: ₦{profit_amount:,.2f}"
                        if discount:
                            msg += f"\nCoupon savings: {self.format_currency(discount)}"
                        self.show_success_dialog(msg)
                    self.update_dashboard()
                    self.root.current = "dashboard"
                    self.pending_coupon_code = None
                else:
                    error_msg = response.get('message', 'Electricity payment failed')
                    self.show_error_dialog(f"Electricity payment failed: {error_msg}")
            
            self.backend_api_request('vtpass/electricity', 'POST', payload, callback)
            
        except Exception as e:
            self.hide_loader()
            self._clear_verified_pin()
            self.show_error_dialog(f"Electricity payment error: {str(e)}")

    def _validate_electricity_input(self):
        """Validate electricity payment input fields"""
        if not self.selected_electricity_provider:
            self.show_error_dialog("Please select an electricity provider")
            return False
        
        if not self.selected_meter_type:
            self.show_error_dialog("Please select meter type")
            return False
        
        screen = self.root.get_screen("electricity")
        meter_number = screen.ids.meter_number_input.text
        amount = screen.ids.electricity_amount_input.text
        phone = screen.ids.electricity_phone_input.text
        
        if len(meter_number) < 6 or not meter_number.isdigit():
            self.show_error_dialog("Please enter a valid meter number")
            return False
        
        if not amount or float(amount.replace('₦', '').replace(',', '')) < 50:
            self.show_error_dialog("Please enter a valid amount (minimum ₦50)")
            return False
        
        if len(phone) != 11 or not phone.isdigit():
            self.show_error_dialog("Please enter a valid 11-digit phone number")
            return False
        
        return True
  
    def _show_electricity_success(self, token, meter_number, amount, profit_amount=0):
        content = MDBoxLayout(
            orientation='vertical', spacing=dp(15),
            padding=dp(20), size_hint_y=None, height=dp(230)
        )
        content.add_widget(MDLabel(text="Payment Successful!", halign='center', bold=True))
        content.add_widget(MDLabel(text=f"Meter: {meter_number}", halign='center'))
        content.add_widget(MDLabel(text=f"Amount: ₦{amount:,}", halign='center'))
        content.add_widget(MDLabel(text=f"Token: {token}", halign='center', bold=True))
        if profit_amount:
            content.add_widget(MDLabel(
                text=f"Profit: ₦{profit_amount:,.2f}", halign='center',
                theme_text_color="Secondary"
            ))
        dialog = MDDialog(
            title="Electricity Token", type="custom", content_cls=content,
            buttons=[
                MDFlatButton(text="COPY TOKEN", theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: (self.copy_to_clipboard(token), dialog.dismiss())),
                MDFlatButton(text="DONE", theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: dialog.dismiss())
            ], radius=[20, 7, 20, 7]
        )
        dialog.open()    
    
    def process_cable_subscription(self):
        """Process cable TV subscription with PIN verification"""
        # Validate inputs
        if not self._validate_cable_input():
            return
        
        # Ask for PIN
        def on_pin_success():
            self._execute_cable_subscription()
        
        self._prompt_coupon_then_pin("cable_tv", self.selected_cable_amount, on_pin_success)

    

    def _validate_cable_input(self):
        """Validate cable TV input fields"""
        if not self.selected_cable_provider:
            self.show_error_dialog("Please select a cable provider")
            return False
        
        if not self.selected_cable_package:
            self.show_error_dialog("Please select a package")
            return False
        
        screen = self.root.get_screen("cable_tv")
        smartcard = screen.ids.smartcard_input.text
        
        if len(smartcard) < 6:
            self.show_error_dialog("Please enter a valid smartcard/IUC number")
            return False
        
        return True 

    def set_funding_amount(self, amount):
        """Set funding amount from quick amount buttons."""
        try:
            self.funding_amount = float(amount)
            screen = self.root.get_screen("funding")
            if hasattr(screen.ids, 'amount_input'):
                screen.ids.amount_input.text = str(int(amount))
            self.validate_funding_amount(str(amount))
        except Exception as e:
            print(f"set_funding_amount error: {e}")

    def show_funding_help(self):
        """Show funding help dialog"""
        dialog = MDDialog(
            title="Funding Help",
            text=(
                "How to fund your wallet:\n\n"
                "1. Enter the amount you want to add\n"
                "2. Choose your preferred payment method\n"
                "3. Follow the instructions to complete payment\n\n"
                "Payment Methods:\n"
                "• Bank Transfer: Get virtual account details\n"
                "• USSD: Pay with USSD code\n"
                "• Card: Pay with debit/credit card\n\n"
                "Minimum amount: ₦100\n"
                "Processing time: Instant"
            ),
            buttons=[
                MDFlatButton(
                    text="GOT IT",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: dialog.dismiss()
                )
            ],
            radius=[20, 7, 20, 7]
        )
        dialog.open()

    def update_funding_screen(self):
        """Update funding screen with current data"""
        if hasattr(self, 'root') and self.root:
            screen = self.root.get_screen("funding")
            if screen:
                # Update current balance
                if hasattr(screen.ids, 'current_balance_label'):
                    balance = self.current_user.get('wallet_balance', 0) if self.current_user else 0
                    screen.ids.current_balance_label.text = self.format_currency(balance)
                
                # Update amount input if funding_amount is set
                if hasattr(self, 'funding_amount') and self.funding_amount:
                    screen.ids.amount_input.text = str(self.funding_amount)
    
    
          
    def select_payment_method(self, method):
        """Select payment method for funding"""
        self.selected_funding_method = method
        
        # Update UI to show selection
        screen = self.root.get_screen("funding")
        for child in screen.children[0].children[0].children:
            if hasattr(child, 'children') and len(child.children) > 0:
                for widget in child.children:
                    if hasattr(widget, 'icon') and "check-circle" in widget.icon:
                        if method == "transfer" and "bank-transfer" in child.children[2].icon:
                            widget.icon = "check-circle"
                            widget.text_color = self.theme_cls.primary_color
                        elif method == "ussd" and "cellphone" in child.children[2].icon:
                            widget.icon = "check-circle"
                            widget.text_color = self.theme_cls.primary_color
                        elif method == "card" and "credit-card" in child.children[2].icon:
                            widget.icon = "check-circle"
                            widget.text_color = self.theme_cls.primary_color
                        else:
                            widget.icon = "circle-outline"
                            widget.text_color = [0.5, 0.5, 0.5, 1]
    
    def validate_funding_amount(self, text):
        """Validate funding amount"""
        try:
            if not text:
                self.funding_amount = 0
                return False
            
            amount = float(text.replace('₦', '').replace(',', ''))
            
            if amount < 100:
                return False
            
            self.funding_amount = amount
            return True
            
        except ValueError:
            self.funding_amount = 0
            return False
    
  
    
    def _credit_wallet_after_payment(self, amount):
        """Credit user's wallet after successful payment"""
        if self.current_user:
            user_id = next((k for k,v in self.users.items() if v == self.current_user), None)
            if user_id:
                self.users[user_id]['wallet_balance'] += amount
                self.current_user = self.users[user_id]
                self.save_users()
                self.update_dashboard()
                
                # Add transaction record
                transaction_id = str(len(self.transactions) + 1)
                transaction = {
                    "user_id": user_id,
                    "type": "Wallet Funding",
                    "amount": f"₦{amount:,.2f}",
                    "status": "Successful",
                    "date": datetime.now().strftime("%B %d, %Y %I:%M:%S %p"),
                    "method": self.selected_funding_method
                }
                self.transactions[transaction_id] = transaction
                self.save_transactions()
#  Ended      
    
  
    def vtpass_backend_request(self, endpoint, method="POST", data=None, callback=None):
        """Make VTPass requests through backend with proper error handling"""
        url = f"{self.backend_url}/api/vtpass/{endpoint}"
        
        print(f"🔧 Backend VTPass Request: {method} {url}")
        print(f"🔧 Request Data: {data}")
        
        def on_success(req, result):
            print(f"✅ Backend VTPass Response: {result}")
            if callback:
                # Check for VTPass error codes
                if result.get('code') == '000':  # VTPass success code
                    callback(True, {'status': 'success', 'data': result})
                elif result.get('status') == 'success':  # Our backend success
                    callback(True, result)
                else:
                    callback(False, result)
        
        def on_failure(req, error):
            print(f"❌ Backend VTPass Failure: {error}")
            if callback:
                callback(False, {"status": "error", "message": str(error)})
        
        def on_error(req, error):
            print(f"❌ Backend VTPass Error: {error}")
            if callback:
                callback(False, {"status": "error", "message": f"Network error: {str(error)}"})
        
        try:
            if method.upper() == "GET":
                UrlRequest(
                    url,
                    on_success=on_success,
                    on_failure=on_failure,
                    on_error=on_error,
                    timeout=30
                )
            else:
                UrlRequest(
                    url,
                    on_success=on_success,
                    on_failure=on_failure,
                    on_error=on_error,
                    req_headers={'Content-Type': 'application/json'},
                    req_body=json.dumps(data) if data else None,
                    timeout=30
                )
        except Exception as e:
            print(f"💥 Backend VTPass Exception: {e}")
            if callback:
                callback(False, {"status": "error", "message": f"Request error: {str(e)}"})
    
    def setup_exam_pin_screen(self):
        """Setup exam PIN screen with exam types - WITH IMAGES"""
        screen = self.root.get_screen("exam_pin")
        
        # Setup exam types with LOGOS
        exam_types = [
            {"name": "WAEC", "logo": "assets/waec.png", "color": [0.1, 0.6, 1, 1]},
            {"name": "NECO", "logo": "assets/neco.png", "color": [0.2, 0.8, 0.2, 1]},
            {"name": "JAMB", "logo": "assets/jamb.png", "color": [0.9, 0.3, 0.3, 1]},
            {"name": "NABTEB", "logo": "assets/nabteb.png", "color": [0.8, 0.4, 0.1, 1]}
        ]
        
        exam_type_grid = screen.ids.exam_type_grid
        exam_type_grid.clear_widgets()
        
        for exam in exam_types:
            # Create card with logo
            card = MDCard(
                orientation='vertical',
                size_hint=(None, None),
                size=(dp(75), dp(75)),
                elevation=2,
                on_release=lambda x, e=exam["name"]: self.select_exam_type(e),
                md_bg_color=[0.95, 0.95, 0.95, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1],
                radius=[15]
            )
            
            # Try to load logo, fallback to icon if image not found
            try:
                logo = FitImage(
                    source=exam["logo"],
                    size_hint=(1, 0.7),
                    radius=[15, 15, 15, 15]
                )
                
            except Exception:
                logo = MDIcon(
                    icon="school",
                    size_hint=(1, 0.7),
                    theme_text_color="Custom",
                    text_color=exam["color"]
                )               
            
            card.add_widget(logo)
            
            # Exam name label
            label = MDLabel(
                text=exam["name"],
                size_hint_y=None,
                height=dp(10),
                halign="center",
                font_style="Caption",
                theme_text_color="Custom",
                text_color=exam["color"]
            )
            card.add_widget(label)
            
            exam_type_grid.add_widget(card)
        
        # Clear quantity input
        screen.ids.quantity_input.text = ""
        
 
    def validate_quantity_input(self, text):
        """Validate quantity input"""
        screen = self.root.get_screen("exam_pin")
        
        if not text:
            screen.ids.quantity_input.error = False
            screen.ids.quantity_input.helper_text = "Enter quantity (1-10)"
            self.selected_exam_quantity = 0
            return False
        
        try:
            quantity = int(text)
            
            if quantity < 1:
                screen.ids.quantity_input.error = True
                screen.ids.quantity_input.helper_text = "Minimum quantity is 1"
                self.selected_exam_quantity = 0
                return False
            elif quantity > 10:
                screen.ids.quantity_input.error = True
                screen.ids.quantity_input.helper_text = "Maximum quantity is 10"
                self.selected_exam_quantity = 0
                return False
            
            # Valid quantity
            screen.ids.quantity_input.error = False
            screen.ids.quantity_input.helper_text = "Valid quantity"
            self.selected_exam_quantity = quantity
            
            # Calculate total amount
            price = self.exam_pin_prices.get(self.selected_exam_type, 0)
            self.exam_pin_total_amount = price * quantity
            
            # Update labels
            screen.ids.selected_quantity_label.text = str(quantity)
            screen.ids.total_amount_label.text = self.format_currency(self.exam_pin_total_amount)
            
            # Show selection boxes
            selected_quantity_box = screen.ids.selected_quantity_box
            if selected_quantity_box.height == 0:
                Animation(height=dp(50), opacity=1, duration=0.2).start(selected_quantity_box)
            
            total_amount_box = screen.ids.total_amount_box
            if total_amount_box.height == 0:
                Animation(height=dp(50), opacity=1, duration=0.2).start(total_amount_box)
            
            return True
            
        except ValueError:
            screen.ids.quantity_input.error = True
            screen.ids.quantity_input.helper_text = "Enter numbers only"
            self.selected_exam_quantity = 0
            return False        
    
   
    def select_exam_type(self, exam_type):
        """Handle exam type selection WITH VISUAL FEEDBACK"""
        screen = self.root.get_screen("exam_pin")
        
        # Reset all cards to default color
        for child in screen.ids.exam_type_grid.children:
            child.md_bg_color = [0.95, 0.95, 0.95, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1]
        
        # Highlight selected card
        for child in screen.ids.exam_type_grid.children:
            if hasattr(child.children[1], 'text') and child.children[1].text == exam_type:
                child.md_bg_color = [0.8, 0.8, 0.8, 1] if self.theme_cls.theme_style == "Light" else [0.3, 0.3, 0.3, 1]
                break
        
        self.selected_exam_type = exam_type
        screen.ids.selected_exam_type_label.text = exam_type
        
        # Show selection box with animation
        selected_box = screen.ids.selected_exam_type_box
        if selected_box.height == 0:
            Animation(height=dp(50), opacity=1, duration=0.2).start(selected_box)
        
        # Enable quantity input
        screen.ids.quantity_input.disabled = False
        screen.ids.quantity_input.opacity = 1
        screen.ids.quantity_input.text = ""
        screen.ids.quantity_input.helper_text = "Enter quantity (1-10)"
        
        # Reset quantity and amount
        self.selected_exam_quantity = 0
        self.exam_pin_total_amount = 0
        
        # Hide quantity and amount boxes
        screen.ids.selected_quantity_box.height = 0
        screen.ids.selected_quantity_box.opacity = 0
        screen.ids.total_amount_box.height = 0
        screen.ids.total_amount_box.opacity = 0

    def select_exam_quantity(self, quantity):
        """Handle quantity selection"""
        screen = self.root.get_screen("exam_pin")
        
        # Reset all buttons
        for child in screen.ids.quantity_grid.children:
            child.md_bg_color = [1, 1, 1, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1]
            child.text_color = child.line_color
        
        # Highlight selected button
        for child in screen.ids.quantity_grid.children:
            if child.text == str(quantity):
                child.md_bg_color = child.line_color
                child.text_color = [1, 1, 1, 1]
                break
        
        self.selected_exam_quantity = quantity
        
        # Calculate total amount
        price = self.exam_pin_prices.get(self.selected_exam_type, 0)
        self.exam_pin_total_amount = price * quantity
        
        # Update labels
        screen.ids.selected_quantity_label.text = str(quantity)
        screen.ids.total_amount_label.text = self.format_currency(self.exam_pin_total_amount)
        
        # Show selection boxes
        selected_quantity_box = screen.ids.selected_quantity_box
        if selected_quantity_box.height == 0:
            Animation(height=dp(50), opacity=1, duration=0.2).start(selected_quantity_box)
        
        total_amount_box = screen.ids.total_amount_box
        if total_amount_box.height == 0:
            Animation(height=dp(50), opacity=1, duration=0.2).start(total_amount_box)
    
   
    def handle_backend_response(self, success, response, service_type):
        """Handle backend responses with profit tracking"""
        if success and response.get('status') == 'success':
            data = response.get('data', {})
            
            # Show success with profit info if available
            if data.get('profit_amount'):
                profit_msg = f"Profit: ₦{data.get('profit_amount', 0):,.2f}"
            else:
                profit_msg = ""
                
            self.show_success_dialog(f"{service_type.title()} successful! {profit_msg}")
            return True
        else:
            error_msg = response.get('message', 'Transaction failed')
            self.show_error_dialog(f"{service_type.title()} failed: {error_msg}")
            return False
    
   
    def process_exam_pin_purchase(self):
        """Process exam PIN purchase with PIN verification"""
        # Validate inputs
        if not self._validate_exam_input():
            return
        
        # Ask for PIN
        def on_pin_success():
            self._execute_exam_pin_purchase()
        
        self._prompt_coupon_then_pin("exam_pin", self.exam_pin_total_amount, on_pin_success)


    def _execute_exam_pin_purchase(self):
        """Execute exam PIN purchase after PIN verified."""
        try:
            amount = self.exam_pin_total_amount  # selling price
            
            # Check wallet balance
            if self.current_user and amount > self.current_user.get('wallet_balance', 0):
                self.show_error_dialog("Insufficient wallet balance")
                self._clear_verified_pin()
                return
            
            self.show_loader("Processing exam PIN purchase...")
            
            payload = {
                'exam_type': self.selected_exam_type,
                'quantity': self.selected_exam_quantity,
                'selling_price': amount,   # ← send selling price to backend
                'pin': self.verified_pin,
                'user_email': self.current_user.get('email'),
                'coupon_code': getattr(self, 'pending_coupon_code', None),
            }
            
            def callback(success, response):
                self.hide_loader()
                self._clear_verified_pin()
                if success and response.get('status') == 'success':
                    data = response.get('data', {})
                    pins = [data.get('pin')] if data.get('pin') else []
                    serial = data.get('serial')
                    profit_amount = data.get('profit_amount', 0)
                    discount = data.get('discount_amount', 0)
                    
                    if pins:
                        self.show_exam_pins_dialog(pins, profit_amount, serial)
                    else:
                        msg = f"{self.selected_exam_type} PIN purchase successful!\nProfit earned: ₦{profit_amount:,.2f}"
                        if discount:
                            msg += f"\nCoupon savings: {self.format_currency(discount)}"
                        self.show_success_dialog(msg)
                    self.update_dashboard()
                    self.root.current = "dashboard"
                    self.reset_exam_pin_selections()
                    self.pending_coupon_code = None
                else:
                    error_msg = response.get('message', 'Exam PIN purchase failed')
                    self.show_error_dialog(f"Exam PIN purchase failed: {error_msg}")
            
            self.backend_api_request('vtpass/exam-pins', 'POST', payload, callback)
            
        except Exception as e:
            self.hide_loader()
            self._clear_verified_pin()
            self.show_error_dialog(f"Exam PIN purchase error: {str(e)}")

   

    def _validate_exam_input(self):
        """Validate exam PIN input fields"""
        if not self.selected_exam_type:
            self.show_error_dialog("Please select an exam type")
            return False
        
        if not self.selected_exam_quantity or self.selected_exam_quantity < 1:
            self.show_error_dialog("Please enter a valid quantity (1-10)")
            return False
        
        return True


    def show_exam_pins_dialog(self, pins, profit_amount, serial=None):
        """Show dialog with generated exam PINs."""
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=dp(20),
            size_hint_y=None,
            height=dp(300)  # increased for serial
        )
        
        content.add_widget(MDLabel(
            text=f"{self.selected_exam_type} PIN(s) Generated Successfully!",
            halign='center',
            bold=True
        ))
        
        content.add_widget(MDLabel(
            text=f"Profit earned: ₦{profit_amount:,.2f}",
            halign='center',
            theme_text_color="Primary"
        ))
        
        # Display PIN
        for i, pin in enumerate(pins):
            pin_box = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(10))
            pin_box.add_widget(MDLabel(text=f"PIN {i+1}:", size_hint_x=0.3))
            pin_box.add_widget(MDLabel(text=pin, bold=True, theme_text_color="Primary", size_hint_x=0.5))
            copy_btn = MDIconButton(icon="content-copy", size_hint_x=0.2, on_release=lambda x, p=pin: self.copy_to_clipboard(p))
            pin_box.add_widget(copy_btn)
            content.add_widget(pin_box)
        
        # Display serial if present
        if serial:
            serial_box = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(10))
            serial_box.add_widget(MDLabel(text="Serial:", size_hint_x=0.3))
            serial_box.add_widget(MDLabel(text=serial, bold=True, theme_text_color="Secondary", size_hint_x=0.5))
            copy_btn2 = MDIconButton(icon="content-copy", size_hint_x=0.2, on_release=lambda x, s=serial: self.copy_to_clipboard(s))
            serial_box.add_widget(copy_btn2)
            content.add_widget(serial_box)
        
        dialog = MDDialog(
            title="Exam PINs Generated",
            type="custom",
            content_cls=content,
            buttons=[MDFlatButton(text="CLOSE", on_release=lambda x: dialog.dismiss())],
            radius=[20, 7, 20, 7]
        )
        dialog.open()
     

    def generate_and_deliver_exam_pins(self):
        """Generate exam PINs and deliver to user"""
        import random
        import string
        
        # Generate unique PINs
        pins = []
        for i in range(self.selected_exam_quantity):
            pin = ''.join(random.choices(string.digits, k=12))
            pins.append(pin)
        
        # Create transaction record
        if self.current_user:
            user_id = list(self.users.keys())[list(self.users.values()).index(self.current_user)]
            
            # Deduct from wallet
            self.users[user_id]['wallet_balance'] -= self.exam_pin_total_amount
            self.current_user = self.users[user_id]
            
            # Save transaction
            transaction_id = str(len(self.transactions) + 1)
            transaction = {
                "user_id": user_id,
                "type": "Exam PIN",
                "exam_type": self.selected_exam_type,
                "quantity": self.selected_exam_quantity,
                "amount": f"₦{self.exam_pin_total_amount:,}",
                "pins": pins,
                "status": "Successful",
                "date": datetime.now().strftime("%B %d, %Y %I:%M:%S %p")
            }
            self.transactions[transaction_id] = transaction
            
            self.save_users()
            self.save_transactions()
            self.update_dashboard()
            
            # Show success with PINs
            self.show_exam_pins_dialog(pins)

   

    def show_exam_pin_help(self):
        """Show help dialog for exam PIN purchase"""
        dialog = MDDialog(
            title="Exam PIN Purchase Help",
            text=(
                "How to purchase exam PINs:\n"
                "1. Select the exam type (WAEC, NECO, JAMB, NABTEB)\n"
                "2. Choose the quantity of PINs needed\n"
                "3. Click CONTINUE to complete payment\n"
                "4. Your PINs will be generated and displayed after payment\n\n"
                "Prices:\n"
                "WAEC/NECO/NABTEB: ₦3,500 per PIN\n"
                "JAMB: ₦5,000 per PIN"
            ),
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: dialog.dismiss()
                )
            ],
            radius=[20, 7, 20, 7]
        )
        dialog.open()

    def buy_exam_pin(self):
        """Navigate to exam PIN screen"""
        if not self.current_user:
            self.show_error_dialog("Please login to purchase exam PINs")
            self.root.current = "login"
            return
        
        self.reset_exam_pin_selections()
        self.root.current = "exam_pin"

    
    def reset_exam_pin_selections(self):
        """Reset all exam PIN selections"""
        self.selected_exam_type = ""
        self.selected_exam_quantity = 0
        self.exam_pin_total_amount = 0
        
        if hasattr(self, 'root') and self.root:
            screen = self.root.get_screen("exam_pin")
            if screen:
                # Reset UI elements
                screen.ids.selected_exam_type_box.height = 0
                screen.ids.selected_exam_type_box.opacity = 0
                screen.ids.quantity_input.text = ""
                screen.ids.quantity_input.error = False
                screen.ids.quantity_input.helper_text = "Enter quantity (1-10)"
                screen.ids.quantity_input.disabled = True
                screen.ids.quantity_input.opacity = 0.5
                screen.ids.selected_quantity_box.height = 0
                screen.ids.selected_quantity_box.opacity = 0
                screen.ids.total_amount_box.height = 0
                screen.ids.total_amount_box.opacity = 0
                
                # Reset button colors
                for child in screen.ids.exam_type_grid.children:
                    child.md_bg_color = [0.95, 0.95, 0.95, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1]
                                            
            
    def _initiate_paystack_card_payment(self):
        """Updated method to use our backend"""
        self.process_payment_via_backend(
            amount=self.payment_amount,
            description=self.payment_description,
            payment_method="card"
        )

    def _initiate_bank_transfer(self):
        """Updated method to use our backend"""
        self.process_payment_via_backend(
            amount=self.payment_amount,
            description=self.payment_description,
            payment_method="bank_transfer"
        )

    def _initiate_ussd_payment(self):
        """Updated method to use our backend"""
        self.process_payment_via_backend(
            amount=self.payment_amount,
            description=self.payment_description,
            payment_method="ussd"
        )
    
    
    
    def quick_backend_test(self):
        """Quick test to see backend connection status"""
        try:
            import requests
            print(f"🧪 Testing backend at: {self.backend_url}")
            
            # Test health endpoint
            health_url = f"{self.backend_url}/health"
            print(f"🧪 Testing: {health_url}")
            
            response = requests.get(health_url, timeout=10)
            print(f"🧪 Response status: {response.status_code}")
            print(f"🧪 Response content: {response.text}")
            
            if response.status_code == 200:
                self.show_success_dialog("Backend is working! ✅")
                return True
            else:
                self.show_error_dialog(f"Backend error: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            self.show_error_dialog("Cannot connect to backend. Make sure server is running on localhost:10000")
            return False
        except Exception as e:
            self.show_error_dialog(f"Connection error: {str(e)}")
            return False
            
    
    def initialize_payment(self, email, amount, service_type, service_details, callback=None, callback_url=None):
        """
        Initialize payment through our backend.
        Calls `callback(success, payment_data)` when done.
        """
        if self.payment_processing:
            self.show_error_dialog("Another payment is already in process")
            if callback:
                callback(False, None)
            return

        self.payment_processing = True
        self.show_loader("Initializing payment...")

        payload = {
            "email": email,
            "amount": amount,
            "service_type": service_type,
            "service_details": service_details
        }
        if callback_url:
            payload["callback_url"] = callback_url

        def on_success(req, result):
            self.hide_loader()
            self.payment_processing = False
            if result and result.get('status') == 'success':
                payment_data = result['data']
                self.current_payment_reference = payment_data.get('reference')
                if callback:
                    callback(True, payment_data)
            else:
                error_msg = result.get('message', 'Payment initialization failed') if result else 'No response'
                self.show_error_dialog(f"Payment failed: {error_msg}")
                if callback:
                    callback(False, None)

        def on_failure(req, error):
            self.hide_loader()
            self.payment_processing = False
            self.show_error_dialog(f"Network error: {error}")
            if callback:
                callback(False, None)

        def on_error(req, error):
            self.hide_loader()
            self.payment_processing = False
            self.show_error_dialog(f"Connection error: {error}")
            if callback:
                callback(False, None)

        UrlRequest(
            f"{self.backend_url}/api/payment/initialize",
            on_success=on_success,
            on_failure=on_failure,
            on_error=on_error,
            req_headers={'Content-Type': 'application/json'},
            req_body=json.dumps(payload),
            timeout=30
        )

    def verify_payment(self, reference):
        """Verify payment status through our backend"""
        try:
            def on_success(req, result):
                if result.get('status') == 'success':
                    return result
                else:
                    return {"status": "error", "message": result.get('error', 'Verification failed')}
                    
            def on_failure(req, error):
                return {"status": "error", "message": f"Verification failed: {error}"}
                
            def on_error(req, error):
                return {"status": "error", "message": f"Network error: {error}"}
                
            UrlRequest(
                f"{self.backend_url}/api/payment/verify/{reference}",
                on_success=on_success,
                on_failure=on_failure,
                on_error=on_error,
                timeout=30
            )
            
        except Exception as e:
            return {"status": "error", "message": f"Error: {str(e)}"}

    def get_payment_methods(self):
        """Get available payment methods from backend"""
        try:
            def on_success(req, result):
                if result.get('status') == 'success':
                    return result.get('data', {})
                return {}
                
            def on_failure(req, error):
                return {}
                
            def on_error(req, error):
                return {}
                
            UrlRequest(
                f"{self.backend_url}/api/payment/methods",
                on_success=on_success,
                on_failure=on_failure,
                on_error=on_error,
                timeout=30
            )
            
        except Exception:
            return {}  
    
    
    def process_payment_via_backend(self, amount, description, payment_method="card"):
        """Process payment using our backend with proper error handling"""
        if not self.current_user:
            email = "guest@example.com"
        else:
            email = self.current_user.get('email', 'guest@example.com')

        webhook_url = f"{self.backend_url}/api/payment/webhook/paystack"

        def on_payment_initialized(success, payment_data):
            if success and payment_data and payment_data.get('authorization_url'):
                # Open payment URL in browser
                import webbrowser
                webbrowser.open(payment_data['authorization_url'])
                self.show_success_dialog("Please complete payment in your browser")
                self.current_payment_reference = payment_data.get('reference', '')
                # Start checking payment status after 10 seconds
                Clock.schedule_once(
                    lambda dt: self.check_payment_status(payment_data['reference']),
                    10
                )
            else:
                self.show_error_dialog("Payment initialization failed")

        self.initialize_payment(
            email=email,
            amount=amount,
            service_type="wallet_funding",
            service_details={
                "description": description,
                "user_id": self.current_user.get('id') if self.current_user else "guest",
                "payment_method": payment_method
            },
            callback=on_payment_initialized,
            callback_url=webhook_url
        )

    def check_payment_status(self, reference):
        """Check payment status with retry logic"""
        if not reference:
            self.show_error_dialog("No payment reference found")
            return
            
        self.show_loader("Verifying payment...")
        
        def verify():
            result = self.verify_payment(reference)
            self.hide_loader()
            
            if result and result.get('status') == 'success':
                payment_status = result.get('data', {}).get('status')
                
                if payment_status == 'success':
                    self.show_success_dialog("Payment verified successfully! Wallet funded.")
                    # Update wallet balance
                    self.update_dashboard()
                    return True
                else:
                    # Payment not yet confirmed, retry after 15 seconds
                    Clock.schedule_once(
                        lambda dt: self.check_payment_status(reference),
                        15
                    )
                    return False
            else:
                error_msg = result.get('message', 'Payment verification failed') if result else 'Verification failed'
                self.show_error_dialog(f"Payment verification failed: {error_msg}")
                return False
        
        # Run verification in a thread to avoid blocking UI
        import threading
        thread = threading.Thread(target=verify)
        thread.daemon = True
        thread.start()


    def show_profile_details(self, from_screen="profile"):

        """Show profile details while remembering previous screen"""

        self._previous_screen = from_screen  # Store where we came from

        if hasattr(self, 'root') and self.root:

            self.root.transition.direction = "left"

            self.root.current = "profile_details"


    def handle_back_button(self, window, key, *args):
        if key == 27:
            back_map = {
                'profile_details': 'profile',
                'airtime_topup':   'dashboard',
                'data_purchase':   'dashboard',
                'electricity':     'dashboard',
                'cable_tv':        'dashboard',
                'exam_pin':        'dashboard',
                'funding':         'dashboard',
                'history':         'dashboard',
                'profile':         'dashboard',
                'referral':        'dashboard',
                'profit':          'dashboard',
                'withdraw':        'profit',
                # FIX: these screens were missing from back_map entirely,
                # so pressing back on any of them fell through to Android's
                # default behavior and exited the app instantly instead of
                # returning to the dashboard like every other screen does.
                'cashback':        'dashboard',
                'spin':            'dashboard',
                'coupons':         'dashboard',
                'merchant':        'dashboard',
                'cards':           'dashboard',
                'reminders':       'dashboard',
                'compare':         'dashboard',
                'gamification':    'dashboard',
            }
            current = self.root.current
            if current in back_map:
                self.root.transition.direction = "right"
                self.root.current = back_map[current]
                return True

            # Nowhere further "back" to go (dashboard, or any screen not
            # listed above) -- require a second press within 2 seconds
            # before actually letting the app exit, so a single accidental
            # tap doesn't close it. Standard Android "press back again to
            # exit" pattern.
            now = time.time()
            last_press = getattr(self, '_last_back_press_time', 0)
            if now - last_press < 2.0:
                return False  # let the system perform the actual exit
            self._last_back_press_time = now
            self.show_toast("Press back again to exit")
            return True
        return False

    def show_toast(self, message, duration=2.0):
        """Lightweight, non-blocking bottom toast for brief hints (like
        'Press back again to exit') that shouldn't interrupt the user the
        way a full dialog would."""
        try:
            toast = MDCard(
                orientation='horizontal', padding=dp(14),
                size_hint=(None, None),
                size=(min(Window.width - dp(40), dp(320)), dp(48)),
                pos_hint={"center_x": 0.5},
                y=dp(70),
                radius=[24], elevation=4,
                md_bg_color=[0.15, 0.15, 0.15, 0.95],
            )
            toast.add_widget(MDLabel(
                text=message, halign="center",
                theme_text_color="Custom", text_color=[1, 1, 1, 1],
            ))
            toast.opacity = 0
            Window.add_widget(toast)
            Animation(opacity=1, duration=0.2).start(toast)

            def _dismiss(*_):
                anim_out = Animation(opacity=0, duration=0.2)
                anim_out.bind(on_complete=lambda *_: Window.remove_widget(toast))
                anim_out.start(toast)

            Clock.schedule_once(_dismiss, duration)
        except Exception as e:
            print(f"show_toast error: {e}")
        
   

    def format_date(self, date_str):

        """Format date string for display"""

        if not date_str:

            return "Unknown"

        try:

            dt = datetime.strptime(date_str, "%Y-%m-%d")

            return dt.strftime("%b %d, %Y")

        except:

            return "Unknown"



    def format_datetime(self, datetime_str):

        """Format datetime string for display"""

        if not datetime_str:

            return "Never"

        try:

            dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

            return dt.strftime("%b %d, %Y at %I:%M %p")

        except:

            return "Recently"



    def show_profile_details(self):

        """Update and show profile details screen"""

        if not hasattr(self, 'root') or not self.root:

            return

        

        # Update last login time

        if self.current_user:

            user_id = next((k for k,v in self.users.items() if v == self.current_user), None)

            if user_id:

                self.users[user_id]['last_login'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                self.current_user = self.users[user_id]

                self.save_users()

        

        # Apply theme-based colors

        screen = self.root.get_screen("profile_details")

        if self.theme_cls.theme_style == "Dark":

            screen.ids.profile_card.md_bg_color = [0.2, 0.2, 0.2, 1]

        else:

            screen.ids.profile_card.md_bg_color = [1, 1, 1, 1]

        

        self.root.transition.direction = "left"

        self.root.current = "profile_details"

    

    def show_change_password(self):

        """Show change password dialog"""

        content = MDBoxLayout(

            orientation='vertical',

            spacing=dp(15),

            size_hint_y=None,

            height=dp(200),

            padding=dp(10)

        )

        

        # Create text fields

        current_password = MDTextField(

            hint_text="Current Password",

            icon_left="key",

            password=True,

            mode="rectangle"

        )

        

        new_password = MDTextField(

            hint_text="New Password", 

            icon_left="key",

            password=True,

            mode="rectangle"

        )

        

        confirm_password = MDTextField(

            hint_text="Confirm New Password",

            icon_left="key-change",

            password=True,

            mode="rectangle"

        )

        

        # Add fields to content

        content.add_widget(current_password)

        content.add_widget(new_password)

        content.add_widget(confirm_password)

        

        dialog = MDDialog(

            title="Change Password",

            type="custom",

            content_cls=content,

            buttons=[

                MDFlatButton(

                    text="CANCEL",

                    theme_text_color="Custom",

                    text_color=self.theme_cls.primary_color,

                    on_release=lambda x: dialog.dismiss()

                ),

                MDRaisedButton(

                    text="UPDATE",

                    md_bg_color=self.theme_cls.primary_color,

                    on_release=lambda x: self.update_password(

                        dialog,

                        current_password.text,

                        new_password.text,

                        confirm_password.text

                    )

                )

            ],

            radius=[20, 7, 20, 7]

        )

        dialog.open()



    def update_password(self, dialog, current_pw, new_pw, confirm_pw):

        """Handle password update logic"""

        dialog.dismiss()

        

        if not self.current_user:

            self.show_error_dialog("No user logged in")

            return

        

        # Validate inputs

        if not current_pw or not new_pw or not confirm_pw:

            self.show_error_dialog("Please fill all fields")

            return

        

        if new_pw != confirm_pw:

            self.show_error_dialog("New passwords don't match")

            return

        

        if len(new_pw) < 6:

            self.show_error_dialog("Password must be at least 6 characters")

            return

        

        # Verify current password

        if hash_password(current_pw) != self.current_user.get('password'):

            self.show_error_dialog("Current password is incorrect")

            return

        

        try:

            # Find user in users dict

            user_id = None

            for uid, user in self.users.items():

                if user == self.current_user:

                    user_id = uid

                    break

            

            if user_id:

                # Update password

                self.users[user_id]['password'] = hash_password(new_pw)

                self.current_user = self.users[user_id]

                

                # Save changes

                self.save_users()

                self.show_success_dialog("Password updated successfully!")

            else:

                self.show_error_dialog("User not found")

                

        except Exception as e:

            self.show_error_dialog(f"Error updating password: {str(e)}")

               

    def show_edit_profile(self):

        """Show edit profile dialog"""

        if not self.current_user:

            return

        

        # Create form fields

        name_field = MDTextField(

            hint_text="Full Name",

            icon_left="account-outline",

            text=self.current_user.get('name', ''),

            mode="rectangle",

            size_hint_x=0.9

        )

        

        email_field = MDTextField(

            hint_text="Email",

            icon_left="email-outline",

            text=self.current_user.get('email', ''),

            mode="rectangle",

            size_hint_x=0.9

        )

        

        phone_field = MDTextField(

            hint_text="Phone Number",

            icon_left="phone-outline",

            text=self.current_user.get('phone', ''),

            mode="rectangle",

            size_hint_x=0.9,

            input_type='number'

        )

        

        content = MDBoxLayout(

            orientation='vertical',

            spacing=dp(15),

            size_hint_y=None,

            height=dp(250)

        )

        

        content.add_widget(name_field)

        content.add_widget(email_field)

        content.add_widget(phone_field)

        

        dialog = MDDialog(

            title="Edit Profile",

            type="custom",

            content_cls=content,

            buttons=[

                MDFlatButton(

                    text="CANCEL",

                    theme_text_color="Custom",

                    text_color=self.theme_cls.primary_color,

                    on_release=lambda x: dialog.dismiss()

                ),

                MDRaisedButton(

                    text="SAVE",

                    md_bg_color=self.theme_cls.primary_color,

                    on_release=lambda x: self.save_profile_changes(

                        dialog, 

                        name_field.text,

                        email_field.text,

                        phone_field.text

                    )

                )

            ],

            radius=[20, 7, 20, 7]

        )

        dialog.open()



    def save_profile_changes(self, dialog, name, email, phone):

        """Save profile changes to user data"""

        dialog.dismiss()

        

        if not self.current_user:

            return

        

        # Validate inputs

        if not name or not email or not phone:

            self.show_error_dialog("Please fill all fields")

            return

        

        if not is_valid_email(email):

            self.show_error_dialog("Invalid email address")

            return

        

        if not is_valid_phone(phone):

            self.show_error_dialog("Invalid phone number")

            return

        

        try:

            # Find user in users dict

            user_id = None

            for uid, user in self.users.items():

                if user == self.current_user:

                    user_id = uid

                    break

            

            if user_id:

                # Update user data

                self.users[user_id]['name'] = name

                self.users[user_id]['email'] = email.lower()

                self.users[user_id]['phone'] = phone

                

                # Update current user reference

                self.current_user = self.users[user_id]

                

                # Save changes

                self.save_users()

                

                # Update profile screen

                self.show_profile_details()

                

                self.show_success_dialog("Profile updated successfully!")

            else:

                self.show_error_dialog("User not found")

                

        except Exception as e:

            self.show_error_dialog(f"Error saving profile: {str(e)}")

   

    def generate_otp(self):

        """Generate a 6-digit OTP"""

        return str(random.randint(100000, 999999))

  
  
    def _fallback_registration(self, email, phone):
        """Fallback registration when OTP fails"""
        
        self.hide_loader()
        self.show_error_dialog(
            "Registration failed. Please check your internet connection and try again."
        )
                       
        self.otp_email = email
        self.otp_phone = phone
        self.otp_expiry = datetime.now() + timedelta(minutes=10)
        
        # Show OTP screen with fallback message
        otp_screen = self.root.get_screen("otp_verification")       
        self.root.current = "otp_verification"
        self.hide_loader()

        
    def send_otp(self, email, phone):
        """
        Sends a real OTP to the user's phone number using the Termii API.
        """
        # 1. Generate OTP and save details
        self.otp_code = self.generate_otp()
        self.otp_email = email
        self.otp_phone = phone
        self.otp_expiry = datetime.now() + timedelta(minutes=10)  # OTP expires in 10 mins

        # 2. Prepare the SMS message
        message = f"Your Cheap4u technology verification code is {self.otp_code}. It expires in 10 minutes."

        # 3. Termii API Configuration - ADD YOUR API KEY HERE
        termii_api_key = os.getenv('TERMII_API_KEY', 'TLyour_actual_termii_api_key_here')  # FIX: Add your actual API key
        termii_url = "https://api.ng.termii.com/api/sms/send"  # Termii SMS Endpoint
        sender_id = "Cheap4uApp"  # Change this to your APPROVED Sender ID from Termii

        # 4. Prepare the data to send (payload)
        payload = {
            "to": phone,  # Recipient's phone number
            "from": sender_id,  # Your approved Sender ID
            "sms": message,  # The message text
            "type": "plain",  # Type of message
            "channel": "generic",  # Channel
            "api_key": termii_api_key,  # Your API Key - FIXED
        }

        headers = {
            'Content-Type': 'application/json',
        }

        # 5. Show loading dialog
        self.show_loader("Sending OTP...")

        # 6. Try to send the SMS
        try:
            response = requests.post(termii_url, json=payload, headers=headers)
            response_data = response.json()

            # Check if SMS was sent successfully
            if response.status_code == 200 and response_data.get('message') == 'Successfully Sent':
                # SUCCESS: Show OTP screen
                self.hide_loader()
                otp_screen = self.root.get_screen("otp_verification")
                otp_screen.ids.otp_email_or_phone.text = f"to {phone}"  # Show user where OTP was sent
                self.root.current = "otp_verification"
                self.show_success_dialog("OTP sent successfully!")
            else:
                # FAILED: Show error
                self.hide_loader()
                error_msg = response_data.get('message', 'Failed to send OTP. Please try again.')
                self.show_error_dialog(f"Error: {error_msg}")
                # Fallback: proceed without OTP for testing
                self._fallback_registration(email, phone)

        except Exception as e:
            # NETWORK ERROR - Fallback to direct registration
            self.hide_loader()
            print(f"OTP sending failed, using fallback: {str(e)}")
            self._fallback_registration(email, phone)

    
    def complete_registration(self):
        """Finalizes the user registration after OTP verification."""
        self.hide_loader()
        
        try:
            # Get the registration data from the pending session
            reg_data = self.pending_registration

            # Create the user account
            user_id = str(len(self.users) + 1)
            self.users[user_id] = {
                'id': user_id,
                'name': reg_data['name'],
                'email': reg_data['email'].lower(),
                'phone': reg_data['phone'],
                'password': hash_password(reg_data['password']),
                'wallet_balance': 0.0,  # Initialize wallet
                'referral_balance': 0.0,
                'joined_date': datetime.now().strftime("%Y-%m-%d"),
                'last_login': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'verified': True  # Mark as verified since OPassed
            }

            # Save the new user
            self.save_users()

            # Clear the pending registration data
            if hasattr(self, 'pending_registration'):
                del self.pending_registration

            # Show success and go to login
            self.show_success_dialog("Registration successful! Please login.")
            self.root.current = "login"

        except Exception as e:
            self.show_error_dialog(f"Registration failed: {str(e)}")

   

    def show_loading(self, message="Processing..."):

           if not hasattr(self, '_loading_dialog'):

                self._loading_dialog = MDDialog(

                   title="",

                   type="custom",

                   content_cls=MDBoxLayout(

                       orientation='vertical',

                       spacing=dp(15),

                       padding=dp(20),

                       size_hint_y=None,

                       height=dp(100),

                       children=[

                          MDSpinner(

                              size_hint=(None, None),

                              size=(dp(46), dp(46)),

                              pos_hint={'center_x': 0.5},

                              active=True

                    ),

                         MDLabel(

                             text=message,

                             halign='center'

                    )

                ]

            ),

                   size_hint=(0.8, None),

                   height=dp(150),

                   auto_dismiss=False

        )

           else:

                  self._loading_dialog.content_cls.children[1].text = message

           self._loading_dialog.open()

    def show_notifications(self):

           """Show notifications dialog"""

           dialog = MDDialog(

               title="Notifications",

               text="You have no new notifications" if self.current_user else "Please login to view notifications",

               buttons=[

                    MDFlatButton(

                        text="OK",

                        theme_text_color="Custom",

                        text_color=self.theme_cls.primary_color,

                        on_release=lambda x: dialog.dismiss()

            )

        ],

               radius=[20, 7, 20, 7]

    )

           dialog.open()
               

    def show_forgot_password(self):
        """Show forgot password dialog — user enters email."""
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton, MDRaisedButton
        from kivymd.uix.textfield import MDTextField
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivy.metrics import dp

        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=[dp(10), dp(10)],
            size_hint_y=None,
            height=dp(100),
        )
        self._reset_email_field = MDTextField(
            hint_text="Enter your email address",
            icon_left="email-outline",
            mode="rectangle",
            size_hint_x=1,
        )
        content.add_widget(self._reset_email_field)

        self._forgot_dialog = MDDialog(
            title="Reset Password",
            text="We will send an OTP to your phone number",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: self._forgot_dialog.dismiss(),
                ),
                MDRaisedButton(
                    text="SEND OTP",
                    md_bg_color=self.theme_cls.primary_color,
                    on_release=lambda x: self._request_reset_otp(),
                ),
            ],
            radius=[20, 7, 20, 7],
        )
        self._forgot_dialog.open()
           
    def _request_reset_otp(self):
        """Send OTP to user's phone for password reset."""
        email = self._reset_email_field.text.strip() if hasattr(self, '_reset_email_field') else ''
        if not email:
            self.show_error_dialog("Please enter your email address")
            return

        if hasattr(self, '_forgot_dialog'):
            self._forgot_dialog.dismiss()

        self.show_loader("Sending OTP...")

        import json
        from kivy.network.urlrequest import UrlRequest

        def on_success(req, result):
            self.hide_loader()
            if result.get('status') == 'success':
                data = result.get('data', {})
                self._reset_user_id = data.get('user_id')
                phone = data.get('phone', '')
                self.show_success_dialog(
                    f"OTP sent to your phone number ending in {phone[-4:] if phone else '****'}.\n"
                    f"Check your SMS."
                )
                # Show OTP + new password dialog after 1.5 seconds
                Clock.schedule_once(lambda dt: self._show_reset_form(), 1.5)
            else:
                self.show_error_dialog(
                    result.get('message', 'Could not send OTP. Check your email.')
                )

        def on_failure(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Network error: {error}")

        def on_error(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Connection error: {error}")

        UrlRequest(
            f"{self.backend_url}/api/auth/forgot-password",
            on_success=on_success,
            on_failure=on_failure,
            on_error=on_error,
            req_headers={'Content-Type': 'application/json'},
            req_body=json.dumps({'email': email}),
            timeout=20,
        )           

    def _submit_password_reset(self):
        """Verify OTP and set new password."""
        otp = self._reset_otp_field.text.strip() if hasattr(self, '_reset_otp_field') else ''
        password = self._reset_pass_field.text.strip() if hasattr(self, '_reset_pass_field') else ''
        confirm = self._reset_pass2_field.text.strip() if hasattr(self, '_reset_pass2_field') else ''
        user_id = getattr(self, '_reset_user_id', None)

        if not otp:
            self.show_error_dialog("Please enter the OTP from your SMS")
            return
        if not password:
            self.show_error_dialog("Please enter a new password")
            return
        if len(password) < 6:
            self.show_error_dialog("Password must be at least 6 characters")
            return
        if password != confirm:
            self.show_error_dialog("Passwords do not match")
            return
        if not user_id:
            self.show_error_dialog("Session expired. Please start again.")
            return

        if hasattr(self, '_reset_dialog'):
            self._reset_dialog.dismiss()

        self.show_loader("Resetting password...")

        import json
        from kivy.network.urlrequest import UrlRequest

        def on_success(req, result):
            self.hide_loader()
            if result.get('status') == 'success':
                data = result.get('data', {})
                # Auto-login with returned token
                if data.get('session_token'):
                    self.session_token = data['session_token']
                    self.current_user = data.get('user', {})
                    self.update_dashboard()
                    self.root.current = "dashboard"
                self.show_success_dialog("Password reset successfully! You are now logged in.")
            else:
                self.show_error_dialog(
                    result.get('message', 'Failed to reset password. Try again.')
                )
                # Re-open the form
                Clock.schedule_once(lambda dt: self._show_reset_form(), 0.5)

        def on_failure(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Network error: {error}")

        def on_error(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Connection error: {error}")

        UrlRequest(
            f"{self.backend_url}/api/auth/reset-password",
            on_success=on_success,
            on_failure=on_failure,
            on_error=on_error,
            req_headers={'Content-Type': 'application/json'},
            req_body=json.dumps({
                'user_id': user_id,
                'otp_code': otp,
                'new_password': password,
            }),
            timeout=20,
        )

    def _resend_reset_otp(self):
        """Resend reset OTP."""
        user_id = getattr(self, '_reset_user_id', None)
        if not user_id:
            self.show_error_dialog("Session expired. Please start again.")
            return

        if hasattr(self, '_reset_dialog'):
            self._reset_dialog.dismiss()

        # Re-trigger the email input flow
        self.show_forgot_password()                
        
    
    def _show_reset_form(self):
        """Show OTP + new password form after OTP is sent."""
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton, MDRaisedButton
        from kivymd.uix.textfield import MDTextField
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivy.metrics import dp

        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=[dp(10), dp(5)],
            size_hint_y=None,
            height=dp(180),
        )
        self._reset_otp_field = MDTextField(
            hint_text="Enter OTP from SMS",
            icon_left="message-text-outline",
            mode="rectangle",
            input_type='number',
            size_hint_x=1,
        )
        self._reset_pass_field = MDTextField(
            hint_text="New Password (min 6 characters)",
            mode="rectangle",
            icon_left="key",
            password=True,
            size_hint_x=1,
        )
        self._reset_pass2_field = MDTextField(
            hint_text="Confirm New Password",
            mode="rectangle",
            icon_left="key-change",
            password=True,
            size_hint_x=1,
        )
        content.add_widget(self._reset_otp_field)
        content.add_widget(self._reset_pass_field)
        content.add_widget(self._reset_pass2_field)

        self._reset_dialog = MDDialog(
            title="Set New Password",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="RESEND OTP",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: self._resend_reset_otp(),
                ),
                MDRaisedButton(
                    text="RESET",
                    md_bg_color=self.theme_cls.primary_color,
                    on_release=lambda x: self._submit_password_reset(),
                ),
            ],
            radius=[20, 7, 20, 7],
        )
        self._reset_dialog.open()

    def send_reset_link(self, dialog):
        """Legacy method — now routes to real OTP flow."""
        dialog.dismiss()
        self.show_forgot_password()

   
    def show_loading_with_wakeup(self, message="Connecting to server..."):
        """Show loading with wake-up awareness for Render free tier."""
        # Start with normal message
        self.show_loader(message)
        
        # Schedule message update after 5 seconds
        def update_message(dt):
            if hasattr(self, '_loading_dialog') and self._loading_dialog:
                self._loading_dialog.content_cls.children[1].text = "Waking up server...\nThis may take 30-60 seconds"
        
        Clock.schedule_once(update_message, 5)
        
        
    def on_keyboard(self, window, key, *args):
        """Handle keyboard events"""
        if key == 27:  # ESC key / Back button
            if hasattr(self, 'file_manager') and self.file_manager.manager_open:
                self.file_manager.close()
                return True
            # Handle screen back navigation
            if self.root.current == "profile_details":
                self.root.transition.direction = "right"
                self.root.current = hetattr(self, '_previous_screen', 'profile')
                return True
        return False

    

    def exit_file_manager(self, *args):

        self.file_manager.close()

    

    def select_path(self, path):

        self.exit_file_manager()

        toast(f"Selected: {path}")

    

    def format_currency(self, amount):

           try:

                return f"₦{float(amount):,.2f}"

           except:

                return "₦0.00"

    

    def update_theme_colors(self):

        if self.theme_cls.theme_style == "Light":

            self.bg_normal = [0.95, 0.95, 0.95, 1]

            self.bg_light = [1, 1, 1, 1]

            self.primary_light = [0.9, 0.95, 1, 1]

        else:

            self.bg_normal = [0.1, 0.1, 0.1, 1]

            self.bg_light = [0.2, 0.2, 0.2, 1]

            self.primary_light = [0.2, 0.2, 0.4, 1]

    # ── Dark Mode ────────────────────────────────────────────────────

    def _detect_system_theme(self):
        """Returns 'Dark' or 'Light' based on the device's OS-level theme.
        Real detection on Android via Configuration.uiMode (the same
        jnius/autoclass pattern already used elsewhere in this file for
        Android integration). Falls back to 'Light' anywhere detection
        isn't available (desktop dev, iOS) rather than guessing."""
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            config = activity.getResources().getConfiguration()
            UI_MODE_NIGHT_MASK = 0x30
            UI_MODE_NIGHT_YES = 0x20
            is_night = (config.uiMode & UI_MODE_NIGHT_MASK) == UI_MODE_NIGHT_YES
            return "Dark" if is_night else "Light"
        except Exception:
            return "Light"

    def _resolve_theme_style(self, preference):
        """'light'/'dark' map directly; 'system' resolves via OS detection."""
        if preference == 'dark':
            return "Dark"
        if preference == 'system':
            return self._detect_system_theme()
        return "Light"

    def load_app_settings(self):
        """Loads the persisted theme preference (light/dark/system) and
        applies it to theme_cls BEFORE the UI is built, so there's never a
        flash of the wrong theme on launch."""
        self.theme_preference = 'light'
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    data = json.load(f)
                    self.theme_preference = data.get('theme_preference', 'light')
        except Exception as e:
            print(f"load_app_settings error: {e}")

        self.theme_cls.theme_style = self._resolve_theme_style(self.theme_preference)

    def save_app_settings(self):
        try:
            with open(self.settings_file, 'w') as f:
                json.dump({'theme_preference': getattr(self, 'theme_preference', 'light')}, f)
        except Exception as e:
            print(f"save_app_settings error: {e}")

    def apply_theme(self, theme_style, animate=True):
        """Switches theme_cls.theme_style with a smooth cross-fade instead
        of an instant, jarring flip — KivyMD doesn't animate this itself."""
        def _swap(*_):
            self.theme_cls.theme_style = theme_style
            self.update_theme_colors()

        if animate and hasattr(self, 'root') and self.root:
            fade_out = Animation(opacity=0.35, duration=0.12, transition='out_quad')

            def _fade_back_in(*_):
                _swap()
                Animation(opacity=1, duration=0.18, transition='out_quad').start(self.root)

            fade_out.bind(on_complete=_fade_back_in)
            fade_out.start(self.root)
        else:
            _swap()

    def set_theme_preference(self, preference):
        """preference: 'light' | 'dark' | 'system'. Persists immediately
        and applies with a smooth transition."""
        self.theme_preference = preference
        self.save_app_settings()
        self.apply_theme(self._resolve_theme_style(preference))


 
    # Splash timing: a short minimum so the brand mark doesn't just flash
    # (feels broken, not "fast"), and a hard maximum failsafe so a slow
    # device/network can never hold the user on the splash screen.
    SPLASH_MIN_DURATION = 0.6
    SPLASH_MAX_DURATION = 2.0

    def on_start(self):
        """Show the splash instantly, then do all real startup work
        (screen setup, login-status/session check, API warm-up) in the
        background while it's on screen, and navigate away the moment
        that work is done - never waiting on animation timers."""
        try:
            self._splash_routed = False
            self._splash_start_time = time.time()
            self.root.current = "splash"
            self.animate_splash_in()

            # Hard failsafe: guarantees we never sit on the splash screen
            # longer than SPLASH_MAX_DURATION even if something below hangs.
            Clock.schedule_once(lambda dt: self.finish_splash(), self.SPLASH_MAX_DURATION)

            # Let the splash screen paint its first frame before running
            # setup, so there's never a blank/frozen frame before it.
            Clock.schedule_once(lambda dt: self.run_startup_tasks(), 0)
        except Exception as e:
            print(f"on_start error: {e}")
            self.route_to_login_or_pin()

    def animate_splash_in(self):
        """Single, fast, subtle fade-in for the logo/text/loading label.
        No staggered multi-second timeline - everything appears together."""
        try:
            screen = self.root.get_screen("splash")
            widgets = [
                screen.ids.splash_logo,
                screen.ids.splash_welcome,
                screen.ids.splash_subtext,
                screen.ids.splash_loading,
            ]
            for w in widgets:
                w.opacity = 0
                Animation(opacity=1, duration=0.3, transition="out_quad").start(w)
        except Exception as e:
            print(f"animate_splash_in error: {e}")

    def run_startup_tasks(self):
        """Prepares everything the app needs (screen widgets, login/session
        status already loaded in build(), API connection warm-up), then
        routes to the correct screen. Login status was already determined
        in build() via load_quick_pin()/load_users(), so routing just reads
        that state - no extra wait here."""
        try:
            self.load_networks()
            self.setup_airtime_topup_screen()
            self.setup_cable_tv_screen()
            self.setup_electricity_screen()
            self.setup_data_purchase_screen()
            self.setup_exam_pin_screen()
            self.setup_a2c_network_screen()
            # Fire-and-forget backend warm-up; does not block navigation.
            self.initialize_services()
        except Exception as e:
            print(f"run_startup_tasks error: {e}")
        finally:
            elapsed = time.time() - self._splash_start_time
            remaining = max(self.SPLASH_MIN_DURATION - elapsed, 0)
            Clock.schedule_once(lambda dt: self.finish_splash(), remaining)

    def on_resume(self):
        """Called by Kivy when the app returns from the background — a
        good moment to check for any bill reminders that queued up while
        the app wasn't running, and to re-sync the theme if it's set to
        follow the system (the OS theme may have changed while backgrounded)."""
        try:
            self.check_pending_bill_reminders()
        except Exception as e:
            print(f"on_resume reminder check error: {e}")

        try:
            if getattr(self, 'theme_preference', 'light') == 'system':
                resolved = self._resolve_theme_style('system')
                if resolved != self.theme_cls.theme_style:
                    self.apply_theme(resolved)
        except Exception as e:
            print(f"on_resume theme sync error: {e}")

        return True

    def finish_splash(self):
        """Routes away from the splash screen exactly once."""
        if self._splash_routed:
            return
        self._splash_routed = True
        self.route_to_login_or_pin()

    def initialize_services(self):
        """Warms up the API connection in the background. Non-blocking:
        UrlRequest runs on its own thread and never delays navigation."""
        def ok(req, r): print(f"✅ Backend: {r.get('message','OK')}")
        def fail(req, e): print(f"⚠️ Backend not ready: {e}")
        try:
            UrlRequest(f"{self.backend_url}/health", on_success=ok, on_failure=fail, timeout=10)
        except Exception as e:
            print(f"Backend test error: {e}")
    
  

    def setup_data_purchase_screen(self):

        """Enhanced setup for data purchase screen with better error handling and UI"""

        try:

            screen = self.root.get_screen("data_purchase")

            

            # Clear any existing widgets

            screen.ids.data_network_grid.clear_widgets()

            screen.ids.data_type_grid.clear_widgets()

            screen.ids.data_plan_grid.clear_widgets()

            

            # Network providers with proper assets and colors

            networks = [

                {"name": "MTN", "logo": "assets/mtn.png", "color": self.mtn_color},

                {"name": "Airtel", "logo": "assets/airtel.png", "color": self.airtel_color},

                {"name": "Glo", "logo": "assets/glo.png", "color": self.glo_color},

                {"name": "9Mobile", "logo": "assets/9mobile.png", "color": self.mobile9_color}

            ]

            

            # Create network selection cards

            for net in networks:

                card = MDCard(

                    orientation='vertical',

                    size_hint=(None, None),

                    size=(dp(75), dp(75)),

                    elevation=2,

                    on_release=lambda x, n=net["name"]: self.select_data_network(n),

                    md_bg_color=[0.95, 0.95, 0.95, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1],

                    radius=[15]

                )

                

                # Try loading logo, fallback to icon if image not found

                try:

                    logo = FitImage(

                        source=net["logo"],

                        size_hint=(1, 0.7),

                        radius=[15, 15, 15, 15]

                    )

                except:

                    logo = MDIcon(

                        icon="network",

                        size_hint=(1, 0.7),

                        theme_text_color="Custom",

                        text_color=net["color"]

                    )

                

                card.add_widget(logo)

                

                label = MDLabel(

                    text=net["name"],

                    size_hint_y=None,

                    height=dp(10),

                    halign="center",

                    font_style="Caption",

                    theme_text_color="Custom",

                    text_color=net["color"]

                )

                card.add_widget(label)

                

                screen.ids.data_network_grid.add_widget(card)

                

        except Exception as e:

            self.show_error_dialog(f"Error setting up data screen: {str(e)}")

            print(f"Error in setup_data_purchase_screen: {traceback.format_exc()}")


 
    def select_data_network(self, network):
        """Handle data network selection and load plans."""
        try:
            screen = self.root.get_screen("data_purchase")
            
            # Reset all network cards
            for child in screen.ids.data_network_grid.children:
                child.md_bg_color = [0.95,0.95,0.95,1] if self.theme_cls.theme_style=="Light" else [0.2,0.2,0.2,1]
            
            # Highlight selected card
            for child in screen.ids.data_network_grid.children:
                if hasattr(child.children[1], 'text') and child.children[1].text == network:
                    child.md_bg_color = [0.8,0.8,0.8,1] if self.theme_cls.theme_style=="Light" else [0.3,0.3,0.3,1]
                    break
            
            self.selected_data_network = network
            screen.ids.selected_data_network_label.text = network
            
            # Show selection box with animation
            selected_box = screen.ids.selected_data_network_box
            if selected_box.height == 0:
                Animation(height=dp(50), opacity=1, duration=0.2).start(selected_box)
            
            # Reset dependent selections
            self.selected_data_type = ""
            self.selected_data_plan = ""
            self.selected_data_amount = ""
            self.selected_plan_id = ""
            
            # Clear existing plan grid
            screen.ids.data_plan_grid.clear_widgets()
            
           
            # Instead, load data types (as before)
            self.load_data_types(network)
            
            # Reset phone input
            screen.ids.data_phone_input.text = ""
            screen.ids.data_phone_input.error = False
            
        except Exception as e:
            self.show_error_dialog(f"Error selecting network: {str(e)}")

  


    def load_data_types(self, network):
        """Load data types for the selected network."""
        try:
            screen = self.root.get_screen("data_purchase")
            type_grid = screen.ids.data_type_grid
            type_grid.clear_widgets()

            data_types = {
                "MTN": [
                    {"name": "SME",       "color": [0.1, 0.6, 1.0, 1]},
                    {"name": "Gifting",   "color": [0.8, 0.2, 0.8, 1]},
                    {"name": "Corporate", "color": [0.9, 0.5, 0.1, 1]},
                ],
                "Airtel": [
                    {"name": "SME",     "color": [0.9, 0.3, 0.3, 1]},
                    {"name": "Gifting", "color": [0.2, 0.8, 0.2, 1]},
                ],
                "Glo": [
                    {"name": "Corporate", "color": [0.9, 0.5, 0.1, 1]},
                    {"name": "Gifting",   "color": [0.8, 0.2, 0.8, 1]},
                ],
                "9Mobile": [
                    # NOTE: there are currently NO 9Mobile data plans in the
                    # database at all (this predates these changes) - these
                    # tabs will show an empty list until 9Mobile plan_ids are
                    # added to init_plans.py.
                    {"name": "SME",     "color": [0.1, 0.6, 1.0, 1]},
                    {"name": "Gifting", "color": [0.8, 0.2, 0.8, 1]},
                ],
            }

            for dt in data_types.get(network, []):
                btn = MDRectangleFlatButton(
                    text=dt["name"],
                    size_hint=(None, None),
                    width=dp(90),
                    height=dp(50),
                    line_color=dt["color"],
                    text_color=dt["color"],
                    font_size='12sp',
                    on_release=lambda x, t=dt["name"]: self.select_data_type(t),
                )
                type_grid.add_widget(btn)

        except Exception as e:
            print(f"load_data_types error: {e}")

    
    def select_data_type(self, data_type):
        """Handle data type selection and load plans for the selected network."""
        try:
            screen = self.root.get_screen("data_purchase")
            
            # Reset all type buttons
            for child in screen.ids.data_type_grid.children:
                child.md_bg_color = [1,1,1,1] if self.theme_cls.theme_style=="Light" else [0.2,0.2,0.2,1]
                child.text_color = child.line_color
            
            # Highlight selected button
            for child in screen.ids.data_type_grid.children:
                if child.text == data_type:
                    child.md_bg_color = child.line_color
                    child.text_color = [1,1,1,1]
                    break
            
            self.selected_data_type = data_type
            screen.ids.selected_data_type_label.text = data_type
            
            # Show selection box
            selected_box = screen.ids.selected_data_type_box
            if selected_box.height == 0:
                Animation(height=dp(50), opacity=1, duration=0.2).start(selected_box)
            
            self.fetch_data_plans(self.selected_data_network, self.selected_data_type)
            
            # Show plan section
            plan_scroll = screen.ids.data_plan_grid.parent
            if plan_scroll.height == 0:
                Animation(height=dp(200), opacity=1, duration=0.2).start(plan_scroll)
                
        except Exception as e:
            self.show_error_dialog(f"Error selecting data type: {str(e)}")
   
    def safe_get(self, response, key, default=None):
        """Safely get a value from a response that might be a string or dict"""
        if isinstance(response, dict):
            return response.get(key, default)
        return default

    def get_response_message(self, response, default="Unknown error"):
        """Safely extract message from response"""
        if isinstance(response, dict):
            return response.get("message", default)
        elif isinstance(response, str):
            return response
        return default

    def get_response_data(self, response, default=None):
        """Safely extract data from response"""
        if isinstance(response, dict):
            return response.get("data", default)
        return default

    def get_fallback_data_plans(self, network, data_type):
        """Provide fallback data plans if API is unavailable"""
        fallback_plans = {
            "MTN": {
                "SME": [
                    {"name": "SME 100MB", "price": 100, "validity": "1 day"},
                    {"name": "500MB", "price": 200, "validity": "1 day"},
                    {"name": "1GB", "price": 350, "validity": "1 day"}
                ],
                "Corporate": [
                    {"name": "1GB", "price": 1000, "validity": "30 days"},
                    {"name": "2GB", "price": 1500, "validity": "30 days"}
                ]
            },
            "Airtel": {
                "SME": [
                    {"name": "100MB", "price": 100, "validity": "1 day"},
                    {"name": "500MB", "price": 200, "validity": "1 day"}
                ]
            }
        }
        
        return fallback_plans.get(network, {}).get(data_type, [])          
   

#class app(app):
    def show_security(self):
        """Show security options"""
        dialog = MDDialog(
            title="Security",
            text=(
                "Security Options:\n\n"
                "• Set Transaction PIN — Profile → Set PIN\n"
                "• Change Password — Profile → Change Password\n"
                "• Always logout after use\n"
                "• Never share your PIN or password"
            ),
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: dialog.dismiss()
                )
            ],
            radius=[20, 7, 20, 7]
        )
        dialog.open()

    def show_pricing(self):
        """Show pricing information dialog"""
        dialog = MDDialog(
            title="Our Pricing",
            text=(
                "Airtime: Buy at discount prices\n\n"
                "Data Bundles:\n"
                "• MTN, Airtel, Glo, 9Mobile\n"
                "• SME & Gifting plans available\n\n"
                "Electricity: All DISCOs supported\n\n"
                "Cable TV: DSTV, GOTV, Startimes\n\n"
                "Exam PINs: WAEC, NECO, JAMB, NABTEB\n\n"
                "Fund your wallet and start saving!"
            ),
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: dialog.dismiss()
                )
            ],
            radius=[20, 7, 20, 7]
        )
        dialog.open()    
            

    def validate_data_purchase(self):

        """Comprehensive validation for data purchase"""

        try:

            if not hasattr(self, 'root') or self.root is None:

                return False

                

            screen = self.root.get_screen("data_purchase")

            phone = screen.ids.data_phone_input.text

            

            # Check all required selections

            if not all([

                self.selected_data_network,

                self.selected_data_type,

                self.selected_data_plan,

                len(phone) == 11 and phone.isdigit()

            ]):

                return False

            

            # Validate phone number matches selected network

            detected_network = self.determine_network(phone)

            if detected_network != self.selected_data_network:

                screen.ids.data_phone_input.error = True

                screen.ids.data_phone_input.helper_text = f"Number belongs to {detected_network}"

                return False

            

            # Check wallet balance if user is logged in

            if self.current_user:

                try:

                    amount = float(self.selected_data_amount.replace('₦', '').replace(',', ''))

                    if amount > self.current_user.get('wallet_balance', 0):

                        self.show_error_dialog("Insufficient wallet balance")

                        return False

                except:

                    return False

            

            return True

            

        except Exception as e:

            print(f"Validation error: {traceback.format_exc()}")

            return False




    def _finalize_data_purchase(self, dialog, phone, amount):

        """Finalize the purchase after confirmation"""

        dialog.dismiss()

        self.show_loader("Processing data purchase...")

        

        try:

            if not self.current_user:

                self.show_error_dialog("Please login to complete purchase")

                self.root.current = "login"

                return

                

            # Process transaction

            user_id = list(self.users.keys())[list(self.users.values()).index(self.current_user)]

            

            # Deduct from wallet

            self.users[user_id]['wallet_balance'] -= amount

            self.current_user = self.users[user_id]

            

            # Create transaction record

            transaction_id = str(len(self.transactions) + 1)

            transaction = {

                "user_id": user_id,

                "type": "Data",

                "network": self.selected_data_network,

                "plan": self.selected_data_plan,

                "amount": f"₦{amount:,.2f}",

                "phone": phone,

                "status": "Successful",

                "date": datetime.now().strftime("%B %d, %Y %I:%M:%S %p")

            }

            self.transactions[transaction_id] = transaction

            

            # Save data

            self.save_users()

            self.save_transactions()

            

            # Update dashboard

            self.update_dashboard()

            

            # Show success and reset

            self.show_success_dialog("Data purchase successful!")

            self.reset_data_selections()

            self.root.current = "dashboard"

            

        except Exception as e:

            self.show_error_dialog(f"Purchase failed: {str(e)}")

            print(f"Error in _finalize_data_purchase: {traceback.format_exc()}")

            

        finally:

            self.hide_loader()



    def reset_data_selections(self):

        """Reset all data purchase selections"""

        self.selected_data_network = ""

        self.selected_data_type = ""

        self.selected_data_plan = ""

        self.selected_data_amount = ""

        

        try:

            screen = self.root.get_screen("data_purchase")

            

            # Reset network selection

            for child in screen.ids.data_network_grid.children:

                child.md_bg_color = [0.95, 0.95, 0.95, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1]

            

            # Clear other grids

            screen.ids.data_type_grid.clear_widgets()

            screen.ids.data_plan_grid.clear_widgets()

            

            # Reset input fields

            screen.ids.data_phone_input.text = ""

            screen.ids.data_phone_input.error = False

            screen.ids.data_phone_input.helper_text = "Enter 11-digit phone number"

            

            # Hide selection boxes

            screen.ids.selected_data_network_box.height = 0

            screen.ids.selected_data_network_box.opacity = 0

            screen.ids.selected_data_type_box.height = 0

            screen.ids.selected_data_type_box.opacity = 0

            screen.ids.selected_data_plan_box.height = 0

            screen.ids.selected_data_plan_box.opacity = 0

            

            # Hide sections

            screen.ids.data_type_grid.height = 0

            screen.ids.data_type_grid.opacity = 0

            screen.ids.data_plan_grid.parent.height = 0

            screen.ids.data_plan_grid.parent.opacity = 0

            

        except Exception as e:

            print(f"Error resetting data selections: {str(e)}")

    

    def fill_my_data_number(self):

        try:

            if not self.current_user:

                self.show_error_dialog("Please login first")

                return

                

            screen = self.root.get_screen("data_purchase")

            

            # Check if phone input exists

            if not hasattr(screen.ids, 'data_phone_input'):

                self.show_error_dialog("Phone input field not found")

                return

                

            # Check if network is selected

            if not hasattr(self, 'selected_data_network') or not self.selected_data_network:

                self.show_error_dialog("Please select a network first")

                return

                

            # Set phone number

            screen.ids.data_phone_input.text = self.current_user.get('phone', '')

            

            # Update button appearance if exists

            if hasattr(screen.ids, 'myself_btn'):

                screen.ids.myself_btn.md_bg_color = self.theme_cls.primary_color

                screen.ids.myself_btn.text_color = [1, 1, 1, 1]

            

            # Validate the phone number

            self.validate_phone_input(

                self.current_user.get('phone', ''),

                self.selected_data_network

            )

            

        except Exception as e:

            import traceback

            print(f"Error in fill_my_data_number: {traceback.format_exc()}")

            self.show_error_dialog("Failed to fill phone number")



    def show_data_help(self):

        """Show help dialog for data purchase"""

        dialog = MDDialog(

            title="Data Purchase Help",

            text=(

                "1. Select your network provider\n"

                "2. Choose your preferred data type\n"

                "3. Select a data plan\n"

                "4. Enter recipient phone number\n"

                "5. Click CONTINUE to complete purchase\n\n"

                "Note: Phone number must match selected network"

            ),

            buttons=[

                MDFlatButton(

                    text="OK",

                    theme_text_color="Custom",

                    text_color=self.theme_cls.primary_color,

                    on_release=lambda x: dialog.dismiss()

                )

            ],

            radius=[20, 7, 20, 7]

        )

        dialog.open()

    

    def validate_phone_input(self, text, network=None):
        try:
            screen = self.root.current_screen
            input_field = None
            for name in ('phone_input', 'data_phone_input', 'electricity_phone_input'):
                if hasattr(screen.ids, name):
                    input_field = screen.ids[name]
                    break
        except Exception:
            input_field = None

        if not text:
            if input_field:
                input_field.error = False
                input_field.helper_text = "Enter 11-digit phone number"
            return False

        if len(text) != 11 or not text.isdigit():
            if input_field:
                input_field.error = True
                input_field.helper_text = "Must be exactly 11 digits"
            return False

        detected = self.determine_network(text)
        if network and detected and detected != network:
            if input_field:
                input_field.error = True
                input_field.helper_text = f"Number belongs to {detected}, not {network}"
            return False

        if input_field:
            input_field.error = False
            input_field.helper_text = f"Valid {detected} number" if detected else "Valid number"
        return True
  

    def determine_network(self, phone_number):

        """

        Determines the network provider from a Nigerian phone number

        Args:

            phone_number: The 11-digit phone number string

        Returns:

            str: Network name (MTN, Airtel, Glo, 9mobile) or None if unknown

        """

        if not phone_number or len(phone_number) != 11 or not phone_number.isdigit():

            return None

        

        # First 4 digits determine the network

        prefix = phone_number[:4]

        

        # Network prefixes in Nigeria (updated as of 2023)

        network_prefixes = {

            'MTN': ['0803', '0806', '0703', '0706', '0813', '0816', '0810', '0814', '0903', '0906'],

            'Airtel': ['0802', '0808', '0708', '0812', '0701', '0902', '0907'],

            'Glo': ['0805', '0807', '0705', '0815', '0811', '0905'],

            '9mobile': ['0809', '0818', '0817', '0909', '0908']

        }

        

        # Check each network's prefixes

        for network, prefixes in network_prefixes.items():

            if prefix in prefixes:

                return network

        

        return None    

            

    def complete_data_purchase(self, dialog, phone_number):

        dialog.dismiss()

        

        # Create transaction record

        if self.current_user:

            transaction_id = str(len(self.transactions) + 1)

            transaction = {

                "user_id": list(self.users.keys())[list(self.users.values()).index(self.current_user)],

                "type": "Data",

                "network": self.selected_data_network,

                "plan": self.selected_data_plan,

                "amount": self.selected_data_amount,

                "phone": phone_number,

                "status": "Successful",

                "date": datetime.now().strftime("%B %d, %Y %I:%M:%S %p")

            }

            self.transactions[transaction_id] = transaction

            self.save_transactions()

        

        self.show_success_dialog(f"Data purchase of {self.selected_data_amount} successful!")

        self.root.current = "dashboard"

        

        # Reset selections

        self.selected_data_network = ""

        self.selected_data_plan = ""

        self.selected_data_amount = 0

        screen = self.root.get_screen("data_purchase")

        screen.ids.data_phone_input.text = ""

        

        # Reset button colors

        for child in screen.ids.data_network_grid.children:

            child.md_bg_color = [1, 1, 1, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1]

            child.text_color = child.line_color

        

        for child in screen.ids.data_plan_grid.children:

            child.md_bg_color = [1, 1, 1, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1]

        

        # Reset selection boxes

        screen.ids.selected_data_network_box.height = 0

        screen.ids.selected_data_network_box.opacity = 0

        screen.ids.selected_data_plan_box.height = 0

        screen.ids.selected_data_plan_box.opacity = 0



    def setup_electricity_screen(self):

        screen = self.root.get_screen("electricity")

        

        # Setup disco buttons with logos and distinct colors

        discos = [

            {"name": "IKEDC", "logo": "assets/lagos electric.png", "color": self.ikeja_color, "full_name": "Ikeja Electric"},

            {"name": "EKEDC", "logo": "assets/eko electric.png", "color": self.eko_color, "full_name": "Eko Electric"},

            {"name": "IBEDC", "logo": "assets/ibadan electric.png", "color": self.ibadan_color, "full_name": "Ibadan Electric"},

            {"name": "EEDC", "logo": "assets/enugu electric.png", "color": self.enugu_color, "full_name": "Enugu Electric"},

            {"name": "AEDC", "logo": "assets/abuja electric.png", "color": self.abuja_color, "full_name": "Abuja Electric"},

            {"name": "KEDCO", "logo": "assets/kano electric.png", "color": [0.8, 0.4, 0.1, 1], "full_name": "Kano Electric"},

            {"name": "PHED", "logo": "assets/harcourt electric.png", "color": [0.1, 0.7, 0.7, 1], "full_name": "Port Harcourt Electric"},

            {"name": "JED", "logo": "assets/jos electric.png", "color": [0.5, 0.5, 0.5, 1], "full_name": "Jos Electric"}

        ]

        
        disco_grid = screen.ids.disco_grid

        disco_grid.clear_widgets()

        

        for disco in discos:

            # Create a card for each disco with logo

            card = MDCard(

                orientation='vertical',

                size_hint=(None, None),

                size=(dp(75), dp(75)),

                elevation=2,

                on_release=lambda x, d=disco["full_name"]: self.select_electricity_provider(x, d),

                md_bg_color=[0.2, 0.2, 0.2, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1],

                radius=[15]

            )            

            # Add logo image
            
            try:
                logo = FitImage(
                    source=disco["logo"],
                    size_hint=(1, 0.7),
                    radius=[15, 15, 15, 15]
                )
            except Exception:
                logo = MDIcon(
                    icon="lightning-bolt",
                    size_hint=(1, 0.7),
                    theme_text_color="Custom",
                    text_color=disco["color"]
                )
            card.add_widget(logo)

            # Add disco name label

            label = MDLabel(

                text=disco["name"],

                size_hint_y=None,

                height=dp(10),

                halign="center",

                font_style="Caption",

                theme_text_color="Custom",

                text_color=disco["color"]

            )

            card.add_widget(label)

            

            disco_grid.add_widget(card)

        

        # Setup meter type buttons

        meter_types = [

            {"name": "Prepaid", "icon": "cash-fast", "color": [0.1, 0.6, 1, 1]},

            {"name": "Postpaid", "icon": "cash-clock", "color": [0.9, 0.3, 0.3, 1]}

        ]

        

        meter_type_grid = screen.ids.meter_type_grid

        meter_type_grid.clear_widgets()

        

        for meter_type in meter_types:

            btn = MDRectangleFlatButton(

                text=meter_type["name"],

                size_hint=(None, None),

                width=dp(150),

                height=dp(50),

                on_release=lambda x, m=meter_type["name"]: self.select_meter_type(x, m),

                line_color=meter_type["color"],

                text_color=meter_type["color"],

                font_size='12sp'

            )

            btn.icon = meter_type["icon"]

            meter_type_grid.add_widget(btn)

            

    def fill_my_electricity_number(self):

          if self.current_user:

             screen = self.root.get_screen("electricity")

             screen.ids.electricity_phone_input.text = self.current_user['phone']

             screen.ids.myself_btn.md_bg_color = self.theme_cls.primary_color

             screen.ids.myself_btn.text_color = [1, 1, 1, 1]

             self.validate_phone_input(self.current_user['phone'])          

    def select_electricity_provider(self, button, provider):

        screen = self.root.get_screen("electricity")

        

        # Reset all buttons to default color

        for child in screen.ids.disco_grid.children:

            child.md_bg_color = [1, 1, 1, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1]

            child.text_color = child.line_color  # Reset to original color

        

        # Highlight selected button with a slight gradient

        button.md_bg_color = button.line_color

        button.text_color = [1, 1, 1, 1]

        

        self.selected_electricity_provider = provider

        screen.ids.selected_disco_label.text = provider

        

        # Animate the selected provider box

        selected_box = screen.ids.selected_disco_box

        if selected_box.height == 0:

            anim = Animation(height=dp(50), opacity=1, duration=0.2)

            anim.start(selected_box)

    

    def select_meter_type(self, button, meter_type):

        screen = self.root.get_screen("electricity")

        

        # Reset all buttons to default color

        for child in screen.ids.meter_type_grid.children:

            child.md_bg_color = [1, 1, 1, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1]

            child.text_color = child.line_color  # Reset to original color

        

        # Highlight selected button with a slight gradient

        button.md_bg_color = button.line_color

        button.text_color = [1, 1, 1, 1]

        
        self.selected_meter_type = meter_type.lower()
      #  self.selected_meter_type = meter_type

        screen.ids.selected_meter_type_label.text = meter_type

        

        # Animate the selected meter type box

        selected_box = screen.ids.selected_meter_type_box

        if selected_box.height == 0:

            anim = Animation(height=dp(50), opacity=1, duration=0.2)

            anim.start(selected_box)

    

    def validate_meter_number(self, text):

        """Enhanced meter number validation"""

        screen = self.root.get_screen("electricity")

        

        if not text:

            screen.ids.meter_number_input.error = False

            screen.ids.meter_number_input.helper_text = "Enter your meter number"

            return False

        

        # Check length based on provider

        min_length = 6

        if self.selected_electricity_provider in ["IKEDC", "EKEDC"]:

            min_length = 10  # Ikeja and Eko typically have longer meter numbers

        

        if len(text) < min_length or not text.isdigit():

            screen.ids.meter_number_input.error = True

            screen.ids.meter_number_input.helper_text = f"Meter number must be at least {min_length} digits"

            return False
        # Additional provider-specific validation

        if self.selected_electricity_provider == "IKEDC" and not text.startswith(('02', '03', '04')):

            screen.ids.meter_number_input.error = True

            screen.ids.meter_number_input.helper_text = "IKEDC meter numbers usually start with 02, 03 or 04"

            return False

        

        screen.ids.meter_number_input.error = False

        screen.ids.meter_number_input.helper_text = "Valid meter number"

        return True

    def validate_electricity_amount(self, text):

        """Enhanced amount validation with provider-specific limits"""

        screen = self.root.get_screen("electricity")

        

        if not text:

            screen.ids.electricity_amount_input.error = False

            screen.ids.electricity_amount_input.helper_text = "Enter amount to pay"

            return False

        

        try:

            amount = float(text.replace('₦', '').replace(',', ''))

            

            # Provider-specific minimum amounts

            min_amount = 50

            if self.selected_electricity_provider in ["AEDC", "EKEDC"]:

                min_amount = 100  # Abuja and Eko have higher minimums

                

            max_amount = 100000

            if amount < min_amount:

                screen.ids.electricity_amount_input.error = True

                screen.ids.electricity_amount_input.helper_text = f"Minimum amount is ₦{min_amount}"

                return False

            elif amount > max_amount:

                screen.ids.electricity_amount_input.error = True

                screen.ids.electricity_amount_input.helper_text = f"Maximum amount is ₦{max_amount:,}"

                return False

            

            # Check wallet balance if logged in

            if self.current_user and amount > self.current_user.get('wallet_balance', 0):

                screen.ids.electricity_amount_input.error = True

                screen.ids.electricity_amount_input.helper_text = "Insufficient wallet balance"

                return False

                

            screen.ids.electricity_amount_input.error = False

            screen.ids.electricity_amount_input.helper_text = "Valid amount"

            return True

            

        except ValueError:

            screen.ids.electricity_amount_input.error = True

            screen.ids.electricity_amount_input.helper_text = "Enter a valid number"

            return False                

   # class app(app):
    def verify_meter_number(self, meter_number):
        """Verify meter number - simplified since verify-meter endpoint not available"""
        if not self.selected_electricity_provider:
            self.show_error_dialog("Please select electricity provider first")
            return False
        
        if not meter_number or len(meter_number) < 6:
            self.show_error_dialog("Please enter a valid meter number (at least 6 digits)")
            return False
        
        # Show success without hitting backend (endpoint not available)
        self._handle_meter_verification_success("Customer Verified")
        return True
        
   

        def callback(success, response):
            self.hide_loader()
            if success and response.get('status') == 'success':
                customer_name = response['data'].get('name', 'Verified Customer')
                self._handle_meter_verification_success(customer_name)
            else:
                error_msg = response.get('message', 'Meter verification failed')
                self.show_error_dialog(f"Meter verification failed: {error_msg}")
                
        self.vtpass_backend_request("verify-meter", "POST", data, callback)        
        return True
    
    def process_backend_request(self, endpoint, method="POST", data=None, callback=None):
        """Make requests to your Flask backend"""
        url = f"{self.backend_url}/api/{endpoint}"
        
        def on_success(req, result):
            if callback:
                callback(True, result)
        
        def on_failure(req, error):
            if callback:
                callback(False, {"message": str(error)})
        
        try:
            if method.upper() == "GET":
                UrlRequest(
                    url,
                    on_success=on_success,
                    on_failure=on_failure,
                    timeout=30
                )
            else:
                UrlRequest(
                    url,
                    on_success=on_success,
                    on_failure=on_failure,
                    req_headers={'Content-Type': 'application/json'},
                    req_body=json.dumps(data) if data else None,
                    timeout=30
                )
        except Exception as e:
            if callback:
                callback(False, {"message": str(e)})  
              
    def _handle_meter_verification_success(self, customer_name):
        """Handle successful meter verification"""
        screen = self.root.get_screen("electricity")
        if hasattr(screen.ids, 'customer_name_label'):
            screen.ids.customer_name_label.text = f"Customer: {customer_name}"
            screen.ids.customer_name_label.opacity = 1
        
        self.show_success_dialog("Meter number verified successfully!")


    
    def _complete_electricity_payment(self, meter_number, amount, phone):
        """Cika biyan wutar lantarki ta amfani da TVPass API"""
        data = {
            "disco": self.selected_electricity_provider.lower(),
            "meter": meter_number,
            "amount": amount,
            "phone": phone,
            "type": self.selected_meter_type.lower()
        }

        def callback(success, response):
            if success and response.get("status") == "success":
                # Aiki nasara
                token = response.get("token", "")
                transaction_id = response.get("transaction_id", "")
                
                # Ƙara transaction cikin tarihi
                if self.current_user:
                    user_id = list(self.users.keys())[list(self.users.values()).index(self.current_user)]
                    self.users[user_id]['wallet_balance'] -= amount
                    self.current_user = self.users[user_id]
                    
                    transaction_record = {
                        "user_id": user_id,
                        "type": "Electricity",
                        "provider": self.selected_electricity_provider,
                        "meter_type": self.selected_meter_type,
                        "meter_number": meter_number,
                        "amount": f"₦{amount:,}",
                        "phone": phone,
                        "status": "Successful",
                        "date": datetime.now().strftime("%B %d, %Y %I:%M:%S %p"),
                        "token": token,
                        "reference": transaction_id
                    }
                    transaction_id_str = str(len(self.transactions) + 1)
                    self.transactions[transaction_id_str] = transaction_record
                    
                    self.save_users()
                    self.save_transactions()
                    self.update_dashboard()
                
                self._show_payment_success_with_token(token, transaction_id)
            else:
                error_msg = response.get("message", "Electricity payment failed")
                self.show_error_dialog(f"Electricity payment failed: {error_msg}")

        self.vtpass_backend_request("electricity", "POST", data, callback)

    def _generate_electricity_token(self):

        """Generate a simulated electricity token"""

        import random

        return ''.join([str(random.randint(0, 9)) for _ in range(20)])



    def _show_payment_success(self, transaction):

        """Show payment success dialog with receipt options"""

        success_dialog = MDDialog(

            title="Payment Successful!",

            text=(

                f"{self.selected_electricity_provider} {self.selected_meter_type}\n"

                f"Meter: {transaction['meter_number']}\n"

                f"Amount: {transaction['amount']}\n"

                f"Token: {transaction.get('token', 'N/A')}"

            ),

            buttons=[

                MDFlatButton(

                    text="DONE",

                    theme_text_color="Custom",

                    text_color=self.theme_cls.primary_color,

                    on_release=lambda x: success_dialog.dismiss()

                ),

                MDRaisedButton(

                    text="VIEW RECEIPT",

                    md_bg_color=self.theme_cls.primary_color,

                    on_release=lambda x: self._show_receipt(transaction, success_dialog)

                ),

                MDRaisedButton(

                    text="SHARE RECEIPT",

                    md_bg_color=[0.2, 0.7, 0.2, 1],

                    on_release=lambda x: self._share_receipt(transaction, success_dialog)

                )

            ],

            radius=[20, 7, 20, 7]

        )

        success_dialog.open()



    def _show_receipt(self, transaction, dialog):

        """Show detailed receipt"""

        dialog.dismiss()

        self.show_success_dialog("Receipt view would open here")



    def _share_receipt(self, transaction, dialog):

        """Share receipt functionality"""

        dialog.dismiss()

        self.show_success_dialog("Receipt sharing would open here")

        

    def buy_electricity(self):

        if not self.current_user:

            self.show_error_dialog("Please login to continue")

            self.root.current = "login"

            return

            

        self.root.current = "electricity"

        screen = self.root.get_screen("electricity")

        screen.ids.meter_number_input.text = ""

        screen.ids.electricity_amount_input.text = ""
           

    def reset_electricity_selections(self):

        """Reset all electricity screen selections"""

        self.selected_electricity_provider = ""

        self.selected_meter_type = ""

        

        if hasattr(self, 'root') and self.root:

            screen = self.root.get_screen("electricity")

            if screen:

                # Clear input fields

                screen.ids.meter_number_input.text = ""

                screen.ids.electricity_amount_input.text = ""

                screen.ids.electricity_phone_input.text = ""

                

                # Hide selection boxes

                screen.ids.selected_disco_box.height = 0

                screen.ids.selected_disco_box.opacity = 0

                screen.ids.selected_meter_type_box.height = 0

                screen.ids.selected_meter_type_box.opacity = 0

                

                # Reset provider buttons

                for child in screen.ids.disco_grid.children:

                    child.md_bg_color = (

                        [0.95, 0.95, 0.95, 1] 

                        if self.theme_cls.theme_style == "Light" 

                        else [0.2, 0.2, 0.2, 1]

                    )

                

                # Reset meter type buttons

                for child in screen.ids.meter_type_grid.children:

                    child.md_bg_color = (

                        [1, 1, 1, 1] 

                        if self.theme_cls.theme_style == "Light" 

                        else [0.2, 0.2, 0.2, 1]

                    )

                    child.text_color = child.line_color



    def update_electricity_provider_colors(self):

        """Update provider colors based on theme"""

        if hasattr(self, 'root') and self.root:

            screen = self.root.get_screen("electricity")

            if screen and hasattr(screen.ids, 'disco_grid'):

                for child in screen.ids.disco_grid.children:

                    if hasattr(child, 'text'):

                        provider = (

                            child.text.split('\n')[0] 

                            if '\n' in child.text 

                            else child.text

                        )

                        if provider == "IKEDC":

                            child.text_color = self.ikeja_color

                        elif provider == "EKEDC":

                            child.text_color = self.eko_color

                        elif provider == "IBEDC":

                            child.text_color = self.ibadan_color

                        elif provider == "AEDC":

                            child.text_color = self.abuja_color

    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        try:
            from kivy.core.clipboard import Clipboard
            Clipboard.copy(text)
            self.show_success_dialog("Copied to clipboard!")
        except Exception as e:
            self.show_error_dialog("Failed to copy to clipboard")
            
    def check_meter_balance(self):
        """Check meter balance through backend"""
        screen = self.root.get_screen("electricity")
        meter_number = screen.ids.meter_number_input.text
        
        if not self.validate_meter_number(meter_number):
            return

        # This would need a separate endpoint in your backend
        # For now, we'll show a placeholder
        self.show_loader("Checking meter balance...")
        
        # Simulate API call delay
        Clock.schedule_once(lambda dt: self._display_meter_balance(meter_number), 2)

    def _display_meter_balance(self, meter_number):
        """Display meter balance result"""
        self.hide_loader()
        
        # Placeholder - in production, this would come from backend
        balance = 542.75
        
        dialog = MDDialog(
            title="Meter Balance",
            text=f"Meter: {meter_number}\nCurrent Balance: ₦{balance:,.2f}",
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: dialog.dismiss()
                )
            ],
            radius=[20, 7, 20, 7]
        )
        dialog.open()


    def show_electricity_help(self):

        """Enhanced help dialog with provider-specific info"""

        providers_info = {

            "IKEDC": "Ikeja Electric\nMinimum: ₦100\nMeter Format: 11 digits starting with 02, 03 or 04",

            "EKEDC": "Eko Electric\nMinimum: ₦100\nMeter Format: 10-12 digits",

            "IBEDC": "Ibadan Electric\nMinimum: ₦50\nMeter Format: 6+ digits",

            "AEDC": "Abuja Electric\nMinimum: ₦100\nMeter Format: 11 digits",

            "Others": "Minimum: ₦50\nMeter Format: 6+ digits"

        }

        

        current_provider = self.selected_electricity_provider or "Others"

        provider_info = providers_info.get(current_provider, providers_info["Others"])

        

        dialog = MDDialog(

            title="Electricity Payment Help",

            text=(

                "How to pay:\n"

                "1. Select your electricity company\n"

                "2. Choose meter type (Prepaid/Postpaid)\n"

                "3. Enter your meter number\n"

                "4. Enter amount to pay\n"

                "5. Click CONTINUE\n\n"

                f"{provider_info}"

            ),

            buttons=[

                MDFlatButton(

                    text="OK",

                    theme_text_color="Custom",

                    text_color=self.theme_cls.primary_color,

                    on_release=lambda x: dialog.dismiss()

                )

            ],

            radius=[20, 7, 20, 7]

        )

        dialog.open()
        
   

    def setup_cable_tv_screen(self):

        """Setup the Cable TV subscription screen with enhanced features"""

        screen = self.root.get_screen("cable_tv")

        

        providers = [

            {"name": "DSTV", "logo": "assets/dstv.png", "color": [0.9, 0.3, 0.3, 1]},

            {"name": "GOTV", "logo": "assets/gotv.png", "color": [0.1, 0.6, 1, 1]},

            {"name": "Startimes", "logo": "assets/startime.png", "color": [0.9, 0.8, 0.1, 1]},

            {"name": "Showmax", "logo": "assets/showmax.png", "color": [0.2, 0.8, 0.5, 1]},]

              

        provider_grid = screen.ids.provider_grid

        provider_grid.clear_widgets()

        

        for provider in providers:

            card = MDCard(

                orientation='vertical',

                size_hint=(None, None),

                size=(dp(75), dp(75)),

                elevation=2,

                on_release=lambda x, p=provider["name"]: self.select_cable_provider(x, p),

                md_bg_color=[0.95, 0.95, 0.95, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1],

                radius=[15]

            )

            

            try:

                logo = FitImage(

                    source=provider["logo"],

                    size_hint=(1, 0.7),

                    radius=[15, 15, 15, 15]

                )

                card.add_widget(logo)

            except:

                logo = MDIcon(

                    icon="television",

                    size_hint=(1, 0.7),

                    theme_text_color="Custom",

                    text_color=provider["color"]

                )

                card.add_widget(logo)

            

            label = MDLabel(

                text=provider["name"],

                size_hint_y=None,

                height=dp(10),

                halign="center",

                font_style="Caption",

                theme_text_color="Custom",

                text_color=provider["color"]

            )

            card.add_widget(label)

            

            provider_grid.add_widget(card)
  
    
    def select_cable_provider(self, card, provider):
        """Handle cable provider selection and load packages."""
        try:
            screen = self.root.get_screen("cable_tv")
            
            # Reset all provider cards
            for child in screen.ids.provider_grid.children:
                child.md_bg_color = [0.95,0.95,0.95,1] if self.theme_cls.theme_style=="Light" else [0.2,0.2,0.2,1]
            
            # Highlight selected card
            card.md_bg_color = [0.9,0.9,0.9,1] if self.theme_cls.theme_style=="Light" else [0.3,0.3,0.3,1]
            
            self.selected_cable_provider = provider
            screen.ids.selected_provider_label.text = provider
            
            # Show selection box
            selected_box = screen.ids.selected_provider_box
            if selected_box.height == 0:
                Animation(height=dp(50), opacity=1, duration=0.2).start(selected_box)
            
            # Reset previous selections
            self.selected_cable_package = ""
            #self.selected_cable_amount = 0
            amount = self.selected_cable_amount
            if self.current_user and amount > self.current_user.get('wallet_balance', 0):
                self.selected_cable_plan_id = ""
            
            # Clear existing packages grid
            screen.ids.package_grid.clear_widgets()
            
            # Fetch cable plans for this provider
            self.fetch_cable_plans(provider)
            
            # Enable smartcard input
            screen.ids.smartcard_input.disabled = False
            screen.ids.smartcard_input.opacity = 1
            
        except Exception as e:
            self.show_error_dialog(f"Error selecting provider: {str(e)}")
      

    def fetch_cable_plans(self, provider=None):
        """Fetch cable plans from backend."""
        self.show_loader("Loading cable plans...")
        
        def on_success(req, result):
            self.hide_loader()
            if result.get('status') == 'success':
                plans = result.get('data', [])
                if provider:
                    plans = [p for p in plans if p['provider'].lower() == provider.lower()]
                self.display_cable_plans(plans)
            else:
                self.show_error_dialog("Failed to load cable plans")
        
        def on_failure(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Network error: {error}")
        
        self.backend_api_request('plans/cable', 'GET', callback=on_success, on_failure=on_failure)

    def display_cable_plans(self, plans):
        """Display cable plans in the cable TV screen grid."""
        screen = self.root.get_screen("cable_tv")
        package_grid = screen.ids.package_grid
        package_grid.clear_widgets()
        
        if not plans:
            no_plan_label = MDLabel(
                text="No packages available for this provider",
                halign="center",
                theme_text_color="Secondary"
            )
            package_grid.add_widget(no_plan_label)
            return
        
        for plan in plans:
            card = MDCard(
                orientation='vertical',
                size_hint=(None, None),
                size=(dp(150), dp(80)),
                elevation=2,
                on_release=lambda x, p=plan: self.select_cable_plan(p),
                md_bg_color=[1,1,1,1] if self.theme_cls.theme_style=="Light" else [0.2,0.2,0.2,1],
                radius=[15]
            )
            # Plan name
            name_label = MDLabel(
                text=plan['plan_name'],
                font_style='Subtitle1',
                bold=True,
                halign='center',
                theme_text_color="Primary",
                size_hint_y=None,
                height=dp(40)
            )
            card.add_widget(name_label)
            # Price
            price_label = MDLabel(
                text=f"₦{plan['selling_price']:,.0f}",
                font_style='H6',
                halign='center',
                theme_text_color="Primary",
                size_hint_y=None,
                height=dp(30)
            )
            card.add_widget(price_label)
            package_grid.add_widget(card)
        
        # Make scroll view visible
        package_grid.parent.height = dp(200)
        package_grid.parent.opacity = 1

    def select_cable_plan(self, plan):
        """Handle cable plan selection, store plan_id and selling price."""
        screen = self.root.get_screen("cable_tv")
        
        # Reset all cards highlight
        for child in screen.ids.package_grid.children:
            if hasattr(child, 'md_bg_color'):
                child.md_bg_color = [1,1,1,1] if self.theme_cls.theme_style=="Light" else [0.2,0.2,0.2,1]
        
        # Highlight selected card
        for child in screen.ids.package_grid.children:
            if hasattr(child, 'children') and len(child.children) >= 2:
                if child.children[1].text == plan['plan_name']:
                    child.md_bg_color = [0.9,0.9,0.9,1] if self.theme_cls.theme_style=="Light" else [0.3,0.3,0.3,1]
                    break
        
        # Store selection
        self.selected_cable_package = plan['plan_name']
        self.selected_cable_amount = plan['selling_price']
        self.selected_cable_plan_id = plan['plan_id']   # Store plan_id
        
        # Update UI labels
        screen.ids.selected_package_label.text = f"{plan['plan_name']} - ₦{plan['selling_price']:,.0f}"
        
        # Show selection box with animation
        selected_box = screen.ids.selected_package_box
        if selected_box.height == 0:
            anim = Animation(height=dp(50), opacity=1, duration=0.2)
            anim.start(selected_box)
        
        # Enable smartcard input and buttons
        screen.ids.smartcard_input.disabled = False
        screen.ids.smartcard_input.opacity = 1
        screen.ids.myself_btn.disabled = False
        screen.ids.myself_btn.opacity = 1

    def load_cable_packages(self, provider):
        """Called when user selects a cable provider. Fetches packages."""
        self.fetch_cable_plans(provider)

    def _execute_cable_subscription(self):
        """Execute cable subscription after PIN verified - uses plan_id."""
        try:
            screen = self.root.get_screen("cable_tv")
            smartcard = screen.ids.smartcard_input.text
            amount = self.selected_cable_amount
            
            # Check wallet balance
            if self.current_user and amount > self.current_user.get('wallet_balance', 0):
                self.show_error_dialog("Insufficient wallet balance")
                self._clear_verified_pin()
                return
            
            self.show_loader("Processing cable subscription...")
            
            payload = {
                'plan_id': self.selected_cable_plan_id,   # Send plan_id, not provider/package names
                'smartcard': smartcard,
                'pin': self.verified_pin,
                'user_email': self.current_user.get('email'),
                'coupon_code': getattr(self, 'pending_coupon_code', None),
            }
            
            def callback(success, response):
                self.hide_loader()
                self._clear_verified_pin()
                if success and response.get('status') == 'success':
                    profit_amount = response.get('data', {}).get('profit_amount', 0)
                    discount = response.get('data', {}).get('discount_amount', 0)
                    msg = f"{self.selected_cable_provider} subscription successful!\nProfit earned: ₦{profit_amount:,.2f}"
                    if discount:
                        msg += f"\nCoupon savings: {self.format_currency(discount)}"
                    self.show_success_dialog(msg)
                    self.update_dashboard()
                    self.root.current = "dashboard"
                    self.reset_cable_selections()
                    self.pending_coupon_code = None
                else:
                    error_msg = response.get('message', 'Cable subscription failed')
                    self.show_error_dialog(f"Cable subscription failed: {error_msg}")
            
            self.backend_api_request('vtpass/cable-tv', 'POST', payload, callback)
            
        except Exception as e:
            self.hide_loader()
            self._clear_verified_pin()
            self.show_error_dialog(f"Cable subscription error: {str(e)}")


    def select_cable_package(self, card, package, amount):

        """Handle package selection with visual feedback"""

        screen = self.root.get_screen("cable_tv")        

        for child in screen.ids.package_grid.children:

            child.md_bg_color = [1, 1, 1, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1]        

        card.md_bg_color = [0.95, 0.95, 0.95, 1] if self.theme_cls.theme_style == "Light" else [0.3, 0.3, 0.3, 1]

        

        self.selected_cable_package = package

        self.selected_cable_amount = amount

        

        screen.ids.selected_package_label.text = f"{package} - ₦{amount:,}"

        

        selected_box = screen.ids.selected_package_box

        if selected_box.height == 0:

            Animation(height=dp(50), opacity=1, duration=0.2).start(selected_box)



    def validate_smartcard_input(self, text):

        """Validate smartcard/IUC number with proper feedback"""

        screen = self.root.get_screen("cable_tv")

        

        if len(text) > 5:

            screen.ids.smartcard_input.error = False

            screen.ids.smartcard_input.helper_text = "Valid smartcard/IUC number"

            return True

        else:

            screen.ids.smartcard_input.error = True

            screen.ids.smartcard_input.helper_text = "Enter a valid smartcard/IUC number"

            return False



    def fill_my_smartcard(self):

        """Auto-fill smartcard with user's registered number"""

        if self.current_user:

            screen = self.root.get_screen("cable_tv")

            screen.ids.smartcard_input.text = self.current_user['phone']

            screen.ids.myself_btn.md_bg_color = self.theme_cls.primary_color

            screen.ids.myself_btn.text_color = [1, 1, 1, 1]

            self.validate_smartcard_input(self.current_user['phone'])



    def show_cable_help(self):

        """Show help dialog for cable subscription"""

        dialog = MDDialog(

            title="Cable TV Subscription Help",

            text="1. Select your cable provider (DStv, GOtv, etc.)\n2. Choose your preferred package\n3. Enter your smartcard/IUC number\n4. Click CONTINUE to complete",

            buttons=[

                MDFlatButton(

                    text="OK",

                    theme_text_color="Custom",

                    text_color=self.theme_cls.primary_color,

                    on_release=lambda x: dialog.dismiss()

                )

            ],

            radius=[20, 7, 20, 7]

        )

        dialog.open()


    
    def _finalize_cable_subscription(self, smartcard_number):
        """Cika cable subscription ta amfani da TVPass API"""
        data = {
            "provider": self.selected_cable_provider.lower(),
            "package": self.selected_cable_package,
            "smartcard": smartcard_number,
            "amount": self.selected_cable_amount
        }

        def callback(success, response):
            if success and response.get("status") == "success":
                # Aiki nasara
                transaction_id = response.get("transaction_id", "")
                
                # Ƙara transaction cikin tarihi
                if self.current_user:
                    user_id = list(self.users.keys())[list(self.users.values()).index(self.current_user)]
                    self.users[user_id]['wallet_balance'] -= self.selected_cable_amount
                    self.current_user = self.users[user_id]
                    
                    transaction_record = {
                        "user_id": user_id,
                        "type": "Cable TV",
                        "provider": self.selected_cable_provider,
                        "package": self.selected_cable_package,
                        "smartcard": smartcard_number,
                        "amount": f"₦{self.selected_cable_amount:,}",
                        "status": "Successful",
                        "date": datetime.now().strftime("%B %d, %Y %I:%M:%S %p"),
                        "reference": transaction_id
                    }
                    transaction_id_str = str(len(self.transactions) + 1)
                    self.transactions[transaction_id_str] = transaction_record
                    
                    self.save_users()
                    self.save_transactions()
                    self.update_dashboard()
                
                self.show_success_dialog(f"Cable TV subscription of ₦{self.selected_cable_amount:,} successful! Transaction ID: {transaction_id}")
                self.reset_cable_selections()
                self.root.current = "dashboard"
            else:
                error_msg = response.get("message", "Cable subscription failed")
                self.show_error_dialog(f"Cable subscription failed: {error_msg}")

        self.vtpass_backend_request("cable", "POST", data, callback)
        
  


    def reset_cable_selections(self):

        """Reset all cable TV selections"""

        self.selected_cable_provider = ""
        self.selected_cable_package = ""
        self.selected_cable_plan_id  = ""
        self.selected_cable_amount = 0

        

        screen = self.root.get_screen("cable_tv")

        screen.ids.smartcard_input.text = ""

        

        screen.ids.selected_provider_box.height = 0

        screen.ids.selected_provider_box.opacity = 0

        screen.ids.selected_package_box.height = 0

        screen.ids.selected_package_box.opacity = 0

        

        for child in screen.ids.provider_grid.children:

            child.md_bg_color = [0.95, 0.95, 0.95, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1]

        

        for child in screen.ids.package_grid.children:

            child.md_bg_color = [1, 1, 1, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1]



    def buy_cable_tv(self):

        """Navigate to cable TV screen with reset"""

        if not self.current_user:

            self.show_error_dialog("Please login to continue")

            self.root.current = "login"

            return

            

        self.reset_cable_selections()

        self.root.current = "cable_tv"

    

    def complete_cable_purchase(self, dialog, smartcard_number):

        dialog.dismiss()

        

        # Create transaction record

        if self.current_user:

            transaction_id = str(len(self.transactions) + 1)

            transaction = {

                "user_id": list(self.users.keys())[list(self.users.values()).index(self.current_user)],

                "type": "Cable TV",

                "provider": self.selected_cable_provider,

                "package": self.selected_cable_package,

                "smartcard": smartcard_number,

                "amount": f"₦{self.selected_cable_amount:,}",

                "status": "Successful",

                "date": datetime.now().strftime("%B %d, %Y %I:%M:%S %p")

            }

            self.transactions[transaction_id] = transaction

            self.save_transactions()

        

        self.show_success_dialog(f"Cable TV subscription of ₦{self.selected_cable_amount:,} successful!")

        self.root.current = "dashboard"

        

        # Reset selections

        self.selected_cable_provider = None

        self.selected_cable_package = None

        self.selected_cable_amount = 0

        screen = self.root.get_screen("cable_tv")

        screen.ids.smartcard_input.text = ""

        

        # Reset button colors

        for child in screen.ids.provider_grid.children:

            child.md_bg_color = [1, 1, 1, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1]

            child.text_color = child.line_color

        

        for child in screen.ids.package_grid.children:

            child.md_bg_color = [1, 1, 1, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1]

        

        # Reset selection boxes

        screen.ids.selected_provider_box.height = 0

        screen.ids.selected_provider_box.opacity = 0

        screen.ids.selected_package_box.height = 0

        screen.ids.selected_package_box.opacity = 0    

    
    def process_payment_via_tvpass(self, amount, description, service_type, service_details):
        """Yi biyayya ta amfani da TVPass API"""
        if not hasattr(self, 'current_user') or not self.current_user:
            email = "guest@example.com"
        else:
            email = self.current_user.get('email', 'guest@example.com')

        data = {
            "email": email,
            "amount": amount,
            "description": description,
            "service_type": service_type,
            "service_details": service_details
        }

        self.show_loader("Processing payment...")

        def callback(success, response):
            self.hide_loader()
            if success and response.get("status") == "success":
                self.show_success_dialog("Payment processed successfully!")
                return True
            else:
                error_msg = response.get("message", "Payment failed")
                self.handle_tvpass_error(error_msg)
                return False

        self.vtpass_backend_request("payment", "POST", data, callback)



    @staticmethod

    def detect_network(phone_number):

        """

        Detect which Nigerian network a phone number belongs to

        Returns: 'MTN', 'Airtel', 'Glo', '9mobile', or 'Unknown'

        """

        # Remove any non-digit characters

        clean_number = ''.join(filter(str.isdigit, str(phone_number)))

        

        # Check if number is valid length (11 digits)

        if len(clean_number) != 11:

            return "Unknown"

        

        # Extract first 4 digits (most accurate way)

        prefix = clean_number[:4]

        

        # Network prefix mappings (updated as of 2023)

        network_prefixes = {

            'MTN': [

                '0803', '0806', '0703', '0706', '0813', '0816',

                '0810', '0814', '0903', '0906', '0913', '0916'

            ],

            'Airtel': [

                '0802', '0808', '0708', '0812', '0901', '0902',

                '0904', '0907', '0912'

            ],

            'Glo': [

                '0805', '0807', '0705', '0815', '0811', '0905', '0915'

            ],

            '9mobile': [

                '0809', '0818', '0817', '0909', '0908'

            ]

        }

        

        # Check each network's prefixes

        for network, prefixes in network_prefixes.items():

            if prefix in prefixes:

                return network

        

        # If no match found

        return "Unknown"


    def setup_airtime_topup_screen(self):

        screen = self.root.get_screen("airtime_topup")

        

        # Setup network buttons with logos

        networks = [

            {"name": "MTN", "logo": "assets/mtn.png", "color": self.mtn_color},

            {"name": "Airtel", "logo": "assets/airtel.png", "color": self.airtel_color},

            {"name": "Glo", "logo": "assets/glo.png", "color": self.glo_color},

            {"name": "9Mobile", "logo": "assets/9mobile.png", "color": self.mobile9_color}

        ]

        

        network_grid = screen.ids.network_grid

        network_grid.clear_widgets()

        

        for net in networks:

            # Create a card for each network

            card = MDCard(

                orientation='vertical',

                size_hint=(None, None),

                size=(dp(75), dp(75)),

                elevation=2,
                
                on_release=lambda x, n=net["name"]: self.select_airtime_network(n),

              #  on_release=lambda x, n=net["name"]: self.select_airtime_network(x, n),

                md_bg_color=[0.2, 0.2, 0.2, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1],

                radius=[15]

            )

     

            # Add logo image
            
            try:
                logo = FitImage(
                    source=net["logo"],
                    size_hint=(1, 0.7),
                    radius=[15, 15, 15, 15]
                )
            except Exception:
                logo = MDIcon(
                    icon="sim",
                    size_hint=(1, 0.7),
                    theme_text_color="Custom",
                    text_color=net["color"]
                )
            card.add_widget(logo)

            #logo = FitImage(

#                source=net["logo"],

#                size_hint=(1, 0.7),

#                radius=[15, 15, 15, 15]

#            )

#            card.add_widget(logo)

            

            # Add network name label

            label = MDLabel(

                text=net["name"],

                size_hint_y=None,

                height=dp(10),

                halign="center",

                font_style="Caption",

                theme_text_color="Custom",

                text_color=net["color"]

            )

            card.add_widget(label)

            

            network_grid.add_widget(card)

        

        # Setup amount buttons

        amounts = [50, 100, 200, 300, 500, 1000, 1500, 2000, 5000]

        amount_grid = screen.ids.amount_grid

        amount_grid.clear_widgets()



        color_variants = [

            self.mtn_color,

            self.airtel_color,

            self.glo_color,

            self.mobile9_color

        ]



        for i, amount in enumerate(amounts):

            color = color_variants[i % len(color_variants)]

            card = MDCard(

                orientation='vertical',

                size_hint=(None, None),

                size=(dp(150), dp(50)),

                elevation=2,

                on_release=lambda x, amt=amount: self.select_airtime_amount(x, amt),

                md_bg_color=[1, 1, 1, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1],

                radius=[15]

            )

            

            # Amount with colored indicator

            amount_box = MDBoxLayout(

                orientation='horizontal',

                size_hint_y=None,

                height=dp(40),

                padding=[dp(10), 0, dp(60), 0]

            )

            amount_box.add_widget(MDLabel(

                text=f"₦{amount:,}",

                font_style='H6',

                halign='center',

                theme_text_color="Custom",

                text_color=color

            ))

            card.add_widget(amount_box)

            

            amount_grid.add_widget(card)

    
    def select_airtime_amount(self, card, amount):

        screen = self.root.get_screen("airtime_topup")

        

        # Reset all cards to default color

        for child in screen.ids.amount_grid.children:

            child.md_bg_color = [1, 1, 1, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1]

        

        # Highlight selected card

        card.md_bg_color = [0.95, 0.95, 0.95, 1] if self.theme_cls.theme_style == "Light" else [0.3, 0.3, 0.3, 1]

        

        self.selected_airtime_amount = amount  # <- This is the important fix

        screen.ids.selected_amount_label.text = f"₦{amount:,}"

        

        # Clear custom amount field

        screen.ids.custom_amount.text = ""

        

        # Animate selection box

        selected_box = screen.ids.selected_amount_box

        if selected_box.height == 0:

            anim = Animation(height=dp(50), opacity=1, duration=0.2)

            anim.start(selected_box)

    

    def validate_custom_amount(self, text):

        """Validate custom amount input with proper error handling"""

        screen = self.root.get_screen("airtime_topup")

        

        if not text:

            screen.ids.custom_amount.error = False

            screen.ids.custom_amount.helper_text = "Enter amount between N100 and N50,000"

            return False

        

        try:

            # Remove any currency symbols or commas

            clean_text = text.replace('N', '').replace(',', '').strip()

            amount = float(clean_text)

            

            if amount < 100:

                screen.ids.custom_amount.error = True

                screen.ids.custom_amount.helper_text = "Minimum amount is N100"

                return False

            elif amount > 50000:

                screen.ids.custom_amount.error = True

                screen.ids.custom_amount.helper_text = "Maximum amount is N50,000"

                return False

            

            # If validation passes

            screen.ids.custom_amount.error = False

            screen.ids.custom_amount.helper_text = "Valid amount"

            

            # Set the selected amount

            self.selected_airtime_amount = amount

            screen.ids.selected_amount_label.text = f"N{amount:,.2f}"

            

            # Show selection box if hidden

            selected_box = screen.ids.selected_amount_box

            if selected_box.height == 0:

                anim = Animation(height=dp(50), opacity=1, duration=0.2)

                anim.start(selected_box)

                

            # Reset all amount cards to default color

            for child in screen.ids.amount_grid.children:

                child.md_bg_color = [1, 1, 1, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1]

                

            return True

            

        except ValueError:

            screen.ids.custom_amount.error = True

            screen.ids.custom_amount.helper_text = "Enter numbers only"

            return False

    

    def show_airtime_help(self):

        dialog = MDDialog(

            title="Airtime Topup Help",

            text="1. Select the amount you want to recharge\n2. Choose your network provider\n3. Enter phone number\n4. Click CONTINUE to complete",

            buttons=[

                MDFlatButton(

                    text="OK",

                    theme_text_color="Custom",

                    text_color=self.theme_cls.primary_color,

                    on_release=lambda x: dialog.dismiss()

                )

            ],

            radius=[20, 7, 20, 7]

           

        )

        dialog.open()



    def complete_airtime_purchase(self, dialog, phone_number):
        """Deprecated — real purchases now go through _execute_airtime_purchase"""
        dialog.dismiss()
        

        # Create transaction record

        if self.current_user:

            transaction_id = str(len(self.transactions) + 1)

            transaction = {

                "user_id": list(self.users.keys())[list(self.users.values()).index(self.current_user)],

                "type": "Airtime",

                "network": self.selected_airtime_network,

                "phone": phone_number,

                "amount": f"₦{self.selected_airtime_amount:,}",

                "status": "Successful",

                "date": datetime.now().strftime("%B %d, %Y %I:%M:%S %p")

            }

            self.transactions[transaction_id] = transaction

            self.save_transactions()

        

        self.show_success_dialog(f"Airtime purchase of ₦{self.selected_airtime_amount:,} successful!")

        self.root.current = "dashboard"

        

        # Reset selections

        self.selected_airtime_amount = 0

        self.selected_airtime_network = ""

        screen = self.root.get_screen("airtime_topup")

        screen.ids.phone_input.text = ""

        screen.ids.custom_amount.text = ""

        

        # Reset button colors

        for child in screen.ids.amount_grid.children:

            child.md_bg_color = [1, 1, 1, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1]

            child.text_color = child.line_color

        

        for child in screen.ids.network_grid.children:

            child.md_bg_color = [1, 1, 1, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1]

            child.text_color = child.line_color

        

        # Reset selection boxes

        screen.ids.selected_amount_box.height = 0

        screen.ids.selected_amount_box.opacity = 0

        screen.ids.selected_network_box.height = 0

        screen.ids.selected_network_box.opacity = 0

    

    def buy_airtime(self):

        if not self.current_user:

            self.show_error_dialog("Please login to continue")

            self.root.current = "login"

            return

            

        self.selected_airtime_network = ""

        self.selected_airtime_amount = 0

        

        screen = self.root.get_screen("airtime_topup")

        screen.ids.phone_input.text = ""

        screen.ids.custom_amount.text = ""

        

        for child in screen.ids.network_grid.children:

            child.md_bg_color = [0.2, 0.2, 0.2, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1]

            

        for child in screen.ids.amount_grid.children:

            child.md_bg_color = [1, 1, 1, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1]

        

        screen.ids.selected_network_box.height = 0

        screen.ids.selected_network_box.opacity = 0

        screen.ids.selected_amount_box.height = 0

        screen.ids.selected_amount_box.opacity = 0

        

        self.root.current = "airtime_topup"                                        

    def fill_my_number(self):

        if self.current_user:

            screen = self.root.get_screen("airtime_topup")

            screen.ids.phone_input.text = self.current_user['phone']

            screen.ids.myself_btn.md_bg_color = self.theme_cls.primary_color

            screen.ids.myself_btn.text_color = [1, 1, 1, 1]

            

            # Validate the phone number

            if is_valid_phone(self.current_user['phone']):

                screen.ids.phone_input.error = False

                screen.ids.phone_input.helper_text = "Valid phone number"

            else:

                screen.ids.phone_input.error = True

                screen.ids.phone_input.helper_text = "Invalid phone number in profile"

                   

    def show_code4balance_dialog(self):

        """Display a dialog with USSD codes for checking data balance"""

        

        # Organized data structure

        balance_codes = [

            {"network": "MTN", "type": "SME", "code": "*461*4#", "icon": "sim"},

            {"network": "MTN", "type": "SME2", "code": "*323*4#", "icon": "sim"},

            {"network": "MTN", "type": "CG", "code": "*460*260#", "icon": "account-network"},

            {"network": "MTN", "type": "Gifting", "code": "*323*4#", "icon": "gift"},

            {"network": "Airtel", "type": "Awoof", "code": "*323#", "icon": "tag"},

            {"network": "Airtel", "type": "CG", "code": "*323#", "icon": "account-network"},

            {"network": "Glo", "type": "General", "code": "*127*0#", "icon": "sim"},

            {"network": "Glo", "type": "Alternative", "code": "*323#", "icon": "sim-alert"},

            {"network": "9mobile", "type": "Gifting", "code": "*323#", "icon": "gift"},            

        ]

        

        # Calculate dynamic height

        row_height = 80  # Height per card

        header_height = 120  # Search + title

        max_height = Window.height * 0.8  # Maximum 80% of screen height

        dialog_height = min(

            len(balance_codes) * row_height + header_height, 

            max_height

        )

        

        # Main content layout

        content = MDBoxLayout(

            orientation='vertical',

            spacing=dp(10),

            size_hint_y=None,

            height=dp(dialog_height),

            padding=dp(10)

        )

        

        # Header with title

        header = MDBoxLayout(

            orientation='vertical',

            size_hint_y=None,

            height=dp(60),

            spacing=dp(10)

        )

        header.add_widget(MDLabel(

            text="[size=20][b]USSD Codes for Data Balance[/b][/size]",

            halign="center",

            markup=True))

        content.add_widget(header)

        

        # Search field

        search_field = MDTextField(

            hint_text="Search network or code...",

            size_hint_y=None,

            height=dp(50),

            icon_left="magnify",

            mode="round",

            on_text=self.filter_codes)

        content.add_widget(search_field)

        

        # Create scroll view with grid

        self.code_grid = MDGridLayout(

            cols=1,

            spacing=dp(15),

            size_hint_y=None,

            adaptive_height=True,

            padding=dp(10))

        

        # Store original items for filtering

        self.all_codes = balance_codes

        

        # Populate grid with code cards

        self.populate_code_grid(balance_codes)

        

        scroll = ScrollView()

        scroll.add_widget(self.code_grid)

        content.add_widget(scroll)

        

        # Create and open dialog

        self.balance_dialog = MDDialog(

            title="",

            type="custom",

            content_cls=content,

            buttons=[

                MDFlatButton(

                    text="CLOSE",

                    theme_text_color="Custom",

                    text_color=self.theme_cls.primary_color,

                    on_release=lambda x: self.balance_dialog.dismiss()

                )

            ],

            radius=[20, 7, 20, 7],

            size_hint=(0.9, None))

        self.balance_dialog.open()



    def populate_code_grid(self, items):

        """Populate the grid with code cards"""

        self.code_grid.clear_widgets()

        

        for item in items:

            # Create card for each code

            card = MDCard(

                orientation='horizontal',

                size_hint_y=None,

                height=dp(70),

                padding=dp(10),

                spacing=dp(15),

                ripple_behavior=True,

                elevation=1)

            

            # Network icon

            card.add_widget(IconLeftWidget(

                icon=item.get("icon", "sim"),

                theme_text_color="Custom",

                text_color=self.theme_cls.primary_color))

            

            # Text content

            text_box = MDBoxLayout(

                orientation='vertical',

                spacing=dp(5))

            

            text_box.add_widget(MDLabel(

                text=f"[b]{item['network']} {item['type']}[/b]",

                markup=True,

                size_hint_y=None,

                height=dp(25)))

            

            text_box.add_widget(MDLabel(

                text=item['code'],

                theme_text_color="Secondary",

                size_hint_y=None,

                height=dp(20)))

            

            card.add_widget(text_box)

            

            # Copy button

            card.add_widget(IconLeftWidget(

                icon="content-copy",

                theme_text_color="Custom",

                text_color=self.theme_cls.primary_color,

                on_release=lambda x, c=item['code']: self.copy_to_clipboard(c)))

            

            self.code_grid.add_widget(card)



    def filter_codes(self, instance, text):

        """Filter codes based on search input"""

        filtered = [

            item for item in self.all_codes

            if text.lower() in item['network'].lower() or 

               text.lower() in item['type'].lower() or 

               text in item['code']

        ]

        self.populate_code_grid(filtered)



    def copy_to_clipboard(self, text):

        """Copy code to clipboard with error handling"""

        try:

            Clipboard.copy(text)

            self.show_success_dialog(f"Copied to clipboard: {text}")

        except Exception as e:

            self.show_error_dialog(f"Failed to copy: {str(e)}")
            
            
    def load_users(self):
        """Load users from storage"""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as f:
                    self.users = json.load(f)
            else:
                self.users = {}
            print(f"✅ Loaded {len(self.users)} users")
        except Exception as e:
            print(f"❌ Error loading users: {e}")
            self.users = {}

    def save_users(self):
        """Save users to storage"""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f, indent=2)
            print("✅ Users saved successfully")
        except Exception as e:
            print(f"❌ Error saving users: {e}")

    def load_transactions(self):
        """Load transactions from storage"""
        try:
            if os.path.exists(self.transactions_file):
                with open(self.transactions_file, 'r') as f:
                    self.transactions = json.load(f)
            else:
                self.transactions = {}
            print(f"✅ Loaded {len(self.transactions)} transactions")
        except Exception as e:
            print(f"❌ Error loading transactions: {e}")
            self.transactions = {}

    def save_transactions(self):
        """Save transactions to storage"""
        try:
            with open(self.transactions_file, 'w') as f:
                json.dump(self.transactions, f, indent=2)
            print("✅ Transactions saved successfully")
        except Exception as e:
            print(f"❌ Error saving transactions: {e}")                      
   


    def load_networks(self):

        networks = [

            {"name": "9Mobile", "icon": "cellphone"},

            {"name": "Glo", "icon": "network"},

            {"name": "Airtel", "icon": "signal"},

            {"name": "MTN", "icon": "transmission-tower"}

        ]

        

        screen = self.root.get_screen("network_select")

        network_list = screen.ids.network_list

        network_list.clear_widgets()

        

        for net in networks:

            item = OneLineIconListItem(

                text=f"{net['name']} Data",

                on_release=lambda x, n=net['name']: self.select_network(x, n),

                theme_text_color="Custom",

                text_color=[0.1, 0.6, 1, 1]

            )

            icon = IconLeftWidget(

                icon=net['icon'],

                theme_text_color="Custom",

                text_color=[0.1, 0.6, 1, 1]

            )

            item.add_widget(icon)

            network_list.add_widget(item)

        

        self.selected_network = None

        self.current_selected_item = None

    

    def select_network(self, list_item, network):

        if self.current_selected_item:

            self.current_selected_item.md_bg_color = [1, 1, 1, 1]

        

        self.current_selected_item = list_item

        list_item.md_bg_color = [0.9, 0.95, 1, 1]

        self.selected_network = network.replace(" Data", "")

    

    def go_to_phone_input(self):

        if self.selected_network:

            self.root.current = "phone_input"

            phone_screen = self.root.get_screen("phone_input")

            phone_screen.ids.phone_input.text = ""

    

    def process_phone_input(self, phone_number):

        if not is_valid_phone(phone_number):

            self.show_error_dialog("Invalid phone number. Please enter 11 digits")

            return

            

        service = "Airtime" if self.service_type == "airtime" else "Data"

        dialog = MDDialog(

            title="Confirm Purchase",

            text=f"Buy {service} for {phone_number} on {self.selected_network}",

            buttons=[

                MDFlatButton(

                    text="CANCEL",

                    theme_text_color="Custom",

                    text_color=self.theme_cls.primary_color,

                    on_release=lambda x: dialog.dismiss()

                ),

                MDRaisedButton(

                    text="CONFIRM",

                    theme_text_color="Custom",

                    text_color=[1, 1, 1, 1],

                    md_bg_color=self.theme_cls.primary_color,

                    on_release=lambda x: self.complete_purchase(dialog, phone_number)

                )

            ],

            radius=[20, 7, 20, 7]

        )

        dialog.open()

    

    def complete_purchase(self, dialog, phone_number):
        """Complete airtime/data purchase (legacy local flow)."""
        dialog.dismiss()

        if not self.current_user:
            return

        # Fix: .vablues() → .values()
        try:
            user_id = next(
                (k for k, v in self.users.items() if v == self.current_user), None
            )
        except Exception:
            user_id = None

        if not user_id:
            self.show_error_dialog("User session error. Please login again.")
            return

        try:
            amount_str = (self.selected_data_amount or '0')
            if isinstance(amount_str, str):
                amount = float(amount_str.replace('₦', '').replace(',', ''))
            else:
                amount = float(amount_str)
        except (ValueError, AttributeError):
            amount = 0

        if amount <= 0:
            self.show_error_dialog("Invalid amount")
            return

        if amount > self.current_user.get('wallet_balance', 0):
            self.show_error_dialog("Insufficient wallet balance")
            return

        self.users[user_id]['wallet_balance'] -= amount
        self.current_user = self.users[user_id]

        transaction_id = str(len(self.transactions) + 1)
        self.transactions[transaction_id] = {
            "user_id": user_id,
            "type": "Data" if self.service_type == "data" else "Airtime",
            "network": self.selected_network,
            "phone": phone_number,
            "amount": f"₦{amount:,.2f}",
            "status": "Successful",
            "date": datetime.now().strftime("%B %d, %Y %I:%M:%S %p"),
        }
        self.save_transactions()
        self.save_users()
        self.update_dashboard()
        self.show_success_dialog("Transaction successful!")
        self.reset_selections()

    def reset_selections(self):
        """Reset all service selections after a transaction."""
        self.selected_network = ""
        self.selected_data_network = ""
        self.selected_data_plan = ""
        self.selected_data_amount = ""
        self.selected_data_type = ""
        self.service_type = ""    

    def show_error_dialog(self, message):

        dialog = MDDialog(

            title="Error",

            text=message,

            buttons=[

                MDFlatButton(

                    text="OK",

                    theme_text_color="Custom",

                    text_color=self.theme_cls.primary_color,

                    on_release=lambda x: dialog.dismiss()

                )

            ],

            radius=[20, 7, 20, 7]

        )

        dialog.open()

    

    def show_success_dialog(self, message):

        dialog = MDDialog(

            title="Success",

            text=message,

            buttons=[

                MDFlatButton(

                    text="OK",

                    theme_text_color="Custom",

                    text_color=self.theme_cls.primary_color,

                    on_release=lambda x: dialog.dismiss()

                )

            ],

            radius=[20, 7, 20, 7]

        )

        dialog.open()

    

    def show_coming_soon(self, service_name):

        dialog = MDDialog(

            title=f"{service_name}",

            text=f"{service_name} service coming soon!",

            buttons=[

                MDFlatButton(

                    text="OK",

                    theme_text_color="Custom",

                    text_color=self.theme_cls.primary_color,

                    on_release=lambda x: dialog.dismiss()

                )

            ],

            radius=[20, 7, 20, 7]

        )

        dialog.open()

    

    def buy_data(self):

        if not self.current_user:

            self.show_error_dialog("Please login first")

            self.root.current = "login"

            return

            

        self.root.current = "data_purchase"

        screen = self.root.get_screen("data_purchase")

        screen.ids.data_phone_input.text = ""

    

    def show_balance_codes(self):

        balance_codes = {

            "MTN": "*556#",

            "Airtel": "*123#", 

            "Glo": "*124*0#",

            "9mobile": "*223#"

        }

        

        content = MDBoxLayout(

          orientation='vertical',

          spacing=dp(15),

          padding=dp(15),

          size_hint_y=None,

          height=dp(150))

        

        content.add_widget(MDLabel(

            text="To fund your wallet via USSD:",

            halign='center'

        ))

        

        # Create a grid to show all balance codes

        grid = MDGridLayout(

            cols=2,

            spacing=dp(10),

            size_hint_y=None,

            height=dp(100))

        

        for network, code in balance_codes.items():

            grid.add_widget(MDLabel(

                text=f"[b]{network}[/b]",

                markup=True,

                halign='left'

            ))

            grid.add_widget(MDFlatButton(

                text=code,

                on_release=lambda x, c=code: self.copy_to_clipboard(c),

                theme_text_color="Custom",

                text_color=self.theme_cls.primary_color

            ))

        

        content.add_widget(grid)

        

        dialog = MDDialog(

            title="Balance Check Codes",

            type="custom",

            content_cls=content,

            buttons=[

                MDFlatButton(

                    text="CLOSE",

                    theme_text_color="Custom",

                    text_color=self.theme_cls.primary_color,

                    on_release=lambda x: dialog.dismiss()

                )

            ],

            radius=[20, 7, 20, 7]

        )

        dialog.open()



    def show_all_users(self):

        if not self.users:

            self.show_error_dialog("No users registered yet")

            return

        

        content = MDBoxLayout(

          orientation='vertical',

          spacing=dp(15),

          padding=dp(15),

          size_hint_y=None,

          height=dp(400))

        

        scroll = ScrollView()

        user_list = MDList(spacing=dp(10))

        

        for user_id, user_data in self.users.items():

            item = TwoLineListItem(

                text=f"User: {user_data['name']}",

                secondary_text=f"Email: {user_data['email']}\nPhone: {user_data['phone']}",

                theme_text_color="Custom",

                text_color=self.theme_cls.primary_color,

                secondary_text_color=[0.4, 0.4, 0.4, 1]

            )

            user_list.add_widget(item)

        

        scroll.add_widget(user_list)

        content.add_widget(scroll)

        

        dialog = MDDialog(

            title="All Registered Users",

            type="custom",

            content_cls=content,

            size_hint=(0.9, None),

            buttons=[

                MDFlatButton(

                    text="CLOSE",

                    theme_text_color="Custom",

                    text_color=self.theme_cls.primary_color,

                    on_release=lambda x: dialog.dismiss()

                )

            ],

            radius=[20, 7, 20, 7]

        )

        dialog.open()



    def switch_screen(self, screen_name):
        """Switch screens directly - no transition, avoids FBO GPU crash."""
        try:
            self.root.current = screen_name
            self.current_screen_name = screen_name
            if screen_name == 'history':
                # Only reload if no transactions already showing
                screen = self.root.get_screen('history')
                if not screen.ids.history_list.children:
                    Clock.schedule_once(
                        lambda dt: self.load_transaction_history(), 0.1
                    )
        except Exception as e:
            print(f"switch_screen error: {e}")
      
    def show_history_filters(self):
        """Show filter menu for transaction history"""
        filter_options = [
            {"text": "All Transactions", "value": "all",         "icon": "format-list-checks"},
            {"text": "Airtime",          "value": "airtime",     "icon": "phone"},
            {"text": "Data",             "value": "data",        "icon": "wifi"},
            {"text": "Electricity",      "value": "electricity", "icon": "flash"},
            {"text": "Cable TV",         "value": "cable",       "icon": "television"},
            {"text": "Successful",       "value": "success",     "icon": "check-circle"},
            {"text": "Failed",           "value": "failed",      "icon": "close-circle"},
        ]

        if self.filter_menu is not None:
            self.filter_menu.dismiss()

        # Use history screen header as caller (always exists)
        screen = self.root.get_screen('history')

        self.filter_menu = MDDropdownMenu(
            caller=screen,
            items=[{
                "text": item["text"],
                "on_release": lambda x=item["value"]: self._apply_history_filter(x)
            } for item in filter_options],
            width_mult=4,
            max_height=dp(350),
            radius=[15, 15, 15, 15],
        )
        self.filter_menu.open()

    def _apply_history_filter(self, filter_type):
        """Apply selected filter"""
        if self.filter_menu is not None:
            self.filter_menu.dismiss()
            self.filter_menu = None
        self.filter_history(filter_type)

    def _show_loading(self, show, message="Loading transactions..."):
        try:
            screen = self.root.get_screen('history')
            screen.ids.loading_indicator.opacity = 1 if show else 0
            screen.ids.history_spinner.active = show
            if not show:
                has_tx = bool(screen.ids.history_list.children)
                screen.ids.history_list.opacity = 1 if has_tx else 0
                screen.ids.empty_state.opacity = 0 if has_tx else 1
        except Exception as e:
            print(f"_show_loading error: {e}")
            

    def filter_history(self, filter_type):
        """Filter history — reloads from backend with filter applied."""
        screen = self.root.get_screen('history')
        self._update_filter_chips(screen, filter_type)
        self.load_transaction_history(filter_type)

    
    def _show_history_skeleton(self, screen, show):
        """Toggles shimmering placeholder rows shaped like transaction
        items while the real list is loading — replaces a blank gap with
        an immediate sense of the page's shape."""
        try:
            box = screen.ids.history_skeleton_box
        except Exception:
            return

        if show:
            box.clear_widgets()
            for _ in range(5):
                box.add_widget(SkeletonCard())
            box.height = 5 * (dp(72) + dp(8))
            box.opacity = 1
        else:
            for child in list(box.children):
                if hasattr(child, 'stop'):
                    child.stop()
            box.clear_widgets()
            box.height = 0
            box.opacity = 0

    def _show_history_offline_banner(self, screen, show):
        """Tells the user plainly when they're looking at locally-cached
        transactions because the live request failed — rather than
        silently showing old data as if it were fresh."""
        try:
            banner = screen.ids.history_offline_banner
        except Exception:
            return
        if show:
            banner.text = "Showing saved data — check your connection for the latest"
            banner.height = dp(30)
            banner.opacity = 1
        else:
            banner.text = ""
            banner.height = 0
            banner.opacity = 0

    def load_transaction_history(self, filter_type='all'):
        """Load transaction history from backend."""
        if not self.current_user or not self.session_token:
            return

        # Safely reset screen state
        try:
            screen = self.root.get_screen("history")
            screen.ids.loading_indicator.opacity = 1
            screen.ids.history_spinner.active = True
            screen.ids.empty_state.opacity = 0
            screen.ids.history_list.clear_widgets()
            screen.ids.history_list.height = 0
            self._show_history_offline_banner(screen, False)
            self._show_history_skeleton(screen, True)
        except Exception as e:
            print(f"History screen reset error: {e}")

        def on_success(req, result):
            try:
                screen.ids.loading_indicator.opacity = 0
                screen.ids.history_spinner.active = False
                self._show_history_skeleton(screen, False)
                self._show_history_offline_banner(screen, False)
            except Exception:
                pass

            if result.get('status') == 'success':
                txns = result.get('data', {}).get('transactions', [])
                Clock.schedule_once(
                    lambda dt: self._display_backend_transactions(txns, filter_type), 0.1
                )
            else:
                self._show_empty_state(True)

        def on_failure(req, error):
            try:
                screen.ids.loading_indicator.opacity = 0
                screen.ids.history_spinner.active = False
                self._show_history_skeleton(screen, False)
                self._show_history_offline_banner(screen, True)
            except Exception:
                pass
            print(f"History load failed: {error}")
            Clock.schedule_once(
                lambda dt: self._display_transaction_history(), 0.1
            )

        def on_error(req, error):
            try:
                screen.ids.loading_indicator.opacity = 0
                screen.ids.history_spinner.active = False
                self._show_history_skeleton(screen, False)
                self._show_history_offline_banner(screen, True)
            except Exception:
                pass
            Clock.schedule_once(
                lambda dt: self._display_transaction_history(), 0.1
            )

        from kivy.network.urlrequest import UrlRequest
        UrlRequest(
            f"{self.backend_url}/api/payment/transactions?per_page=50",
            on_success=on_success,
            on_failure=on_failure,
            on_error=on_error,
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            timeout=20,
        )  

    def _display_transaction_history(self):
        """Fallback: display local transactions when backend unavailable."""
        screen = self.root.get_screen("history")

        try:
            screen.ids.loading_indicator.opacity = 0
            screen.ids.history_spinner.active = False
        except Exception:
            pass

        if not self.transactions:
            self._show_empty_state(True)
            return

        self._show_empty_state(False)
        history_list = screen.ids.history_list
        history_list.clear_widgets()

        for tx_id, tx_data in self.transactions.items():
            if not isinstance(tx_data, dict):
                continue
            try:
                card = self._create_transaction_item(tx_data)
                history_list.add_widget(card)
            except Exception as e:
                print(f"Local transaction card error: {e}")

        history_list.height = history_list.minimum_height

    

    def _update_filter_chips(self, screen, filter_type):
        """No-op — filter chips widget removed, filter applied directly."""
        pass


    def _get_filtered_transactions(self, filter_type):

        """Get filtered transactions for the current user"""

        try:

            if not self.current_user:

                return []

            

            if not hasattr(self, '_cached_user_id') or not self._cached_user_id:

                self._cached_user_id = next((k for k, v in self.users.items() if v == self.current_user), None)

            

            if not self._cached_user_id:

                return []

            

            transactions = [t for t in self.transactions.values() if t.get('user_id') == self._cached_user_id]

            

            if filter_type.lower() == "all":

                return sorted(

                    transactions,

                    key=lambda x: self._parse_transaction_date(x.get('date', '')),

                    reverse=True

                )

            

            filter_map = {

                "airtime": lambda t: t.get('type', '').lower() == "airtime",

                "data": lambda t: t.get('type', '').lower() == "data",

                "electricity": lambda t: t.get('type', '').lower() == "electricity",

                "cable": lambda t: t.get('type', '').lower() == "cable tv",

                "success": lambda t: t.get('status', '').lower() == "successful",

                "failed": lambda t: t.get('status', '').lower() == "failed",

                "week": lambda t: self._is_within_days(t.get('date', ''), 7),

                "month": lambda t: self._is_within_days(t.get('date', ''), 30)

            }

            

            filter_func = filter_map.get(filter_type.lower(), lambda t: True)

            return sorted(

                [t for t in transactions if filter_func(t)],

                key=lambda x: self._parse_transaction_date(x.get('date', '')),

                reverse=True

            )

        

        except Exception as e:

            print(f"Filter error: {e}")

            return []



    def _is_within_days(self, date_str, days):

        """Check if transaction date is within specified days"""

        try:

            trans_date = self._parse_transaction_date(date_str)

            return (datetime.now() - trans_date).days <= days

        except:

            return False



    def _parse_transaction_date(self, date_str):

        """Parse transaction date with multiple format support"""

        if not date_str or not isinstance(date_str, str):

            return datetime.min

        

        formats = [

            "%B %d, %Y %I:%M:%S %p",

            "%Y-%m-%d %H:%M:%S",

            "%d/%m/%Y %H:%M:%S"

        ]

        

        for fmt in formats:

            try:

                return datetime.strptime(date_str, fmt)

            except ValueError:

                continue

        

        print(f"Invalid date format: {date_str}")

        return datetime.min



    def _display_transactions(self, transactions):

        """Display transactions in the history list"""

        screen = self.root.get_screen('history')

        history_list = screen.ids.history_list

        history_list.clear_widgets()

        

        for transaction in transactions:

            item = self._create_transaction_item(transaction)

            history_list.add_widget(item)

        

        history_list.height = history_list.minimum_height

        screen.ids.history_scroll.scroll_y = 1

        screen.ids.empty_state.opacity = 0


    def _show_empty_state(self, show):
        try:
            screen = self.root.get_screen('history')
            screen.ids.empty_state.opacity = 1 if show else 0
            screen.ids.history_list.opacity = 0 if show else 1
        except Exception as e:
            print(f"_show_empty_state error: {e}")



    def _create_transaction_item(self, transaction):
        if not self._validate_transaction(transaction):
            return MDLabel(
                text="Invalid transaction",
                size_hint_y=None,
                height=dp(50)
            )
        card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            size_hint_x=1,
            height=dp(90),
            padding=[dp(16), dp(10), dp(16), dp(10)],
            spacing=dp(6),
            radius=[12],
            elevation=1,
            md_bg_color=self._get_card_bg_color(),
            on_release=lambda x: self.show_transaction_details(transaction)
        )
        self._build_card_content(card, transaction)
        return card

    def _validate_transaction(self, transaction):

        """Validate transaction has all required fields"""

        required_fields = ['type', 'amount', 'status', 'date']

        return all(field in transaction for field in required_fields)



    def _get_card_bg_color(self):

        """Get card background color based on theme"""

        return [0.95, 0.95, 0.98, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.25, 1]



    def _get_status_color(self, status):

        """Return color based on transaction status"""

        return self.theme_cls.success_color if status.lower() == "successful" else self.theme_cls.error_color



    def _get_transaction_icon(self, trans_type):

        """Return icon and color for transaction type"""

        icon_map = {

            'airtime': ('phone', [0, 0.7, 0, 1]),

            'data': ('wifi', [0.2, 0.5, 1, 1]),

            'electricity': ('flash', [1, 0.8, 0, 1]),

            'cable tv': ('television', [0.7, 0, 0.7, 1])

        }

        return icon_map.get(trans_type.lower(), ('history', [0.5, 0.5, 0.5, 1]))



    def _get_text_color(self):

        """Return primary text color based on theme"""

        return [0, 0, 0, 1] if self.theme_cls.theme_style == "Light" else [1, 1, 1, 1]



    def _get_secondary_text_color(self):

        """Return secondary text color based on theme"""

        return [0.54, 0.54, 0.54, 1] if self.theme_cls.theme_style == "Light" else [0.7, 0.7, 0.7, 1]



    def _build_card_content(self, card, transaction):
        """Build the content for a transaction card - fixed layout"""
            
        first_row = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            adaptive_height=True,
            spacing=dp(10)
        )                    

        icon, icon_color = self._get_transaction_icon(transaction.get('type', '').lower()
        )
        
        
        first_row.add_widget(MDIcon(
            icon=icon,
            theme_text_color="Custom",
            text_color=icon_color,
            size_hint=(None, None),
            padding=[0, dp(50), 0, 0],
            pos_hint={"center_y": .83},
            size=(dp(22), dp(22)),
        ))
        first_row.add_widget(MDLabel(
            text=transaction.get('type', 'Transaction'),
            font_style='Subtitle1',
            theme_text_color="Custom",
            text_color=self._get_text_color(),
            size_hint_x=0.5,
            halign="left",
        ))
        raw_date = str(
            transaction.get('date') or
            transaction.get('created_at') or ''
        )
        try:
            from datetime import datetime
            if raw_date and raw_date[4:5] == '-':
                # Backend ISO format: "2026-06-17T..." or "2026-06-17 ..."
                dt = datetime.strptime(raw_date[:10], "%Y-%m-%d")
                date_str = dt.strftime("%b %d, %Y")
            elif raw_date and ',' in raw_date:
                # Local format: "June 17, 2026 12:00:00 PM"
                # Split on space, take first 3 parts: ["June", "17,", "2026"]
                parts = raw_date.split()
                date_str = ' '.join(parts[:3]) if len(parts) >= 3 else raw_date[:15]
            else:
                date_str = raw_date[:10]
        except Exception:
            date_str = raw_date[:12]
        
        first_row.add_widget(MDLabel(
            text=date_str,
            font_style='Caption',
            theme_text_color="Custom",
            text_color=self._get_secondary_text_color(),
            halign='right',
            size_hint_x=None,
            width=dp(90),
        ))
        card.add_widget(first_row)
        
        # Row 2: Amount on left, status on right (single line)
        second_row = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            adaptive_height=True,
            spacing=dp(8)
        )

        amount = str(transaction.get('amount', '₦0.00'))
        if not amount.startswith('₦'):
            amount = f'₦{amount}'

        second_row.add_widget(MDLabel(
            text=amount,
            font_style='H6',
            theme_text_color="Custom",
            text_color=self._get_text_color(),
            bold=True,
            size_hint_x=0.55,
        ))
        
        status_box = MDBoxLayout(
            orientation="horizontal",
            adaptive_width=True,
            spacing=dp(5),
        )

        status = str(transaction.get('status', 'pending')).lower()
        status_color = self._get_status_color(status)
        status_text = 'Successful' if status in ('successful', 'success') else status.capitalize()

        second_row.add_widget(MDIcon(
            icon="check-circle" if status in ('successful', 'success') else "close-circle",
            theme_text_color="Custom",
            text_color=status_color,                    
            size_hint=(None, None),
            size=(dp(20), dp(20)),
            pos_hint={"center_y": .5},
        ))
          
        second_row.add_widget(MDLabel(
            text=status_text,
            font_style='Body2',
            theme_text_color="Custom",
            text_color=status_color,
            bold=True,
            size_hint_x=0.35,
            adaptive_width=True,
            halign='left',
        ))
        card.add_widget(second_row)


    def show_transaction_details(self, transaction):
        """Show full details of a transaction in a dialog."""
        if not isinstance(transaction, dict):
            self.show_error_dialog("Invalid transaction data")
            return

        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(12),
            padding=dp(20),
            size_hint_y=None,
            height=dp(320),
        )

        fields = [
            ("Type", (transaction.get('service_type') or transaction.get('type') or 'Unknown').replace('_', ' ').title()),
            ("Status", transaction.get('status', 'Unknown').capitalize()),
            ("Amount", transaction.get('amount') or f"₦{transaction.get('amount', 0):,.2f}"),
            ("Date", (transaction.get('date') or transaction.get('created_at') or 'Unknown')[:19]),
            ("Reference", transaction.get('reference', 'N/A')),
        ]

        # Add service-specific fields
        details = transaction.get('details') or {}
        if isinstance(details, dict):
            if details.get('phone'):
                fields.append(("Phone", details['phone']))
            if details.get('meter_number'):
                fields.append(("Meter", details['meter_number']))
            if details.get('token'):
                fields.append(("Token", details['token']))
            if details.get('smartcard'):
                fields.append(("Smartcard", details['smartcard']))

        # Direct fields
        if transaction.get('phone'):
            if not any(f[0] == 'Phone' for f in fields):
                fields.append(("Phone", transaction['phone']))
        if transaction.get('network'):
            fields.append(("Network", transaction['network']))

        for label, value in fields:
            row = MDBoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(35),
                spacing=dp(10),
            )
            row.add_widget(MDLabel(
                text=f"[b]{label}:[/b]",
                markup=True,
                size_hint_x=0.35,
                theme_text_color="Secondary",
                font_style="Body2",
            ))
            val_label = MDLabel(
                text=str(value),
                size_hint_x=0.65,
                theme_text_color="Primary",
                font_style="Body2",
            )
            row.add_widget(val_label)
            content.add_widget(row)

        # Copy button for token
        if isinstance(details, dict) and details.get('token'):
            token = details['token']
            content.add_widget(MDRaisedButton(
                text="COPY TOKEN",
                size_hint_y=None,
                height=dp(40),
                md_bg_color=self.theme_cls.primary_color,
                on_release=lambda x, t=token: self.copy_to_clipboard(t),
            ))

        dialog = MDDialog(
            title="Transaction Details",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CLOSE",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: dialog.dismiss(),
                )
            ],
            radius=[20, 7, 20, 7],
        )
        dialog.open()


    def _add_detail_row(self, container, label, value, value_color=None):

        """Add a detail row to the details box"""

        row = MDBoxLayout(

            orientation='horizontal',

            adaptive_height=True,

            spacing=dp(10)

        )

        

        row.add_widget(MDLabel(

            text=f"{label}:",

            halign='left',

            size_hint_x=0.4,

            theme_text_color="Secondary",

            bold=True,

            font_style="Subtitle1"

        ))

        

        value_label = MDLabel(

            text=str(value),

            halign='left',

            size_hint_x=0.6,

            theme_text_color="Primary" if not value_color else "Custom",

            text_color=value_color if value_color else self._get_text_color(),

            font_style="Subtitle1"

        )

        

        if label.lower() in ["phone", "meter", "smartcard", "transaction id"]:

            value_label.theme_text_color = "Custom"

            value_label.text_color = self.theme_cls.primary_color

            value_label.bind(on_touch_down=lambda x, touch, text=value: self._copy_text(x, touch, text))

        

        row.add_widget(value_label)

        container.add_widget(row)



    def _copy_text(self, instance, touch, text):

        """Handle text copying when user taps on certain fields"""

        if instance.collide_point(*touch.pos):

            Clipboard.copy(text)

            toast(f"Copied: {text}")

            return True

        return False



    def share_transaction(self, transaction):

        """Share transaction details via platform sharing"""

        share_text = f"Transaction Details:\nType: {transaction['type']}\n"

        share_text += f"Amount: {transaction['amount']}\n"

        share_text += f"Status: {transaction['status']}\n"

        share_text += f"Date: {transaction['date']}"

        

        if 'phone' in transaction:

            share_text += f"\nPhone: {transaction['phone']}"

        if 'network' in transaction:

            share_text += f"\nNetwork: {transaction['network']}"

        

        if platform == 'android':

            from jnius import autoclass

            Intent = autoclass('android.content.Intent')

            intent = Intent(Intent.ACTION_SEND)

            intent.setType('text/plain')

            intent.putExtra(Intent.EXTRA_TEXT, share_text)

            current_activity = autoclass('org.kivy.android.PythonActivity').mActivity

            current_activity.startActivity(Intent.createChooser(intent, 'Share Transaction'))

        else:

            toast("Sharing not implemented on this platform")

            print(share_text)

        

        toast("Sharing transaction details...")

    def show_error_dialog(self, message):

        """Show error dialog with message"""

        dialog = MDDialog(

            title="Error",

            text=message,

            buttons=[

                MDFlatButton(

                    text="OK",

                    on_release=lambda x: dialog.dismiss()

                )

            ]

        )

        dialog.open()
        

    def show_profile(self):

        if not self.current_user:

            return
          

        profile_screen = self.root.get_screen("profile")

        profile_screen.ids.profile_name.text = self.current_user['name']

        self.root.current = "profile"

    
    def handle_session_expired(self):
        """Called whenever any backend call comes back 401 (expired/invalid token)."""
        if getattr(self, '_session_expired_handled', False):
            return
        self._session_expired_handled = True
        self.current_user = None
        self.session_token = None
        self.show_error_dialog("Your session expired - please log in again")
        self.route_to_login_or_pin()
        Clock.schedule_once(lambda dt: setattr(self, '_session_expired_handled', False), 2)

    def route_to_login_or_pin(self):
        """Go to the PIN quick-unlock screen if one is configured, else full login."""
        if self.quick_pin_data and self.quick_pin_data.get('pin_hash'):
            try:
                pin_screen = self.root.get_screen("pin_login")
                cached_user = self.quick_pin_data.get('user') or {}
                name = cached_user.get('name') or self.quick_pin_data.get('email', '')
                pin_screen.ids.pin_welcome_label.text = f"Welcome back, {name}!"
            except Exception as e:
                print(f"pin welcome label error: {e}")
            self.root.current = "pin_login"
        else:
            self.root.current = "login"

    def logout_user(self):

        self.current_user = None

        self.session_token = None

        self.show_success_dialog("Logged out successfully")

        self.route_to_login_or_pin()

    def register_user(self, name, email, phone, referral_code, password, confirm_password):
        """Handle user registration with backend API"""
        # Validation (same as before)
        if not all([name, email, phone, password, confirm_password]):
            self.show_error_dialog("Please fill all required fields")
            return
        
        if password != confirm_password:
            self.show_error_dialog("Passwords do not match")
            return
        
        if not is_valid_email(email):
            self.show_error_dialog("Invalid email address")
            return
        
        if not is_valid_phone(phone):
            self.show_error_dialog("Phone number must be 11 digits")
            return
        
        self.show_loader("Creating your account...")

        registration_data = {
            'name': name,
            'email': email.lower(),
            'phone': phone,
            'password': password   # ✅ Raw password, NOT hashed
        }
        if referral_code and referral_code.strip():
            registration_data['referral_code'] = referral_code.strip()

        def callback(success, response):
            self.hide_loader()

            # Check if account was actually created despite error status
            # (happens when SMS fails — backend returns 500 but account exists)
            if response and response.get('data', {}).get('user_id'):
                # Account was created — go to OTP screen regardless
                data = response.get('data', {})
                self.pending_user_id = data.get('user_id')
                self.pending_user_phone = data.get('phone', '')

                otp_screen = self.root.get_screen("otp_verification")
                otp_screen.ids.otp_email_or_phone.text = f"to {data.get('phone', '')}"
                self.root.current = "otp_verification"
                self.clear_registration_form()

                if data.get('sms_failed'):
                    self.show_error_dialog(
                        "Account created but SMS failed.\n"
                        "Tap 'Resend OTP' to get your code."
                    )
                return

            if success and response and response.get('status') == 'success':
                data = response.get('data', {})
                self.pending_user_id = data.get('user_id')
                self.pending_user_phone = data.get('phone', '')

                otp_screen = self.root.get_screen("otp_verification")
                otp_screen.ids.otp_email_or_phone.text = f"to {data.get('phone', '')}"
                self.root.current = "otp_verification"
                self.clear_registration_form()
            else:
                msg = (response.get('message', 'Registration failed')
                       if response else 'Connection failed')
                self.show_error_dialog(f"Registration failed: {msg}")

        self.backend_api_request('auth/register', 'POST', registration_data, callback)

     
    def verify_otp(self, otp_code):
        if not hasattr(self, 'pending_user_id') or not self.pending_user_id:
            self.show_error_dialog("No pending verification found. Please login again.")
            self.root.current = "login"
            return

        if not otp_code or len(otp_code) != 6 or not otp_code.isdigit():
            self.show_error_dialog("Please enter a valid 6-digit OTP")
            return

        self.show_loader("Verifying OTP...")
        data = {'user_id': self.pending_user_id, 'otp_code': otp_code}

        def callback(success, response):
            self.hide_loader()
            if success and response.get('status') == 'success':
                data = response.get('data', {})
                self.session_token = data.get('session_token')   # ✅ Store JWT
                self.current_user = data.get('user', {})
                self.update_dashboard()
                self.show_success_dialog("Account verified successfully!")
                self.root.current = "dashboard"
                # Clear pending data
                self.pending_user_id = None
                self.pending_user_email = None
                self.pending_user_phone = None
            else:
                error_msg = response.get('message', 'Verification failed') if response else 'Network error'
                self.show_error_dialog(f"OTP verification failed: {error_msg}")

        self.backend_api_request('auth/verify-otp', 'POST', data, callback)
   
    
    
    def update_dashboard_virtual_account(self):
        """Update the virtual account label on dashboard."""
        screen = self.root.get_screen('dashboard')
        if hasattr(screen.ids, 'virtual_account_display'):
            if self.virtual_account_number:
                screen.ids.virtual_account_display.text = f"{self.virtual_bank_name} - {self.virtual_account_number}"
            else:
                screen.ids.virtual_account_display.text = "No virtual account yet"   
   
    def fetch_virtual_account_details(self):
        if not self.session_token:
            return

        def on_success(req, result):
            if result.get('status') == 'success':
                data = result['data']
                self.virtual_account_number = data.get('account_number') or ''
                self.virtual_bank_name = data.get('bank_name') or ''
                self.virtual_account_name = data.get('account_name') or ''
                balance = data.get('wallet_balance')
                if balance is not None and self.current_user:
                    self.current_user['wallet_balance'] = balance
                self.update_dashboard()
                self.update_dashboard_virtual_account()

        def on_failure(req, error):
            print(f"fetch_virtual_account_details failed: {error}")

        def on_error(req, error):
            print(f"fetch_virtual_account_details error: {error}")

        UrlRequest(
            f"{self.backend_url}/api/payment/account-details",
            on_success=on_success, on_failure=on_failure, on_error=on_error,
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            timeout=15,
        )
    
    
    def update_dashboard_virtual_account(self):
        """Update virtual account display on dashboard."""
        try:
            screen = self.root.get_screen('dashboard')
            if hasattr(screen.ids, 'virtual_account_display'):
                if self.virtual_account_number:
                    screen.ids.virtual_account_display.text = (
                        f"{self.virtual_bank_name} — {self.virtual_account_number}"
                    )
                else:
                    screen.ids.virtual_account_display.text = "Loading account..."
        except Exception as e:
            print(f"update_dashboard_virtual_account error: {e}")                    
            
    
    def copy_virtual_account(self):
        """Copy virtual account number to clipboard."""
        if self.virtual_account_number:
            from kivy.core.clipboard import Clipboard
            Clipboard.copy(self.virtual_account_number)
            self.show_success_dialog(
                f"Account number copied!\n\n"
                f"Bank:    {self.virtual_bank_name}\n"
                f"Number:  {self.virtual_account_number}\n"
                f"Name:    {self.virtual_account_name}\n\n"
                f"Transfer any amount to fund your wallet instantly."
            )
        else:
            # Try fetching first
            self.fetch_virtual_account_details()
            self.show_error_dialog(
                "Account number not loaded yet. Please wait and try again."
            )                            
            

    
    def show_funding_options(self):
        self.selected_funding_method = ""
        self.funding_amount = 0
        self.root.current = "funding"
        Clock.schedule_once(lambda dt: self.fetch_virtual_account_details(), 0.5)
        
        
    def fund_wallet_card(self):
        """Open Paystack card payment in browser."""
        if not self.current_user or not self.session_token:
            self.show_error_dialog("Please login first")
            return
        amount = self.funding_amount
        if amount < 100:
            self.show_error_dialog("Minimum funding amount is ₦100")
            return
        self.show_loader("Initializing payment...")
        payload = {'amount': amount}
        def on_success(req, result):
            self.hide_loader()
            if result.get('status') == 'success':
                auth_url = result['data']['authorization_url']
                self.current_payment_reference = result['data']['reference']
                import webbrowser
                webbrowser.open(auth_url)
                self.show_success_dialog(
                    "Complete payment in your browser.\n"
                    "Your wallet will be credited automatically."
                )
                # Start checking after 15 seconds
                from kivy.clock import Clock
                Clock.schedule_once(
                    lambda dt: self._check_payment_status(self.current_payment_reference),
                    15
                )
            else:
                self.show_error_dialog(result.get('message', 'Payment failed'))
        def on_failure(req, error):
            self.hide_loader()
            self.show_error_dialog(f"Network error: {error}")
        import json
        from kivy.network.urlrequest import UrlRequest
        UrlRequest(
            f"{self.backend_url}/api/payment/initialize",
            on_success=on_success,
            on_failure=on_failure,
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            req_body=json.dumps(payload),
            timeout=30,
        )

    def _check_payment_status(self, reference, attempt=0):
        """Poll payment status after card payment."""
        if attempt >= 20 or not self.session_token:
            return

        from kivy.clock import Clock
        from kivy.network.urlrequest import UrlRequest

        def on_success(req, result):
            if result.get('status') == 'success':
                self.fetch_virtual_account_details()
                balance = result.get('data', {}).get('wallet_balance', '')
                msg = (f"Wallet funded successfully!\nNew balance: ₦{balance:,.2f}"
                       if balance else "Wallet funded successfully!")
                self.show_success_dialog(msg)
            else:
                Clock.schedule_once(
                    lambda dt: self._check_payment_status(reference, attempt + 1), 30
                )

        def on_failure(req, error):
            Clock.schedule_once(
                lambda dt: self._check_payment_status(reference, attempt + 1), 30
            )

        UrlRequest(
            f"{self.backend_url}/api/payment/verify/{reference}",
            on_success=on_success,
            on_failure=on_failure,
            req_headers={
                'Authorization': f'Bearer {self.session_token}',
                'Content-Type': 'application/json',
            },
            timeout=15,
        )           

    
    def _quick_pin_path(self):
        try:
            return os.path.join(self.user_data_dir, "quick_pin.json")
        except Exception:
            return "quick_pin.json"

    def load_quick_pin(self):
        """Load saved quick-PIN data (email, pin_hash, session_token, cached user), if any."""
        try:
            path = self._quick_pin_path()
            if os.path.exists(path):
                with open(path, "r") as f:
                    self.quick_pin_data = json.load(f)
            else:
                self.quick_pin_data = None
        except Exception as e:
            print(f"load_quick_pin error: {e}")
            self.quick_pin_data = None
        return self.quick_pin_data

    def save_quick_pin(self, pin, email, session_token, user):
        """Persist a hashed PIN plus the session needed to restore login on unlock.
        Returns True on success, False on failure (caller should check this -
        previously a failed save still showed a false 'success' message)."""
        try:
            path = self._quick_pin_path()
            os.makedirs(os.path.dirname(path), exist_ok=True)
            pin_hash = hashlib.sha256(f"{pin}:{email.lower()}".encode()).hexdigest()
            data = {
                "email": email.lower(),
                "pin_hash": pin_hash,
                "session_token": session_token,
                "user": user,
            }
            with open(path, "w") as f:
                json.dump(data, f)
            # Verify it actually round-trips before trusting it
            with open(path, "r") as f:
                json.load(f)
            self.quick_pin_data = data
            return True
        except Exception as e:
            print(f"save_quick_pin error: {e}")
            return False

    def clear_quick_pin(self):
        try:
            path = self._quick_pin_path()
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            print(f"clear_quick_pin error: {e}")
        self.quick_pin_data = None

    def prompt_setup_quick_pin(self, email, session_token, user):
        """After a successful full login, offer to set up a quick PIN for next time."""
        try:
            pin_field = MDTextField(
                hint_text="Choose a 4-6 digit PIN",
                icon_left="shield-key-outline",
                password=True,
                input_filter="int",
                max_text_length=6,
            )
            confirm_field = MDTextField(
                hint_text="Confirm PIN",
                icon_left="shield-key-outline",
                password=True,
                input_filter="int",
                max_text_length=6,
            )
            content = MDBoxLayout(
                orientation="vertical",
                spacing=dp(15),
                size_hint_y=None,
                height=dp(120),
                padding=[dp(10), dp(10), dp(10), dp(10)],
            )
            content.add_widget(pin_field)
            content.add_widget(confirm_field)

            def do_enable(*a):
                pin = pin_field.text.strip()
                confirm = confirm_field.text.strip()
                if len(pin) < 4:
                    self.show_error_dialog("PIN must be at least 4 digits")
                    return
                if pin != confirm:
                    self.show_error_dialog("PINs do not match")
                    return
                if self.save_quick_pin(pin, email, session_token, user):
                    dialog.dismiss()
                    self.show_success_dialog("Quick PIN login enabled!")
                else:
                    dialog.dismiss()
                    self.show_error_dialog("Couldn't save PIN - please try again")

            def do_skip(*a):
                dialog.dismiss()

            dialog = MDDialog(
                title="Set up quick PIN login?",
                text="Skip typing your email and password next time - just use a short PIN.",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(text="SKIP", on_release=do_skip),
                    MDRaisedButton(text="ENABLE", on_release=do_enable),
                ],
            )
            dialog.open()
        except Exception as e:
            print(f"prompt_setup_quick_pin error: {e}")

    def attempt_pin_login(self):
        """Validate the entered PIN against the saved hash and restore the session."""
        try:
            screen = self.root.get_screen("pin_login")
            pin = screen.ids.pin_input.text.strip()
            if not self.quick_pin_data:
                self.switch_to_full_login()
                return
            expected_hash = hashlib.sha256(
                f"{pin}:{self.quick_pin_data.get('email', '')}".encode()
            ).hexdigest()
            if pin and expected_hash == self.quick_pin_data.get("pin_hash"):
                self.session_token = self.quick_pin_data.get("session_token") or ""
                self.current_user = self.quick_pin_data.get("user") or {}
                self.virtual_account_number = self.current_user.get('virtual_account_number') or ''
                self.virtual_bank_name = self.current_user.get('virtual_bank_name') or ''
                self.virtual_account_name = self.current_user.get('virtual_account_name') or ''
                screen.ids.pin_input.text = ""
                self.update_dashboard()
                self.update_dashboard_virtual_account()
                self.fetch_virtual_account_details()
                self.root.current = "dashboard"
            else:
                screen.ids.pin_input.text = ""
                self.show_error_dialog("Incorrect PIN")
        except Exception as e:
            print(f"attempt_pin_login error: {e}")

    def switch_to_full_login(self):
        try:
            screen = self.root.get_screen("pin_login")
            screen.ids.pin_input.text = ""
        except Exception:
            pass
        self.root.current = "login"

    def setup_a2c_network_screen(self):
        try:
            screen = self.root.get_screen("airtime_to_cash")
            grid = screen.ids.a2c_network_grid
            grid.clear_widgets()
            self.a2c_network_cards = {}

            networks = [
                {"name": "MTN", "logo": "assets/mtn.png", "color": self.mtn_color},
                {"name": "Airtel", "logo": "assets/airtel.png", "color": self.airtel_color},
                {"name": "Glo", "logo": "assets/glo.png", "color": self.glo_color},
                {"name": "9Mobile", "logo": "assets/9mobile.png", "color": self.mobile9_color},
            ]

            for net in networks:
                card = MDCard(
                    orientation='vertical',
                    size_hint=(1, 1),
                    elevation=2,
                    on_release=lambda x, n=net["name"]: self.select_a2c_network(n),
                    md_bg_color=[0.95, 0.95, 0.95, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1],
                    radius=[15]
                )
                try:
                    logo = FitImage(
                        source=net["logo"],
                        size_hint=(1, 0.7),
                        radius=[15, 15, 15, 15]
                    )
                except Exception:
                    logo = MDIcon(
                        icon="network",
                        size_hint=(1, 0.7),
                        theme_text_color="Custom",
                        text_color=net["color"]
                    )
                label = MDLabel(
                    text=net["name"],
                    halign="center",
                    font_style="Caption",
                    size_hint=(1, 0.3),
                )
                card.add_widget(logo)
                card.add_widget(label)
                grid.add_widget(card)
                self.a2c_network_cards[net["name"].upper()] = card
        except Exception as e:
            print(f"setup_a2c_network_screen error: {e}")

    def select_a2c_network(self, name):
        network = name.upper()
        self.a2c_network = network
        try:
            for net_key, card in self.a2c_network_cards.items():
                if net_key == network:
                    card.md_bg_color = self.theme_cls.primary_color
                else:
                    card.md_bg_color = [0.95, 0.95, 0.95, 1] if self.theme_cls.theme_style == "Light" else [0.2, 0.2, 0.2, 1]
        except Exception as e:
            print(f"select_a2c_network error: {e}")

    def a2c_reset_flow(self):
        """Reset the Airtime-to-Cash screen back to its starting state."""
        try:
            screen = self.root.get_screen("airtime_to_cash")
            screen.ids.a2c_phone_input.text = ""
            screen.ids.a2c_amount_input.text = ""
            screen.ids.a2c_otp_input.text = ""
            screen.ids.a2c_sim_pin_input.text = ""
        except Exception:
            pass
        self.a2c_step = "input"
        self.a2c_network = ""
        self.a2c_session_id = ""
        self.a2c_airtime_balance = ""

    def a2c_send_otp(self):
        try:
            screen = self.root.get_screen("airtime_to_cash")
            phone = screen.ids.a2c_phone_input.text.strip()
            amount = screen.ids.a2c_amount_input.text.strip()

            if not self.a2c_network:
                self.show_error_dialog("Please select a network")
                return
            if len(phone) != 11 or not phone.isdigit():
                self.show_error_dialog("Enter a valid 11-digit phone number")
                return
            if not amount or not amount.isdigit() or int(amount) < 50:
                self.show_error_dialog("Enter a valid amount (minimum ₦50)")
                return

            self.show_loader("Sending OTP...")

            def on_result(success, result):
                self.hide_loader()
                if success:
                    self.a2c_step = "otp"
                    self.show_success_dialog(result.get("message", "OTP sent!"))
                else:
                    self.show_error_dialog(result.get("message", "Failed to send OTP"))

            self.backend_api_request(
                "airtime-to-cash/generate-otp",
                "POST",
                data={"network": self.a2c_network, "phone": phone},
                callback=on_result,
            )
        except Exception as e:
            self.hide_loader()
            print(f"a2c_send_otp error: {e}")

    def a2c_verify_otp(self):
        try:
            screen = self.root.get_screen("airtime_to_cash")
            phone = screen.ids.a2c_phone_input.text.strip()
            otp = screen.ids.a2c_otp_input.text.strip()

            if not otp:
                self.show_error_dialog("Enter the OTP sent to your phone")
                return

            self.show_loader("Verifying OTP...")

            def on_result(success, result):
                self.hide_loader()
                if success:
                    data = result.get("data", {})
                    self.a2c_session_id = data.get("session_id") or ""
                    self.a2c_airtime_balance = data.get("airtime_balance") or ""
                    self.a2c_step = "confirm"
                else:
                    self.show_error_dialog(result.get("message", "Invalid or expired OTP"))

            self.backend_api_request(
                "airtime-to-cash/verify-otp",
                "POST",
                data={"network": self.a2c_network, "phone": phone, "otp": otp},
                callback=on_result,
            )
        except Exception as e:
            self.hide_loader()
            print(f"a2c_verify_otp error: {e}")

    def a2c_confirm_transfer(self):
        try:
            screen = self.root.get_screen("airtime_to_cash")
            phone = screen.ids.a2c_phone_input.text.strip()
            amount = screen.ids.a2c_amount_input.text.strip()
            sim_pin = screen.ids.a2c_sim_pin_input.text.strip()

            if not sim_pin:
                self.show_error_dialog("Enter your SIM's airtime transfer PIN")
                return

            self.show_loader("Converting airtime to cash...")

            def on_result(success, result):
                self.hide_loader()
                if success:
                    data = result.get("data", {})
                    credited = data.get("credited_amount")
                    new_balance = data.get("new_balance")
                    self.show_success_dialog(
                        f"₦{credited} credited to your wallet! New balance: ₦{new_balance}"
                    )
                    self.a2c_reset_flow()
                    self.update_dashboard()
                    self.fetch_virtual_account_details()
                    self.root.current = "dashboard"
                else:
                    message = result.get("message", "Conversion failed")
                    self.show_error_dialog(message)
                    if "session" in message.lower():
                        self.a2c_reset_flow()

            self.backend_api_request(
                "airtime-to-cash/transfer",
                "POST",
                data={
                    "network": self.a2c_network,
                    "phone": phone,
                    "amount": amount,
                    "sim_pin": sim_pin,
                    "session_id": self.a2c_session_id,
                },
                callback=on_result,
            )
        except Exception as e:
            self.hide_loader()
            print(f"a2c_confirm_transfer error: {e}")

    def login_user(self, email, password):
        if not email or not password:
            self.show_error_dialog("Email and password are required")
            return

        self.show_loader("Signing in...")
        login_data = {'email': email.lower(), 'password': password}

        def callback(success, response):
            self.hide_loader()
            if success and response.get('status') == 'success':
                data = response.get('data', {})
                self.session_token = data.get('session_token') or ''
                self.current_user = data.get('user', {})
                self.virtual_account_number = self.current_user.get('virtual_account_number') or ''
                self.virtual_bank_name = self.current_user.get('virtual_bank_name') or ''
                self.virtual_account_name = self.current_user.get('virtual_account_name') or ''
                self.update_dashboard()
                self.update_dashboard_virtual_account()
                self.fetch_virtual_account_details()   # token is set now
                self.show_success_dialog("Login successful!")
                self.root.current = "dashboard"
                if not self.quick_pin_data or self.quick_pin_data.get('email') != email.lower():
                    Clock.schedule_once(lambda dt: self.prompt_setup_quick_pin(email, self.session_token, self.current_user), 1)

            elif response and response.get('requires_verification'):
                self.pending_user_id = response.get('user_id')
                self.pending_user_phone = response.get('phone', '')
                otp_screen = self.root.get_screen("otp_verification")
                otp_screen.ids.otp_email_or_phone.text = (
                    f"to {response.get('phone', self.pending_user_phone)}"
                )
                self.root.current = "otp_verification"
                self.show_error_dialog("Account not verified. OTP sent to your phone.")
            else:
                msg = response.get('message', 'Login failed') if response else 'Connection failed'
                self.show_error_dialog(f"Login failed: {msg}")

        self.backend_api_request('auth/login', 'POST', login_data, callback)

  
    def resend_otp(self):
        if not hasattr(self, 'pending_user_id') or not self.pending_user_id:
            self.show_error_dialog("No pending verification found. Please login again.")
            self.root.current = "login"
            return

        self.show_loader("Resending OTP...")
        data = {'user_id': self.pending_user_id}

        def callback(success, response):
            self.hide_loader()
            if success and response.get('status') == 'success':
                data = response.get('data', {})
                if data.get('mock_otp'):
                    self.show_success_dialog(f"New OTP: {data.get('mock_otp')}")
                else:
                    self.show_success_dialog("New OTP sent to your phone")
            else:
                error_msg = response.get('message', 'Failed to resend OTP') if response else 'Network error'
                # ✅ Handle rate limit message
                if "wait 60 seconds" in error_msg:
                    self.show_error_dialog("Please wait 60 seconds before requesting a new OTP.")
                else:
                    self.show_error_dialog(f"Failed to resend OTP: {error_msg}")

        self.backend_api_request('auth/resend-otp', 'POST', data, callback)
 
    def clear_registration_form(self):
        """Clear all registration form fields"""
        try:
            screen = self.root.get_screen("register")
            screen.ids.reg_name.text = ""
            screen.ids.reg_email.text = ""
            screen.ids.reg_phone.text = ""
            screen.ids.reg_referral_code.text = ""
            screen.ids.reg_password.text = ""
            screen.ids.reg_confirm_password.text = ""
        except Exception as e:
            print(f"Error clearing registration form: {str(e)}")

   

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.users_file = "users.json"
        self.transactions_file = "transactions.json"
        self.settings_file = "app_settings.json"
        self.load_quick_pin()
        self.load_app_settings()   # sets self.theme_preference + resolves theme_cls.theme_style
        self.theme_cls.primary_hue = "500"
        self._shrink_font_styles(0.82)
        self.update_theme_colors()
        Window.bind(on_keyboard=self.handle_back_button)
        root = Builder.load_string(KV)
        register_challenge_screens(root, self)
        # These are local JSON caches nothing in the KV tree reads at parse
        # time (route_to_login_or_pin only depends on load_quick_pin(),
        # called above) — deferring them until right after the window can
        # render removes their I/O from the black-screen window before the
        # first frame paints, instead of blocking it.
        self.users = {}
        self.transactions = {}
        Clock.schedule_once(lambda dt: self.load_users(), 0)
        Clock.schedule_once(lambda dt: self.load_transactions(), 0)
        return root

    def _shrink_font_styles(self, scale):
        """Scales down KivyMD's whole default type scale (H1..Caption) by
        `scale`, applied once before the KV tree is built. Every MDLabel
        that uses font_style (nearly all text in this app) picks this up
        automatically — no need to touch each label individually, and it
        applies uniformly to bold heading styles (H6, Subtitle2, Button)
        the same as regular body text."""
        try:
            scaled = {}
            for name, props in self.theme_cls.font_styles.items():
                props = list(props)
                props[1] = max(10, round(props[1] * scale))   # never shrink below 10sp
                scaled[name] = props
            self.theme_cls.font_styles = scaled
        except Exception as e:
            print(f"_shrink_font_styles error: {e}")
    
    
    def handle_tvpass_error(self, error_msg):
        """Sarrafa errors daga TVPass API"""
        if "insufficient balance" in error_msg.lower():
            self.show_error_dialog("Insufficient balance in your TVPass account")
        elif "invalid api key" in error_msg.lower():
            self.show_error_dialog("Invalid TVPass API key. Please contact support.")
        elif "network" in error_msg.lower():
            self.show_error_dialog("Network error. Please check your connection.")
        else:
            self.show_error_dialog(f"TVPass API Error: {error_msg}")
            

    
    def update_dashboard(self):
        """Update dashboard with current data"""
        if hasattr(self, 'root') and self.root:
            screen = self.root.get_screen("dashboard")
            if screen:
                # Wallet balance - in production, this would come from backend
                balance = self.current_user.get('wallet_balance', 0) if self.current_user else 0
                screen.ids.wallet_balance.text = self.format_currency(balance)
                
                # Referral balance
                referral_balance = self.current_user.get('referral_balance', 0) if self.current_user else 0
                screen.ids.referral_balance.text = self.format_currency(referral_balance)

                self.check_pending_bill_reminders()
                


    def show_settings(self):
        """Show app settings"""
        content = MDBoxLayout(
            orientation='vertical', spacing=dp(10), padding=dp(15),
            size_hint_y=None, height=dp(230),
        )

        content.add_widget(MDLabel(text="Theme", font_style="Subtitle1",
                                     size_hint_y=None, height=dp(30)))

        current_pref = getattr(self, 'theme_preference', 'light')
        theme_row = MDBoxLayout(orientation='horizontal', spacing=dp(8),
                                  size_hint_y=None, height=dp(45))
        theme_buttons = {}

        def _select(pref):
            self._settings_selected_theme = pref
            for key, btn in theme_buttons.items():
                btn.md_bg_color = self.theme_cls.primary_color if key == pref else [0, 0, 0, 0]

        self._settings_selected_theme = current_pref
        for pref, label in (('light', 'Light'), ('dark', 'Dark'), ('system', 'Auto')):
            btn = MDFlatButton(
                text=label,
                md_bg_color=self.theme_cls.primary_color if pref == current_pref else [0, 0, 0, 0],
                on_release=lambda x, p=pref: _select(p),
            )
            theme_buttons[pref] = btn
            theme_row.add_widget(btn)
        content.add_widget(theme_row)

        notifications = MDCheckbox(
            active=self.current_user.get('notifications_enabled', True) if self.current_user else True,
            size_hint=(None, None), size=(dp(48), dp(48)),
        )
        notifications_label = MDLabel(text="Enable Notifications", font_style="Subtitle1")
        notifications_box = MDBoxLayout(orientation='horizontal', spacing=dp(10),
                                          size_hint_y=None, height=dp(50))
        notifications_box.add_widget(notifications)
        notifications_box.add_widget(notifications_label)
        content.add_widget(notifications_box)

        dialog = MDDialog(
            title="Settings", type="custom", content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL", theme_text_color="Custom",
                              text_color=self.theme_cls.primary_color,
                              on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(text="SAVE", theme_text_color="Custom", text_color=[1, 1, 1, 1],
                                md_bg_color=self.theme_cls.primary_color,
                                on_release=lambda x: self.save_settings(dialog, self._settings_selected_theme, notifications.active)),
            ],
            radius=[20, 7, 20, 7],
        )
        dialog.open()

    def save_settings(self, dialog, theme_preference, notifications_enabled):
        """Save app settings — persists the theme choice locally so it
        survives app restarts, and applies it with a smooth transition."""
        self.set_theme_preference(theme_preference)

        if self.current_user:
            # Find user by email, not list index
            user_key = None
            for uid, user in self.users.items():
                if user.get('email') == self.current_user.get('email'):
                    user_key = uid
                    break

            if user_key:
                self.users[user_key]['notifications_enabled'] = notifications_enabled
                self.current_user = self.users[user_key]
                self.save_users()
            else:
                # Backend user not in local dict — save on current_user directly
                self.current_user['notifications_enabled'] = notifications_enabled

        self.show_success_dialog("Settings saved!")
        dialog.dismiss()



    def show_legal(self):

           """Show legal information"""

           content = MDBoxLayout(

                 orientation='vertical',

                 spacing=dp(10),

                 padding=dp(15),

                 size_hint_y=None,

                 height=dp(300)

    )

    

           content.add_widget(MDLabel(

                 text="Terms of Service",

                 font_style="H6",

                 halign="center"

    ))

           content.add_widget(MDLabel(

                 text="By using this app, you agree to our terms of service and privacy policy.",

                 font_style="Body1",

                 halign="center"

    ))

           content.add_widget(MDRectangleFlatButton(

                 text="View Full Terms",

                 size_hint=(1, None),

                 height=dp(50),

                 on_release=lambda x: (dialog.dismiss(), setattr(self.root, 'current', 'terms'))

    ))

           content.add_widget(MDRectangleFlatButton(

                 text="View Privacy Policy",

                 size_hint=(1, None),

                 height=dp(50),

                 on_release=lambda x: (dialog.dismiss(), setattr(self.root, 'current', 'privacy'))

    ))

    

           dialog = MDDialog(

                title="Legal Information",

                type="custom",

                content_cls=content,

                buttons=[

                     MDFlatButton(

                             text="CLOSE",

                                theme_text_color="Custom",

                             text_color=self.theme_cls.primary_color,

                             on_release=lambda x: dialog.dismiss()

            )

        ],

                radius=[20, 7, 20, 7]

    )

           dialog.open()



    def show_account_deletion(self):

           """Show account deletion confirmation"""

           if not self.current_user:

                 return

    

           dialog = MDDialog(

                 title="Delete Account",

                 text="Are you sure you want to permanently delete your account? This action cannot be undone.",

                buttons=[

                      MDFlatButton(

                              text="CANCEL",

                                theme_text_color="Custom",

                              text_color=self.theme_cls.primary_color,

                              on_release=lambda x: dialog.dismiss()

            ),

                      MDRaisedButton(

                              text="DELETE",

                                 theme_text_color="Custom",

                              text_color=[1, 1, 1, 1],

                              md_bg_color=[0.9, 0.1, 0.1, 1],

                              on_release=lambda x: self.delete_account(dialog)

            )

        ],

               radius=[20, 7, 20, 7]

    )

           dialog.open()



    def delete_account(self, dialog):

           """Delete user account"""

           user_id = list(self.users.keys())[list(self.users.values()).index(self.current_user)]

           del self.users[user_id]

           self.save_users()

           self.current_user = None

           self.show_success_dialog("Account deleted successfully")

           dialog.dismiss()

           self.root.current = "login"



    def show_referrals(self):

           """Show referral information"""

           if not self.current_user:

                self.show_error_dialog("Please login to view referrals")

                self.root.current = "login"

                return

    

           content = MDBoxLayout(

                 orientation='vertical',

                 spacing=dp(10),

                 padding=dp(15),

                 size_hint_y=None,

                 height=dp(200)

    )

    

           referral_code = self.current_user.get('referral_code', 'ABC123')  # Example code

           content.add_widget(MDLabel(

                 text=f"Your Referral Code: {referral_code}",

                 font_style="H6",

                 halign="center"

    ))

           content.add_widget(MDRectangleFlatButton(

                 text="Copy Code",

                 size_hint=(1, None),

                 height=dp(50),

                 on_release=lambda x: self.copy_to_clipboard(referral_code)

    ))

           content.add_widget(MDLabel(

                  text=f"Referral Balance: {format_currency(self.current_user.get('referral_balance', 0))}",

                  font_style="Subtitle1",

                  halign="center"

    ))

    

           dialog = MDDialog(

                 title="My Referrals",

                 type="custom",

                 content_cls=content,

                 buttons=[

                       MDFlatButton(

                              text="CLOSE",

                                      theme_text_color="Custom",

                              text_color=self.theme_cls.primary_color,

                              on_release=lambda x: dialog.dismiss()

            )

        ],

                 radius=[20, 7, 20, 7]

    )

           dialog.open()



    def show_upgrade_options(self):

           """Show account upgrade options"""

           if not self.current_user:

                 self.show_error_dialog("Please login to upgrade account")

                 self.root.current = "login"

                 return

    

           content = MDBoxLayout(

                 orientation='vertical',

                 spacing=dp(10),

                 padding=dp(15),

                 size_hint_y=None,

                 height=dp(250)

    )

    

           content.add_widget(MDLabel(

                 text="Upgrade Your Account",

                 font_style="H6",

                 halign="center"

    ))

    

           plans = [

                 {"name": "Premium", "price": "₦5,000/month", "benefits": "Higher limits, priority support"},

                 {"name": "Business", "price": "₦10,000/month", "benefits": "API access, bulk transactions"}

    ]

    

           for plan in plans:

                 box = MDBoxLayout(

                       orientation='vertical',

                       size_hint_y=None,

                       height=dp(80),

                       padding=dp(10)

        )

                 box.add_widget(MDLabel(

                       text=f"{plan['name']} - {plan['price']}",

                       font_style="Subtitle1"

        ))

                 box.add_widget(MDLabel(

                       text=plan['benefits'],

                       font_style="Caption",

                           theme_text_color="Secondary"

        ))

                 content.add_widget(box)

    

           dialog = MDDialog(

                 title="Account Upgrade",

                 type="custom",

                 content_cls=content,

                 buttons=[

                      MDFlatButton(

                              text="CANCEL",

                                 theme_text_color="Custom",

                              text_color=self.theme_cls.primary_color,

                              on_release=lambda x: dialog.dismiss()

            ),

                     MDRaisedButton(

                           text="UPGRADE",

                              theme_text_color="Custom",

                           text_color=[1, 1, 1, 1],

                           md_bg_color=self.theme_cls.primary_color,

                           on_release=lambda x: self.process_upgrade(dialog)

            )

        ],

        

                 radius=[20, 7, 20, 7]

    )

           dialog.open()



    def process_upgrade(self, dialog):

           """Process account upgrade (placeholder)"""

           self.show_success_dialog("Upgrade request sent! We'll contact you soon.")

           dialog.dismiss()



    def switch_theme(self):

           """Toggle between light and dark theme"""

           self.theme_cls.theme_style = "Dark" if     self.theme_cls.theme_style == "Light"  else "Light"

           self.update_theme_colors()

           self.show_success_dialog(f"Switched to {self.theme_cls.theme_style} theme")



    # ═════════════════════════════════════════════════════════════════
    # SUPPORT CENTER
    # Replaces the old WhatsApp redirect. Tapping "Support" now opens
    # an in-app screen with three options: AI Assistant, Phone, Email —
    # instead of leaving the app for WhatsApp.
    # ═════════════════════════════════════════════════════════════════

    def open_support(self):
        """Open the in-app Support Center."""
        self.switch_screen('support')

    # Kept so any old call sites (or saved deep-links) still work -
    # now opens the in-app Support Center instead of WhatsApp.
    def open_whatsapp_support(self):
        self.open_support()

    def call_phone_support(self):
        """Open the native phone dialer pre-filled with the support number."""
        try:
            webbrowser.open(f"tel:{self.support_phone}")
        except Exception as e:
            print(f"call_phone_support error: {e}")
            self.show_error_dialog("Could not open the phone dialer.")

    def open_email_support(self):
        """Open the user's email app pre-filled with the support address."""
        try:
            subject = "Cheap4U%20Support%20Request"
            webbrowser.open(f"mailto:{self.support_email}?subject={subject}")
        except Exception as e:
            print(f"open_email_support error: {e}")
            self.show_error_dialog("Could not open your email app.")

    # ── AI Chat Assistant ────────────────────────────────────────────

    def _get_ai_chat_screen(self):
        try:
            return self.root.get_screen('ai_chat')
        except Exception:
            return None

    def open_ai_chat(self):
        """Open the AI Assistant chat screen, restore history, show suggestions."""
        self.switch_screen('ai_chat')
        Clock.schedule_once(lambda dt: self._safe_call(self._render_suggested_questions), 0.1)
        if not self.ai_chat_messages:
            Clock.schedule_once(lambda dt: self._safe_call(self.load_ai_chat_history), 0.15)
        else:
            Clock.schedule_once(lambda dt: self._safe_call(self._render_chat_messages), 0.1)

    @staticmethod
    def _safe_call(fn, *args, **kwargs):
        """
        Runs a UI-building callback and swallows any exception instead of
        letting it propagate into Kivy's Clock/event loop — an uncaught
        exception there crashes the whole app with no on-screen error.
        Used as a safety net around the chat screen's widget builders.
        """
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            print(f"[AI Chat] safe_call caught an error in {getattr(fn, '__name__', fn)}: {e}")
            return None

    def load_ai_chat_history(self):
        """Fetch saved chat history from the backend for this user/session."""
        def on_result(success, result):
            if success and result and result.get('data'):
                self.ai_chat_session_id = result.get('session_id') or self.ai_chat_session_id
                self.ai_chat_messages = result['data']
            self._safe_call(self._render_chat_messages)

        endpoint = "chat/history"
        if self.ai_chat_session_id:
            endpoint += f"?session_id={self.ai_chat_session_id}"
        self.backend_api_request(endpoint, method="GET", callback=on_result, on_failure=on_result)

    def _render_suggested_questions(self):
        screen = self._get_ai_chat_screen()
        if not screen or 'suggestions_box' not in screen.ids:
            return
        box = screen.ids.suggestions_box
        box.clear_widgets()
        for question in self.AI_SUGGESTED_QUESTIONS:
            # NOTE: MDRaisedButton (unlike MDLabel) has no .texture_size
            # attribute — don't read it. KivyMD auto-sizes button width
            # to fit the text on its own; we only need to fix the height.
            chip = MDRaisedButton(
                text=question,
                size_hint_y=None,
                height=dp(38),
                radius=[dp(19)],
                elevation=0,  # avoid shadow-shader crash on some Android GPUs
                md_bg_color=[0.898, 0.945, 1, 1],
                theme_text_color="Custom",
                text_color=[0.1294, 0.5882, 0.9529, 1],
                font_size="12sp",
                on_release=lambda x, q=question: self.send_ai_message(text=q),
            )
            box.add_widget(chip)

    def toggle_chat_search(self):
        """Show/hide the search bar above the chat list."""
        self.ai_search_active = not self.ai_search_active
        screen = self._get_ai_chat_screen()
        if not self.ai_search_active and screen and 'chat_search_field' in screen.ids:
            screen.ids.chat_search_field.text = ""
            self._render_chat_messages()

    def filter_chat_search(self, query):
        """Re-render the chat list showing only messages matching the query."""
        try:
            screen = self._get_ai_chat_screen()
            if not screen or 'chat_list' not in screen.ids:
                return
            query = (query or "").strip().lower()
            chat_list = screen.ids.chat_list
            chat_list.clear_widgets()

            messages = self.ai_chat_messages
            if query:
                messages = [m for m in messages if query in (m.get('content') or '').lower()]

            if not messages:
                chat_list.add_widget(MDLabel(
                    text="No matching messages" if query else "No messages yet",
                    halign="center", theme_text_color="Secondary",
                    size_hint_y=None, height=dp(60),
                ))
                return

            last_ai_index = None
            for i, m in enumerate(messages):
                if m.get('role') == 'assistant':
                    last_ai_index = i
            for i, m in enumerate(messages):
                chat_list.add_widget(self._safe_build(self._build_chat_bubble, m, is_last_ai=(i == last_ai_index)))
        except Exception as e:
            print(f"filter_chat_search error: {e}")

    def confirm_clear_ai_chat(self):
        dialog = MDDialog(
            title="Start a new chat?",
            text="This will clear your current conversation with the AI Assistant.",
            buttons=[
                MDFlatButton(
                    text="CANCEL", theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: dialog.dismiss(),
                ),
                MDFlatButton(
                    text="CLEAR", theme_text_color="Custom",
                    text_color=self.theme_cls.error_color,
                    on_release=lambda x: (dialog.dismiss(), self.clear_ai_chat()),
                ),
            ],
            radius=[20, 7, 20, 7],
        )
        dialog.open()

    def clear_ai_chat(self):
        """Clear chat history locally (instantly) and on the backend."""
        self.ai_chat_messages = []
        self.ai_last_user_message = ""
        self._render_chat_messages()
        Clock.schedule_once(lambda dt: self._render_suggested_questions(), 0.1)
        self.backend_api_request("chat/history", method="DELETE", callback=lambda *a: None)

    def send_ai_message(self, text=None):
        """Send a message (typed or tapped from suggestions) to the AI assistant."""
        screen = self._get_ai_chat_screen()
        if not screen:
            return
        if text is None:
            text = screen.ids.ai_chat_input.text.strip() if 'ai_chat_input' in screen.ids else ""
        text = (text or "").strip()
        if not text:
            return
        if 'ai_chat_input' in screen.ids:
            screen.ids.ai_chat_input.text = ""

        self.ai_last_user_message = text
        self.ai_chat_messages = self.ai_chat_messages + [{'role': 'user', 'content': text}]
        self._render_chat_messages()
        self.ai_chat_typing = True

        payload = {'message': text}
        if self.ai_chat_session_id:
            payload['session_id'] = self.ai_chat_session_id

        self._send_chat_streaming(payload)

    def _send_chat_json(self, payload):
        """Non-streaming fallback: one request, one full reply."""
        def on_result(success, result):
            self.ai_chat_typing = False
            result = result or {}
            action = None
            message_id = None
            if success and result.get('reply'):
                self.ai_chat_session_id = result.get('session_id') or self.ai_chat_session_id
                reply = result['reply']
                action = result.get('action')
                message_id = result.get('message_id')
            else:
                reply = result.get('message') or (
                    f"Sorry, I couldn't process that right now. Please contact support "
                    f"at {self.support_phone} or {self.support_email}."
                )
            self.ai_chat_messages = self.ai_chat_messages + [
                {'role': 'assistant', 'content': reply, 'action': action, 'id': message_id}
            ]
            self._render_chat_messages()
            if action:
                self._offer_smart_action(action)

        self.backend_api_request("chat", method="POST", data=payload,
                                  callback=on_result, on_failure=on_result)

    def _send_chat_streaming(self, payload):
        """
        Streams the AI reply token-by-token (Server-Sent Events from
        POST /api/chat with stream=true) so replies appear progressively
        instead of all at once, like ChatGPT. Falls back to a single
        JSON request if the backend URL isn't set or streaming fails
        before any text arrives.
        """
        if not self.backend_url:
            self._send_chat_json(payload)
            return

        payload = dict(payload)
        payload['stream'] = True
        url = f"{self.backend_url}/api/chat"
        headers = {'Content-Type': 'application/json'}
        if getattr(self, 'session_token', None):
            headers['Authorization'] = f'Bearer {self.session_token}'

        # Placeholder bubble that gets filled in as chunks arrive
        self.ai_chat_messages = self.ai_chat_messages + [
            {'role': 'assistant', 'content': '', 'action': None, 'id': None}
        ]

        def worker():
            accumulated = ''
            got_any_chunk = False
            fallback = (
                f"Sorry, I couldn't process that right now. Please contact support "
                f"at {self.support_phone} or {self.support_email}."
            )
            try:
                resp = requests.post(url, json=payload, headers=headers, timeout=60, stream=True)
                content_type = resp.headers.get('Content-Type', '')

                if 'text/event-stream' not in content_type:
                    # Backend didn't stream (e.g. an error before the
                    # stream started, or a proxy that buffers/rewrites
                    # the response) - it's likely one JSON body instead.
                    # Parse it so the bubble still shows a real message
                    # instead of staying blank.
                    try:
                        body = resp.json()
                    except Exception:
                        body = {}
                    text = body.get('reply') or body.get('message') or fallback
                    Clock.schedule_once(lambda dt, t=text: self._update_streaming_bubble(t), 0)
                    Clock.schedule_once(
                        lambda dt, a=body.get('action'), mid=body.get('message_id'):
                            self._finish_streaming_bubble(a, mid), 0
                    )
                    return

                for raw_line in resp.iter_lines(decode_unicode=True):
                    if not raw_line or not raw_line.startswith('data:'):
                        continue
                    try:
                        chunk = json.loads(raw_line[len('data:'):].strip())
                    except Exception:
                        continue
                    if chunk.get('delta'):
                        got_any_chunk = True
                        accumulated += chunk['delta']
                        Clock.schedule_once(lambda dt, t=accumulated: self._update_streaming_bubble(t), 0)
                    if chunk.get('done'):
                        if not got_any_chunk:
                            # done=true arrived but no delta was ever sent
                            Clock.schedule_once(lambda dt: self._update_streaming_bubble(fallback), 0)
                        Clock.schedule_once(
                            lambda dt, a=chunk.get('action'), mid=chunk.get('message_id'):
                                self._finish_streaming_bubble(a, mid), 0
                        )
                        return
                # Stream ended with no explicit "done" (dropped connection etc.)
                if not got_any_chunk:
                    Clock.schedule_once(lambda dt: self._update_streaming_bubble(fallback), 0)
                Clock.schedule_once(lambda dt: self._finish_streaming_bubble(None, None), 0)
            except Exception as e:
                print(f"stream chat error: {e}")
                if not got_any_chunk:
                    Clock.schedule_once(lambda dt: self._update_streaming_bubble(fallback), 0)
                Clock.schedule_once(lambda dt: self._finish_streaming_bubble(None, None), 0)

        threading.Thread(target=worker, daemon=True).start()

    def _update_streaming_bubble(self, accumulated_text):
        """Update the last (still-streaming) assistant bubble's text as chunks arrive."""
        if not self.ai_chat_messages or self.ai_chat_messages[-1].get('role') != 'assistant':
            return
        updated = dict(self.ai_chat_messages[-1])
        updated['content'] = accumulated_text
        self.ai_chat_messages = self.ai_chat_messages[:-1] + [updated]
        self.ai_chat_typing = False  # first chunk arrived - hide the typing dots
        self._render_chat_messages()

    def _finish_streaming_bubble(self, action, message_id):
        """Called when the stream reports done=true (or the connection ends)."""
        self.ai_chat_typing = False
        if self.ai_chat_messages and self.ai_chat_messages[-1].get('role') == 'assistant':
            updated = dict(self.ai_chat_messages[-1])
            updated['action'] = action
            updated['id'] = message_id
            self.ai_chat_messages = self.ai_chat_messages[:-1] + [updated]
        self._render_chat_messages()
        if action:
            self._offer_smart_action(action)

    # ── Smart Actions ────────────────────────────────────────────────
    # Maps an action code returned by the backend to something the app
    # actually does. e.g. user says "I want MTN data" -> backend detects
    # 'data_purchase' -> we take them straight to the Data screen.
    SMART_ACTION_MAP = {
        'data_purchase': lambda app: app.switch_screen('data_purchase'),
        'airtime_topup': lambda app: app.switch_screen('airtime_topup'),
        'wallet_funding': lambda app: app.switch_screen('funding'),
        'transaction_history': lambda app: app.switch_screen('history'),
        'password_reset': lambda app: app.show_forgot_password(),
    }

    SMART_ACTION_LABELS = {
        'data_purchase': 'Buy Data',
        'airtime_topup': 'Buy Airtime',
        'wallet_funding': 'Fund Wallet',
        'transaction_history': 'View Transactions',
        'password_reset': 'Reset Password',
    }

    def _offer_smart_action(self, action):
        """Show a quick-action snackbar/toast-style prompt after a matching reply."""
        try:
            label = self.SMART_ACTION_LABELS.get(action)
            if not label:
                return
            toast(f"Tip: tap the '{label}' button below to go there directly")
            screen = self._get_ai_chat_screen()
            if screen and 'chat_list' in screen.ids:
                # NOTE: MDRaisedButton has no .texture_size attribute (that's
                # a Label/MDLabel-only property) — don't read it here.
                btn = MDRaisedButton(
                    text=label, size_hint_y=None, height=dp(40),
                    radius=[dp(20)], elevation=0,  # avoid shadow-shader crash on some Android GPUs
                    md_bg_color=[0.1294, 0.5882, 0.9529, 1],
                    theme_text_color="Custom", text_color=[1, 1, 1, 1],
                    on_release=lambda x, a=action: self.run_smart_action(a),
                )
                row = MDBoxLayout(orientation='vertical', size_hint_y=None,
                                   padding=[dp(58), dp(2), dp(12), dp(4)])
                row.bind(minimum_height=row.setter('height'))
                row.add_widget(btn)
                screen.ids.chat_list.add_widget(row)
                Clock.schedule_once(self._scroll_chat_to_bottom, 0.05)
        except Exception as e:
            print(f"_offer_smart_action error: {e}")

    def run_smart_action(self, action):
        handler = self.SMART_ACTION_MAP.get(action)
        if handler:
            handler(self)

    def regenerate_last_ai_response(self):
        """Re-ask the assistant using the last user message and replace the last reply."""
        if not self.ai_last_user_message:
            return
        if self.ai_chat_messages and self.ai_chat_messages[-1].get('role') == 'assistant':
            self.ai_chat_messages = self.ai_chat_messages[:-1]
        self._render_chat_messages()
        self.ai_chat_typing = True

        payload = {'message': self.ai_last_user_message}
        if self.ai_chat_session_id:
            payload['session_id'] = self.ai_chat_session_id

        self._send_chat_streaming(payload)

    def send_chat_feedback(self, message_id, rating):
        """Thumbs up/down on a specific AI reply."""
        if not message_id:
            toast("Thanks for the feedback!")
            return
        self.backend_api_request(
            "chat/feedback", method="POST",
            data={'message_id': message_id, 'rating': rating},
            callback=lambda success, result: toast("Thanks for the feedback!" if success else "Could not send feedback"),
        )

    def copy_chat_message(self, text):
        try:
            Clipboard.copy(text)
            toast("Copied to clipboard")
        except Exception as e:
            print(f"copy_chat_message error: {e}")

    def start_voice_input(self):
        """
        Voice-to-text for the chat input box. Uses Android's native
        speech recognizer via pyjnius when running on Android; shows a
        friendly message anywhere else (desktop testing, iOS) instead
        of crashing, since that API isn't available there.
        """
        try:
            from kivy.utils import platform
            if platform != "android":
                toast("Voice input is available on Android devices")
                return
            self._start_android_voice_input()
        except Exception as e:
            print(f"start_voice_input error: {e}")
            toast("Voice input isn't available right now")

    def _start_android_voice_input(self):
        try:
            from jnius import autoclass
            from android import activity

            RecognizerIntent = autoclass('android.speech.RecognizerIntent')
            Intent = autoclass('android.content.Intent')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')

            intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
            intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Ask the AI Assistant...")

            def on_activity_result(request_code, result_code, intent_data):
                try:
                    if request_code == 1001 and intent_data:
                        results = intent_data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)
                        if results and results.size() > 0:
                            spoken_text = results.get(0)
                            Clock.schedule_once(lambda dt: self._on_voice_result(spoken_text), 0)
                except Exception as e:
                    print(f"voice result error: {e}")
                finally:
                    activity.unbind(on_activity_result=on_activity_result)

            activity.bind(on_activity_result=on_activity_result)
            PythonActivity.mActivity.startActivityForResult(intent, 1001)
        except Exception as e:
            print(f"_start_android_voice_input error: {e}")
            toast("Couldn't start voice input")

    def _on_voice_result(self, spoken_text):
        screen = self._get_ai_chat_screen()
        if screen and 'ai_chat_input' in screen.ids:
            screen.ids.ai_chat_input.text = spoken_text

    def _render_chat_messages(self):
        """Redraw every chat bubble from self.ai_chat_messages, then auto-scroll down."""
        try:
            screen = self._get_ai_chat_screen()
            if not screen or 'chat_list' not in screen.ids:
                return
            chat_list = screen.ids.chat_list
            chat_list.clear_widgets()

            newest_widget = None
            if not self.ai_chat_messages:
                chat_list.add_widget(self._safe_build(self._build_chat_welcome_widget))
            else:
                last_ai_index = None
                for i, m in enumerate(self.ai_chat_messages):
                    if m.get('role') == 'assistant':
                        last_ai_index = i
                for i, m in enumerate(self.ai_chat_messages):
                    widget = self._safe_build(self._build_chat_bubble, m, is_last_ai=(i == last_ai_index))
                    chat_list.add_widget(widget)
                    newest_widget = widget

            if self.ai_chat_typing:
                newest_widget = self._safe_build(self._build_typing_bubble)
                chat_list.add_widget(newest_widget)

            # Subtle fade-in for whichever bubble just appeared (the newest
            # message, or the typing indicator). We only animate the newest
            # widget — animating every bubble on every re-render would
            # replay the fade for old messages too, which looks jarring.
            if newest_widget is not None:
                self._animate_bubble_in(newest_widget)

            Clock.schedule_once(self._scroll_chat_to_bottom, 0.05)
        except Exception as e:
            print(f"_render_chat_messages error: {e}")

    def _safe_build(self, builder_fn, *args, **kwargs):
        """
        Builds a chat widget (bubble/typing indicator/welcome card) and
        falls back to a plain MDLabel if the fancy version raises for
        any reason — keeps one bad widget from taking down the whole
        chat screen (or the app, since an uncaught exception inside a
        widget-building call can crash Kivy's event loop entirely).
        """
        try:
            return builder_fn(*args, **kwargs)
        except Exception as e:
            print(f"[AI Chat] widget build failed in {getattr(builder_fn, '__name__', builder_fn)}: {e}")
            text = ''
            if args and isinstance(args[0], dict):
                text = args[0].get('content', '')
            fallback = MDBoxLayout(orientation='vertical', size_hint_y=None, padding=[dp(12), dp(6)])
            fallback.bind(minimum_height=fallback.setter('height'))
            fallback.add_widget(Factory.ChatBubbleLabel(
                text=text or " ", theme_text_color="Custom",
                text_color=[0.1216, 0.1608, 0.2157, 1],
            ))
            return fallback

    @staticmethod
    def _animate_bubble_in(widget):
        try:
            widget.opacity = 0
            Animation(opacity=1, duration=0.22, t='out_quad').start(widget)
        except Exception as e:
            print(f"_animate_bubble_in error: {e}")

    @staticmethod
    def _markdown_lite_to_markup(text):
        """
        Converts the small subset of Markdown the AI is allowed to use
        (see SYSTEM_PROMPT on the backend: **bold** and "- " bullets
        only) into KivyMD's BBCode-style markup, since MDLabel doesn't
        render raw Markdown. Kept deliberately simple/safe — no
        headings, tables, links, or code blocks are expected or handled.
        """
        if not text:
            return text
        # **bold** -> [b]bold[/b]
        text = re.sub(r'\*\*(.+?)\*\*', r'[b]\1[/b]', text)
        # Turn "- item" bullet lines into "  •  item"
        lines = text.split('\n')
        lines = [re.sub(r'^\s*[-*]\s+', '  \u2022  ', ln) for ln in lines]
        return '\n'.join(lines)

    def _scroll_chat_to_bottom(self, *_):
        screen = self._get_ai_chat_screen()
        if screen and 'chat_scroll' in screen.ids:
            screen.ids.chat_scroll.scroll_y = 0

    def _build_chat_welcome_widget(self):
        box = MDBoxLayout(
            orientation='vertical', spacing=dp(8), size_hint_y=None,
            padding=[dp(20), dp(30), dp(20), dp(10)],
        )
        box.bind(minimum_height=box.setter('height'))
        icon = MDIcon(
            icon="robot-happy-outline", halign="center", font_size="48sp",
            theme_text_color="Custom", text_color=[0.1294, 0.5882, 0.9529, 1],
            size_hint_y=None, height=dp(60),
        )
        title = MDLabel(
            text="Hi! I'm your Cheap4U AI Assistant", halign="center",
            font_style="Subtitle1", bold=True,
            theme_text_color="Custom", text_color=[0.1216, 0.1608, 0.2157, 1],
            size_hint_y=None, height=dp(30),
        )
        subtitle = MDLabel(
            text="Ask me about data, airtime, bills, wallet, referrals, or your account.",
            halign="center", font_style="Caption",
            theme_text_color="Custom", text_color=[0.4196, 0.4471, 0.5020, 1],
            size_hint_y=None, height=dp(40),
        )
        box.add_widget(icon)
        box.add_widget(title)
        box.add_widget(subtitle)
        return box

    def _build_typing_bubble(self):
        """Classic three-dot typing indicator, each dot pulsing in sequence."""
        row = MDBoxLayout(orientation='vertical', size_hint_y=None, height=dp(52),
                           padding=[dp(4), 0, dp(40), 0])
        bubble = GradientCard(
            size_hint=(None, None), size=(dp(72), dp(42)),
            radius=[18, 18, 18, 4], elevation=0, padding=[dp(16), dp(12)],  # elevation=0 avoids a known shadow-shader crash on some Android GPUs
        )
        dots_row = MDBoxLayout(spacing=dp(6))
        dots = []
        for _ in range(3):
            dot = MDIcon(
                icon="circle", font_size="10sp",
                theme_text_color="Custom", text_color=[1, 1, 1, 1],
                size_hint=(None, None), size=(dp(10), dp(10)),
            )
            dots.append(dot)
            dots_row.add_widget(dot)
        bubble.add_widget(dots_row)
        row.add_widget(bubble)

        # Stagger each dot's pulse start by 0.15s so they animate one
        # after another, like ChatGPT/Claude's typing indicator.
        for i, dot in enumerate(dots):
            def start_pulse(dt, d=dot):
                anim = Animation(opacity=0.3, duration=0.35) + Animation(opacity=1, duration=0.35)
                anim.repeat = True
                anim.start(d)
            Clock.schedule_once(start_pulse, i * 0.15)
        return row

    def _build_chat_bubble(self, message, is_last_ai=False):
        role = message.get('role')
        text = message.get('content', '')
        message_id = message.get('id')
        is_user = (role == 'user')

        outer = MDBoxLayout(
            orientation='horizontal', size_hint_y=None, spacing=dp(8),
            padding=[dp(40), 0, dp(4), 0] if is_user else [dp(4), 0, dp(40), 0],
        )
        outer.bind(minimum_height=outer.setter('height'))

        # Avatar — wrapped in a FloatLayout so the icon glyph is always
        # perfectly centered in its circular badge (MDCard alone does
        # not reliably honor pos_hint for a single child, which is why
        # the robot icon looked off-center before).
        avatar_bg = MDCard(
            size_hint=(None, None), size=(dp(32), dp(32)), radius=[dp(16)],
            md_bg_color=[0.898, 0.945, 1, 1] if is_user else [0.1294, 0.5882, 0.9529, 1],
            pos_hint={"top": 1},
        )
        avatar_float = FloatLayout()
        avatar_float.add_widget(MDIcon(
            icon="account-circle" if is_user else "robot-happy-outline",
            font_size="20sp",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            theme_text_color="Custom",
            text_color=[0.1294, 0.5882, 0.9529, 1] if is_user else [1, 1, 1, 1],
        ))
        avatar_bg.add_widget(avatar_float)

        # Bot bubble = blue gradient, user bubble = light blue flat,
        # per the Cheap4U Support Center design spec.
        if is_user:
            bubble = MDCard(
                orientation='vertical', size_hint_x=1, size_hint_y=None,
                radius=[18, 18, 4, 18], elevation=0, padding=dp(14), spacing=dp(6),  # elevation=0 avoids a known shadow-shader crash on some Android GPUs
                md_bg_color=[0.898, 0.945, 1, 1],
            )
        else:
            bubble = GradientCard(
                orientation='vertical', size_hint_x=1, size_hint_y=None,
                radius=[18, 18, 18, 4], elevation=0, padding=dp(14), spacing=dp(6),  # elevation=0 avoids a known shadow-shader crash on some Android GPUs
            )
        bubble.bind(minimum_height=bubble.setter('height'))

        label = Factory.ChatBubbleLabel(
            text=self._markdown_lite_to_markup(text) if not is_user else text,
            markup=(not is_user),
            theme_text_color="Custom",
            text_color=[0.1216, 0.1608, 0.2157, 1] if is_user else [1, 1, 1, 1],
        )
        bubble.add_widget(label)

        if not is_user:
            # Evenly spaced action row: copy / like / dislike / regenerate.
            # Icons are light (not grey) since they sit on the blue
            # gradient bubble, where grey would be nearly invisible.
            actions = MDBoxLayout(size_hint_y=None, height=dp(30), spacing=dp(14))
            actions.add_widget(MDIconButton(
                icon="content-copy", user_font_size="18sp",
                theme_icon_color="Custom", icon_color=[1, 1, 1, 0.85],
                on_release=lambda x, t=text: self.copy_chat_message(t),
            ))
            actions.add_widget(MDIconButton(
                icon="thumb-up-outline", user_font_size="18sp",
                theme_icon_color="Custom", icon_color=[1, 1, 1, 0.85],
                on_release=lambda x, mid=message_id: self.send_chat_feedback(mid, 'up'),
            ))
            actions.add_widget(MDIconButton(
                icon="thumb-down-outline", user_font_size="18sp",
                theme_icon_color="Custom", icon_color=[1, 1, 1, 0.85],
                on_release=lambda x, mid=message_id: self.send_chat_feedback(mid, 'down'),
            ))
            if is_last_ai:
                actions.add_widget(MDIconButton(
                    icon="refresh", user_font_size="18sp",
                    theme_icon_color="Custom", icon_color=[1, 1, 1, 0.85],
                    on_release=lambda x: self.regenerate_last_ai_response(),
                ))
            actions.add_widget(Widget())
            bubble.add_widget(actions)

        if is_user:
            outer.add_widget(bubble)
            outer.add_widget(avatar_bg)
        else:
            outer.add_widget(avatar_bg)
            outer.add_widget(bubble)

        return outer



    def show_beneficiaries(self):

           """Show saved beneficiaries"""

           if not self.current_user:

                 self.show_error_dialog("Please login to view beneficiaries")

                 self.root.current = "login"

                 return

    

           content = MDBoxLayout(

                 orientation='vertical',

                 spacing=dp(10),

                 padding=dp(15),

                 size_hint_y=None,

                 height=dp(300)

    )

    

           scroll = ScrollView()

           beneficiary_list =   MDList(spacing=dp(10))

    

           beneficiaries = self.current_user. get('beneficiaries', [])

           if not beneficiaries:

                 beneficiary_list.add_widget(MDLabel(

                 text="No beneficiaries added yet",

                 halign="center",

                 font_style="Subtitle1"

        ))

           else:

                 for beneficiary in beneficiaries:

                       item = TwoLineListItem(

                       text=beneficiary['name'],

                       secondary_text=f"Phone: {beneficiary['phone']}",

                       on_release=lambda x, b=beneficiary: self.use_beneficiary(b)

            )

                 beneficiary_list.add_widget(item)

    

           scroll.add_widget(beneficiary_list)

           content.add_widget(scroll)

    

           content.add_widget(MDRectangleFlatButton(

                 text="Add New Beneficiary",

                 size_hint=(1, None),

                 height=dp(50),

                 on_release=lambda x: self. show_add_beneficiary()

    ))

    

           dialog = MDDialog(

                 title="My Beneficiaries",

                 type="custom",

                 content_cls=content,

                 buttons=[

                      MDFlatButton(

                              text="CLOSE",

                               theme_text_color="Custom",

                              text_color=self.theme_cls.primary_color,

                              on_release=lambda x: dialog.dismiss()

            )

        ],

                 radius=[20, 7, 20, 7]

    )

           dialog.open()



    def show_add_beneficiary(self):

           """Show dialog to add new beneficiary"""

           content = MDBoxLayout(

                 orientation='vertical',

                 spacing=dp(10),

                 padding=dp(15),

                 size_hint_y=None,

                 height=dp(200)

    )

    

           name_input = MDTextField(

                 hint_text="Beneficiary Name",

                 icon_left="account-outline",

                 required=True

    )

           phone_input = MDTextField(

                 hint_text="Phone Number",

                 icon_left="phone-outline",

                 input_type='number',

                 max_text_length=11,

                 required=True

    )

    

           content.add_widget(name_input)

           content.add_widget(phone_input)

    

           dialog = MDDialog(

                title="Add Beneficiary",

                type="custom",

                content_cls=content,

                buttons=[

                     MDFlatButton(

                             text="CANCEL",

                              theme_text_color="Custom",

                             text_color=self.theme_cls.primary_color,

                             on_release=lambda x: dialog.dismiss()

            ),

                     MDRaisedButton(

                           text="SAVE",

                              theme_text_color="Custom",

                           text_color=[1, 1, 1, 1],

                           md_bg_color=self.theme_cls.primary_color,

                           on_release=lambda x: self.save_beneficiary(dialog, name_input.text, phone_input.text)

            )

        ],

                     radius=[20, 7, 20, 7]

    )

           dialog.open()



    def save_beneficiary(self, dialog, name, phone):
        """Save new beneficiary"""
        dialog.dismiss()

        if not all([name, phone]):
            self.show_error_dialog("All fields are required")
            return

        if not is_valid_phone(phone):
            self.show_error_dialog("Invalid phone number. Must be 11 digits")
            return

        if not self.current_user:
            self.show_error_dialog("Please login first")
            return

        # FIX: use email to find user, not list.index()
        user_id = None
        for uid, user in self.users.items():
            if user.get('email') == self.current_user.get('email'):
                user_id = uid
                break

        if not user_id:
            # User logged in via backend but not in local users dict
            # Save beneficiary directly on current_user dict
            if 'beneficiaries' not in self.current_user:
                self.current_user['beneficiaries'] = []

            for b in self.current_user['beneficiaries']:
                if b['phone'] == phone:
                    self.show_error_dialog("Phone number already added as beneficiary")
                    return

            self.current_user['beneficiaries'].append({'name': name, 'phone': phone})
            self.show_success_dialog("Beneficiary added successfully!")
            return

        if 'beneficiaries' not in self.users[user_id]:
            self.users[user_id]['beneficiaries'] = []

        for b in self.users[user_id]['beneficiaries']:
            if b['phone'] == phone:
                self.show_error_dialog("Phone number already added as beneficiary")
                return

        self.users[user_id]['beneficiaries'].append({'name': name, 'phone': phone})
        self.current_user = self.users[user_id]
        self.save_users()
        self.show_success_dialog("Beneficiary added successfully!")                


    def use_beneficiary(self, beneficiary):

           """Use beneficiary for transaction"""

           screen_names = {

                 "airtime_topup": "phone_input",

                 "data_purchase": "data_phone_input",

                 "cable_tv": "smartcard_input"

    }

    

           current_screen = self.root.current

           if current_screen in screen_names:

                 screen = self.root.  get_screen(current_screen)

                 screen.ids[screen_names[current_screen]].text = beneficiary['phone']    

                 self.show_success_dialog(f"Selected {beneficiary['name']}'s number")



    def buy_beneficiary(self):

           """Initiate transaction using beneficiary"""

           if not self.current_user:

                 self.show_error_dialog("Please login to continue")

                 self.root.current = "login"

                 return

    

           self.show_beneficiaries() 
    def _award_referral_commission(user, selling_price):
        """Award 2% commission to referrer on every VTU purchase."""
        if not user or not user.referred_by_user_id:
            return

        commission = round(selling_price * 0.02, 2)
        if commission <= 0:
            return

        referrer = User.query.get(user.referred_by_user_id)
        if referrer:
            # FIX: add to both balance (spendable) AND earnings (total shown)
            referrer.referral_balance = round(referrer.referral_balance + commission, 2)
            referrer.referral_earnings = round(referrer.referral_earnings + commission, 2)
            db.session.add(ReferralTransaction(
                referrer_id=referrer.id,
                referred_user_id=user.id,
                amount=commission,
                type='commission',
            ))   
            
                              

 
if __name__ == '__main__':

    DashboardApp().run()
