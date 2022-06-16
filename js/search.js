function deleteAllCards() {
    const parentElement = document.getElementById('cards');

    while (parentElement.firstChild) {
        parentElement.removeChild(parentElement.firstChild);
    }
}


async function addAllCards() {
    deleteAllCards();
    const parentElement = document.getElementById('cards');
    const users = await eel.select_all_db()();

    let user;
    for (user of users) {
        const id = user[0];
        const img_path = user[1];
        const user_name = user[2];
        const nickname = user[3];
        const tags = user[4];
        const newElement = document.createElement('div');
        newElement.classList.add('cards__item');
        let content = '<div class="card__item__content">';
        content += '<div><img src=".' + img_path + '" width="320" height="180" onclick="linkFriend(' + id + ')"></div>';
        content += '<div class="cards__item__content__value">';
        content += '<div>ユーザー名: ' + user_name + '</div>';
        content += '<div>呼び方: ' + nickname + '</div>';
        content += '<div>';
        if (hasValue(tags[0])) {
            content += '<input type="button" value="' + tags[0] + '">';
        }
        if (hasValue(tags[1])) {
            content += '<input type="button" value="' + tags[1] + '">';
        }
        if (hasValue(tags[2])) {
            content += '<input type="button" value="' + tags[2] + '">';
        }
        if (hasValue(tags[3])) {
            content += '<input type="button" value="' + tags[3] + '">';
        }
        if (hasValue(tags[4])) {
            content += '<input type="button" value="' + tags[4] + '">';
        }
        content += '</div>';
        content += '</div>';
        content += '</div>';
        newElement.innerHTML = content;
        parentElement.appendChild(newElement);
    }
}


function hasValue(v) {
    return v !== "";
}


function linkFriend(id) {
    window.location.href = 'memo.html?id=' + id;
}