# mini_survey Solution

The give site is vulnerable to Prototype Pollution. Data sent in the POST request of '/pollutionsurvey' can be used to pollute the child object with data requried to configure the socket connection in the code. The 'host' and 'port' values must pe polluted to the attacker's host and port to receive the flag.
