from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from gpt_util import GptService

prompt = '''
You are given an instruction within <INSTRUCTION> tags in POLISH language that describes where to fly a drone. 
Based on this instruction you need to move the drone to the correct square on a map and say what this square contains (in POLISH language).

MAP is a square divided into 16 smaller squares, 4 by 4. Let's assign numbers, starting from 1, to each square, left to right, top to bottom.
So to summarize: 
a) top-left square is 1, top-right is 4, bottom-left is 13, and bottom-right is 16
b) top row contains squares 1,2,3,4 and bottom row contains squares 13,14,15,16
c) left column contains squares 1,5,9,13 (from top to bottom)
d) right column contains squares 4,8,12,16 (from top to bottom)

WHAT EACH SQUARE CONTAINS:
1 - STARTING POINT, you always start from here
2 - grass
3 - one tree
4 - house
5 - grass
6 - mill
7 - grass
8 - grass
9 - grass
10 - grass
11 - rocks
12 - two trees
13 - mountains
14 - mountains
15 - car
16 - cave

IMPORTANT: instruction might not be a simple set of single steps from one square to another, in one command it may tell you to move multiple squares, so analyze thoroughly what is said! 
Especially when e.g. you're told to move to the very bottom (you should move as far down as possible, not just one square) or to move maximally to the left (you should move to the left most square, not just one step to the left)

<INSTRUCTION>
{instruction}
</INSTRUCTION>

Return an answer in a following JSON format:
{{
    "_thoughts": "think out loud about the instruction, apply it as faithfully as possible to the map, stick to the map description, think where you end up after following each command from the instruction"
    "_verification": "based on the map and the given instruction analyze if your _thoughts are correct, verify if you ended up on the right square"
    "description": "very short (1 or 2 words) description of what's in the square you ended up on (IN POLISH)"
}}
'''

class MyRequestHandler(BaseHTTPRequestHandler):
    gpt = GptService()

    def do_POST(self):
        print('POST request')
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
            print(f'received data: {data}')
            received_instruction = data['instruction']

            response = self.gpt.user_completion_json(prompt.format(instruction=received_instruction))
            print(f'gpt response: {response}')

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(response).encode('utf-8'))

        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {"error": "Invalid JSON format"}
            self.wfile.write(json.dumps(response).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=MyRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'server listening on port {port}...')
    httpd.serve_forever()


if __name__ == "__main__":
    run()