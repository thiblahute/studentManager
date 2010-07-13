set terminal png transparent
set size 0.5,0.5

set output 'month_of_year.png'
unset key
set xrange [0.5:12.5]
set xtics 1
set ylabel "Commits"
plot 'month_of_year.dat' using 1:2:(0.5) w boxes fs solid
