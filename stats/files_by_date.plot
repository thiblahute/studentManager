set terminal png transparent
set size 0.5,0.5

set output 'files_by_date.png'
unset key
set xdata time
set timefmt "%Y-%m-%d"
set format x "%Y-%m-%d"
set ylabel "Files"
set xtics rotate by 90
set bmargin 6
plot 'files_by_date.dat' using 1:2 w steps
