const axios = require('axios');

// Make a request for a user with a given ID
axios.get('http://localhost:8082/public/index.html')
  .then(function (response) {
    // handle success
    console.log(response);
  })
  .catch(function (error) {
    // handle error
    console.log(error);
  })
  .finally(function () {
    // always executed
  });