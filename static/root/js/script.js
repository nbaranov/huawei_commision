window.onload = () => {
    loadCategoryes()
    loadDevices()
}

function colorize(el_class, element) {
    // console.log("gotten class", el_class);
    let divOutputBlock = element.parentNode.previousElementSibling;
    let clasList = divOutputBlock.classList  
    clasList.remove('ok')
    clasList.remove('false')
    clasList.add(el_class)
    
    let textarea = divOutputBlock.getElementsByClassName("comment")[0]
    // console.log(textarea);
    if (el_class === 'false' && !textarea) {
        html_to_insert = `
        <textarea placeholder="Comment" class="comment"></textarea>
        `
        divOutputBlock.insertAdjacentHTML('beforeend', html_to_insert);
    } else if (el_class === 'ok' && textarea) {
        divOutputBlock.removeChild(textarea)
    }
}

function generateHTML() {
    $.get('static/style.css', function (css) {
        saveHTML(css)
    })
}

    
function saveHTML(css) {
    const ip = document.getElementById('ip').value.trim()
    const ne = sessionStorage.getItem('ne')
    let new_doc = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>` + ne + ip + `</title>
    <style>
` + css + `
    </style>
</head>
<body>
    `
    let element = document.getElementById('output').cloneNode(true);
    let blocks = element.getElementsByClassName('block')
    for (const block of blocks) {
        let buttons = block.getElementsByClassName('button-block')
        for (const button of buttons) {
            block.removeChild(button)
        }
        const tav = block.getElementsByTagName('textarea')[0]
        if (tav) {
            div = document.createElement('div')
            div.classList.add('comment')
            div.innerHTML = 'Comment: ' + tav.value
            tav.parentNode.appendChild(div)
            tav.parentNode.removeChild(tav)
        }
    }    
    var bl = new Blob([new_doc, element.innerHTML, '</body>'], { type: "text/html" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(bl);
    a.download = ne + "_" + ip + ".html";
    a.hidden = true;
    document.body.appendChild(a);
    a.innerHTML = "something random";
    a.click();
}



function loadDevices() {
    fetch(("/api-v1/devices/"))
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            const devices = []
            for (const device of data.results) {
                devices[device.id] = device.name
            }
            sessionStorage.setItem('devs', JSON.stringify(devices))
            console.log("devices loaded ", { devices });
            return devices
        })
        .then((devices) => {
            devices = JSON.parse(sessionStorage.getItem('devs'))
            const node = document.getElementById("devices")
            for (let i = 0; i < devices.length; i++) {
                if (devices[i]) {
                    let html = document.createElement('div')
                    html.insertAdjacentHTML('beforeend', `
            <label>
                <input type="radio" id="`+ devices[i] + `" name="ne" 
                value=` + i.toString() + ` onclick="getCommands(` + i.toString() + `, this)">` + devices[i] +
                        `
            </label>
            `)
                    node.appendChild(html)
                }
            }
            node.getElementsByTagName("label")[0].click()
        })
}

function loadCategoryes() {
    fetch(("/api-v1/categoryes/"))
        .then((response) => {
            if (!response.ok) { throw new Error(`HTTP error: ${response.status}`); }
            return response.json();
        })
        .then((data) => {
            const devices = []
            for (const device of data.results) {
                devices[device.id] = device.name
            }
            sessionStorage.setItem("cat", JSON.stringify(devices))
            return devices
        })
}


function addCategory(cat_id) {
            let html = document.createElement('div');
            cat = JSON.parse(sessionStorage.getItem("cat"))[cat_id]
            html.classList.add('category');
            // console.log(html);
            html.insertAdjacentHTML('beforeend', `<label>
            <input class="category" type="checkbox" onclick="toogleCategory(this);">
            ` + cat + ` </label>`)
            return html
        }

        function getCommands(dev_id) {
            fetch("/api-v1/commands/?for_device=" + dev_id.toString())
                .then((response) => response.json())
                .then((data) => {
                    coms = data.results
                    catsIds = []
                    for (const com of coms) {
                        catsIds.push(com.category)
                    }
                    const uniqCatsIds = catsIds.filter(uniqueArrayFilter)
                    const commandsNode = document.getElementById("commands")
                    commandsNode.innerHTML = '';
                    for (cat_id of uniqCatsIds) {
                        filteredComs = coms.filter(com => com.category == cat_id)
                        // console.log({ filteredComs });
                        categoryNode = addCategory(cat_id)
                        for (const com of filteredComs) {
                            let div = document.createElement('div');
                            div.className = 'command';
                            div.innerHTML = `<label>
                                <input type="checkbox" name="` + com.command + `" 
                                onclick="updateCheckboxInGroup(this);" 
                                value=`+ com.id + `>`
                                + com.command + `</label>`
                            categoryNode.appendChild(div)
                        }
                        commandsNode.appendChild(categoryNode)
                    }
                })
        }


function toogleCategory(cat_node) {
    const curChecked = cat_node.checked
    cat_node = cat_node.parentNode.parentNode
    commands = cat_node.getElementsByClassName("command")
    for (const command of commands) {
        const input = command.getElementsByTagName('input')[0]
        input.checked = curChecked
    }
}

function updateCheckboxInGroup(element) {
    const container = element.parentNode.parentNode.parentNode 
    const overall = container.getElementsByTagName('input')[0]
    const ingredients = Array.from(container.getElementsByTagName('input')).slice(1)
    // console.log(ingredients);
    let checkedCount = 0;
    for (const ingredient of ingredients) {
      if (ingredient.checked) {
        checkedCount++;
      }
    }
  
    if (checkedCount === 0) {
      overall.checked = false;
      overall.indeterminate = false;
    } else if (checkedCount === ingredients.length) {
      overall.checked = true;
      overall.indeterminate = false;
    } else {
      overall.checked = false;
      overall.indeterminate = true;
    }
  }

function uniqueArrayFilter(value, index, array) {
    return array.indexOf(value) === index;
  }

function nl2br (str, is_xhtml) {
    if (typeof str === 'undefined' || str === null) {
        return '';
    }
    var breakTag = (is_xhtml || typeof is_xhtml === 'undefined') ? '<br />' : '<br>';
    return (str + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1' + breakTag + '$2');
}

function getIDList() {
    let com_divs = document.getElementsByClassName("command")
    com_divs = Array.from(com_divs)
    com_divs = com_divs.filter((obj) => obj.getElementsByTagName('input')[0].checked === true)
    id_list = []
    for (const div of com_divs) {
        id_list.push(Number(div.getElementsByTagName('input')[0].value));
    }
    return id_list
}

function getCredentials() {
    const ip = document.getElementById('ip').value.toString().trim()
    const login = document.getElementById('login').value.toString().trim()
    const password = document.getElementById('password').value.toString().trim()
    if (ip && login && password) {
        return {
            'ip': ip,
            'login': login,
            'password': password
        }
    } else alert("You need to input IP, Login and Password")
}

function runSocket() {
    const cred = getCredentials();
    console.log({cred});
    const id_list = getIDList();
    console.log({ id_list });
    if (id_list) {
        ws = new WebSocket('ws://' + window.location.toString().split('//')[1] + 'ws/checkne/')
        ws.onopen = function () {
            ws.send(JSON.stringify({
                'ip': cred.ip,
                'login': cred.login,
                'password': cred.password,
                'id_list': id_list
            }));
            container = document.getElementById('output')
            container.innerHTML = `<h2 id="status">Try to connect to ` + cred.ip + `</h2>`
        }
    }

    ws.onmessage = function (e) {
        console.log('runned onmessage method');
        console.log({e});
        data = JSON.parse(e.data)
        if (data.status) updateStatus(data.status)
        if (data.ne) sessionStorage.setItem('ne', data.ne)
        if (data.command) addOutputBlock(
                data.command,
                (data.output) ? data.check_status : "ok",
                (data.output) ? data.output : "Output is empty"
        )
        
    };

    ws.onerror = function(err) {
        console.error('Socket encountered error: ', err.message, 'Closing socket');
        updateStatus(`<h2 id="status">Error during work with NE </h2>`)
        ws.close();
      };
}

function updateStatus(stat) {
    container = document.getElementById('status')
    container.innerHTML = stat
}

function addOutputBlock(command, checkStatus , output) {
    comment = (checkStatus ===  'false') ? `<textarea placeholder="Comment" class="comment"></textarea>` : ''
    template = `<div class="block">
    <div class="output-block ` + checkStatus + `">
        <b>` + command + `</b>
        <pre>` + output + `</pre>
` + comment + `
    </div>
    
    <div class="button-block">
        <button class="button ok" onclick="colorize('ok', this)"> Ok </button>
        <button class="button false" onclick="colorize('false', this)"> False </button>
    </div>
</div>`
    
    container = document.getElementById('output')
    container.insertAdjacentHTML('beforeend', template)
}


function checkAll() {
    checkboxes = document.getElementsByClassName('category')
    for (const box of checkboxes) {
        if (box.checked === false) {
            box.click()
        }
    }
}

function uncheckAll() {
    checkboxes = document.getElementsByClassName('category')
    for (const box of checkboxes) {
        if (box.checked === true) {
            box.click()
        }
    }
}