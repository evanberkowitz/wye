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

from matplotlib.lines import Line2D
from wye.artist import Artist, _Queue
from wye.style import style

class Scatter(Artist):
    def _register(subparsers, parents=[]):
        parser = subparsers.add_parser('scatter', 
            parents=parents,
            description='''Properties get cycled together.

''',
            epilog='''wye Copyright (C) 2021 Evan Berkowitz.
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it under the GPLv3 or any later version.
''')
        Scatter._parser_setup(parser)

    def _parser_setup(parser):
        Artist._parser_setup(parser, 'y')
        parser.add_argument('--x', type=int, nargs=1, default=None, help='Field to use for the common x-axis.  If unspecified, [0, 1, 2, ...]')
        parser.add_argument('--marker', type=str, nargs="*", default=style['markers'], help=f'Defaults to {style["markers"]}.  See https://matplotlib.org/stable/api/markers_api.html for a list of markers.')
        parser.add_argument('--markeredgecolor', type=str, nargs="*", default=['none'], help=f'Defaults to \'none\'')
        parser.add_argument('--markerfillstyle', choices=Line2D.fillStyles, default='full')

    def __init__(self, ax, args):
        super().__init__(ax, args, 'y')
        
        # Allow for the integer-indicated ticks and carets:
        self.args.marker = [int(m) if m in "11023456789" else m for m in self.args.marker]
        
        self.x = _Queue(self.args.last)
        
        self.line = dict()
        for field, name, linestyle, color, alpha, marker, markeredgecolor, in zip(
            self.data,
            cycle(self.args.name),
            cycle(self.args.linestyle),
            cycle(self.args.color),
            cycle(self.alpha),
            cycle(self.args.marker),
            cycle(self.args.markeredgecolor)
            ):
            self.line[field],=ax.plot([0],[0], linestyle=linestyle, label=(name if name else field), color=color, alpha=alpha, marker=marker, markeredgecolor=markeredgecolor)
        
        self.ax.legend()
    
    def update_data(self, i, fields):
        super().update_data(i, fields)
        if self.args.x is not None:
            self.x.append(float(fields[self.args.x]))
        else:
            self.x.append(i)
    
    def update_figure(self, ):
        for f in self.data:
            self.line[f].set_data(self.x,self.data[f])
        super().update_figure()


