document.getElementById("session-form").addEventListener("submit", function(event) {
  event.preventDefault();

  var valor = parseInt(document.getElementById("valor-input").value);
  var sessaoMaxima = parseInt(document.getElementById("sessao-maxima-input").value);
  var sessoesPorDia = parseInt(document.getElementById("sessoes-por-dia-input").value);

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/calculate", true);
  xhr.setRequestHeader("Content-Type", "application/json");

  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
      var resultado = JSON.parse(xhr.responseText);
      document.getElementById("resultado").textContent = resultado;
    }
  };

  var data = JSON.stringify({
    valor: valor,
    sessao_maxima: sessaoMaxima,
    sessoes_por_dia: sessoesPorDia
  });

  xhr.send(data);
});
