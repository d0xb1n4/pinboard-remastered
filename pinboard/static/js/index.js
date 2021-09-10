// функция-конструктор Toast (для создания объектов Toast)
var Toast = function (element, config) {
// приватные переменные класса Toast
    var
        _this = this,
        _element = element,
        _config = {
            autohide: true,
            delay: 5000
        };
// установление _config
    for (var prop in config) {
        _config[prop] = config[prop];
    }
// get-свойство element
    Object.defineProperty(this, 'element', {
        get: function () {
            return _element;
        }
    });
// get-свойство config
    Object.defineProperty(this, 'config', {
        get: function () {
            return _config;
        }
    });
// обработки события click (скрытие сообщения при нажатии на кнопку "Закрыть")
    _element.addEventListener('click', function (e) {
        if (e.target.classList.contains('toast__close')) {
            _this.hide();
        }
    });
}
// методы show и hide, описанные в прототипе объекта Toast
Toast.prototype = {
    show: function () {
        var _this = this;
        this.element.classList.add('toast_show');
        if (this.config.autohide) {
            setTimeout(function () {
                _this.hide();
            }, this.config.delay)
        }
    },
    hide: function () {
        this.element.classList.remove('toast_show');
    }
};
// статическая функция для Toast (используется для создания сообщения)
Toast.create = function (text, color) {
    var
        fragment = document.createDocumentFragment(),
        toast = document.createElement('div'),
        toastClose = document.createElement('button');
    toast.classList.add('toast');
    toast.style.backgroundColor = 'rgba(' + parseInt(color.substr(1, 2), 16) + ',' + parseInt(color.substr(3, 2), 16) + ',' + parseInt(color.substr(5, 2), 16) + ',0.5)';
    toast.textContent = text;
    toastClose.classList.add('toast__close');
    toastClose.setAttribute('type', 'button');
    toastClose.textContent = '×';
    toast.appendChild(toastClose);
    fragment.appendChild(toast);
    return fragment;
};
// статическая функция для Toast (используется для добавления сообщения на страницу)
Toast.add = function (params) {
    var config = {
        header: 'Название заголовка',
        text: 'Текст сообщения...',
        color: '#ffffff',
        autohide: true,
        delay: 5000
    };
    if (params !== undefined) {
        for (var item in params) {
            config[item] = params[item];
        }
    }
    if (!document.querySelector('.toasts')) {
        var container = document.createElement('div');
        container.classList.add('toasts');
        container.style.cssText = 'position: fixed; top: 15px; right: 15px; width: 250px;';
        document.body.appendChild(container);
    }
    document.querySelector('.toasts').appendChild(Toast.create(config.text, config.color));
    var toasts = document.querySelectorAll('.toast');
    var toast = new Toast(toasts[toasts.length - 1], {autohide: config.autohide, delay: config.delay});
    toast.show();
    return toast;
}

function error(text) {
    Toast.add({
        text: text,
        color: '#dc3545',
        autohide: true
    });
}

function success(text) {
    Toast.add({
        text: text,
        color: '#00e600',
        autohide: true
    })
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// Получаем нужный элемент
var element = document.querySelector('#target');

var Visible = function (target) {
    // Все позиции элемента
    var targetPosition = {
            top: window.pageYOffset + target.getBoundingClientRect().top,
            left: window.pageXOffset + target.getBoundingClientRect().left,
            right: window.pageXOffset + target.getBoundingClientRect().right,
            bottom: window.pageYOffset + target.getBoundingClientRect().bottom
        },
        // Получаем позиции окна
        windowPosition = {
            top: window.pageYOffset,
            left: window.pageXOffset,
            right: window.pageXOffset + document.documentElement.clientWidth,
            bottom: window.pageYOffset + document.documentElement.clientHeight
        };

    if (targetPosition.bottom > windowPosition.top && // Если позиция нижней части элемента больше позиции верхней чайти окна, то элемент виден сверху
        targetPosition.top < windowPosition.bottom && // Если позиция верхней части элемента меньше позиции нижней чайти окна, то элемент виден снизу
        targetPosition.right > windowPosition.left && // Если позиция правой стороны элемента больше позиции левой части окна, то элемент виден слева
        targetPosition.left < windowPosition.right) { // Если позиция левой стороны элемента меньше позиции правой чайти окна, то элемент виден справа
        // Если элемент полностью видно, то запускаем следующий код
        console.clear();
        console.log('Вы видите элемент :)');
    } else {
        // Если элемент не видно, то запускаем этот код
        console.clear();
    }
    ;
};

// Запускаем функцию при прокрутке страницы
window.addEventListener('scroll', function () {
    Visible(element);
});

const domain = 'http://127.0.0.1:8000/'

function DeletePin(pin_id) {
    let response = fetch(
        domain + 'api/deletePin/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify({
                pin_id: pin_id
            })
        });
    success('Пин удалён')
    document.getElementById(pin_id).remove()
}

