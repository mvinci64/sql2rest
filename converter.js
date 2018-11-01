fs = require('fs')
//var cmd=require('node-cmd');
var exec = require('child_process').exec;

fs.readFile('config/converter/keyStore.json', 'utf8', function (err,data) {
  if (err) {
    return console.log(err);
  }
  //console.log(data);
  var json = JSON.parse(data);
  //console.log(json.authentications[0].pem);
  var string = json.pem;
  var split = string.split("-----BEGIN CERTIFICATE-----");
  split[1] = "-----BEGIN CERTIFICATE-----" + split[1];
  fs.writeFile("config/converter/pKey.pem", split[0], function(err) {
      if(err) {
          return console.log(err);
      }
      console.log("The file was saved!");
      //cmd.get("openssl rsa -in pKey.pem -passin pass:" + json.authentications[0].secret + " -out newStore.pem",
      exec("c:/openSSL-Win64/bin/openssl rsa -in config/converter/pKey.pem -passin pass:" + json.secret + " -out config/converter/newStore.pem",
        function(err, data, stderr){
            if (!err) {
               console.log('success' + data)
               fs.readFile('config/converter/newStore.pem', 'utf8', function (err,data) {
                  if (err) {
                    return console.log(err);
                  }
                  data = data + split[1];
                  fs.writeFile("config/converter/keyStore.pem", data, function(err) {
                      if(err) {
                          return console.log(err);
                      }

                      console.log("The file was saved!");
                  });
                });
            } else {
               console.log('error', err)
            }

        }
    );
  });
});