set terminal png transparent
set size 0.5,0.5

set output 'hour_of_day.png'
unset key
set xrange [0.5:24.5]
set xtics 4
set ylabel "Commits"
plot 'hour_of_day.dat' using 1:2:(0.5) w boxes fs solid
