

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/singup', methods=['GET', 'POST'])
def singup():
    """User registration route."""
    def validate_reg():
        """""
        validate that the username or email does not in the database 
        """""
        nonlocal msg
        email = User.query.filter_by(email=form.email.data).first()
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            msg += 'Username already exists.\n'
        if email:
            msg += 'Email already exists.\n'


    if current_user.is_authenticated:
        # if user is logged in we get out of here
        return redirect(url_for('index'))

    form = SingupForm()
    if form.validate_on_submit():
        msg = ''
        validate_reg()
        if len(msg) > 0:
            flash(msg)
            return redirect(url_for('singup'))
        # add new user to the database
        user = User(username=form.username.data, password=form.password.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()

        # redirect to the two-factor auth page, passing username in session
        session['username'] = user.username
        return redirect(url_for('two_factor_setup'))
    return render_template('singup.html', form=form)


@app.route('/twofactor')
def two_factor_setup():
    if 'username' not in session:
        return redirect(url_for('index'))
    user = User.query.filter_by(username=session['username']).first()
    if not user :
        return redirect(url_for('index'))
    # since this page contains the sensitive qrcode, make sure the browser
    # does not cache it
    return render_template('2FA_reg.html'), 200, {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@app.route('/qrcode')
def qrcode():
    if 'username' not in session:
        abort(404)
    user = User.query.filter_by(username=session['username']).first()
    if not user:
        abort(404)

    # for added security, remove username from session
    del session['username']

    # render qrcode for FreeTOTP
    url = pyqrcode.create(user.get_otp_uri())
    stream = BytesIO()
    url.svg(stream, scale=3)
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""

    def login_verify():
        msg = ''
        if not user:
            msg += 'Wrong username'
        if not user.verify_password(form.password.data):
            msg += 'Wrong password'
        if len(msg) > 0:
            flash(msg)
            return redirect(url_for('login'))

    if current_user.is_authenticated:
        # if user is logged in we get out of here
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_verify()
        session['username'] = user.username ; session['type'] = 'login'
        return redirect(url_for('two_factor_token'))
    return render_template('login.html', form=form)