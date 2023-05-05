
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
        svg0.css_height = "255.0px"
        svg0.css_left = "60.0px"
        svg0.css_position = "absolute"
        svg0.css_top = "60.0px"
        svg0.css_width = "270.0px"
        svg0.variable_name = "svg0"
        svgcircle0 = SvgCircle()
        svgcircle0.attr_class = "SvgCircle"
        svgcircle0.attr_cx = 135.0
        svgcircle0.attr_cy = 120.0
        svgcircle0.attr_editor_newclass = False
        svgcircle0.attr_fill = "rgb(200,200,200)"
        svgcircle0.attr_r = "90.0"
        svgcircle0.attr_stroke = "rgb(0,0,0)"
        svgcircle0.css_left = "190.875px"
        svgcircle0.css_top = "165.90625px"
        svgcircle0.variable_name = "svgcircle0"
        svg0.append(svgcircle0,'svgcircle0')
        svg0.ontouchend.do(self.ontouchend_svg0)
        svg0.ontouchstart.do(self.ontouchstart_svg0)
        

        self.svg0 = svg0
        return self.svg0
    
    def ontouchend_svg0(self, emitter, x, y):
        pass

    def ontouchstart_svg0(self, emitter, x, y):
        pass



#Configuration
configuration = {'config_project_name': 'untitled', 'config_address': '0.0.0.0', 'config_port': 8081, 'config_multiple_instance': True, 'config_enable_file_cache': True, 'config_start_browser': True, 'config_resourcepath': './res/'}

if __name__ == "__main__":
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(untitled, address=configuration['config_address'], port=configuration['config_port'], 
                        multiple_instance=configuration['config_multiple_instance'], 
                        enable_file_cache=configuration['config_enable_file_cache'],
                        start_browser=configuration['config_start_browser'])
