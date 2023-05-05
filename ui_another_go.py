
# -*- coding: utf-8 -*-

from remi.gui import *
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
        svg0.css_height = "200px"
        svg0.css_left = "150.0px"
        svg0.css_position = "absolute"
        svg0.css_top = "135.0px"
        svg0.css_width = "200px"
        svg0.variable_name = "svg0"
        svgcircle0 = SvgCircle()
        svgcircle0.attr_class = "SvgCircle"
        svgcircle0.attr_cx = "100.0"
        svgcircle0.attr_cy = "100.0"
        svgcircle0.attr_editor_newclass = False
        svgcircle0.attr_r = "100.0"
        svgcircle0.css_left = "380.890625px"
        svgcircle0.css_top = "297.71875px"
        svgcircle0.variable_name = "svgcircle0"
        svg0.append(svgcircle0,'svgcircle0')
        

        self.svg0 = svg0
        return self.svg0
    


#Configuration
configuration = {'config_project_name': 'untitled', 'config_address': '0.0.0.0', 'config_port': 8081, 'config_multiple_instance': True, 'config_enable_file_cache': True, 'config_start_browser': True, 'config_resourcepath': './res/'}

if __name__ == "__main__":
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(untitled, address=configuration['config_address'], port=configuration['config_port'], 
                        multiple_instance=configuration['config_multiple_instance'], 
                        enable_file_cache=configuration['config_enable_file_cache'],
                        start_browser=configuration['config_start_browser'])
