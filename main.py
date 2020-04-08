from gui_main import GUIMain


g = GUIMain()
g.set_layout()
while g.event_handler():
    pass

g.window.close()
