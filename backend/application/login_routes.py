from flask import current_app as app, Response, request

@app.route('/login', methods=['POST'])
def login():
    return 'success'


@app.route('/register', methods=['POST'])
def register():


@app.route('/logout', methods=['POST'])
def logout():
