#!/bin/bash

start_day=42
end_day=45
start_q=83

for (( day=start_day; day<=end_day; day++ )); do
    # Check if the directory already exists
    if [ -d "day$day" ]; then
        # Calculate the two question numbers for the current day
        q1=$(( start_q + (day - start_day) * 2 ))
        q2=$(( q1 + 1 ))
        
        # Create the two C files inside the existing directory
        touch "day$day/day$day-$q1.c"
        touch "day$day/day$day-$q2.c"
        
        echo "Added files to day$day: day$day-$q1.c and day$day-$q2.c"
    else
        echo "Folder day$day not found, skipping..."
    fi
done