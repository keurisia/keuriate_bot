import os
import schedule
import time
import datetime
import pickle
import tkinter
import json
import wmi
import requests
import threading #MK: threading을 사용하기 위해 추가
from tkinter.messagebox import *
import customtkinter
import pyperclip
import slack_sdk
import random
import webbrowser
import linecache
import keyboard
from slack_sdk import WebClient
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
    
SLACK_TOKEN = 'xoxb-4499975982261-4488413284439-B7q6yPTZ05jlhFzCPAM9FLG7'
SLACK_CHANNEL = 'C04ESPY68V9'

message_list_1 = [' 포스팅을 보며 정성이 가득하다고 느꼈어요', ' 포스팅을 보며 도움이 많이 됐어요', ' 포스팅을 보며 전문가의 포스를 느꼈어요']

message_list_2 = ['! ', '!! ', '!!! ', '~ ', '~~ ', '~! ', '!~ ', '. ', '.. ', '!~~ ' ,'~~! ', ' ㅎ ', ' ㅎㅎ ', ' ㅎㅎㅎ ', ' ㅋㅋㅋ ', ' ㅋㅋㅋㅋ ']

message_list_3 = ['(•̀ᴗ•́)و ̑̑♡٩', '૮꒰ ྀི ◜ . ◝ ྀི꒱ა', '⸝⸝◜࿀◝ ⸝⸝', '( ◜࿀◝ )', '( ◜‿◝ )*.✧', '⸝⸝ʚ̴̶̷̆ᴗʚ̴̶̷̆⸝⸝', '《 ͡꘠ ͜ゝ ͡꘠》', '❣°ʚ(❛ั ᴗ ❛ั)ɞ°❣',
                  'ฅ(^▸ਉ◂^)ฅ', '( ᵔᵒᵔ )ᵍᵒᵒᵈᵎᵎ', '(ꆧ⩊ꆧ )', '( ˊᵕ̤ ̮ ᵕ̤ˋ )', '❉𓂂(◕˓˳◕ )𓂂❉', 'ପ(｡ᵔ ⩊ ᵔ｡)ଓ', '●̑ᴗ●̑', 'ฅ(•ㅅ•❀)ฅ', '( *˘╰╯˘*)',
                  '(｡⌒𖧉⌒)⋆.˚⊹⁺', '( ◠ •̫̮ ◠)☆', '(ˊ•͈ ˓ •͈ˋ)', '(̂˃ꄃ˂ )̂', '( • .̮ •)◞⸒⸒', '(ᵔᵕᵔ)']

message_list_4 = [' 항상 좋은 글 부탁드려요', ' 언제나 좋은 글 부탁드려요', ' 다음에도 좋은 글 부탁드려요', ' 주기적으로 좋은 글 부탁드려요',
                  ' 매일매일 좋은 글 부탁드려요', ' 내일도 좋은 글 부탁드려요', ' 또 좋은 글 부탁드려요',
                  
                  ' 다음에도 보러 올게요', ' 매일매일 보러 올게요', ' 내일도 보러 올게요', ' 또 보러 올게요', ' 항상 보러 올게요',
                  
                  ' 오늘도 좋은 정보 감사해요', ' 항상 좋은 정보 감사해요', ' 언제나 좋은 정보 감사해요', ' 다음에도 좋은 정보 감사해요',
                  ' 매일매일 좋은 정보 감사해요', ' 주기적으로 좋은 정보 감사해요', ]

message_list_5 = [' ☆', ' ★', ' ♡', ' ♥']

site_url = 'https://nid.naver.com/nidlogin.login?svctype=262144&amp;url=http://undefined/aside/'    #네이버 모바일 로그인 URL

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

fg_color = "#6667AB"
hover_color = "#4d4e8d"

