# Raspberry-pi-timer_audio


## Raspberry pi volume control in command line  
`alsamixer`


## Audio 재생은 pygame 라이브러리를 사용했다.  
[https://www.pygame.org/docs/](https://www.pygame.org/docs/)
`pygame.mixer.music`을 사용해서 재생을 하면 한번에 1개읙 곡만 재생 가능하며,  
곡 재생을 멈추고 다시 재생할 때 멈추기 전에 재생되는 부분을 1초 정도 재생하고 다시 재생하는 버그가 있다.  
음악을 재생하고 싶으면 `pygmae.mixer.Channel` 혹은 `pygmae.mixer.Sound`함수를 사용하는 것이 좋다.  
이 두 함수는 mp3를 재생할 수 없다. 따라서 ogg 포맷 혹은 wav 파일만 불러와서 재생해야 한다.  
(ogg파일은 압축되어 mp3와 비슷한 크기이고, wav파일은 비압축이여서 크기가 크다)  
ogg파일 같은 경우 처음 파일을 mixer로 불러올 때 로딩 시간이 필요하다.  
하지만 이것은 처음에 프로그램을 실행 시킬때 로딩해 주면 나중에 재생은 즉각 가능하다.  

pygame의 장점으로 오디오 볼품조절 및 fade-in fade-out 기능이 있다.  
즉 음악의 볼륨 조절 및 컨트롤이 좋다.  
그리고 중간으로 이동하고 어느 부분에 있는지 알 수 있는 함수가 잘 준비되어 있다.  

---

## 상태 Display 부분  
Command line에서 현재의 상태를 확인하고 싶었고, 하나의 페이지 처럼 나오면 좋겠다는 생각이 들았다.  
즉 내가 많이 쓰는 `nvidia-smi -l 1`과 `watch -n 1 nvidia-smi`의 차이 처럼 현재 정보를 업데이트 하는 표현 방식을 원했다.  
