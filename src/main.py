import time
import json
import keyboard

def config():
    return json.load(open('config.json'))

muted = config()["muted_on_start"]
mute_key = config()['discord_mute_hotkey_scancode']

def toggle_mute():
    global muted
    muted = not muted
    key = mute_key
    keyboard.press_and_release(key)

def key_pressed(event):
    global muted
    global last_keypress

    last_keypress = event.time
    if event.scan_code == mute_key:
        return

    if not muted:
        toggle_mute()

def main():
    last_keypress = 0
    keyboard.on_press(key_pressed)
    
    typing_check = config()['update_typing_check_seconds']
    unmute_delay = config()['unmute_after_not_typing_for_seconds']
    
    print(typing_check, unmute_delay)

    while True:
        time.sleep(typing_check)
        delay = time.time() - last_keypress

        if delay > unmute_delay:
            if muted:
                toggle_mute()

if __name__ == '__main__':
    main()