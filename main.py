from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Float
from google import translate  # for Yusuf for local run
from datetime import datetime as dt
from pytz import timezone
from user_agents import parse
import time

# INIT APP
app = Flask(__name__)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


# Config app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///translation.db"
db = SQLAlchemy(model_class=Base)
# Init app with Extension
db.init_app(app)


# CREATE TABLE
class Translation(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uzb_content: Mapped[str] = mapped_column(String, nullable=False)
    eng_content: Mapped[str] = mapped_column(String, nullable=False)
    uzb_content_length: Mapped[int] = mapped_column(Integer, nullable=False)
    eng_content_length: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[str] = mapped_column(String, nullable=False)
    input_time: Mapped[str] = mapped_column(String, nullable=False)
    output_time: Mapped[str] = mapped_column(String, nullable=False)
    duration: Mapped[str] = mapped_column(Float, nullable=False)
    ip_address: Mapped[str] = mapped_column(String, nullable=False)
    browser_family: Mapped[str] = mapped_column(String, nullable=False)
    browser_version: Mapped[str] = mapped_column(String, nullable=False)
    device_family: Mapped[str] = mapped_column(String, nullable=False)
    device_brand: Mapped[str] = mapped_column(String, nullable=False)
    device_model: Mapped[str] = mapped_column(String, nullable=False)
    os_family: Mapped[str] = mapped_column(String, nullable=False)
    os_version: Mapped[str] = mapped_column(String, nullable=False)


# Create Table Schema in DB
with app.app_context():
    db.create_all()


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# About Page
@app.route("/biz-haqimizda")
def about():
    print(request)
    return render_template("about.html")


@app.route("/kontakt")
def contact():
    print(request)
    return render_template("contact.html")


def localize_date():
    """Localize date & time of request"""
    uzb_timezone = timezone('Asia/Tashkent')
    localized_dt = dt.now(uzb_timezone)
    formatted_localized_dt = localized_dt.strftime('%Y-%m-%d %H:%M:%S')
    return str(formatted_localized_dt).split()


def get_client_data(ua_str: str):
    """Get client data (Browser, Device, OS)"""
    user_agent = parse(ua_str)
    # Browser
    br_data_list = []
    if br_fam := user_agent.browser.family:
        br_data_list.append(br_fam)
    else:
        br_data_list.append(-1)
    if br_ver := user_agent.browser.version_string:
        br_data_list.append(br_ver)
    else:
        br_data_list.append(-1)

    # Device
    dv_data_list = []
    if dv_fam := user_agent.device.family:
        dv_data_list.append(dv_fam)
    else:
        dv_data_list.append(-1)
    if dv_brand := user_agent.device.brand:
        dv_data_list.append(dv_brand)
    else:
        dv_data_list.append(-1)
    if dv_model := user_agent.device.model:
        dv_data_list.append(dv_model)
    else:
        dv_data_list.append(-1)

    # OS
    os_data_list = []
    if os_fam := user_agent.os.family:
        os_data_list.append(os_fam)
    else:
        os_data_list.append(-1)
    if os_ver := user_agent.os.version_string:
        os_data_list.append(os_ver)
    else:
        os_data_list.append(-1)

    return [[br_fam, br_ver], [dv_fam, dv_brand, dv_model], [os_fam, os_ver]]


@app.route("/translate", methods=["POST"])
def translate_endpoint():
    # ## get client content
    client_content = request.form["eng-field"]
    client_content_len = len(client_content)

    # ## get client data (Browser, Device, OS)
    client_data = get_client_data(str(request.headers['User-Agent']))
    # browser data
    client_browser_data = client_data[0]
    client_br_fam = client_browser_data[0] if client_browser_data[0] != -1 else str(-1)
    client_br_ver = client_browser_data[1] if client_browser_data[1] != -1 else str(-1)
    # device data
    client_device_data = client_data[1]
    client_dv_fam = client_device_data[0] if client_device_data[0] != -1 else str(-1)
    client_dv_brand = client_device_data[1] if client_device_data[1] != -1 else str(-1)
    client_dv_model = client_device_data[2] if client_device_data[2] != -1 else str(-1)
    # os data
    client_os_data = client_data[2]
    client_os_fam = client_os_data[0] if client_os_data[0] != -1 else str(-1)
    client_os_ver = client_os_data[1] if client_os_data[1] != -1 else str(-1)

    # ## get ip address
    client_ip_address = request.remote_addr

    # ## get input & output time and duration
    t_before = time.time()
    d_date, input_start = localize_date()
    # translate content
    translated_text = translate(client_content)
    t_after = time.time()
    _, output_end = localize_date()
    duration = round(t_after - t_before, 2)
    translated_text_len = len(translated_text)

    # ## commit content & translated content to DB
    translation = Translation(
        uzb_content=client_content,
        eng_content=translated_text,
        uzb_content_length=client_content_len,
        eng_content_length=translated_text_len,
        date=d_date,
        input_time=input_start,
        output_time=output_end,
        duration=duration,
        ip_address=client_ip_address,
        browser_family=client_br_fam,
        browser_version=client_br_ver,
        device_family=client_dv_fam,
        device_brand=client_dv_brand,
        device_model=client_dv_model,
        os_family=client_os_fam,
        os_version=client_os_ver
    )
    db.session.add(translation)
    db.session.commit()
    return translated_text


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)

# #006C80 --> Color Primary
