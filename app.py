from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

from sqlite_creator import create_db

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

questions = [
    {"question": "İsminiz nedir?", "type": "text"},
    {"question": "En sevdiğiniz renk nedir?", "type": "radio", "options": ["Kırmızı", "Mavi", "Yeşil"]},
    {"question": "En sevdiğiniz hayvan nedir?", "type": "radio", "options": ["Köpek", "Kedi", "Papağan"]},
    {"question": "Hobileriniz veya ilgi alanlarınız nelerdir?", "type": "textarea"}
]

@app.route('/', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
       
        answers = request.form
        name = answers.get('question1') 

        score = calculate_score(answers)

   
        save_result(name, score)
        session['best_score'] = get_best_score(name)

        return render_template('result.html', score=score)

    best_score = session.get('best_score', 0)
    return render_template('quiz_template.html', questions=questions, best_score=best_score)

def calculate_score(answers):
    score = 0
    if answers.get('question2') == 'Mavi':  
        score += 50
    if answers.get('question2') == 'Yeşil':  
        score += 20
    if answers.get('question3') == 'Kedi':  
        score += 20
    if answers.get('question3') == 'Köpek':  
        score += 50
    if answers.get('question3') == 'Papağan':  
        score += 15
    if answers.get('question4') == 'Yazmak':  
        score += 10
    return score

def save_result(name, score):
    conn = sqlite3.connect('quiz_results.db')
    c = conn.cursor()

   
    c.execute('''SELECT MAX(score) FROM results WHERE name = ?''', (name,))
    existing_best_score = c.fetchone()[0]

  
    if existing_best_score is None or score > existing_best_score:
        c.execute('''INSERT INTO results (name, score)
                     VALUES (?, ?)''', (name, score))
        conn.commit()

    conn.close()

def get_best_score(name):
    conn = sqlite3.connect('quiz_results.db')
    c = conn.cursor()

    
    c.execute('''SELECT MAX(score) FROM results WHERE name = ?''', (name,))
    best_score = c.fetchone()[0]

    conn.close()
    return best_score or 0  

if __name__ == '__main__':
    create_db()  
    app.run(debug=True)
