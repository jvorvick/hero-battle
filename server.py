from flask import Flask, Response
import json

app = Flask(__name__)

counter = 0
def increment(amount):
    global counter
    counter += amount

def get_state():
    global counter
    return {'counter': counter}

@app.route("/")
def index():
    return '''
        <div id="score">0</div>
        <script>
            function updateScore(n) {
                document.getElementById("score").innerHTML = n * 1000
            }

            function increment(amount) {
                fetch('/api/score/increment/' + amount)
                .then(response => response.json())
                .then(data => updateScore(data.counter));
            }
        </script>
        <button onclick="increment(5)">Click me!</button>
    '''

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