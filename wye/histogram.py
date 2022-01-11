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

_parser = argparse.ArgumentParser(allow_abbrev=False)
_parser.add_argument('--bins', type=int, nargs='+', default=[21])
_parser.add_argument('--alpha', type=float, default=None)
_parser.add_argument('--normalize', default=False, action='store_true')
_parser.add_argument('--orientation', type=str, default='vertical', help="vertical or horizontal")


class Histogram(Artist):
    
    def __init__(self, ax, args):
        super().__init__(ax, args, "field")
        
        
        args, unparsed = _parser.parse_known_args(args)
        self.args = argparse.Namespace(**vars(self.args), **vars(args))

        if args.alpha is None:
            if len(self.data) == 1:
                self.alpha=style['alpha'][0]
            else:
                self.alpha = 0.125 + 0.5**(len(self.data) - 1)
        else:
            self.alpha=self.args.alpha
        
        self.hist= dict()
        for field, linestyle, color, in zip(
            self.data,
            cycle(self.args.linestyle),
            cycle(self.args.color),
            ):
            self.hist[field]=ax.hist([0], linestyle=linestyle, label=field, color=color, alpha=self.alpha, orientation=self.args.orientation)
        
        self.ax.legend()

    def update_figure(self, ):
        for f, linestyle, color, bins in zip(
            self.data,
            cycle(self.args.linestyle),
            cycle(self.args.color),
            cycle(self.args.bins)
            ):
            _, _, bars = self.hist[f]
            [b.remove() for b in bars]
            self.hist[f]=self.ax.hist(self.data[f], bins=bins, linestyle=linestyle, label=f, color=color, alpha=self.alpha, density=self.args.normalize, orientation=self.args.orientation)
        super().update_figure()


