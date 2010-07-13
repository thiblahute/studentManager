set terminal png transparent
set size 0.5,0.5

set output 'commits_by_year.png'
unset key
set xtics 1
set ylabel "Commits"
set yrange [0:]
plot 'commits_by_year.dat' using 1:2:(0.5) w boxes fs solid
