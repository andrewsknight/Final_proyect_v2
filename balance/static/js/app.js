function save_movement(){
    const money_from = document.getElementById("money_from");
    const money_to = document.getElementById("money_to");
    const amount = document.getElementById("amount");
    var date = new Date();
const hora = date.getHours() + ':' + date.getMinutes();
const fecha = date.getFullYear()
    fetch("/api/v1/movimiento", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        fecha: fecha,
        hora: hora,
        money_from: money_from.value,
        amount: amount.value,
        money_to: money_to.value,
        amount_to: amount.value * currency.rate
        ,
      }),
    })
      .then((resultServer) => {
        return resultServer.json();
      })
      .then((result) => {
        alert(result.ok);
      });
  }
 
 
 
 function exchange_crypto() {
    fetch(
        `https://rest.coinapi.io/v1/exchangerate/${}/${}?time={}apikey=E01CCF95-56F6-42CD-9ABA-67E8380016F1`    )
      .then((response) => response.json())
      .then((result) => {

       let swap_crypto = amount.value * rate
       const cryptos_change = { 

         amount : amount.value,  
         money_from: asset_id_base, 
         money_to: asset_id_quote,
         amount_to : swap_crypto,
         time: time
        };
        result.rates.forEach((currency) => {
            cryptos_change[amount, money_from, money_to, amount_to, time] = amount.value, asset_id_base, asset_id_quote, swap_crypto, time
      });
    })
  };

function get_movements(){
  fetch("/api/v1/movimientos")
  .then((reponse) => reponse.json())
  .then((result) => {
    let complete_crypto = {
      "fecha":fecha,
      "hora": hora,
      "from_moneda": from_moneda,
      "from_cantidad": from_cantidad,
      "to_moneda": to_moneda,
      "to_cantidad": to_cantidad
      
    });
    result.rates.forEach((currency)=>{
      let time = currency.time
      let time_part = time.split("T")
      let fecha = time_part[0]
      let hora = time_part[1]
      let swap_crypto = amount.value * parseInt(currency.rate)
      complete_crypto[fecha,hora,from_moneda,from_cantidad, to_moneda, to_cantidad] = fecha, hora, currency.asset_id_base, amount.value, currency.asset_id_quote,swap_crypto


    });
  });
}