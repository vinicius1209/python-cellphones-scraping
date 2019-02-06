from flask import render_template, redirect, session, json, make_response
from app import phone_scraping
from app.analytics import getDataFrame, append_memories, clear_data, new_info, df_to_csv

@phone_scraping.route('/', methods=['GET', 'POST'])
@phone_scraping.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html', title='Home')

@phone_scraping.route('/create_df/<int:pages>', methods=['GET', 'POST'])
def create_df(pages):
    phones_df = getDataFrame(pages)
    phones_df = append_memories(phones_df)
    phones_df = clear_data(phones_df)
    phones_df = new_info(phones_df)
    session['data_frame'] = phones_df.to_html(classes='table table-bordered table-striped table-hover',
                                              columns=['phone_title', 'last_price', 'current_price', 'rating', 'discount_percent'],
                                              justify='center',
                                              table_id='phone_table')
    session['csv'] = df_to_csv(phones_df)
    return '200'

@phone_scraping.route('/data_frame', methods=['GET'])
def show_df():
    if session['data_frame']:
        return render_template('data_frame.html', title='Data Frame')
    else:
        return redirect('home')

@phone_scraping.route('/clear', methods=['GET'])
def clear():
    session.pop('data_frame', None)
    return redirect('home')

@phone_scraping.route('/csv', methods=['GET'])
def csv():
    resp = make_response(session['csv'])
    resp.headers["Content-Disposition"] = "attachment; filename=phone.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp
