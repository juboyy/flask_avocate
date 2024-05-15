from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone


#app setup
app = Flask(__name__)
Scss = (app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///avocado.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

#data class
class processo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    processo = db.Column(db.String(100), nullable=False)
    cliente = db.Column(db.String(100), nullable=False)
    prazo = db.Column(db.DateTime , default=lambda: datetime.now(timezone.utc))
    todo = db.Column(db.String(100))
    obs = db.Column(db.String(500))

    def __repr__(self) -> str:
        return f"{self.id} - {self.processo} - {self.cliente} - {self.prazo} - {self.todo} - {self.obs}"

with app.app_context():
    db.create_all()

#Homepage
@app.route("/", methods=["GET", "POST"])
def index():

    #add a process
    if request.method == "POST":
        newProcess = request.form['processo']
        newCliente = request.form['cliente']
        newPrazo = request.form['prazo']
        newPrazo = datetime.strptime(newPrazo, "%Y-%m-%d")
        newTodo = request.form['todo']
        newObservacao = request.form['obs']
        newProcess = processo(processo=newProcess, cliente=newCliente, prazo=newPrazo, todo=newTodo, obs=newObservacao)

        try:
            db.session.add(newProcess)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(e)
            return f"Error:{e}"
    else:
        processos = processo.query.order_by(processo.prazo).all()
        return render_template('index.html', processos=processos)


#Delete an Process
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = processo.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"Error:{e}"

#Edit a process
@app.route("/edit/<int:id>", methods=["POST", "GET"])
def edit(id:int):
    process = processo.query.get_or_404(id)
    if request.method == "POST":
        process.processo = request.form['processo']
        process.cliente = request.form['cliente']
        process.prazo = request.form['prazo']
        process.prazo = datetime.strptime(process.prazo, "%Y-%m-%d")
        process.todo = request.form['todo']
        process.obs = request.form['obs']

        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Error:{e}"
    else:
        return render_template("edit.html", process=process)
    
#Debugger and Runner
if __name__ == "__main__":
    app.run(debug=True)