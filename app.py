from flask import Flask, Response, request
import json
from Game import Game
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

game = Game()
counter = 0
def increment(amount):
    global counter
    counter += amount
    return counter

def get_state():
    global counter
    return {'counter': counter}

@app.route("/")
def index():
    global counter
    return '''
        <div id="score">%d</div>
        <script>
            function updateScore(n) {
                document.getElementById("score").innerHTML = n * 1000
            }

            function increment(amount) {
                fetch('/api/score/increment/' + amount)
                .then(response => response.json())
                .then(data => updateScore(data.counter));
            }

            function increment2(amount) {
                fetch('/api/bump', {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'    
                    },
                    method: 'POST',
                    body: 'amount=' + amount
                })
                .then(
                    data => data.text()
                )
                .then(text => updateScore(parseInt(text)));
            }
        </script>

        <button onclick="increment(5)">Click me!</button>
        <button onclick="increment2(5)">Click me!2</button>
    ''' % counter

@app.route("/hello")
def hello_world():
    return '''
        <p>Hello, <b>World!!!</b></p>
        <script>
            fetch('/api')
            .then(response => response.json())
            .then(data => alert(data[0].name));

            /* var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                // Typical action to be performed when the document is ready:
                // document.getElementById("demo").innerHTML = xhttp.responseText;
                    var data = JSON.parse(xhttp.responseText);
                    alert(data[0].name)
                }
            };
            xhttp.open("GET", "/api", true);
            xhttp.send(); */
        </script>
    '''

@app.route("/api")
def api():
    return Response('[{"name": "Conan"}]', mimetype='text/json')

@app.route("/api/score/increment/<amount>")
def api_increment(amount):
    increment(int(amount))
    return Response(json.dumps(get_state()), mimetype='text/json')

@app.route("/api/bump", methods=["POST", "GET"])
def api_bump():
    c = increment(int(request.form.get("amount")))
    return str(c)

@app.route("/api/command", methods=["POST", "GET"])
@cross_origin()
def api_command():
    text = game.command(request.form.get("command"))
    return text