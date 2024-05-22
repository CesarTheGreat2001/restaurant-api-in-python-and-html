from flask import Flask, render_template, request, redirect
import pandas as pd

app = Flask(__name__)

# Load your data
data_file = 'data.csv'
df = pd.read_csv(data_file)

@app.route('/')
def index():
    # Get current page from query parameters, default to 1
    page = request.args.get('page', 1, type=int)
    per_page = 10
    total_pages = (len(df) - 1) // per_page + 1
    start = (page - 1) * per_page
    end = start + per_page
    df_page = df.iloc[start:end]

    tables = [df_page.to_html(classes='data', header=True, index=True)]
    titles = ['Data Table']

    return render_template('index.html', tables=tables, titles=titles, page=page, total_pages=total_pages)

@app.route('/add', methods=['POST'])
def add():
    new_row = {
        'Company': request.form['company'],
        'Index': request.form['index'],
        'CEO': request.form['ceo'],
        'Number of Restaurants (Millions)': request.form['number_of_restaurants'],
        'Most Famous Dish': request.form['most_famous_dish'],
        'Type of Restaurant': request.form['type_of_restaurant'],
        'City': request.form['city'],
        'State': request.form['state'],
        'Yearly Revenue (Millions USD)': request.form['yearly_revenue']
    }
    df.loc[len(df)] = new_row
    df.to_csv(data_file, index=False)
    return redirect('/')

@app.route('/delete', methods=['POST'])
def delete():
    delete_index = int(request.form['delete_index'])
    if 0 <= delete_index < len(df):
        df.drop(delete_index, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.to_csv(data_file, index=False)
    return redirect('/')

@app.route('/modify', methods=['POST'])
def modify():
    modify_index = int(request.form['modify_index'])
    if 0 <= modify_index < len(df):
        if request.form['company']:
            df.at[modify_index, 'Company'] = request.form['company']
        if request.form['ceo']:
            df.at[modify_index, 'CEO'] = request.form['ceo']
        if request.form['number_of_restaurants']:
            df.at[modify_index, 'Number of Restaurants (Millions)'] = request.form['number_of_restaurants']
        if request.form['most_famous_dish']:
            df.at[modify_index, 'Most Famous Dish'] = request.form['most_famous_dish']
        if request.form['type_of_restaurant']:
            df.at[modify_index, 'Type of Restaurant'] = request.form['type_of_restaurant']
        if request.form['city']:
            df.at[modify_index, 'City'] = request.form['city']
        if request.form['state']:
            df.at[modify_index, 'State'] = request.form['state']
        if request.form['yearly_revenue']:
            df.at[modify_index, 'Yearly Revenue (Millions USD)'] = request.form['yearly_revenue']
        df.to_csv(data_file, index=False)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
