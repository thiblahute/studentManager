set terminal png transparent
set size 0.5,0.5

set output 'lines_of_code.png'
unset key
set xdata time
set timefmt "%s"
set format x "%Y-%m-%d"
set ylabel "Lines"
set xtics rotate by 90
set bmargin 6
plot 'lines_of_code.dat' using 1:2 w lines
