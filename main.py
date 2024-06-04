from flask import Flask, request, render_template
from lexer_parser import analyze_code

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    lexical_analysis = syntactic_analysis = code = None
    if request.method == 'POST':
        code = request.form.get('code')
        file = request.files.get('file')
        if file:
            code = file.read().decode('utf-8')

        lexical_analysis, syntactic_analysis = analyze_code(code)

    return render_template('index.html', code=code, lexical_analysis=lexical_analysis,
                           syntactic_analysis=syntactic_analysis)


if __name__ == '__main__':
    app.run(debug=True)
