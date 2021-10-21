from flask import Flask, render_template, redirect, url_for, request, session
import google_auth, socket, pymysql, os, math
from twilio import twilio_send_code, twilio_view_verification, twilio_verify_code
from coindesk import coindesk_get_BPI

app = Flask(__name__)
app.secret_key = 'mysecretkey'
app.register_blueprint(google_auth.app)

app.config['MYSQL_HOST'] = 'gator4004.hostgator.com'
app.config['MYSQL_USER'] = 'jrobles_agente'
app.config['MYSQL_DB'] = 'jrobles_agentebitcoin'
app.config['MYSQL_PASSWORD'] = 'bngN38a@'

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


def get_connection():
    if socket.gethostname() == "MacBook-Pro-de-Javier.local":
        return pymysql.connect(host=app.config["MYSQL_HOST"], user=app.config["MYSQL_USER"],
                               password=app.config["MYSQL_PASSWORD"], db=app.config["MYSQL_DB"],
                               charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
    else:
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        try:
            if os.environ.get('GAE_ENV') == 'standard':
                conn = pymysql.connect(user=db_user, password=db_password,
                                       unix_socket=unix_socket, db=db_name,
                                       cursorclass=pymysql.cursors.DictCursor
                                       )
        except pymysql.MySQLError as e:
            print(e)
        return conn


def get_trust_level(connection, user_data):
    email = user_data.get('email')
    given_name = user_data.get('given_name')
    family_name = user_data.get('family_name')
    google_id = user_data.get('id')
    cur = connection.cursor()
    cur.execute(
        'select user_id, trust_level, verified_telephone, verified_document, verified_address from ab_user where google_id=%s',
        google_id)
    data = cur.fetchone()
    if data == None:
        sql = 'insert into ab_user(email, given_name, family_name, google_id) values (%s, %s, %s, %s)'
        val = (email, given_name, family_name, google_id)
        cur.execute(sql, val)
        connection.commit()
        session['user_id'] = cur.lastrowid
        session['trust_level'] = 0
        session['verified_telephone'] = 0
        session['verified_document'] = 0
        session['verified_address'] = 0
    else:
        session['user_id'] = data["user_id"]
        session['trust_level'] = data["trust_level"]
        session['verified_telephone'] = data["verified_telephone"]
        session['verified_document'] = data["verified_document"]
        session['verified_address'] = data["verified_address"]
    cur.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/member')
@google_auth.no_cache
def member():
    if google_auth.is_logged_in():
        user = google_auth.get_user_info()
        connection = get_connection()
        get_trust_level(connection, user)
        connection.close()
        if session['trust_level'] == 0:
            return redirect(url_for('account'))
        else:
            return redirect(url_for('dashboard'))

    else:
        return redirect(url_for('login'))


@app.route('/login')
def login():
    if google_auth.is_logged_in():
        return redirect(url_for('member'))
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    if google_auth.is_logged_in():
        return redirect(url_for('google_auth.logout'))
    else:
        return redirect(url_for('login'))


@app.route('/account')
def account():
    if google_auth.is_logged_in():
        user = google_auth.get_user_info()
        connection = get_connection()
        cur = connection.cursor()
        sql = "select email, given_name, family_name, birth_date, address_line1, address_line2, address_country, telephone_number, document_country, document_type, document_number, verified_telephone, verified_document, verified_address from ab_user where google_id=%s"
        val = (user.get("id"))
        cur.execute(sql, val)
        data = cur.fetchone()
        connection.close()
        if data == None:
            return redirect(url_for('member'))
        else:
            return render_template('account.html', user_data=data, google_user_data=user)
    else:
        return redirect(url_for('login'))


@app.route('/account_update', methods=["POST"])
def account_update():
    if google_auth.is_logged_in():
        user = google_auth.get_user_info()
        document_country = request.form["document_country"]
        document_type = request.form["document_type"]
        document_number = request.form["document_number"]
        birth_date = request.form["birth_date"]
        address_line1 = request.form["address_line1"]
        address_line2 = request.form["address_line2"]
        address_country = request.form["address_country"]
        telephone_number = request.form["telephone_number"]
        connection = get_connection()
        cur = connection.cursor()
        sql = "update ab_user set document_country=%s, document_type=%s, document_number=%s, birth_date=STR_TO_DATE(%s, '%%d/%%m/%%Y'), address_line1=%s, address_line2=%s, address_country=%s, telephone_number=%s where google_id=%s"
        val = (
            document_country, document_type, document_number, birth_date, address_line1, address_line2, address_country,
            telephone_number, user.get("id"))
        cur.execute(sql, val)
        connection.commit()
        connection.close()
        return redirect(url_for('account'))


@app.route('/verify_telephone')
def verify_telephone():
    if google_auth.is_logged_in():
        user = google_auth.get_user_info()
        connection = get_connection()
        get_trust_level(connection, user)
        if session['verified_telephone'] == 0:
            cur = connection.cursor()
            sql = "select telephone_number from ab_user where google_id=%s"
            val = (user.get("id"))
            cur.execute(sql, val)
            data = cur.fetchone()
            connection.close()
            if data["telephone_number"] == None:
                return redirect(url_for('member'))
            else:
                return render_template('verify_telephone.html', user_data=data, google_user_data=user)
        else:
            return redirect(url_for('account'))
    else:
        return redirect(url_for('login'))


@app.route('/verify_telephone_process', methods=["POST"])
def verify_telephone_process():
    if google_auth.is_logged_in():
        user = google_auth.get_user_info()
        connection = get_connection()
        get_trust_level(connection, user)
        if session['verified_telephone'] == 0:
            cur = connection.cursor()
            sql = "select telephone_number from ab_user where google_id=%s"
            val = (user.get("id"))
            cur.execute(sql, val)
            data = cur.fetchone()
            connection.close()
            if data == None:
                return redirect(url_for('member'))
            else:
                twilio_response = twilio_send_code(data["telephone_number"], request.form["rg_method"])
                if "error" in twilio_response:
                    return redirect(url_for('account'))
                else:
                    return redirect(url_for('verify_telephone_code', sid=twilio_response["sid"]))
        else:
            return redirect(url_for('account'))
    else:
        return redirect(url_for('login'))


@app.route('/verify_telephone_code/<sid>', methods=["POST", "GET"])
def verify_telephone_code(sid):
    if google_auth.is_logged_in():
        user = google_auth.get_user_info()
        connection = get_connection()
        get_trust_level(connection, user)
        if session['verified_telephone'] == 0:
            twilio_response = twilio_view_verification(sid)
            if "error" in twilio_response:
                return redirect(url_for('account'))
            else:
                if request.method == "POST":
                    verification_code = request.form["verification_code"]
                    if verification_code == None or verification_code == "":
                        return render_template('verify_telephone_code.html', sid=sid, google_user_data=user)
                    else:
                        telephone_number = twilio_response["to"]
                        twilio_response = twilio_verify_code(telephone_number, verification_code)
                        if "status" in twilio_response:
                            if twilio_response["status"] == "approved":
                                cur = connection.cursor()
                                sql = "update ab_user set verified_telephone=1, trust_level=1 where google_id=%s"
                                val = (user.get("id"))
                                cur.execute(sql, val)
                                connection.commit()
                                connection.close()
                                return redirect(url_for('member'))
                            else:
                                return render_template('verify_telephone_code.html', sid=sid, google_user_data=user)
                        else:
                            return render_template('verify_telephone_code.html', sid=sid, google_user_data=user)
                else:
                    return render_template('verify_telephone_code.html', sid=sid, google_user_data=user)
        else:
            return redirect(url_for('account'))
    else:
        return redirect(url_for('login'))


@app.route('/verify_identity')
def verify_identity():
    if google_auth.is_logged_in():
        user = google_auth.get_user_info()
        connection = get_connection()
        get_trust_level(connection, user)
        if session['verified_document'] == 0:
            cur = connection.cursor()
            sql = "select document_country, document_type, document_number from ab_user where google_id=%s"
            val = (user.get("id"))
            cur.execute(sql, val)
            data = cur.fetchone()
            connection.close()
            if data["document_number"] == None:
                return redirect(url_for('member'))
            else:
                return render_template('verify_identity.html', user_data=data, google_user_data=user)
        else:
            return redirect(url_for('account'))
    else:
        return redirect(url_for('login'))


@app.route('/verify_address')
def verify_address():
    if google_auth.is_logged_in():
        user = google_auth.get_user_info()
        connection = get_connection()
        get_trust_level(connection, user)
        if session['verified_address'] == 0:
            cur = connection.cursor()
            sql = "select address_line1, address_line2, address_country from ab_user where google_id=%s"
            val = (user.get("id"))
            cur.execute(sql, val)
            data = cur.fetchone()
            connection.close()
            if data["address_line1"] == None:
                return redirect(url_for('member'))
            else:
                return render_template('verify_address.html', user_data=data, google_user_data=user)
        else:
            return redirect(url_for('account'))
    else:
        return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if google_auth.is_logged_in():
        user = google_auth.get_user_info()
        if session['trust_level'] == 0:
            return redirect(url_for('member'))
        else:
            return render_template('dashboard.html', google_user_data=user)
    else:
        return redirect(url_for('login'))


@app.route('/doBuy/<btcToBuy>/<currencyCode>/<walletAddress>/<payMethod>')
def doBuy(btcToBuy, currencyCode, walletAddress, payMethod):
    if google_auth.is_logged_in():

        if session['trust_level'] == 1 and session['verified_telephone'] == 1:

            btcToBuy = float(btcToBuy)
            coindesk_response = coindesk_get_BPI(currencyCode)
            basePrice = float(coindesk_response[currencyCode]["rate_float"])
            commissionPercentage = 0.07 - 0.0275 * math.log(btcToBuy)
            priceToPay = round(basePrice * btcToBuy * (1 + commissionPercentage), 0)

            connection = get_connection()
            cur = connection.cursor()
            sql = "insert into ab_trade(user_id, btcToBuy, currencyCode, walletAddress, payMethod, basePrice, commissionPercentage, priceToPay)"\
                  " values(%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (session["user_id"], btcToBuy, currencyCode, walletAddress, payMethod, basePrice, commissionPercentage, priceToPay)
            cur.execute(sql, val)
            trade_id=cur.lastrowid
            connection.commit()
            connection.close()
            return redirect(url_for('trade', trade_id=trade_id))
        else:
            return redirect(url_for('member'))
    else:
        return redirect(url_for('login'))

@app.route('/trade/<trade_id>')
def trade(trade_id):
    if google_auth.is_logged_in():
        if session['trust_level'] == 1:
            user = google_auth.get_user_info()
            return render_template('trade.html', google_user_data=user, trade_id=trade_id)
        else:
            return redirect(url_for('member'))
    else:
        return redirect(url_for('login'))


@app.route('/buy', methods=["GET", "POST"])
def buy():
    if google_auth.is_logged_in():
        if session['trust_level'] == 1:
            if request.method == "POST":
                strbtcToBuy = str(int(request.form["sliderBtcToBuy"]) / 1000)
                return redirect(url_for('doBuy', btcToBuy=strbtcToBuy, currencyCode=request.form["currencyCode"], walletAddress=request.form["walletAddress"], payMethod=request.form["payMethod"]))
            else:
                user = google_auth.get_user_info()
                return render_template('buy.html', google_user_data=user)
        else:
            return redirect(url_for('member'))
    else:
        return redirect(url_for('login'))


@app.route('/sell')
def sell():
    if google_auth.is_logged_in():
        if session['trust_level'] == 1:
            user = google_auth.get_user_info()
            return render_template('sell.html', google_user_data=user)
        else:
            return redirect(url_for('member'))
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
