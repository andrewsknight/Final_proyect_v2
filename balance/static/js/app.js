const apikey = window.api_key4;
const money_from_input = document.getElementById("money_from");
const money_to_input = document.getElementById("money_to");
const amount_input = document.getElementById("amount");
const result_input = document.getElementById("result");
const result_label = document.getElementById("result_label");
const send = document.getElementById("send");
const tbody = document.getElementById("tbody");
const invest = document.getElementById("invest");
const actual_value = document.getElementById("actual_value");
const diferencia = document.getElementById("diferencia");
const crypto_money = document.getElementById("crypto_money");
const crypto_money_value = document.getElementById("crypto_money_value");
const crypto_amount = document.getElementById("crypto_amount");
const crypto_amount_label = document.getElementById("crypto_amount_label");
const crypto_money_value_label = document.getElementById(
  "crypto_money_value_label"
);
let valid_coins = [];
let last_date = new Date();

function get_movements_cryptos() {
  fetch(`/api/v1/crypto/${crypto_money.value}`)
    .then((resultServer) => {
      return resultServer.json();
    })
    .then((result) => {
      if (result.status === "success") {
        crypto_money_value_label.classList.add("active");
        crypto_amount_label.classList.add("active");
        crypto_amount.value = result.amount;
        crypto_money_value.value = result.crypto_money_value;
      } else {
        alert(result.message);
      }
    });
}

function get_movements_invest() {
  fetch("/api/v1/status")
    .then((resultServer) => {
      return resultServer.json();
    })
    .then((result) => {
      if (result.status === "success") {
        invest.value = result.data.invest + " €";
        actual_value.value = result.data.tot_money;
        diferencia.value = result.data.tot_money - result.data.invest;
        if (diferencia.value < 0) {
          diferencia.classList.add("invalid");
        } else {
          diferencia.classList.remove("invalid");
        }
      } else {
        alert(result.message2);
      }
    });
}
function get_movements() {
  fetch("/api/v1/movimientos")
    .then((resultServer) => {
      return resultServer.json();
    })
    .then((result) => {
      if (result.status === "success") {
        tbody.innerHTML = "";
        result.data.forEach((element) => {
          tbody.innerHTML += `<tr>

            <td>
              Compra Venta ${element.id}
            </td>
            <td>
              ${element.fecha}
            </td>
              <td>
              ${element.hora}
            </td>
            <td>
              ${element.from_moneda}
            </td>
            <td>
              ${element.from_cantidad}
            </td>
            <td>
              ${element.to_moneda}
            </td>
            <td>
              ${element.to_cantidad}
            </td>
        </tr>`;
        });
      } else {
        debugger;
        alert(result.mensaje);
      }
    });
}

function send_data() {
  const [date, hour] = last_date.toLocaleString().split(", ");
  fetch("/api/v1/movimiento", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      fecha: date,
      hora: hour,
      from_moneda: money_from_input.value,
      from_cantidad: amount_input.value,
      to_moneda: money_to_input.value,
      to_cantidad: result_input.value,
    }),
  })
    .then((resultServer) => {
      return resultServer.json();
    })
    .then((result) => {
      if (result.status === "success") {
        get_movements();
        get_movements_invest();
        money_from_input.value = "";
        amount_input.value = "";
        money_to_input.value = "";
        result_input.value = "";

        alert("operación realizada con éxito");
      } else {
        alert(result.mensaje);
      }
    });
}
function fill_select_own_money() {
  fetch(`/api/v1/cryptos/diferent`)
    .then((response) => response.json())
    .then((result) => {
      $("#crypto_money").autocomplete({
        data: result.data,
      });
    });
}

function fill_select() {
  fetch(`https://rest.coinapi.io/v1/exchangerate/EUR?apikey=${apikey}`)
    .then((response) => response.json())
    .then((result) => {
      valid_coins = result.rates.map((rate) => {
        return rate.asset_id_quote;
      });
      valid_coins.push("EUR");
      const cryptos = { EUR: null };

      result.rates.forEach((currency) => {
        cryptos[currency.asset_id_quote] = null;
      });
      $("#money_from").autocomplete({
        data: cryptos,
      });
      $("#money_to").autocomplete({
        data: cryptos,
      });
    });
}

/**
 *
 * */
function exchange_crypto(money_from, money_to, amount) {
  fetch(
    `https://rest.coinapi.io/v1/exchangerate/${money_from}/${money_to}?apikey=${apikey}`
  )
    .then((response) => {
      if (response.status !== 200) {
        throw new Error(response.status);
      }
      return response.json();
    })
    .then((conversion) => {
      result_input.value = amount * conversion.rate;
      // esta fecha es la que me devuelve el api para guardarla en una variable y enviarla al post.
      last_date = new Date(conversion.time);
      try {
        send.attributes.removeNamedItem("disabled");
      } catch (error) {}
      result_label.classList.add("active");
    })
    .catch((e) => {
      send.disabled = true;
      result_input.value = "";
      switch (e.message) {
        case "550":
          alert("Este par no está disponible");
          break;

        case "429":
          alert("Servicio no disponible inténtelo más tarde");
          break;
        default:
          alert("Ha ocurrido un error");
      }
    });
}

function validate_input(input) {
  if (input.value) {
    input.classList.remove("invalid");
    return true;
  } else {
    input.classList.add("invalid");
    return false;
  }
}

function validate_negative(input) {
  if (input.value <= 0) {
    input.classList.add("invalid");
    alert("La cantidad debe ser válida");
    return false;
  } else {
    input.classList.remove("invalid");
    return true;
  }
}

function validate_equal_money(input_from, input_to) {
  if (input_from.value === input_to.value) {
    input_from.classList.add("invalid");
    input_to.classList.add("invalid");
    alert("El cambio debe ser entre dos valores distintos");
    return false;
  } else {
    input_from.classList.remove("invalid");
    input_to.classList.remove("invalid");
    return true;
  }
}

function validate_money(input) {
  const isValid = valid_coins.includes(input.value);
  if (isValid) input.classList.remove("invalid");
  return isValid;

  input.classList.add("invalid");
  return false;
}

function input_change() {
  const money_from_value = money_from_input.value;
  const money_to_value = money_to_input.value;
  const amount_value = amount_input.value;

  validate_input(money_from_input);
  validate_input(money_to_input);
  validate_input(amount_input);

  if (
    money_from_value &&
    money_to_value &&
    amount_value &&
    validate_equal_money(money_from_input, money_to_input) &&
    validate_negative(amount_input) &&
    validate_money(money_from_input) &&
    validate_money(money_to_input)
  ) {
    exchange_crypto(money_from_value, money_to_value, amount_value);
  } else {
    send.disabled = true;
  }
  console.log("me esta llamando");
}

$(document).ready(function () {
  fill_select();
  fill_select_own_money();
  get_movements();
  get_movements_invest();
}); // end of jQuery name space
