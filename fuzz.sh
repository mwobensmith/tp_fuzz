#!/bin/bash
echo
echo Start...
echo  
echo
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

NUM_ITERATIONS=2000
# needs error check here... if fail, abort run
python $DIR'/shavar_server.py' &

# TODO: save process ID for python and kill later

kill_firefox()
{
	temp=$( ps -A | grep -m1 'Nightly' )
	FX1=$(echo $temp | awk '{print $1}' )
	FX2=$(echo ${temp#*pipe.} | cut -f1,1 -d " ")
	process=$((FX1))
	nightly=$((FX2))
	kill $nightly
	kill $process
}

run()
{
	open $DIR'/fuzz_profile_clean.zip' 
	sleep 5
	echo Launching Firefox...
	cd /Applications/Nightly.app/Contents/MacOS
	./firefox -profile $DIR'/fuzz_shavar' &
	sleep 7

	kill_firefox
	rm -rf $DIR'/fuzz_shavar'
	sleep 5
}

for i in {1..$NUM_ITERATIONS}
do
	run
done