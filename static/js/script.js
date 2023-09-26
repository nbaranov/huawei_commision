window.onload = () => {
    loadCategoryes()
    loadDevices()
    loadCred()
}


function saveIP() {
    const ip = document.getElementById('ip').value.toString().trim()
    localStorage.setItem("ip", ip);
}
function saveLogin() {
    const login = document.getElementById('login').value.toString().trim()
    localStorage.setItem("login", login);
}
function savePassword() {
    const password = document.getElementById('password').value.toString().trim()
    localStorage.setItem("password", password);
}
function saveIPList() {
    const iplist = document.getElementById('iplist').value.toString().trim()
    localStorage.setItem("iplist", iplist);
}

function loadCred() {
    document.getElementById('ip').value = localStorage.getItem("ip");
    document.getElementById('login').value = localStorage.getItem("login");
    document.getElementById('password').value = localStorage.getItem("password");
    document.getElementById('iplist').value = localStorage.getItem("iplist");
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
            div.innerHTML = tav.value.replace(/\n/g, '<br>')
            tav.parentNode.appendChild(div)
            tav.parentNode.removeChild(tav)
        }
        let outputBlock = block.getElementsByClassName('output-block')[0]
        let hideButton = block.getElementsByClassName('acc_head')[0]
        // console.log(hideButton);
        if (hideButton) { outputBlock.removeChild(hideButton) }
        let hidetext = block.getElementsByClassName('acc_body')[0]
        hidetext.style.display = 'block'
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
            sessionStorage.setItem('devs', JSON.stringify(data.results))
            return data.results
        })
        .then((devices) => {
            const node = document.getElementById("devices")
            devices = JSON.parse(sessionStorage.getItem('devs'))
            // console.log(devices);
            sort_devices = devices.sort((a, b) => a.vendor > b.vendor ? 1 : -1);;
            for (const device of sort_devices) {
                // console.log(device)
                let html = document.createElement('div')
                html.insertAdjacentHTML('beforeend', `
            <label>
                <input type="radio" id="`+ device.id + `" name="ne" 
                value=` + device.id + ` onclick="getCommands(` + device.id + `, this)">` +
                    device.vendor + ` - ` + device.name + `
            </label>
            `)
                    node.appendChild(html)
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

function getCheckedVendor() {
    var ele = document.getElementsByName('ne');

    for (i = 0; i < ele.length; i++) {
        if (ele[i].checked)
            return ele[i].parentElement.textContent.split(' - ')[0].toLowerCase().trim()
    }
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
    const iplist = document.getElementById('iplist').value.toString().trim()
    if (ip && login && password) {
        return {
            'ip': ip,
            'login': login,
            'password': password,
            'iplist' : (iplist) ? iplist : ''
        }
    } else alert("Вам нужно ввести IP оборудования, Логин и Пароль")
}

function runSocket() {
    const cred = getCredentials();
    // console.log({cred});
    const vendor = getCheckedVendor()
    // console.log(vendor);
    const id_list = getIDList();
    // console.log({ id_list });
    if (id_list) {
        ws = new WebSocket('ws://' + window.location.toString().split('//')[1] + 'ws/checkne/')
        ws.onopen = function () {
            ws.send(JSON.stringify({
                'ip': cred.ip,
                'login': cred.login,
                'password': cred.password,
                'iplist': cred.iplist,
                'id_list': id_list,
                'vendor' : vendor
            }));
            container = document.getElementById('output')
            container.innerHTML = `<h2 id="status">Пытаюсь подключиться к ` + cred.ip + `</h2>`
        }
    }

    ws.onmessage = function (e) {
        // console.log('runned onmessage method');
        data = JSON.parse(e.data)
        // console.log({data});
        if (data.status) updateStatus(data.status)
        if (data.ne) sessionStorage.setItem('ne', data.ne)
        if (data.command) {
            addOutputBlock(
                data.command,
                (data.output) ? data.check_status : "ok",
                (data.output) ? data.output : "Output is empty",
                data.comment
            )
            fix_text_area()
        }
    };

    ws.onerror = function(err) {
        console.error('Socket encountered error: ', err.message, 'Closing socket');
        updateStatus(`<h2 id="status">Ошибка во время работы с оборудованием.</h2>`)
        ws.close();
      };
}

function updateStatus(stat) {
    container = document.getElementById('status')
    container.innerHTML = stat
}

function addOutputBlock(command, checkStatus , output, comment_text) {
    // console.log(comment_text);
    if (checkStatus === 'false') {
        comment = document.createElement("textarea");
        comment.placeholder = 'Comment'
        comment.classList.add("comment")
        comment.setAttribute("oninput", "auto_grow(this)");
        comment.innerHTML = comment_text
        
    }
    else { comment = '' }
    comment = (comment.outerHTML) ? comment.outerHTML : ''
    
    display = (output.split(/\n/g).length > 30) ? 'none' : 'block'
    show = (output.split(/\n/g).length > 30) ? 'Показать' : 'Скрыть'

    template = `<div class="block">
    <div class="output-block ` + checkStatus + `">
        <b>` + command + `</b>
        <button class="acc_head" onclick="showHide(this)">` + show +` вывод команды</button>
        <pre class="acc_body" style="display: ` + display + `;">` + output.replace(/\</g, "&lt;").replace(/\>/g, "&gt;") + `</pre>
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

function showHide(el) {
    // console.log({el});
    if (el.innerHTML === "Показать вывод команды") {
        el.innerHTML = "Скрыть  вывод команды"
    }
    else {
        el.innerHTML = "Показать  вывод команды"
    }
    $(el).siblings('.acc_body').slideToggle();
}

function auto_grow(element) {
    element.style.height = "5px";
    element.style.height = (element.scrollHeight) + "px";
}
  
function fix_text_area() {
    let comments = document.getElementsByClassName('comment');
    for (let i = 0; i < comments.length; i++) 
            auto_grow(comments[i]);
}
    
function dynamicSort(property) {
    var sortOrder = 1;
    if(property[0] === "-") {
        sortOrder = -1;
        property = property.substr(1);
    }
    return function (a,b) {
        /* next line works with strings and numbers, 
         * and you may want to customize it to your needs
         */
        var result = (a[property] < b[property]) ? -1 : (a[property] > b[property]) ? 1 : 0;
        return result * sortOrder;
    }
}