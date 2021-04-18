#!/bin/bash
###################### ERROR MESSAGES ##############################
if [ "$#" -ne 1 ]; then
	echo 'Error: No log file given.'
	echo 'Usage: ./webmetrics.sh <logfile>'
	exit 1
fi

if [ ! -f "$1" ]; then
	echo "Error: File '"$1"' does not exist."
	echo 'Usage: ./webmetrics.sh <logfile>'
	exit 2
fi

###################### BROWSER REQUESTS #############################

echo 'Number of requests per web browser'

input=$1
count_Safari=$(grep -o 'Safari' "$input" | wc -l)
count_Firefox=$(grep -o 'Firefox' "$input" | wc -l)
count_Chrome=$(grep -o 'Chrome' "$input" | wc -l)

echo 'Safari,'"$count_Safari"
echo 'Firefox,'"$count_Firefox"
echo 'Chrome,'"$count_Chrome"

###################### DISTINCT USERS ###############################

echo ''
echo 'Number of distinct users per day'

date_time=$(awk '/[0-9]{2}\/[A-Z][a-z]{2}\/[0-9]{4}/' < "$input" | sed 's/].*/]/')

dates=$(echo "$date_time" | sed -e 's/.*\[//' -e 's/:.*$//' | sort -u)

while IFS= read -r line; do
    requests=$(echo "$date_time" | grep "$line" | sed 's/ .*//')
    request_count=$(echo "$requests" | sort -u | wc -l)
    echo  $line','"$request_count"
done <<< "$dates"


###################### POPULAR REQUESTS #############################

echo ''
echo 'Top 20 popular product requests'

requestID=$(awk '/GET \/product\/[0-9]/' < "$input")
requests=$(echo "$requestID" | sed -e 's/.*GET \/product\///' -e 's/\/.*//' -e '/.*[^0-9].*/d')
request_count=$(echo "$requests" | sort | uniq -c | sort -bnr)

echo "$request_count" | awk '{s=$1;$1=$NF;$NF=s}1' | sed 's/ /,/' | sort -t, -k2,2nr -k1,1nr | head -20

echo ''

exit 0
