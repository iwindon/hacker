from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

files = ['file1.txt', 'file2.txt', 'servers.txt']
servers = ['192.168.1.1', '192.168.1.2', '192.168.1.3']
valid_server = '192.168.1.2'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/command', methods=['POST'])
def command():
    command = request.json.get('command')
    response = handle_command(command)
    return jsonify(response=response)

def handle_command(command):
    if command == 'ls':
        return '\n'.join(files)
    elif command == 'cat servers.txt':
        return '\n'.join(servers)
    elif command.startswith('ping '):
        ip = command.split(' ')[1]
        if ip == valid_server:
            response = [f'PING {ip} (56 bytes of data)']
            for i in range(1, 6):
                response.append(f'64 bytes from {ip}: icmp_seq={i} ttl=64 time=0.123 ms')
            return '\n'.join(response)
        else:
            response = [f'PING {ip} (56 bytes of data)']
            for i in range(1, 6):
                response.append(f'Request timeout for icmp_seq {i}')
            return '\n'.join(response)
    elif command.startswith('ssh '):
        ip = command.split(' ')[1]
        if ip == valid_server:
            return 'redirect:/login'
        else:
            return f'ssh: connect to host {ip} port 22: Connection refused'
    else:
        return f'{command}: command not found'

if __name__ == '__main__':
    app.run(debug=True)
