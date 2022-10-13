// stripe secret key
let stripe = Stripe('pk_test_51Lc5tMG7qH1UlLmbPNmCk7YYGvnJyKUKGtv0SpStsTB9eENXOLluBGiSnKwVoUE3o54fkO8a1dmNB7J1eheqSodi00P7O7JWoS')


// ajax code not working. CSRF TOKEN problems
  // $.ajax({
  //   type: "POST",
  //   url: 'http://127.0.0.1:8000/orders/add/',
  //   data: {
  //     order_key: clientsecret,
  //     csrfmiddlewaretoken: CSRF_TOKEN,
  //     action: "post",
  //   },
  //   success: function (json) {
  //     console.log(json.success)
  //
  //
  //   },
  //   error: function (xhr, errmsg, err) {},
  // });



let elem = document.getElementById('submit');
clientsecret = elem.getAttribute('data-secret');

// Set up Stripe.js and Elements to use in checkout form
let elements = stripe.elements();
let style = {
    base: {
        color: '#000',
        lineHeight: '2.4',
        fontSize: '16px',
    }
};

let card = elements.create("card", { style: style });
card.mount("#card-element");

// code to display errors with the payments
// card.on(
//   'change', function(event) {
//     var displayError = document.getElementById('card-errors');
//     if (event.error) {
//         displayError.textContent = event.error.message;
//         $('#card-errors').addClass('alert alert-info');
//     } else {
//         displayError.textContent = '';
//         $('#card-errors').removeClass('alert alert-info');
//     }
// });

// Real time validation errors from the card element
card.on('change', ({error}) => {
  let displayError = document.getElementById('card-errors');
  if (error) {
    displayError.textContent = error.message;
    $('#card-errors').addClass('alert alert-info');
  } else {
    displayError.textContent = '';
    $('#card-errors').removeClass('alert alert-info');
  }
});

// handle form submissions
let form = document.getElementById('payment-form');

form.addEventListener('submit', function(e) {
    e.preventDefault();

    let custfirstName = document.getElementById("custfirstName").value;
    let custlastName = document.getElementById("custlastName").value;
    let custAdd = document.getElementById("custAdd").value;
    let custAdd2 = document.getElementById("custAdd2").value;
    let postCode = document.getElementById("postCode").value;

    $.ajax({
    type: "POST",
    url: 'http://msp4-hopeservices.herokuapp.com/orders/add/',
    data: {
      order_key: clientsecret,
      csrfmiddlewaretoken: CSRF_TOKEN,
      action: "post",
    },
    success: function (json) {
      console.log(json.success)

    stripe.confirmCardPayment(clientsecret, {
        payment_method: {
          card: card,
          billing_details: {
            address:{
                line1:custAdd,
                line2:custAdd2,
                postal_code:postCode
            },
            name: custfirstName + ' ' + custlastName
          },
        }
      }
      ).then(
        function(result) {
        if (result.error) {
          console.log('payment error')
          console.log(result.error.message);
        } else {
          if (result.paymentIntent.status === 'succeeded') {
            console.log('payment processed')
            // There's a risk of the customer closing the window before callback
            // execution. Set up a webhook or plugin to listen for the
            // payment_intent.succeeded event that handles any business critical
            // post-payment actions.
            window.location.replace("http://127.0.0.1:8000/payment/orderplaced/");
          }
        }
      });
          },
    error: function (xhr, errmsg, err) {},
  });
    });
    //  code from:
    // https://stripe.com/docs/payments/accept-card-payments?platform=web&ui=elements
    // section Submit the payment to stripe