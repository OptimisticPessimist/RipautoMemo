async function writeUser() {
    let element = document.getElementsByName('information');
    let picture = element[0].value;
    let user_name = element[1].value;
    let nickname = element[2].value;
    let date = element[3].value;
    let place = element[4].value;
    let tag1 = element[5].value;
    let tag2 = element[6].value;
    let tag3 = element[7].value;
    let tag4 = element[8].value;
    let tag5 = element[9].value;
    let uid = element[10].value;
    let memo = document.getElementsByName('input-memo')[0].value;

    let userData = {
        "uid": uid,
        "user_name": user_name,
        "nickname": nickname,
        "img_path": picture,
        "met": date,
        "place": place,
        "tag1": tag1,
        "tag2": tag2,
        "tag3": tag3,
        "tag4": tag4,
        "tag5": tag5,
        "memo": memo
    }

    await eel.insert_db(userData)();
}


function previewImage(obj) {
    let fileReader = new FileReader();
    fileReader.onload = (function() {
        document.getElementById("preview").src = fileReader.result;
    });
    fileReader.readAsDataURL(obj.files[0]);
}


async function getFriend() {
    const urlParam = location.search.substring(1);
    if (urlParam) {
        const param = urlParam.split('&');
        let paramArray = Array();
        let item;
        for (item of param) {
            const paramItem = item.split('=');
            paramArray[paramItem[0]] = paramItem[1];
        }

        const user = await eel.select_by_id_db(paramArray['id'])();

        let preview = document.querySelector('#preview');
        preview.src = '.' + user.img_path;
        let userName = document.querySelector('#user-name');
        userName.value = user.user_name;
        let nickname = document.querySelector('#nickname');
        nickname.value = user.nickname;
        let met = document.querySelector('#met');
        met.value = user.met;
        let place = document.querySelector('#place');
        place.value = user.place;
        let tag1 = document.querySelector('#tag1');
        tag1.value = user.tags[0];
        let tag2 = document.querySelector('#tag2');
        tag2.value = user.tags[1];
        let tag3 = document.querySelector('#tag3');
        tag3.value = user.tags[2];
        let tag4 = document.querySelector('#tag4');
        tag4.value = user.tags[3];
        let tag5 = document.querySelector('#tag5');
        tag5.value = user.tags[4];
        let uid = document.querySelector('#uid');
        uid.value = user.uid;
        let memo = document.querySelector('#input-memo');
        memo.value = user.memo;
    }
}
