var myCarousel = document.getElementById('imageCarousel')

myCarousel.addEventListener('slid.bs.carousel', function () {
    var filename = document.querySelector('.carousel-item.active > img').src

    var imageInfo = document.querySelector('#image')
    imageInfo.value = filename.substring(filename.lastIndexOf('/')+1)
})

window.addEventListener('DOMContentLoaded', (event) => {
    var ul = document.getElementById('questions');
    var divUl = ul.parentNode;
    while (ul.firstChild) {
        ul.removeChild(ul.lastChild);
    }
    document.querySelectorAll('ul')[1].childNodes
    var label = document.querySelectorAll('ul')[1].previousElementSibling;
    console.log(label)
    const $div = document.createElement('div')
    $div.classList.add('row');
    $div.classList.add('mb-2');
    const $labelDiv = document.createElement('div');
    $labelDiv.classList.add('col-6');
    $labelDiv.classList.add('col-sm');
    const $butDiv = document.createElement('div');
    $butDiv.classList.add('col-3');
    $butDiv.classList.add('col-sm');
//    $butDiv.classList.add('d-grid');
//    $butDiv.classList.add('gap-2');
//    $butDiv.classList.add('d-md-flex');
//    $butDiv.classList.add('justify-content-md-end');
    const $butDiv2 = document.createElement('div');
    $butDiv2.classList.add('col-3');
    $butDiv2.classList.add('col-sm');
//    $butDiv2.classList.add('d-grid');
//    $butDiv2.classList.add('gap-2');
//    $butDiv2.classList.add('d-md-flex');
//    $butDiv2.classList.add('justify-content-md-end');

    divUl.prepend($div);
    $div.appendChild($labelDiv);
    $div.appendChild($butDiv);
    $div.appendChild($butDiv2);
    $labelDiv.appendChild(label)
    


    const $but = document.createElement('button');
    $but.type = 'button';
    $but.textContent = 'Сгенерировать набор';
    $but.classList.add('btn');
    $but.classList.add('btn-primary');
    $but.classList.add('btn-sm');
    $but.onclick = () => {
        while (ul.firstChild) {
            ul.removeChild(ul.lastChild);
        }
        var listItems = document.querySelectorAll('.list-group-item');
        listItems = Array.prototype.slice.call(listItems);
        let c = listItems.map(item => item);
        for(i=0;i<(listItems.length>10 ? 10 : listItems.length);i++)
        {
            let ind = Math.floor(Math.random() * c.length);
            var currentInput = c[ind].children[0]
            var currentText = c[ind].childNodes[2].textContent.trim();
            var li = document.createElement('li');
            var input = document.createElement('input')
            var label = document.createElement('label')

            input.id = ul.id + '-' + i;
            input.name = ul.id;
            input.style = "list-style-type: none;";
            input.type = 'checkbox';
            input.checked = true;
            input.value = currentInput.getAttribute('value');

            label.htmlFor = ul.id + '-' + i
            label.textContent = currentText;
            li.appendChild(input);
            li.appendChild(label);
            ul.appendChild(li);
            c.splice(ind, 1)
        }
    }
    $butDiv.appendChild($but)
    const $addbut = document.createElement('button');
    $addbut.type = 'button';
    $addbut.textContent = 'Добавить вопрос';
    $addbut.classList.add('btn');
    $addbut.classList.add('btn-primary');
    $addbut.classList.add('btn-sm');
    $addbut.setAttribute('data-bs-toggle','modal');
    $addbut.setAttribute('data-bs-target','#selectQuestion');

    $butDiv2.appendChild($addbut)
});
function saveQuets()
{
var listItems = document.querySelectorAll('.list-group-item > input');
    var selectedQuestion = document.querySelectorAll('#questions > li > input');
    listItems.forEach(function(item, i, arr1) {
        selectedQuestion.forEach(function(quest, j, arr2) {
            if(item.getAttribute('value') == quest.getAttribute('value'))
            {
                quest.checked=item.checked;
            }
        });
    });
}

var myModalEl = document.getElementById('selectQuestion')
//myModalEl.addEventListener('hidden.bs.modal', function (event) {
//    var listItems = document.querySelectorAll('.list-group-item > input');
//    var selectedQuestion = document.querySelectorAll('#questions > li > input');
//    listItems.forEach(function(item, i, arr1) {
//        selectedQuestion.forEach(function(quest, j, arr2) {
//            if(item.getAttribute('value') == quest.getAttribute('value'))
//            {
//                quest.checked=item.checked;
//            }
//        });
//    });
//})
myModalEl.addEventListener('show.bs.modal', function (event) {
    var selectedQuestion = document.querySelectorAll('#questions > li > input');
    var listItems = document.querySelectorAll('.list-group-item > input');
    selectedQuestion.forEach(function(item, i, arr1) {
        listItems.forEach(function(listItem, j, arr2) {
            if(listItem.getAttribute('value') == item.getAttribute('value'))
            {
                listItem.checked=item.checked;
            }
        });
    });

    var searchQuest = document.getElementById('search');
    var labels = document.querySelectorAll('.list-group-item');
    searchQuest.oninput = function() {
        labels.forEach(function(item, j, arr2) {
            if(!item.childNodes[2].textContent.trim().includes(searchQuest.value))
            {
                item.setAttribute('style','display:none;')
            }
            else
            {
                item.setAttribute('style','')
            }
        });
    };
})