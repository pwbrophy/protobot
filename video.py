
# -*- coding: utf-8 -*-

from remi.gui import *
from widgets.toolbox_opencv import *
from remi import start, App


class untitled(App):
    def __init__(self, *args, **kwargs):
        #DON'T MAKE CHANGES HERE, THIS METHOD GETS OVERWRITTEN WHEN SAVING IN THE EDITOR
        if not 'editing_mode' in kwargs.keys():
            super(untitled, self).__init__(*args, static_file_path={'my_res':'./res/'})

    def idle(self):
        #idle function called every update cycle
        pass
    
    def main(self):
        return untitled.construct_ui(self)
        
    @staticmethod
    def construct_ui(self):
        #DON'T MAKE CHANGES HERE, THIS METHOD GETS OVERWRITTEN WHEN SAVING IN THE EDITOR
        svg0 = Svg()
        svg0.attr_class = "Svg"
        svg0.attr_editor_newclass = False
        svg0.css_height = "300.0px"
        svg0.css_left = "165.0px"
        svg0.css_position = "absolute"
        svg0.css_top = "165.0px"
        svg0.css_width = "315.0px"
        svg0.variable_name = "svg0"
        opencvvideo0 = OpencvVideo()
        opencvvideo0.attr_class = "OpencvVideo"
        opencvvideo0.attr_editor_newclass = False
        opencvvideo0.css_height = "180px"
        opencvvideo0.css_left = "210.0px"
        opencvvideo0.css_position = "absolute"
        opencvvideo0.css_top = "225.0px"
        opencvvideo0.css_width = "200px"
        opencvvideo0.framerate = 10
        opencvvideo0.variable_name = "opencvvideo0"
        opencvvideo0.video_source = 0
        svg0.append(opencvvideo0,'opencvvideo0')
        

        self.svg0 = svg0
        return self.svg0
    


#Configuration
configuration = {'config_project_name': 'untitled', 'config_address': '0.0.0.0', 'config_port': 8081, 'config_multiple_instance': True, 'config_enable_file_cache': True, 'config_start_browser': True, 'config_resourcepath': './res/'}

if __name__ == "__main__":
    start(MyApp, debug=False, address='192.168.86.22', port=8081, start_browser=False, multiple_instance=True)
