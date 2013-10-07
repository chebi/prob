# gnuplot script to plot the results

# how to produce berlin.png using google static API.e.g:
#http://maps.googleapis.com/maps/api/staticmap?center=52.516288,13.377689&zoom=11&size=2000x2000&key=...&sensor=false&path=color:0x0000ff80|weight:1|52.437385,13.553989|52.590117,13.39915&markers=color:blue|label:W|52.529198,13.274099

set size square
set view map
set contour
unset surface
set autoscale fix
set palette defined (0 "blue", 0.5 "red")
unset colorbox
set isosamples 1000,1000
set term pdf
set output "map.pdf"
set xrange [13.274099:13.553989]
set yrange [52.437385:52.590117]
set multiplot
set cntrparam levels incremental 0,0.03,0.5
splot "berlin.png" binary filetype=png dx=0.000171922604423 dy=0.000104467852257 origin=(13.274099,52.437385,0) format='%uchar%uchar%uchar' with rgbimage notitle
set cbrange [0.0:0.5]
set colorbox
splot "4gnuplot.txt" matrix using (13.274099 + 0.0027989 * $1):(52.437385 + 0.00152732 * $2):3 w pm3d palette notitle
set dgrid3d
unset contour
set surface
splot "<echo '13.49801075 52.48931392 0'" with points pt 7 ps 0.3 notitle
unset multiplot
