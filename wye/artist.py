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
from matplotlib.scale import get_scale_names
from wye.style import style

class _Queue:
    
    def __init__(self, maxSize=float('Inf')):
        self.data=[]
        self.maxSize = maxSize
        if self.maxSize <= 0:
            self.maxSize = float('Inf')
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, key):
        return self.data[key]
    
    def put(self, item):
        self.data.append(item)
        if(len(self.data) > self.maxSize):
            self.data = self.data[-self.maxSize:]
    
    append = put
    
    def __iter__(self):
        return self.data.__iter__()

        


class Artist:
    def _parser_setup(parser, data):
        parser.add_argument(f'--{data}', type=int, nargs='+', default=[0], help="zero-indexed awk-style field index")
        parser.add_argument(f'--name',   type=str, nargs='+', default=[''])
        parser.add_argument('--color', type=str, nargs='+', default=style['colors'], help=f'Defaults to {style["colors"]}.  See https://matplotlib.org/stable/gallery/color/named_colors.html for a list of named colors.')
        parser.add_argument('--alpha', type=float, nargs='+', default=style['alpha'], help=f'Truncated to between 0 and 1.  If {data} is one field, defaults to 1.  Otherwise defaults to 0.125 + 0.5**(number of {data} - 1)')
        parser.add_argument('--linestyle', type=str, nargs='*', choices=['solid', 'dotted', 'dashed', 'dashdot'], default=[style['linestyle']])
        
        parser.add_argument('--xscale', choices=['linear'] + [s for s in  get_scale_names() if 'function' not in s and s != 'linear'], default='linear')
        parser.add_argument('--yscale', choices=['linear'] + [s for s in  get_scale_names() if 'function' not in s and s != 'linear'], default='linear')
        
        parser.add_argument('--xlabel', type=str, default='')
        parser.add_argument('--ylabel', type=str, default='')
        parser.add_argument('--title', type=str, default='')
        
        parser.add_argument('--hline', type=float, nargs='*', default=[])
        parser.add_argument('--hspan', type=float, nargs=2, help="low high")
        parser.add_argument('--vline', type=float, nargs='*', default=[])
        parser.add_argument('--vspan', type=float, nargs=2, help="low high")
        
        parser.add_argument('--last',  type=int, default=0, help="Only retain the LAST most recent rows.")

    def _default_alpha(self):
        if self.args.alpha == style['alpha']:
            if len(self.data) == 1:
                self.alpha=style['alpha']
            else:
                self.alpha = [0.125 + 0.5**(len(self.data) - 1)]
        else:
            self.alpha=self.args.alpha
        self.alpha = [ 0 if a < 0 else a for a in self.alpha ]
        self.alpha = [ 1 if a > 1 else a for a in self.alpha ]
    
    def __init__(self, ax, args, data):
        self.ax = ax
        self.args = args
        
        ax.set_xscale(self.args.xscale)
        ax.set_yscale(self.args.yscale)
        ax.set_xlabel(self.args.xlabel)
        ax.set_ylabel(self.args.ylabel)
        ax.set_title(self.args.title)
        
        for h in self.args.hline:
            self.ax.axhline(h, color='black')
        for v in self.args.vline:
            self.ax.axvline(v, color='black')
        if self.args.hspan:
            self.ax.axhspan(self.args.hspan[0], self.args.hspan[1], color='gray', alpha=0.25)
        if self.args.vspan:
            ax.axvspan(self.args.vspan[0], self.args.vspan[1], color='gray', alpha=0.25)
        
        self.data = {label: _Queue(self.args.last) for label in vars(self.args)[data]}
        self._default_alpha()
    
    def update_data(self, i, fields):
        for f in self.data:
            self.data[f].append(float(fields[f]))
    
    def update_figure(self, ):
        self.ax.relim()
        self.ax.autoscale_view()
    
    def clear_data(self, ):
        for f in self.data:
            self.data[f] = _Queue(self.args.last)
        self.x = []