async function SignUp() {
    success('Подождите')
    full_name = document.getElementById('signup-fullname').value
    password = document.getElementById('signup-password').value
    password1 = document.getElementById('signup-password1').value
    email = document.getElementById('signup-email').value

    if (password && email && password1 && full_name) {
        if (password === password1) {
            let response = await fetch(
                domain + 'api/signUp/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json;charset=utf-8'
                    },
                    body: JSON.stringify({
                        password: password,
                        email: email,
                        full_name: full_name
                    })
                });

            let res = await response.json()
            console.log(res)

            if (res['status'] === 'ERR') {
                error(res['data']['message'])
            } else {
                window.location.href = '/'
                success(res['data']['message'])
            }
        } else {
            error('Пароли не совпадают.')
        }
    } else {
        error('Ошибка. Одно из полей пустое, или неверно заполнено.')
    }
}


async function SignIn() {
    success('Авторизация...')
    password = document.getElementById('signin-password').value
    email = document.getElementById('signin-email').value

    if (password && email) {
        let response = await fetch(
            domain + 'api/signIn/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json;charset=utf-8'
                },
                body: JSON.stringify({
                    password: password,
                    email: email
                })
            });

        let res = await response.json()
        console.log(res)

        if (res['status'] === 'ERR') {
            error(res['data']['message'])
        } else {
            window.location.href = '/'
        }
    } else {
        error('Ошибка. Одно из полей пустое, или неверно заполнено.')
    }
}


function SignInHtml() {
    document.getElementById('sign').style.display = 'block'
    document.getElementById('up').style.display = 'none'
    document.getElementById('in').style.display = 'block'
    document.getElementById('content').style.display = 'none'
}

function SignUpHtml() {
    document.getElementById('sign').style.display = 'block'
    document.getElementById('up').style.display = 'block'
    document.getElementById('in').style.display = 'none'
    document.getElementById('content').style.display = 'none'
}

function CloseSignHtml() {
    document.getElementById('sign').style.display = 'none'
    document.getElementById('in').style.display = 'none'
    document.getElementById('content').style.display = 'block'
}

async function CancelSignUp(user_id) {
    let response = await fetch(
        domain + 'api/cancelSignUp/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify({
                user_id: user_id
            })
        });
    window.location.href = '/'
}


async function CheckAuthCode(username) {
    success('Проверяю код')
    let code = document.getElementById('code-input').value

    if (code) {
        let response = await fetch(
            domain + 'api/checkAuthCode/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json;charset=utf-8'
                },
                body: JSON.stringify({
                    username: username,
                    code: code
                })
            });
        let res = await response.json()

        if (res['data']['status'] === false) {
            error(res['data']['message'])
        } else {
            window.location.href = '/'
            success('Вы успешно зарегистрировались.')
        }
    } else {
        error('Ошибка. Одно из полей пустое.')
    }
}


async function SignOut() {
    let response = await fetch(
        domain + 'api/signOut/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json;charset=utf-8'
            }
        });
    let res = await response.json()
    window.location.href = '/'
}

let edit = false

function EditProfileHtml() {
    document.getElementById('profile').style.display = 'none'
    document.getElementById('profile-edit').style.display = 'block'

}

function CloseEditProfileHtml() {
    document.getElementById('profile').style.display = 'block'
    document.getElementById('profile-edit').style.display = 'none'
}


async function DeleteCapAndAvatar(user_id) {
    let formData = new FormData()
    formData.append('user_id', user_id)
    formData.append('cap', null)
    formData.append('avatar', null)

    let response = await fetch(
        domain + 'api/editAccount/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData
        })
    let res = await response.json()

    success('Шапка и фото профиля удалены. Обновите страницу, чтобы увидеть изменения.')
}


