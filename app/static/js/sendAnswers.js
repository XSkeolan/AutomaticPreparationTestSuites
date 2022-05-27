function sendAnswers()
{
    var selectionAnswers = document.querySelectorAll('.list-group > input:checked');
    let selectedIds = []
    selectionAnswers.forEach(function(item, i, arr) {
        selectedIds.push(item.value)
    });

    let data = {
        "answers": selectedIds
    }

    var xhr = new XMLHttpRequest();
    var loc = location.href.split('/')
    var testid = loc[loc.length-1]
    xhr.open('POST', '/tests/'+testid+'/getResult', true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.send(JSON.stringify(data));

    xhr.onreadystatechange = function () {
        if(xhr.readyState == 4) {
            window.scrollTo({ top: 0, behavior: 'smooth' });
            if(xhr.status == 400)
            {
                console.log('400')
                var beginBtn = document.querySelector('.row.mt-4.mb-4');
                var msg = document.getElementById('info')
                console.log(msg)
                if(msg == null)
                {
                    var info = document.createElement('div');
                    info.id='info'
                    info.classList.add('alert')
                    info.classList.add('alert-danger');
                    info.setAttribute('role', 'alert');
                    info.innerText = 'Не на все вопросы были выбраны ответы';
                    beginBtn.appendChild(info);
                    console.log(beginBtn)
                }
            }
            else
            {
                var msg = document.getElementById('info')
                if(msg != null)
                {
                    document.getElementById(info).remove()
                }
                var rightAnswers = 0;
                var result = JSON.parse(xhr.responseText)
                for (const [key, value] of Object.entries(result['answers'])) {
                    var lables = document.querySelectorAll('.list-group > label')
                    var allAnswer = document.querySelectorAll('.list-group > input')
                    allAnswer.forEach(function(answer, i, arr){
                        if(answer.value==value)
                        {
                            lables.forEach(function(label, j, arr2){
                                if(label.getAttribute('for') == answer.id)
                                {
                                    label.setAttribute('style', 'background-color: #18bf4a8c; color: #000')
                                    rightAnswers++;
                                }
                            });
                        }
                    });
                    if(key != value)
                    {
                        selectionAnswers.forEach(function(answer, i, arr) {
                            if(answer.value == key)
                            {
                                answer.setAttribute('checked', false)
                                lables.forEach(function(label, j, arr2){
                                    if(label.getAttribute('for') == answer.id)
                                    {
                                        label.setAttribute('style', 'background-color: #ee42428c; color: #000')
                                    }
                                });
                            }
                        });
                    }
                }

                var card = document.querySelector('.card')
                var cardTexts = document.querySelectorAll('.card-text')
                cardTexts[0].textContent = 'Правильные ответы: ' + rightAnswers;
                cardTexts[1].textContent = 'Всего вопросов: ' + selectionAnswers.length;
                card.setAttribute('style', '')
            }
        };
    };
}

function openTest()
{
    var test = document.getElementById('mainTest');
    test.style='';

    var desc = document.querySelectorAll('.row > p')[1]
    desc.setAttribute('style','display: none');
    var beginBtn = document.getElementById('begin');
    beginBtn.style='display: none';
}
