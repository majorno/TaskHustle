import asyncio
import argparse

import aiohttp

SERVICE_HOST = 'localhost'
SERVICE_PORT = 8080


class TaskApiClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def url(self, path):
        return 'http://{}:{}/{}'.format(self.host, self.port, path)

    async def create_task(self, kind: int, data: str) -> int:
        path = 'tasks/'
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url(path), json={'kind': kind, 'data': data}) as resp:
                json_response = await resp.json()

                if 'id' in json_response:
                    return json_response['id']
                else:
                    raise Exception('Invalid server response')

    async def get_task_status(self, task_id: int) -> str:
        path = 'tasks/{}/status'.format(task_id)
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url(path)) as resp:
                if resp.status == 200:
                    json_response = await resp.json()
                    if 'status' in json_response:
                        return json_response['status']
                elif resp.status == 404:
                    json_response = await resp.json()
                    if 'detail' in json_response:
                        raise Exception(json_response['detail'])

                raise Exception('Invalid server response: {}'.format(resp.reason))

    async def get_task_result(self, task_id: int) -> str:
        path = 'tasks/{}/result'.format(task_id)
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url(path)) as resp:
                if resp.status == 200:
                    json_response = await resp.json()
                    if 'result' in json_response:
                        return json_response['result']
                elif resp.status == 404:
                    json_response = await resp.json()
                    if 'detail' in json_response:
                        raise Exception(json_response['detail'])

                raise Exception('Invalid server response: {}'.format(resp.reason))


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default=SERVICE_HOST, help='Server host (default: {})'.format(SERVICE_HOST))
    parser.add_argument('--port', type=int, default=SERVICE_PORT, help='Server port (default: {})'.format(SERVICE_PORT))
    parser.add_argument('--command', type=str, help=f"Command to execute: 'create' - create new task, "
                                                    f"'status' - get task status, "
                                                    f"'result' - get task result")
    parser.add_argument('--kind', type=int, help='New task kind: 1-reverse, 2-swap, 3-repeat')
    parser.add_argument('--data', type=str, help='New task data')
    parser.add_argument('--task', type=int, help='Task ID')
    parser.add_argument('--mode', type=str, default='simple',
                        help=f"Execution mode: 'simple' - execute single command, "
                             f"'package' - create task and waiting completion")
    args = parser.parse_args()

    if args.mode == 'package':
        if not args.kind:
            print('Missing options: --kind')
            return

        if not args.data:
            print('Missing options: --data')
            return

        # ex: --mode package --kind 3 --data abcdefg
        try:
            client = TaskApiClient(host=args.host, port=args.port)
            task_id = await client.create_task(args.kind, args.data)
            print('Task created: {}'.format(task_id))

            while True:
                status = await client.get_task_status(task_id)
                print('Task status: {}'.format(status))

                if status == 'Complete':
                    break

            result = await client.get_task_result(task_id)
            print('Task result: {}'.format(result))

        except asyncio.CancelledError:
            print('Interrupted')

        return

    if not args.command:
        print('Missing options: --command')
        return

    if args.command == 'create':
        if not args.kind:
            print('Missing options: --kind')
            return

        if not args.data:
            print('Missing options: --data')
            return

        # ex: --command create --kind 1 --data abcdefg
        client = TaskApiClient(host=args.host, port=args.port)
        task_id = await client.create_task(args.kind, args.data)
        print('Task created: {}'.format(task_id))

    if args.command == 'status':
        if not args.task:
            print('Missing options: --task')
            return

        # ex: --command status --task 1
        client = TaskApiClient(host=args.host, port=args.port)
        status = await client.get_task_status(args.task)
        print('Task status: {}'.format(status))

    if args.command == 'result':
        if not args.task:
            print('Missing options: --task')
            return

        # ex: --command result --task 1
        client = TaskApiClient(host=args.host, port=args.port)
        result = await client.get_task_result(args.task)
        print('Task result: {}'.format(result))


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
