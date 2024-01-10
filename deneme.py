# integrate html with flask
# http get and post

'''
jinja2 template engine
{{ xxx }}
{% xxx %} for and conditions
    {% if  result >= 50 %}
    <h1>Passed</h1>
    {% else %}
    <h1>Failed</h1>
    {% endif %}

    {% for key, value in result.items() %}
        <h1>{{key}}: {{value}}</h1>
    {% endfor %}
{# xxx #} for comments
'''

from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)


@app.route("/")
def welcome():
    return render_template("main.html")

# result checker html page


@app.route("/submit", methods=["POST", "GET"])
def submit():
    total_score = 0
    if request.method == "POST":
        science = float(request.form["science"])
        math = float(request.form["math"])
        history = float(request.form["history"])
        physics = float(request.form["physics"])
        total_score_avg = (science + math + history + physics) / 4

    res = ""
    if total_score_avg >= 50:
        res = "success"
    else:
        res = "fail"

    return redirect(url_for(res, score=total_score_avg))

# build url dynamically


@app.route("/success/<int:score>")
def success(score):
    if score < 50:
        return redirect(url_for("fail", score=score))
    # return f"Your score is {score} and you have passed."
    return "<html><body><h1>Your score is {score} and you have passed.</h1></body></html>".format(score=score)


@app.route("/fail/<int:score>")
def fail(score):
    if score > 50:
        return redirect(url_for("success", score=score))
    return f"Your score is {score} and you have failed."


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8080)
