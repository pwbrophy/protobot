
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
        container0 = Container()
        container0.attr_class = "Container"
        container0.attr_editor_newclass = False
        container0.css_height = "510.0px"
        container0.css_left = "180.0px"
        container0.css_position = "absolute"
        container0.css_top = "120.0px"
        container0.css_width = "945.0px"
        container0.variable_name = "container0"
        svg0 = Svg()
        svg0.attr_class = "Svg"
        svg0.attr_editor_newclass = False
        svg0.css_height = "345.0px"
        svg0.css_left = "105.0px"
        svg0.css_position = "absolute"
        svg0.css_top = "75.0px"
        svg0.css_width = "645.0px"
        svg0.variable_name = "svg0"
        container0.append(svg0,'svg0')
        opencvvideo0 = OpencvVideo()
        opencvvideo0.attr_class = "OpencvVideo"
        opencvvideo0.attr_editor_newclass = False
        opencvvideo0.css_height = "240.0px"
        opencvvideo0.css_left = "210.0px"
        opencvvideo0.css_position = "absolute"
        opencvvideo0.css_top = "150.0px"
        opencvvideo0.css_width = "495.0px"
        opencvvideo0.framerate = 10
        opencvvideo0.variable_name = "opencvvideo0"
        opencvvideo0.video_source = 0
        container0.append(opencvvideo0,'opencvvideo0')
        

        self.container0 = container0
        return self.container0
    


#Configuration
configuration = {'config_project_name': 'untitled', 'config_address': '0.0.0.0', 'config_port': 8081, 'config_multiple_instance': True, 'config_enable_file_cache': True, 'config_start_browser': True, 'config_resourcepath': './res/'}

if __name__ == "__main__":
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(untitled, address=configuration['config_address'], port=configuration['config_port'], 
                        multiple_instance=configuration['config_multiple_instance'], 
                        enable_file_cache=configuration['config_enable_file_cache'],
                        start_browser=configuration['config_start_browser'])
