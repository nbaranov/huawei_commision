window.onload = () => {
    getDevices()
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

function generatePDF() {
    const ip = document.getElementById('ip').value.trim()
    const element = document.getElementById('output');
    let blocks = element.getElementsByClassName('block')
    for (const block of blocks) {
        let buttons = block.getElementsByClassName('button-block')
        for (const button of buttons) {
            block.removeChild(button)
        }
    }
    // textareas = document.getElementsByClassName('comment')
    // for (const ta of textareas) {
    //     ta.value = nl2br(ta.value)
    // }

    var opt = {
        margin: 0.2,
        filename:     ip +'.pdf',
        image:        { type: 'jpeg', quality: 0.4 },
        html2canvas:  { scale: 1, scrollX: 0, scrollY: 0 },
        jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
    };

    window.html2pdf().set(opt)
        .from(element)
        .save();
}


function getDevices() {
    devices = JSON.parse(sessionStorage.getItem('devs'))
    const node = document.getElementById("devices")
    // console.log("run getDevices functions", {devices});
    for (let i = 0; i < devices.length; i++) {
        if (devices[i]) {
            let html = document.createElement('div')
            html.insertAdjacentHTML('beforeend', `
            <label>
                <input type="radio" id="`+ devices[i] + `" name="ne" 
                value=` + i.toString() + ` onclick="getCommands(` + i.toString() +`, this)">` + devices[i] + 
                `
            </label>
            `)
            node.appendChild(html)
        }
    }
    node.getElementsByTagName("label")[0].click()
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

        function getCommands(dev_id, dev_div) {
            // console.log("run getCommands for device with id", {dev_id}, {dev_div});
            // get commands from DB
            fetch("/api-v1/commands/?for_device=" + dev_id.toString())
                .then((response) => response.json())
                .then((data) => {
                    coms = data.results
                    // console.log({coms});
            // get list of unique categoryes
                    catsIds = []
                    for (const com of coms) {
                        catsIds.push(com.category)
                    }
                    const uniqCatsIds = catsIds.filter(uniqueArrayFilter)
            // create elements for command by categoryes
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
                                value=`+ com.id + `">`
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