server_start = False
now_ver = "22.12.15"
    
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        try:
            with open('config', 'rb') as f:    # 로그인 정보 가져오기
                user_id = pickle.load(f)
                user_pw = pickle.load(f)
                user_like = pickle.load(f)
                user_comment = pickle.load(f)
                user_log = pickle.load(f)
                post_range = pickle.load(f)
                speed = pickle.load(f)
        except Exception:   # 없으면 기본 정보 등록
                user_id = ''
                user_pw = ''
                user_like = 1
                user_comment = 1
                user_log = 1
                post_range = 20
                speed = 1
            
        self.json_get()
        
        path = os.path.join(os.path.dirname(__file__), "icon.ico")
        if os.path.isfile(path):
            self.iconbitmap(path)
        # configure window
        self.title("Keuriate Blog Bot.py")
        self.frame_size(180, 200)
        self.resizable(width=False, height=False)
        
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # 왼쪽
        self.sidebar_frame = customtkinter.CTkFrame(self, width=180, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=8, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)
        
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="로그인 정보", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(10, 5))
        
        self.entry_1 = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="ID")
        self.entry_1.grid(row=1, column=0, columnspan=1, padx=(20, 20), pady=(0, 10), sticky="nsew")
        
        self.entry_2 = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="PW", show="*")
        self.entry_2.grid(row=2, column=0, columnspan=1, padx=(20, 20), pady=(0, 10), sticky="nsew")
        
        self.entry_3 = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="SN")
        self.entry_3.grid(row=3, column=0, columnspan=1, padx=(20, 20), pady=(0, 10), sticky="nsew")
        
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, fg_color=fg_color, hover_color=hover_color, text="저장하기", command=self.login_save)
        self.sidebar_button_1.grid(row=4, column=0, columnspan=1, padx=(20, 20), pady=(0, 10))
        
        
        self.version1_label = customtkinter.CTkLabel(self.sidebar_frame, text="현재 버전 : " + now_ver, font=customtkinter.CTkFont(size=12))
        self.version1_label.grid(row=5, column=0, padx=(20, 20), pady=(10, 0))
        
        self.version2_label = customtkinter.CTkLabel(self.sidebar_frame, text="최신 버전 : " + new_ver, font=customtkinter.CTkFont(size=12))
        self.version2_label.grid(row=6, column=0, padx=(20, 20), pady=(0, 0))
        
        self.date_label = customtkinter.CTkLabel(self.sidebar_frame, text=auth_notice, font=customtkinter.CTkFont(size=12))
        self.date_label.grid(row=7, column=0, padx=(20, 20), pady=(0, 10))
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=9, column=0, padx=20, pady=(0, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=10, column=0, padx=20, pady=(0, 10))
        
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=11, column=0, padx=20, pady=(0, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=12, column=0, padx=20, pady=(0, 20))
        
        # 중앙
        self.textbox = customtkinter.CTkTextbox(self, width=450, font=customtkinter.CTkFont(size=12))
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.progressbar_1 = customtkinter.CTkProgressBar(self)
        self.progressbar_1.grid(row=5, column=0, columnspan=5, padx=(0, 0), pady=(0, 0), sticky="nsew")

        # 오른쪽 상단
        self.tabview = customtkinter.CTkTabview(self, width=130, segmented_button_selected_color=fg_color, segmented_button_selected_hover_color=hover_color)
        self.tabview.grid(row=0, column=3, padx=(20, 20), pady=(0, 0), sticky="nsew")
        self.tabview.add("정보")
        self.tabview.add("Tab 2")
        self.tabview.add("Tab 3")
        self.tabview.tab("정보").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)

        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("정보"))
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=(10, 0))
        self.label_tab_3 = customtkinter.CTkLabel(self.tabview.tab("정보"))
        self.label_tab_3.grid(row=1, column=0, padx=20, pady=(5, 0))
        self.label_tab_4 = customtkinter.CTkLabel(self.tabview.tab("정보"))
        self.label_tab_4.grid(row=2, column=0, padx=20, pady=(5, 0))
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Tab 2"), dynamic_resizing=False, values=["Value 1", "Value 2", "Value Long Long Long"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("Tab 2"), values=["Value 1", "Value 2", "Value Long....."])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("Tab 2"), text="입력하기", command=self.open_input_dialog_event)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))

        # 오른쪽 하단
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        
        self.switch_1 = customtkinter.CTkSwitch(master=self.checkbox_slider_frame, progress_color=fg_color, text="         공감")
        self.switch_1.grid(row=1, column=0, padx=20, pady=(5, 10), sticky="n")
        
        self.switch_2 = customtkinter.CTkSwitch(master=self.checkbox_slider_frame, progress_color=fg_color, text="         댓글")
        self.switch_2.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="n")
        
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, fg_color=fg_color, hover_color=hover_color, text=' 실시간 로그 출력')
        self.checkbox_1.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="n")

        self.scaling_label1 = customtkinter.CTkLabel(self.checkbox_slider_frame, text="게시글 범위", anchor="w")
        self.scaling_label1.grid(row=4, column=0, padx=10, pady=(0, 0))
        
        self.speed_slider1 = customtkinter.CTkSlider(self.checkbox_slider_frame, button_color=fg_color, button_hover_color=hover_color, from_=10, to=50, number_of_steps=4)
        self.speed_slider1.grid(row=5, column=0, padx=20, pady=(0, 0), sticky="n")

        self.scaling_label2 = customtkinter.CTkLabel(self.checkbox_slider_frame, text="딜레이 속도", anchor="w")
        self.scaling_label2.grid(row=6, column=0, padx=10, pady=(0, 0))
        
        self.speed_slider2 = customtkinter.CTkSlider(self.checkbox_slider_frame, button_color=fg_color, button_hover_color=hover_color, from_=0.5, to=2.5, number_of_steps=4)
        self.speed_slider2.grid(row=7, column=0, padx=20, pady=(0, 0), sticky="n")

        self.start_button = customtkinter.CTkButton(self.checkbox_slider_frame, width=200, fg_color=fg_color, hover_color=hover_color, text="시작", command=self.thread_start)
        self.start_button.grid(row=8, column=0, padx=(10, 10), pady=(20, 0), sticky="n")

        # set default values
        self.entry_1.insert(0, user_id)
        self.entry_2.insert(0, user_pw)
        self.entry_3.insert(0, serial)
        self.entry_3.configure(state="disabled")
        self.speed_slider1.set(post_range)
        self.speed_slider2.set(speed)
        self.checkbox_1.select()
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.optionmenu_1.set("메뉴")
        self.combobox_1.set("콤보박스")
        
        if user_like == 0:
            self.switch_1.deselect()
        else: 
            self.switch_1.select()
            
        if user_comment == 0:
            self.switch_2.deselect()
        else: 
            self.switch_2.select()
        
        if user_log == 0:
            self.checkbox_1.deselect()
        else: 
            self.checkbox_1.select()
            
        self.progressbar_1.configure(mode="indeterminnate")
        self.progressbar_1.start()

    def frame_size(self, width: int, height: int):
        x_Left = int(self.winfo_screenwidth()/2 - width/2)
        y_Top = int(self.winfo_screenheight()/2 - height/2)
        
        self.geometry(f"{width}x{height}")
        self.geometry("+{}+{}".format(x_Left, y_Top))

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        
    #크롬 실행
    def exec_chrom(self):
        options = webdriver.ChromeOptions()
        options.add_argument("disable-gpu")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=options)
        driver.maximize_window()
        return driver
    
    #로그인
    def login(self, driver):
        global user_id, user_pw
        driver.get(site_url)
        pyperclip.copy(user_id)  # id를 클립보드에 복사
        driver.find_element(by='name', value='id').send_keys(Keys.CONTROL + 'v')  # id 입력창에 보냄
        pyperclip.copy(user_pw)  # 패스워드를 클립보드에 복사
        driver.find_element(by='name', value='pw').send_keys(Keys.CONTROL + 'v')  # 패스워드를 입력창에 보냄
        driver.find_element(by='xpath', value='//*[@id="log.login"]').click()  # 로그인 버튼 클릭
        time.sleep(speed)  # 로그인 되는 시간을 위해 슬립
        driver.find_element(by='xpath', value='//*[@id="HOME_SHORTCUT"]/ul/li[7]/a/div/picture/img').click()  # 블로그 아이콘 클릭


    #블로그 링크따기
    def get_blog(self, driver):
        for i in range(0, int(post_range), 1):  # 반복 횟수로 불러올 게시글량 조절 가능
            driver.find_element(by='tag name', value='body').send_keys(Keys.PAGE_DOWN)
            time.sleep(speed)
        html = driver.page_source  # 링크를 따와야 하므로 게시글이 많이 불러진 상태에서 html 객체를 생성
        soup = BeautifulSoup(html, 'html.parser')
        link_list = soup.select('.thumb_area__IeDdQ > a')   #링크 추출
        return link_list


    #포스팅별 방문하여 좋아요 클릭
    def click_like(self, driver, link_list):
        like_cnt = 0  # 좋아요 버튼 누른 횟수 저장 변수
        comment_cnt = 0  # 댓글 작성 횟수 저장 변수

        #추출된 링크 수 만큼 방문하여 좋아요 버튼 클릭
        for i in range(len(link_list)):
            site = (link_list[i]['href'])
            driver.get(site)
            time.sleep(2)
            title = driver.title.strip(" : 네이버 블로그")   # 블로그 제목 크롤링
            try:
                is_like = driver.find_element(by='xpath', value='//*[@id="body"]/div[10]/div/div[1]/div/div/a').get_attribute('aria-pressed')   #좋아요 버튼 상태 확인
                #print(is_like)
            except Exception:   #간혹 공감 버튼 자체가 없는 게시글이 존재함
                if user_log == 1:
                    self.send_message(title + ' 게시물에 공감이 비활성화 되어있습니다.')
                continue
            if is_like == 'false':  #좋아요 버튼 상태가 안눌러져있는 상태일 경우에만 좋아요 버튼 클릭
                time.sleep(10) # 좋아요 누르기 전 90초 대기
                try:
                    driver.find_element(by='xpath', value='//*[@id="body"]/div[10]/div/div[1]/div/div/a/span').click()  #하트 클릭
                except Exception:
                    driver.find_element(by='xpath', value='//*[@id="ct"]/div[4]/div[2]/div/div[1]/div/div/a/span').click()  #하트 클릭
                    print("게시글 내에 있는 하트 클릭")
                    continue
                if user_log == 1:
                    self.send_message(title + ' 게시물에 좋아요를 클릭했습니다.')
                like_cnt += 1   #좋아요 횟수 1증가
                time.sleep(speed)
                
                try:
                    time.sleep(10) # 댓글 누르기 전 90초 대기
                    driver.find_element(by='xpath', value='//*[@id="body"]/div[10]/div/div[2]/a[1]/span').click()  #댓글 클릭
                    time.sleep(speed)
                
                    driver.find_element(by='xpath', value='//*[@id="naverComment"]/div/div[7]/div[1]/form/fieldset/div/div/div[2]').click()  #입력 클릭
                    time.sleep(speed)
                
                    comment_msg = random.choice(message_list_1) + random.choice(message_list_2) + random.choice(message_list_3) + random.choice(message_list_4) + random.choice(message_list_5)
                    pyperclip.copy(title + comment_msg)  # 메세지를 클립보드에 복사
                    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                    if user_log == 1:
                        self.send_message(title + ' 게시물에 댓글 작성을 완료했습니다.')
                        self.send_message('작성한 댓글 : ' + comment_msg)
                    time.sleep(speed)
                
                    driver.find_element(by='xpath', value='//*[@id="naverComment"]/div/div[7]/div[1]/form/fieldset/div/div/div[6]/button/span[2]').click()  #등록 클릭
                    comment_cnt += 1   #좋아요 횟수 1증가
                    time.sleep(speed)
                except:
                    if user_log == 1:
                        self.send_message(title + ' 게시물에 댓글이 비활성화 되어있습니다.')
                    continue
            try:
                time.sleep(speed)
                alert = Alert(driver)   #팝업창으로 메시지 뜰 경우를 대비
                alert.accept()
            except Exception:
                continue
        return like_cnt, comment_cnt
    
    #크롬
    def pause(self):
        schedule.every(1).seconds.do(exit)
        driver = self.exec_chrom()
        driver.close()
        global server_start
        server_start = False

    # 블로그 봇 시작
    def start(self):
        self.send_message('1/5 크롬 드라이버에 연결하는 중...')
        driver = self.exec_chrom()
        self.send_message('2/5 네이버에 로그인하는 중...')
        self.login(driver)
        self.send_message('3/5 블로그 리스트를 가져오는 중...')
        link_list = self.get_blog(driver)
        self.send_message('4/5 좋아요 클릭, 댓글 작성 진행 중...')
        like_cnt, comment_cnt = self.click_like(driver, link_list)
        self.send_message('5/5 서버 종료 중...')
        self.close()
        self.send_message("총 {}개의 게시글 중 {}개의 공감, {}개의 댓글을 작성했습니다.".format(len(link_list), like_cnt, comment_cnt))
        self.slack_bot("[" + user_id + "] 총 {}개의 게시글 중 {}개의 공감, {}개의 댓글을 작성했습니다.".format(len(link_list), like_cnt, comment_cnt))
    
    # 블로그 봇 종료
    def close(self):
        time.sleep(speed)
        driver = self.exec_chrom()
        driver.close()
        global server_start
        server_start = False
        
    # 메세지 전송
    def send_message(self, msg):
        now = datetime.datetime.now()
        tm = now.strftime('%H:%M:%S') + " "
        message = msg
        self.textbox.insert("0.0", tm + "[알림] " + message + "\n" * 1)
    
    # 슬랙 디버깅
    def slack_bot(self, bot_message):
        now = datetime.datetime.now()
        tm = now.strftime('%H:%M:%S') + " "
        
        slack_token = SLACK_TOKEN
        channel = SLACK_CHANNEL
        message = bot_message
        client = slack_sdk.WebClient(token = slack_token)
        client.chat_postMessage(channel = channel, text = tm + message)
        
    #로그인 저장
    def login_save(self):
        user_id = self.entry_1.get()
        user_pw = self.entry_2.get()
        if user_id and user_pw:
            self.frame_size(900, 580)
            self.resizable(width=False, height=False)
            self.entry_1.configure(state="disabled")
            self.entry_2.configure(state="disabled")
            self.sidebar_button_1.configure(state="disabled")
            self.send_message("로그인 정보가 저장되었습니다.")
            self.visit_get()
        else:
            showerror("오류", "아이디와 비밀번호를 입력해주세요.")
         
    #세팅 저장
    def config_save(self):
        global user_id, user_pw, user_like, user_comment, user_log, post_range, speed
        user_id = self.entry_1.get()
        user_pw = self.entry_2.get()
        user_like = self.switch_1.get()
        user_comment = self.switch_2.get()
        user_log = self.checkbox_1.get()
        post_range = self.speed_slider1.get()
        speed = self.speed_slider2.get()
        print("저장 : " + user_id, user_pw, user_like, user_comment, user_log, post_range, speed)
        try:
            with open('config', 'wb') as f:
                pickle.dump(user_id, f)
                pickle.dump(user_pw, f)
                pickle.dump(user_like, f)
                pickle.dump(user_comment, f)
                pickle.dump(user_log, f)
                pickle.dump(post_range, f)
                pickle.dump(speed, f)
        except Exception:   # 없으면 기본 정보 등록
            print("저장 실패")
            
    # 1초마다 start 실행
    def schedule_start(self):
        global server_start
        server_start = True
        self.config_save()
        self.send_message("마지막 실행 정보가 저장되었습니다.")
        self.start_button.configure(state="disabled")
        schedule.every(1).seconds.do(self.visit_get)
        schedule.every(1).seconds.do(self.start)
        #schedule.every(30).minutes.do(self.start)
        while True:
            schedule.run_pending()
            time.sleep(1)

    # 크롬을 위한 스레드
    def thread_start(self):
        if (auth_date.days >= 0): # 인증 기간이 남아 있으면
            t=threading.Thread(target=self.schedule_start)
            if server_start == False:
                t.setDaemon(True) # GUI 종료 시 데몬 스레드 종료 
                t.start()
            else:
                showerror("오류", "이미 실행 중입니다.")
        else:
            answer = askyesno("오류", "기간 연장 후 사용 가능합니다.\n\n연장하시겠습니까?")
            if answer:
                driver = self.exec_chrom()
                webbrowser.open("https://open.kakao.com/me/keuriate")

    # json 파싱
    def json_get(self):
        global new_ver, serial, auth_date, auth_notice
        url = "http://dailyjung.kr/auth/serial_auth.json"
        data = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).json() # json 데이터 가져오기
        
        c = wmi.WMI()
        m = c.Win32_Processor()
        s = m[0].ProcessorId # 하드 시리얼 넘버 체크
        serial = s[9] + s[0] + s[11] + s[3] + s[1] + s[12] + s[4] + s[2] + s[15] + s[7] + s[10] + s[6] + s[5] + s[8] + s[13]
        self.slack_bot("ProcessorId" + serial)
        try:
            new_ver = data["admin"]["ver"]
            now_date = datetime.datetime.now()
            set_date = datetime.datetime.strptime(data[serial]["date"],'%Y%m%d')
            auth_date = set_date - now_date
            if (auth_date.days >= 0): # 인증 기간이 남아 있으면
                auth_notice = str(auth_date.days) + "일 남았습니다."
            else:
                auth_notice = "사용 기간이 끝났습니다."
        except Exception:   # 사용자가 등록이 되어있지 않으면
            auth_notice = "사용 기간이 끝났습니다."
            
    def visit_get(self):
        global visit
        url = "https://m.blog.naver.com/api/blogs/"
        data = requests.get(url + self.entry_1.get(), headers={"User-Agent": "Mozilla/5.0", "referer": "https://m.blog.naver.com/PostList.naver?blogId=" + self.entry_1.get()}).json()

        self.label_tab_2.configure(text="오늘 방문자 : " + str(data["result"]["dayVisitorCount"]) + "명")
        self.label_tab_3.configure(text="전체 방문자 : " + str(data["result"]["totalVisitorCount"]) + "명")
        self.label_tab_4.configure(text="이웃 : " + str(data["result"]["subscriberCount"]) + "명")
        print("블로그 정보 get")
            
            
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
