import os
import json
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def scrollytelling():
    # Define the path to sections.json
    data_dir = os.path.join(app.root_path, 'data')
    sections_file = os.path.join(data_dir, 'sections.json')

    # Load sections.json
    with open(sections_file, 'r', encoding='utf-8') as f:
        sections = json.load(f)
    return render_template('scrollytelling.html', sections=sections)

if __name__ == '__main__':
    app.run(debug=True)