async function EditProfile(user_id) {
    let formData = new FormData()
    formData.append('user_id', user_id)
    formData.append('full_name', document.getElementById('full_name').value)
    formData.append('description', document.getElementById('description').value)
    formData.append('two_factor', document.getElementById('two_factor').checked)
    formData.append('cap', document.getElementById('cap').files[0])
    formData.append('avatar', document.getElementById('avatar').files[0])

    let response = await fetch(
        domain + 'api/editAccount/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData
        })
    let res = await response.json()

    success('Профиль изменён. Чтобы увидеть изменения перезагрузите страницу.')
}


async function CreatePin(username) {
    let img = document.getElementById('file-upload').files[0]
    if (document.getElementById('file-upload').files.length !== 0) {
        if (img['name'].includes('jpg') || img['name'].includes('jpeg') || img['name'].includes('gif') || img['name'].includes('png')) {
            let formData = new FormData()
            formData.append('username', username)
            formData.append('image', document.getElementById('file-upload').files[0])
            formData.append('title', document.getElementById('title').value)
            formData.append('description', document.getElementById('description').value)
            formData.append('sourse', document.getElementById('sourse').value)
            let response = await fetch(
                domain + 'api/createPin/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: formData
                })
            let res = await response.json()

            if (res['status'] === 'OK') {
                success('Пин создан')
                window.location.href = '/pin/' + res['data']['id'] + '/'

            } else {
                error(res['data']['message'])
            }
        } else {
            error('Для загрузки доступны только фото в формате PNG, JPEG и GIF')
        }
    } else {
        error('Фотография к пину обязятельна')
    }
}


async function LikeCheck(username, pin_id, set = false) {
    console.log(set)
    let response = await fetch(
        domain + 'api/likeCheck/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify({
                username: username,
                pin_id: pin_id,
                set: set
            })
        });
    let res = await response.json()
    console.log(res)

    if (res['data']['like'] === true) {
        if (set === true) {
            success('Пин добавлен на доску "понравившиеся"')
        }
        try {
            document.getElementById('likes').innerHTML = '❤'
        } catch {
            document.getElementById('likes' + pin_id).innerHTML = '❤'
        }
    } else {
        if (set === true) {
            success('Пин убран из доски "понравившиеся"')
        }

        try {
            document.getElementById('likes').innerHTML = '🤍'
        } catch {
            document.getElementById('likes' + pin_id).innerHTML = '🤍'
        }
    }
}

async function CreateComment(username, pin_id) {
    let response = await fetch(
        domain + 'api/createComment/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify({
                username: username,
                pin_id: pin_id,
                text: document.getElementById('comment-text').value
            })
        });
    document.getElementById('comment-text').value = ''
    success('Комментарий опубликован. Обновите страницу, чтобы увидеть его.')
}

async function DeleteComment(comment_id) {
    let response = await fetch(
        domain + 'api/deleteComment/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify({
                comment_id: comment_id
            })
        });
    document.getElementById(comment_id).remove()
    success('Комментарий удалён.')
}


async function Subscribe(from_username, to_username) {
    let response = await fetch(
        domain + 'api/subscribe/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify({
                from_username: from_username,
                to_username: to_username
            })
        });

    let res = await response.json()
    if (res['data']['subscribe'] === true) {
        success('Подписка оформлена.')
        document.getElementById('subscribe-button').innerHTML = 'Отписаться'
        document.getElementById('subscribers').innerHTML = parseInt(document.getElementById('subscribers').innerHTML) + 1
    }
    else {
        success('Подписка отменена.')
        document.getElementById('subscribe-button').innerHTML = 'Подписаться'
        document.getElementById('subscribers').innerHTML = parseInt(document.getElementById('subscribers').innerHTML) - 1
    }
}


async function CreateBoard(owner_id) {
    let img = document.getElementById('file-upload').files[0]
    if (document.getElementById('file-upload').files.length !== 0) {
        if (img['name'].includes('jpg') || img['name'].includes('jpeg') || img['name'].includes('gif') || img['name'].includes('png')) {
            if (document.getElementById('name').value) {
                let formData = new FormData()
                formData.append('owner_id', owner_id)
                formData.append('cover', document.getElementById('file-upload').files[0])
                formData.append('name', document.getElementById('name').value)

                let response = await fetch(
                    domain + 'api/createBoard/', {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        body: formData
                    })

                let res = await response.json()

                if (res['status'] === 'OK') {
                    success('Доска создана')
                    window.location.href = '/board/' + res['data']['id'] + '/'

                } else {
                    error(res['data']['message'])
                }
            } else {
                error('Название доски обязятально.')
            }
        } else {
            error('Для загрузки доступны только фото в формате PNG, JPEG и GIF')
        }
    } else {
        error('Обложка доски обязательна')
    }
}


