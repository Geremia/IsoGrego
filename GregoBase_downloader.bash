#!/usr/bin/bash

# Download GregoBase GABCs

max_id=${1:?Max GregoBase ID}

rm -f lower_triangular.npz

parallel --bar "curl -s -o GABCs/{}.gabc 'https://gregobase.selapa.net/download.php?id='{}'&format=gabc&elem=1' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'Sec-Fetch-Dest: document' -H 'Sec-Fetch-Mode: navigate' -H 'Sec-Fetch-Site: none'" ::: `seq $max_id`

echo $max_id > max_id.txt
