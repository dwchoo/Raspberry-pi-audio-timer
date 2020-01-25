import RPi.GPIO as GPIO
import time
from datetime import datetime
import threading
import curses
import pygame
from pygame import mixer

class play_music_control:
    def __init__(self,timer_start=[None,None], timer_stop=[None,None]):
        try:
            #sound_file_1 = 'Music/brownworship.wav'
            sound_file_1 = 'Music/brownworship.ogg'
            #sound_file_2 = 'Music/brownworship_2.wav'
            sound_file_2 = 'Music/brownworship_2.ogg'

            frq = 44100
            bitsize = -16
            channels = 2
            buffer = 1024

            self.sound_mixer = mixer

            self.sound_mixer.init(frequency = frq,
                          size = bitsize,
                          channels = channels,
                          buffer = buffer)

            self.sound_mixer.set_num_channels(2)

            self.sound_1 = self.sound_mixer.Sound(sound_file_1)
            self.sound_2 = self.sound_mixer.Sound(sound_file_2)

            self.channel_1 = self.sound_mixer.Channel(0)
            self.channel_2 = self.sound_mixer.Channel(1)


            GPIO.setmode(GPIO.BCM)
            GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

            GPIO.setup(17, GPIO.OUT)
            GPIO.output(17,False)

            GPIO.add_event_detect(4, GPIO.RISING, callback=self.play_sound, bouncetime=2000)
            GPIO.add_event_detect(27, GPIO.RISING, callback=self.stop_sound, bouncetime=2000)
            
            
            # display part
            
            self.now_playing = False
            self.special_system_message = [ "Ready" ]
            
            self.start_time = timer_start#[21, 54]
            self.stop_time = timer_stop#[21, 56]
            
            try:
                self.stdscr = curses.initscr()
                curses.noecho()
                curses.cbreak()


                progress_list = ["|", "/","-","\\","|","/","-","\\"]
                counter = 0
                while True:
                    for progress in progress_list:
                        hour, minute, second, now_ = self.now_time()
                        self.display(now_, progress, self.now_playing,
                                     timer_state=[self.start_time, self.stop_time],
                                     system_message=self.special_system_message)
                        time.sleep(0.4)
                        
                        self.timer_start_music(hour, minute, second, self.start_time)
                        self.timer_stop_music(hour, minute, second, self.stop_time)
                        
                    if self.special_system_message is not ["Ready"]:
                        counter += 1
                    if counter == 3:
                        self.special_system_message = ["Ready"]
                        counter = 0
                        
            finally:

                curses.echo()
                curses.nocbreak()
                curses.endwin()
                
        finally:
            self.sound_mixer.quit()
            GPIO.cleanup()
            print('\nFinish!!')
        
        
    def play_sound(self,pin, fade_in=0):
        #print("\nMusic play")
        self.special_system_message = ["Music play"]
        self.LED_ON(pin)
        self.channel_1.play(self.sound_1,
                            loops = -1,
                            fade_ms = fade_in
                            #시작시 fader를 주면 잘못해서 연속으로 버튼을 누를 때 소리가 작게 재생되는 버그가 있다.
                           )
        self.now_playing = True
        pass
    
    def stop_sound(self, pin):
        #print("\nMusic off")
        self.special_system_message = ["Music Off"]
        self.LED_OFF(pin)
        self.channel_1.fadeout(int(5e3))
        self.now_playing = False
        pass
    
    def LED_ON(self, pin):
        #print('LED On')
        self.special_system_message += ["LED On"]
        GPIO.output(17,True)
        pass
    
    def LED_OFF(self, pin):
        #print('LED Off')
        self.special_system_message += ["LED Off"]
        GPIO.output(17,False)
        pass
    
    def timer(self,hour, minute, second, timer):
        if minute == timer[1] and hour == timer[0] and second < 3:
            return True
        return False
    
    def timer_start_music(self,now_hour, now_minute, second, timer):
        if self.timer(now_hour, now_minute, second, timer) and self.now_playing is False:
            self.play_sound(None, fade_in=5)
        pass
    
    #TODO: 미완성
    def timer_stop_music(self, now_hour, now_minute, second, timer):
        if self.timer(now_hour, now_minute, second, timer) and self.now_playing is True:
            self.stop_sound(None)
        pass
    
        
    def now_time(self):
        now = datetime.now()
        week = ['월', '화', '수', '목', '금', '토', '일']
        now_ = "{.month:02}/{.day:02} {} {.hour:02}:{.minute:02}:{.second:02}".format(now, now, week[now.weekday()], now, now, now)
        return now.hour, now.minute, now.second, now_
        
        
    def display(self,now_time, progress, music_playing=True, timer_state = None,system_message=None):
        if music_playing == True:
            music_progress = progress
        else:
            music_progress = "."

        self.stdscr.addstr(0,0, "now time : {}".format(now_time))
        self.stdscr.addstr(1,0, "Program is running  {}".format(progress))
        self.stdscr.addstr(2,0, "Music playing       {}".format(music_progress))
        self.stdscr.addstr(3,0, "Timer state -  start    {:02}:{:02}".format(timer_state[0][0], timer_state[0][1]))
        self.stdscr.addstr(4,0, "Timer state -  stop     {:02}:{:02}".format(timer_state[1][0], timer_state[1][1]))
        self.stdscr.addstr(5,0, "System Message          {}".format(system_message))
        self.stdscr.clrtoeol()
        self.stdscr.refresh()
        pass
    
    
if __name__ == "__main__":
    
    start_time = [22,1]
    stop_time = [22,3]
    
    music_player = play_music_control(timer_start=start_time, timer_stop=stop_time)

 
