Server
	pip3 install -r .\app\requirements.txt
	python3 -m app

	OpenAPI docs:
	http://localhost:8080/docs#/

←[32mINFO←[0m:     Started server process [←[36m3488←[0m]
←[32mINFO←[0m:     Waiting for application startup.
←[32mINFO←[0m:     Application startup complete.
←[32mINFO←[0m:     Uvicorn running on ←[1mhttp://0.0.0.0:8080←[0m (Press CTRL+C to quit)
←[32mINFO←[0m:     Shutting down
←[32mINFO←[0m:     Waiting for application shutdown.
←[32mINFO←[0m:     Application shutdown complete.
←[32mINFO←[0m:     Finished server process [←[36m3488←[0m]

Client:
	pip3 install -r .\client\requirements.txt
	python3 client\client.py -h

usage: client.py [-h] [--host HOST] [--port PORT] [--command COMMAND] [--kind KIND] [--data DATA] [--task TASK] [--mode MODE]

options:
  -h, --help         show this help message and exit
  --host HOST        Server host (default: localhost)
  --port PORT        Server port (default: 8080)
  --command COMMAND  Command to execute: 'create' - create new task, 'status' - get task status, 'result' - get task result
  --kind KIND        New task kind: 1-reverse, 2-swap, 3-repeat
  --data DATA        New task data
  --task TASK        Task ID
  --mode MODE        Execution mode: 'simple' - execute single command, 'package' - create task and waiting completion

Examples:

## run in package mode ##

python3 client\client.py --mode package --kind 3 --data abcdefg
Task created: 8
Task status: Processing
Task status: Processing
Task status: Processing
Task status: Complete
Task result: abbcccddddeeeeeffffffggggggg


## create task ##

python3  client\client.py --command create --kind 1 --data abcdefg
Task created: 9


## get task status ##

python3  client\client.py --command status --task 1
Task status: Complete


## get task result ##

python3  client\client.py --command result --task 1
Task result: allerbmu
