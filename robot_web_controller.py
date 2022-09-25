
import remi.gui as gui
from remi import start, App
import threading



global do_walk_forwards
do_walk_forwards = False

class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def idle(self):
        # this function is called automatically by remi library at specific interval
        # so here I can assign values to widget
        self.lbl.set_text('Thread result:' + str(self.my_thread_result))

    def main(self):
        # margin 0px auto allows to center the app to the screen
        wid = gui.VBox(width=300, height=200, margin='0px auto')
        self.lbl = gui.Label('Thread result:', width='80%', height='50%')
        self.lbl.style['margin'] = 'auto'

        bt = gui.Button('Stop algorithm', width=200, height=30)
        bt.style['margin'] = 'auto 50px'
        bt.style['background-color'] = 'red'

        wid.append(self.lbl)
        wid.append(bt)

        self.thread_alive_flag = True
        self.my_thread_result = 0
        # Here I start a parallel thread that executes my algorithm for a long time
        t = threading.Thread(target=self.my_intensive_long_time_algorithm)
        t.start()

        bt.onclick.do(self.on_button_pressed)

        # returning the root widget
        return wid

    def my_intensive_long_time_algorithm(self):
        while self.thread_alive_flag:
            do_walk_forwards = True

    def on_button_pressed(self, emitter):
        self.thread_alive_flag = False

    def on_close(self):
        self.thread_alive_flag = False
        super(MyApp, self).on_close()


if __name__ == "__main__":
    start(MyApp, debug=True, address='192.168.86.40', port=8081, update_interval=0.1)
