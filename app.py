from flask import Flask, render_template, request, redirect, url_for, session

from quiz_data import QUIZZES

app = Flask(__name__)
app.secret_key = "quiz-sistema-urinario-secret-key"


@app.route("/", methods=["GET", "POST"])
def nome():
    if request.method == "POST":
        nome_informado = request.form.get("nome", "").strip()
        if not nome_informado:
            return render_template("nome.html", erro="Por favor, digite seu nome.")
        session.clear()
        session["nome"] = nome_informado
        return redirect(url_for("faixa"))
    return render_template("nome.html")


@app.route("/faixa", methods=["GET", "POST"])
def faixa():
    if "nome" not in session:
        return redirect(url_for("nome"))

    if request.method == "POST":
        faixa_escolhida = request.form.get("faixa")
        if faixa_escolhida not in QUIZZES:
            return redirect(url_for("faixa"))
        session["faixa"] = faixa_escolhida
        return redirect(url_for("quiz"))

    return render_template("faixa.html", nome=session["nome"], quizzes=QUIZZES)


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "nome" not in session or "faixa" not in session:
        return redirect(url_for("nome"))

    quiz_atual = QUIZZES[session["faixa"]]

    if request.method == "POST":
        acertos = 0
        for pergunta in quiz_atual["perguntas"]:
            resposta = request.form.get(f"q{pergunta['id']}")
            if resposta == pergunta["correta"]:
                acertos += 1
        session["acertos"] = acertos
        return redirect(url_for("resultado"))

    return render_template("quiz.html", nome=session["nome"], quiz=quiz_atual)


@app.route("/resultado")
def resultado():
    if "nome" not in session or "faixa" not in session or "acertos" not in session:
        return redirect(url_for("nome"))

    quiz_atual = QUIZZES[session["faixa"]]
    acertos = session["acertos"]
    total = len(quiz_atual["perguntas"])
    ganhou = acertos >= 6

    return render_template(
        "resultado.html",
        nome=session["nome"],
        quiz=quiz_atual,
        acertos=acertos,
        total=total,
        ganhou=ganhou,
    )


@app.route("/reiniciar")
def reiniciar():
    session.clear()
    return redirect(url_for("nome"))


if __name__ == "__main__":
    app.run(debug=True)
