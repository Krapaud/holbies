from flask import Flask, render_template

app = Flask(__name__)

@app.route('/badge/<int:progress>')
def badge(progress):
    return render_template('badges.html', progress=progress)

if __name__ == '__main__':
    app.run(debug=True)
