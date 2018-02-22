
from flask import Flask, request
app = Flask(__name__)

@app.route("/crawl_results")
def crawl_results():
    if request.method == "POST":
        # crawl.post_results()
        print(request)
    return "Hello World!"


def main():
    return True

if __name__ == '__main__':
    main()