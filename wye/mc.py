#   wye
#   tee, but produces graphs via matplotlib
#   Copyright (C) 2021 Evan Berkowitz
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
from itertools import cycle

from wye.scatter import Scatter
from wye.histogram import Histogram

class MC:
    def _register(subparsers, parents=[]):
        parser = subparsers.add_parser('mc', 
            parents=parents,
            description='''Properties get cycled together.

''',
            epilog='''wye Copyright (C) 2021 Evan Berkowitz.
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it under the GPLv3 or any later version.
''')
        MC._parser_setup(parser)

    def _parser_setup(parser):
        Scatter._parser_setup(parser)
        Histogram._parser_setup(parser, False)
        
    def __init__(self, ax, args):
        
        self.scatter   = Scatter(ax[0], args)
        
        args.title=''
        args.field = self.scatter.data.keys()
        args.orientation = 'horizontal'
        if args.normalize:
            args.xlabel="probability"
        else:
            args.xlabel="#"
        self.histogram = Histogram(ax[1], args)
        # Share the data!
        self.histogram.data = self.scatter.data
        
    def update_data(self, i, fields):
        self.scatter.update_data(i, fields)
        # histogram data is updated becaause the .data is shared.
    
    def update_figure(self, ):
        self.scatter.update_figure()
        self.histogram.update_figure()

    def clear_data(self):
        self.scatter.clear_data()
        # histogram data is cleared because the data is shared.
