# wye
Tee but make graphs

Sometimes it is useful to pipe data from one command-line utility to another.  [tee][`tee`] allows you to send data down a pipe but also save a copy to a file.  `wye`, also named after a plumbing fitting, acts like `tee` but creates a visualization of data.

In other words, if you have a pipeline like `produce_data | process_data` you can do something like
```
> produce_data | wye scatter | process_data | wye histogram
```
to see a scatter plot of the produced data and a histogram of the processed data.

By default the figures are opened as interactive [mpl][`matplotlib`] figures.  You can supprress the interactive figure with the `--no-show` option, in which case you probably also want the `--save <filename>` option.

Data is read line-by-line and split into fields according to the `--delimiter` (which defaults to whitespace).

# Artists

`wye` alone doesn't do anything; you need to specify a subcommand that specifies an artist.

Currently, `wye` has three artists,
 - `scatter`   which plots traces of data; the x-axis defaults to the line number, but a field for a common x-axis can be set with `--x`.
 - `histogram` which bins data into histograms
 - `mc`        which is useful for understanding Markov Chain / Monte Carlo data.

Each artist accepts a variety of options, allowing you to cycle `--color`s, draw `--hline`s or a `--vspan`, put a `--title` or axes labels, for example.  Some options are artist-specific, such as `--bin` (unused by `scatter`).

You can see examples by running `./examples/<artist>.sh`.


[mpl]:	https://matplotlib.org/
[tee]:	https://www.gnu.org/software/coreutils/manual/html_node/tee-invocation.html
