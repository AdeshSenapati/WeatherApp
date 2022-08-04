import bs4
from requests_html import HTMLSession
import databaseMongo as dm
from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatIconButton,MDFillRoundFlatButton
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel, MDIcon
from kivy.clock import Clock
from plyer import notification
from kivy.lang import Builder

requests = HTMLSession()
mongoemail = dm.Mongo()

KV = f'''
MDScreen:

    MDBoxLayout:
        orientation: "vertical"

        MDToolbar:
            title: "Weather App"
            md_bg_color: 0,1,.5,.5
            id: btn
        ScrollView:
            MDScreen:
                adaptive_height: True
                id: box
'''
gugu = []
dd = {}


class Weather(MDApp):
    def get_weather(self, args):
        city = self.input.text
        url = f'https://www.google.com/search?q=weather in {city}'
        res = requests.get(url)
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        temp = res.html.xpath('//*[@id="wob_tm"]')[0].text
        precip = res.html.xpath('//*[@id="wob_pp"]')[0].text
        humidity = res.html.xpath('//*[@id="wob_hm"]')[0].text
        wind = res.html.xpath('//*[@id="wob_ws"]')[0].text
        loc = res.html.find('#wob_loc')[0].text
        time = res.html.find('#wob_dts')[0].text
        sky = res.html.find('#wob_dcp')[0].text
        self.tloclabel.text = f'Location: {loc} \nAt Time: {time}'
        self.templabel.text = f'Temperature: {temp}°C'
        self.skylabel.text = f'Sky condition: {sky}'
        self.phwlabel.text = f'Precipitation: {precip} \nHumidity: {humidity} \nWind Speed: {wind}'
        self.for7dayslabel.text = ''
        self.confirmation.text = ''
        self.email_notif.disabled = True
        self.email_notif.opacity = 0
        self.send_email.disabled = True
        self.send_email.opacity = 0
        for i in range(1, 8):
            dd[f'self.forecastlabel' + str(i)].text = ''

    def get_forecast(self, args):
        city = self.input.text
        url = f'https://www.google.com/search?q=weather in {city}'
        res = requests.get(url)
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        forcasts = res.html.find('.wob_df')
        cond = soup.find_all('img', attrs={'class': 'uW5pk'})
        self.tloclabel.text = ''
        self.templabel.text = ''
        self.skylabel.text = ''
        self.phwlabel.text = ''
        self.confirmation.text = ''
        self.email_notif.disabled = True
        self.email_notif.opacity = 0
        self.send_email.disabled = True
        self.send_email.opacity = 0
        self.for7dayslabel.text = 'Upcoming 7 days Forecasts:'
        for i in range(1, len(forcasts)):
            ss = forcasts[i].text
            tt = list(ss.split('\n'))
            dd[f'self.forecastlabel'+str(i)].text = f'{tt[0]}\nmax: {tt[1][:2]}\nmin:{tt[2][:2]}\n{cond[i]["alt"]}'

    def get_notification(self, args):
        city = self.input.text
        url = f'https://www.google.com/search?q=weather in {city}'
        res = requests.get(url)
        temp = res.html.xpath('//*[@id="wob_tm"]')[0].text
        sky = res.html.find('#wob_dcp')[0].text
        message = f'Temperature now is {temp}°C\nSky condition is {sky}'
        if self.notif_btn.active:
            notification.notify(title='Weather Notification', message=message, app_icon=None, timeout=10, toast=False)

    def get_email_notification(self, args):
        self.email_notif.disabled = False
        self.email_notif.opacity = 1
        self.send_email.disabled = False
        self.send_email.opacity = 1
        self.send_email.md_bg_color = '#B2DFDB'
        self.tloclabel.text = ''
        self.templabel.text = ''
        self.skylabel.text = ''
        self.phwlabel.text = ''
        self.for7dayslabel.text = ''
        for i in range(1, 8):
            dd[f'self.forecastlabel' + str(i)].text = ''

    def send_email_notif(self, args):
        email = self.email_notif.text
        location = self.input.text
        validate = mongoemail.check_email(email)
        if validate == 'Valid Email':
            results = mongoemail.find_email(email)
            if results == email:
                self.confirmation.text = 'Email provided is already present with us...'
            elif results != email:
                add_email = mongoemail.post_email(email, location)
                self.confirmation.text = f'Your email has been {add_email}'
        else:
            self.confirmation.text = f'{validate} provided!!!'


    def build(self):
        # screen = MDScreen(adaptive_height=True)
        screen = Builder.load_string(KV)
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Lime"
        self.theme_cls.primary_hue = "100"
        # screen.cols = 1
        self.input = MDTextField(
            hint_text='Enter your location',
            halign='left',
            size_hint=(0.8, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            font_size=22,
            required=True,
            text_color=(0, 0, 0, 1),
            input_type='text'
        )
        screen.ids.box.add_widget(self.input)
        self.weather_btn = MDFillRoundFlatIconButton(
            text='GET WEATHER',
            icon='weather-cloudy',
            font_size=17,
            pos_hint={"center_x": 0.25, "center_y": -0.2},
            on_press=self.get_weather
        )
        screen.ids.box.add_widget(self.weather_btn)
        self.forecast_btn = MDFillRoundFlatIconButton(
            text='GET FORECAST',
            font_size=17,
            icon='chart-areaspline',
            pos_hint={"center_x": 0.5, "center_y": -0.2},
            on_press=self.get_forecast
        )
        screen.ids.box.add_widget(self.forecast_btn)
        self.email_notif_btn = MDFillRoundFlatIconButton(
            text='GET EMAIL NOTIFICATIONS',
            font_size=17,
            icon='email-send-outline',
            pos_hint={"center_x": 0.8, "center_y": -0.2},
            on_press=self.get_email_notification
        )
        screen.ids.box.add_widget(self.email_notif_btn)
        self.notif_btn = MDSwitch(
            pos_hint={"center_x": 0.9, "center_y": 0.5},
            #width=dp(64),
            # on_press=self.get_notification
        )
        self.notif_text = MDLabel(
            text='Get Notifications:',
            halign="right",
            pos_hint={"center_x": 0.8, "center_y": 0.51},
            theme_text_color="Primary",
            font_style="H6"
        )
        Clock.schedule_interval(self.get_notification, 3600)
        screen.ids.btn.add_widget(self.notif_text)
        screen.ids.btn.add_widget(self.notif_btn)

        self.tloclabel = MDLabel(
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": -0.8},
            theme_text_color="Primary",
            font_style="H5"
        )
        self.templabel = MDLabel(
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": -1.5},
            theme_text_color="Primary",
            font_style="H5"
        )
        self.skylabel = MDLabel(
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": -2},
            theme_text_color="Primary",
            font_style="H5"
        )
        self.phwlabel = MDLabel(
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": -2.9},
            theme_text_color="Primary",
            font_style="H5"
        )
        self.for7dayslabel = MDLabel(
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": -0.8},
            theme_text_color="Primary",
            font_style="H5"
        )
        self.email_notif = MDTextField(
            hint_text='Enter your email',
            halign='left',
            size_hint=(0.5, 1),
            helper_text_mode="on_error",
            pos_hint={'center_x': 0.4, 'center_y': -1},
            disabled=True,
            opacity=0,
            font_size=17,
            required=True,
            text_color=(0, 0, 0, 1),
            input_type='text'
        )
        self.send_email = MDFillRoundFlatIconButton(
            text='SEND',
            font_size=17,
            pos_hint={"center_x": 0.75, "center_y": -0.9},
            icon='cube-send',
            disabled=True,
            opacity=0,
            on_press=self.send_email_notif
        )
        screen.ids.box.add_widget(self.send_email)
        self.confirmation = MDLabel(
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": -2},
            theme_text_color="Primary",
            font_style="H5"
        )
        screen.ids.box.add_widget(self.confirmation)
        w4 = 0
        h4 = 0
        w2 = 0
        h2 = 0
        count = 0
        for i in range(1, 8):
           if count <= 4:
               dd['self.forecastlabel'+str(i)] = MDLabel(
                    halign="center",
                    pos_hint={"center_x": 0.1+w4, "center_y": -2-h4},
                    theme_text_color="Primary",
                    font_style="H6"
                )
               w4 += 0.2
               h4 += 0
           elif count > 4:
               dd['self.forecastlabel' + str(i)] = MDLabel(
                   halign="center",
                   pos_hint={"center_x": 0.4 + w2, "center_y": -3.5 - h2},
                   theme_text_color="Primary",
                   font_style="H6"
               )
               w2 += 0.2
               h2 += 0
           count += 1

        screen.ids.box.add_widget(self.tloclabel)
        screen.ids.box.add_widget(self.templabel)
        screen.ids.box.add_widget(self.skylabel)
        screen.ids.box.add_widget(self.phwlabel)
        screen.ids.box.add_widget(self.for7dayslabel)
        screen.ids.box.add_widget(self.email_notif)
        for i in range(1, 8):
            screen.ids.box.add_widget(dd[f'self.forecastlabel'+str(i)])
        return screen


if __name__ == '__main__':
    Weather().run()