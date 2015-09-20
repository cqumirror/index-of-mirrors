from actor import app
from flask import request, redirect


# Handle static files for debug
@app.before_request
def add_static():
    if not app.debug:
        return
    path = request.path
    if path == "/":
        return redirect("/static/index.html")


def main():
    app.run(host="0.0.0.0", debug=True)


if __name__ == '__main__':
    main()
