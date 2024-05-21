import os
import sys

import sys
sys.path.append('../AntiBot-Desktop')

from FileSystems.LoggingFilesInterface import LoggingFilesInterface

class LogReader:
    def __init__(self):
        self.log_interface = LoggingFilesInterface()

    def getData(self):
        data = self.log_interface.getLogData()
        result_string = '<style>p {color: red;}</style>'

        for curr_file in data.keys():
            result_string = result_string + f'<h1>{curr_file}</h1><br>'
            for line in data[curr_file]:
                split = line.split(',')
                split[0] = f'<span style="color:green">{split[0]}</span>'
                split[1] = f'<span style="color:Tomato">{split[1]}</span><br>'
                split[2] = f'<span>{split[2]}</span>'

                result_string = result_string + f'&ensp;{split[0]}-{split[1]}-{split[2]}<br>'

        return result_string