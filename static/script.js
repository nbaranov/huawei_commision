// console.log("I'm loaded!");

function colorize(clas, element) {
    console.log("gotten class", clas);
    let divOutputBlock = element.parentNode.previousElementSibling;
    let clasList = divOutputBlock.classList  
    clasList.remove('ok')
    clasList.remove('false')
    clasList.add(clas)
    
    let textarea = divOutputBlock.getElementsByClassName("comment")[0]
    console.log(textarea);
    if (clas === 'false' && !textarea) {
        html_to_insert = `
        <textarea placeholder="Comment" class="comment"> </textarea>
        `
        divOutputBlock.insertAdjacentHTML('beforeend', html_to_insert);
    } else if (clas === 'ok' && textarea) {
        divOutputBlock.removeChild(textarea)
    }
}

function delay(time) {
    return new Promise(resolve => setTimeout(resolve, time));
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

console.log(categoryes);
console.log(commands);