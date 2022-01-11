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

from wye.artist import Artist, _Queue
from wye.style import style

_parser = argparse.ArgumentParser(allow_abbrev=False)
_parser.add_argument('--marker', type=str, nargs="*", default=style['markers'])
_parser.add_argument('--alpha', type=float, nargs='+', default=style['alpha'])
_parser.add_argument('--x', type=int, nargs=1, default=None, help='Defaults to [0, 1, 2, ...]')



class Scatter(Artist):
    
    def __init__(self, ax, args):
        super().__init__(ax, args, 'y')
        
        
        args, unparsed = _parser.parse_known_args(args)
        self.args = argparse.Namespace(**vars(self.args), **vars(args))
        
        self.x = _Queue(self.args.last)
        
        self.line = dict()
        for field, linestyle, color, alpha, marker in zip(
            self.data,
            cycle(self.args.linestyle),
            cycle(self.args.color),
            cycle(self.args.alpha),
            cycle(self.args.marker),
            ):
            self.line[field],=ax.plot([0],[0], linestyle=linestyle, label=field, color=color, alpha=alpha, marker=marker)
        
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


