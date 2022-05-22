from libqtile import widget
from libqtile import qtile
from requests import get, post

COMMAND = "/home/jicg/.config/qtile/scripts/q_pomodoro.sh"

url = "http://localhost:4884/pomodoro"
url_toggle = "http://localhost:4884/pomodoro/toggle"

GPT = None

break_color = "#ffff00"
paused_color = "#ff0000"
pomodoro_color = "#30f0ff"

TMR = 0
ST = 1
PM = 2

def set_colors(st, pm):
    color = "NONE"
    if GPT is not None:
        if st == "stopped":
            GPT.foreground = paused_color
            color = paused_color
        else:
            if pm == "POMODORO": 
                GPT.foreground = pomodoro_color 
                color = pomodoro_color
            else: 
                GPT.foreground = break_color
                color = break_color
    with open("/tmp/color", "a") as f:
        f.write(f"{st} - {pm} - {color}\n")

def run_it():
    resp = ""
    try:
        response = get(url)
         
        if response.status_code == 200:
            r = response.text.strip().split()
            resp = r[TMR]
            set_colors(r[ST], r[PM])
    except:
        pass
    return resp


def toggle_it():
    try:
        post(url_toggle)
    except:
        pass

def get_gen_poll_text(fg, bg):
    global GPT
    GPT = widget.GenPollText(update_interval=1, 
                        font="Noto Sans",
                        padding = 0,
                        # foreground = colors[5],
                        foreground = fg,
                        background = bg,
                        fontsize = 14,
                        # func=lambda: subprocess.check_output("/home/jicg/.config/qtile/scripts/q_pomodoro.sh").decode('UTF-8'),
                        func=run_it,
                        # mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("curl localhost:4884/pomodoro/toggle -X POST")}
                        mouse_callbacks={"Button1": toggle_it}
                        )
    return GPT

