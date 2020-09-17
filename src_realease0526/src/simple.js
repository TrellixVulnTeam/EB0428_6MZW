var fetch = require("node-fetch");
var fs = require("fs");

function download(u, p) {
    return fetch(u, {
        method: 'GET',
        headers: { 'Content-Type': 'application/octet-stream' },
    }).then(res => res.buffer()).then(_ => {
        fs.writeFile(p, _, "binary", function (err) {
            console.log(err || p);
        });
    });
}
////////======= 
var url = "https://nodejs.org/dist/v8.9.4/node-v8.9.4-win-x64.zip";
download(url, url.split("/").reverse()[0])

