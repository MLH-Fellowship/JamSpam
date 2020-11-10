const fetch = require('node-fetch'); 
 
 const fetchText =   (url) => {
    let settings = { method: "Get" };
      return fetch(url, settings)
      .then ( res => {
         return res.text().then((data)=>  {
          
          return data;
        });
        
      })
  }
  module.exports = fetchText;
