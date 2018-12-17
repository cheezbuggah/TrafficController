#!/usr/bin/env python
"""This is the controller entry point."""

import asyncio
import argparse
import os
import json
import websockets

from Scripts.controller import logging
from Scripts.controller.controller import Controller
from Resources.algorithms.manager import Manager

algorithm_manager = Manager()
parser = argparse.ArgumentParser()
parser.add_argument(
	"--log-level",
	help="level of logging to do",
	choices=logging.Log_levels.keys()
)
parser.add_argument(
	"--algorithm",
	help='algorithm to use',
	choices=algorithm_manager.get_algorithm_names()
)
parser.add_argument(
	"--port",
	help="port to host the controller on. Defaults to 5678",
	type=int
)
parser.add_argument(
	"--hostname",
	help="host name. Defaults to 'localhost'"
)
parser.add_argument(
	"--log-to-console",
	help='whether logging should also be available in the console',
	action='store_true'
)

args = parser.parse_args()

if args.log_level is None:
	args.log_level = 'DEBUG'

if args.log_to_console is None:
	args.log_to_console = True

if args.algorithm is None:
	args.algorithm = 'Heuristic'

logging.setup_loggers(args.log_level)
logger = logging.get_logger('script')

if not args.port:
	args.port = os.environ.get('CONTROLLER_PORT', 5678)

logger.debug('Set port to %s', args.port)

#141.252.224.63
if not args.hostname:
	args.hostname = os.environ.get('CONTROLLER_HOST_NAME', '141.252.224.63')

logger.debug('Set hostname to %s', args.hostname)

# Process init
controller = Controller(logging.get_logger('controller'))
controller.prepare_floor_plan()
controller.set_algorithm(algorithm_manager.get_algorithm(args.algorithm))


async def process_message(websocket, path):
	async for message in websocket:
		logger.info('Received message: %s', message)
		if type(message) is str:
			data = json.loads(message)
		else:
			data = json.loads(message.decode('utf-8'))

		if type(data) is dict:
			if 'quit' in data:
				await websocket.send("quit", "Acknowledged")
				quit()

		for item in data:
			#Ignore echo'd data
			if type(item) is dict:
				return
			controller.queue_traffic(item.upper())


async def process_floor_plan(websocket, path):
	while True:
		controller.calculate_floor_plan()

		response = list(controller.get_floor_plan())

		# Set Allow_nan to False to ensure strict JSON standard compatibility
		response = json.dumps(response, allow_nan=False)
		await websocket.send(response)

		# Sleep for 100 milliseconds. 60 FPS would be 166 and 2/3.
		await asyncio.sleep(1)


async def handler(websocket, path):
	message_processor_task = asyncio.ensure_future(process_message(websocket, path))
	floorplan_handler_task = asyncio.ensure_future(process_floor_plan(websocket, path))

	done, pending = await asyncio.wait(
		[message_processor_task, floorplan_handler_task],
		return_when=asyncio.FIRST_COMPLETED
	)

	for task in pending:
		task.cancel()

start_server = websockets.serve(handler, args.hostname, args.port)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
