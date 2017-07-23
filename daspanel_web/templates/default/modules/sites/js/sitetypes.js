function chgTypes(select_type) {

    var myHeaders = {
        "Content-type": "application/json",
        "Accept": "application/json"
    };
    var master = document.getElementById("runtime");
    var child = document.getElementById("sitetype");

    var current_type = child.value;
    if (select_type !== undefined && typeof select_type === 'string') {
        current_type = select_type;
    }

    child.length = 0;
    axios
        //.get("\{\{ url_for('sites.get_sitetypes', cfggroup='engines') \}\}", {
        //    params: {
        //        q: master.options[master.selectedIndex].value
        //    },
        //    headers: myHeaders
        //})

        // https://stackoverflow.com/questions/10314800/flask-url-for-urls-in-javascript
        .get("{{ url_for('sites.get_sitetypes', engine='REPLACE') }}".replace("REPLACE", master.options[master.selectedIndex].value), {
            headers: myHeaders
        })

        .then(function (response) {
            //console.log("Dados: ", response.status, response.data);
            response.data.forEach(function(item, i) {
                //console.log("Index: ", i, "Key: ", item[0], " Value: ", item[1]);
                child.options[i]=new Option(item.description, item.sitetype);
                if (item.sitetype === current_type) {
                    child.options[i].selected = true;
                    child.value = current_type;
                }
            });

        })
        .catch(function (error) {
            if (error.response) {
                // The request was made and the server responded with a status code
                // that falls out of the range of 2xx
                console.log(error.response.data);
                console.log(error.response.status);
                console.log(error.response.headers);
            } else if (error.request) {
                // The request was made but no response was received
                // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
                // http.ClientRequest in node.js
                console.log(error.request);
            } else {
                // Something happened in setting up the request that triggered an Error
                console.log('Error', error.message);
            }
            console.log(error.config);
        });

    return true;
}

function setEngines(current_engine, current_type) {

    var myHeaders = {
        "Content-type": "application/json",
        "Accept": "application/json"
    };
    var master = document.getElementById("runtime");

    master.length = 0;
    axios
        .get("{{ url_for('sites.get_engines') }}", {
            headers: myHeaders
        })
        .then(function (response) {
            //console.log("Dados: ", response.status, response.data);
            response.data.forEach(function(item, i) {
                //console.log("Index: ", i, "Key: ", item[0], " Value: ", item[1]);
                master.options[i]=new Option(item.description, item.runtime);
            });
            // If must set current select engine
            if (current_engine !== undefined) {
                master.value = current_engine;
            }
            // Now update the sitetype's select because Axios call is defered
            //chgTypes();
            // If must set current select engine
            if (current_type !== undefined && typeof current_type === 'string') {
                chgTypes(current_type);
            } else {
                chgTypes();
            }
        })
        .catch(function (error) {
            if (error.response) {
                // The request was made and the server responded with a status code
                // that falls out of the range of 2xx
                console.log(error.response.data);
                console.log(error.response.status);
                console.log(error.response.headers);
            } else if (error.request) {
                // The request was made but no response was received
                // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
                // http.ClientRequest in node.js
                console.log(error.request);
            } else {
                // Something happened in setting up the request that triggered an Error
                console.log('Error', error.message);
            }
            console.log(error.config);
        });

    return true;
}





