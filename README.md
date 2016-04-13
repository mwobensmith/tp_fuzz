# tp_fuzz
Fuzzing the shavar protocol in the Firefox client. 

Currently Mac only.

To run:
* Have latest Firefox installed. 
* Quit all open instances of Firefox (important).
* Launch shavar_server.py, which opens a server on port 13000.
* Launch fuzz.sh, which automatically opens and closes Firefox.

What it does:
* Each time Fx opens, a new, clean profile is created. 
* When Fx connects to the locally-running server on port 13000, a dump of the response is printed to the console.
* After the client receives the shavar response, it is shut down.
* Script defauls to 2000 iterations and this quantity can be modified.

To be improved:
* The shavar service as used in Fx (for tracking protection) actually hits two endpoints. This script only satisfies the first endpoint, and sends back a malformed shavar response. It could be modified to serve a legitimate response instead - which includes the location of the second endpoint - and decide to send malformed data from the second endpoint instead.
* There is logic to automatically find the current Fx process and kill it with each test. The logic is fragile.
* There is no logic to kill the server running on port 13000 after it is opened. You may need to do this manually.
