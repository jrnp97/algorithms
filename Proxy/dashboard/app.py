from flask import Flask, render_template

app = Flask(__name__)

app.config.from_pyfile('config.py')


@app.route("/")
def hello():
    info = dict({'status': 'ON',
                 'request_url': 'savio.utbvirtual.edu.co/',
                 'request_body': '<html>asdasd</html>',
                 'request_history': 'No information yet.'
                 })
    return render_template('index.html', **info)


if __name__ == "__main__":
    app.run()