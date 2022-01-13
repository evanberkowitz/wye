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

from wye.artist import Artist
from wye.style import style

class Histogram(Artist):
    def _register(subparsers, parents=[]):
        parser = subparsers.add_parser('histogram', 
            parents=parents,
            description='''Properties get cycled together.

''',
            epilog='''wye Copyright (C) 2021 Evan Berkowitz.
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it under the GPLv3 or any later version.
''')
        Histogram._parser_setup(parser)
    
    def _parser_setup(parser, setup_Artist=True):
        if setup_Artist:
            Artist._parser_setup(parser, 'field')
        parser.add_argument('--bins', type=int, nargs='+', default=[21], help='Number of bins; Defaults to 21')
        parser.add_argument('--normalize', default=False, action='store_true')
        parser.add_argument('--orientation', type=str, choices=['vertical', 'horizontal'], default='vertical')
    
    def __init__(self, ax, args):
        super().__init__(ax, args, "field")
        
        self.hist= dict()
        for field, name, linestyle, color, alpha, in zip(
            self.data,
            cycle(self.args.name),
            cycle(self.args.linestyle),
            cycle(self.args.color),
            cycle(self.alpha),
            ):
            self.hist[field]=ax.hist([0], linestyle=linestyle, label=(name if name else field), color=color, alpha=alpha, orientation=self.args.orientation)
        
        self.ax.legend()
    
    def update_figure(self, ):
        for f, linestyle, color, alpha, bins in zip(
            self.data,
            cycle(self.args.linestyle),
            cycle(self.args.color),
            cycle(self.alpha),
            cycle(self.args.bins),
            ):
            _, _, bars = self.hist[f]
            [b.remove() for b in bars]
            self.hist[f]=self.ax.hist(self.data[f], bins=bins, linestyle=linestyle, label=f, color=color, alpha=alpha, density=self.args.normalize, orientation=self.args.orientation)
        super().update_figure()