function DeleteBoard(board_id) {
    let response = fetch(
        domain + 'api/deleteBoard/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify({
                board_id: board_id
            })
        });
    success('Доска удалена')
    location.reload()
}

function PinEditHtml() {
    document.getElementById('pin-edit').style.display = 'block'
    document.getElementById('pin-view').style.display = 'none'
}

function PinViewHtml() {
    document.getElementById('pin-edit').style.display = 'none'
    document.getElementById('pin-view').style.display = 'block'
}

async function PinEdit(username, pin_id) {
    let img = document.getElementById('file-upload').files[0]
    let formData = new FormData()
    formData.append('username', username)
    if (document.getElementById('file-upload').files.length !== 0) {
        if (img['name'].includes('jpg') || img['name'].includes('jpeg') || img['name'].includes('gif') || img['name'].includes('png')) {
            formData.append('image', document.getElementById('file-upload').files[0])
        } else {
            error('Для загрузки доступны только фото в формате PNG, JPEG и GIF')
        }
    }

    formData.append('title', document.getElementById('title').value)
    formData.append('description', document.getElementById('description').value)
    formData.append('sourse', document.getElementById('sourse').value)
    formData.append('pin_id', pin_id)

    let response = await fetch(
        domain + 'api/editPin/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData
        })
    let res = await response.json()

    if (res['status'] === 'OK') {
        success('Пин создан')
        window.location.href = '/pin/' + res['data']['id'] + '/'

    } else {
        error(res['data']['message'])
    }
}


async function PinAddToBoardHtml(user_id, pinid) {
    localStorage.setItem('pin_id', pinid);

    let response = await fetch(domain + 'api/general/?method=getUserBoards&user_id=' + user_id)
    let res = await response.json()

    if (res['data']['count'] === 0) {
        error('У вас нет досок')
    } else {
        console.log(res['data']['boards'])

        select = document.getElementById('boards-addpin');

        for (var board in res['data']['boards']) {
            console.log(res['data']['boards'][board]['id'])
            var opt = document.createElement('option');
            opt.value = res['data']['boards'][board]['name'];
            opt.innerHTML = res['data']['boards'][board]['name'];
            opt.value = res['data']['boards'][board]['id']
            select.appendChild(opt);
        }

        document.getElementById('content').style.display = 'none'
        document.getElementById('add-pin-to-board').style.display = 'block'
    }
}

function PinAddToBoardClose() {
    document.getElementById('content').style.display = 'block'
    document.getElementById('add-pin-to-board').style.display = 'none'
}


async function PinAddToBoard(pin_id) {
    var select = document.getElementById("boards-addpin");
    var board_id = select.value;
    console.log(board_id)


    let response = await fetch(
        domain + 'api/pinAddToBoard/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify({
                pin_id: localStorage.getItem('pin_id'),
                board_id: board_id
            })
        });
    let res = await response.json()
    PinAddToBoardClose()
    success('Пин сохранён на доску.')
}

async function PinDeleteToBoard(pin_id, board_id) {
    let response = await fetch(
        domain + 'api/pinDeleteToBoard/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify({
                pin_id: pin_id,
                board_id: board_id
            })
        });
    let res = await response.json()
    document.getElementById('pins_count').innerHTML = parseInt(document.getElementById('pins_count').innerHTML) - 1
    document.getElementById(pin_id).remove()
    success('Пин удалён из доски')
}


async function NewPassword(user_id) {
    let pass = document.getElementById('password').value
    let pass1 = document.getElementById('password1').value

    if (pass && pass1) {
        let response = await fetch(
        domain + 'api/newPassword/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify({
                password: pass,
                password1: pass1,
                user_id: user_id
            })
        });
        let res = await response.json()
        if (res['status'] === 'ERR') {
            error(res['data']['message'])
        }
        else {
            success(res['data']['message'])
            location.href = '/'
        }
    } else {
        error('Одно из полей пустое.')
    }
}