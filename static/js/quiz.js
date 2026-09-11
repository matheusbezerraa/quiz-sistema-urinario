document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form-quiz");
  if (!form) return;

  const erro = document.getElementById("erro-quiz");

  form.querySelectorAll(".opcao").forEach((label) => {
    const input = label.querySelector("input[type='radio']");
    input.addEventListener("change", () => {
      const nome = input.name;
      form.querySelectorAll(`input[name="${nome}"]`).forEach((outro) => {
        outro.closest(".opcao").classList.remove("selecionada");
      });
      label.classList.add("selecionada");
    });
  });

  form.addEventListener("submit", (evento) => {
    const perguntas = new Set(
      Array.from(form.querySelectorAll("input[type='radio']")).map((i) => i.name)
    );
    const semResposta = Array.from(perguntas).some(
      (nome) => !form.querySelector(`input[name="${nome}"]:checked`)
    );

    if (semResposta) {
      evento.preventDefault();
      erro.hidden = false;
      erro.scrollIntoView({ behavior: "smooth", block: "center" });
    } else {
      erro.hidden = true;
    }
  });
});
