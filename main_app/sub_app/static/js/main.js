// const form = document.getElementById('form');


// form.addEventListener('submit', (e) => {
//     e.preventDefault();

//     getValue();

// })

// function getValue(){
//     const search = document.getElementById('search');
//     value = search.value;
//     var url = '/search/';

//     fetch(url, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrftoken,
//         },
//         body: JSON.stringify({'value': value})
//     })

//     .then((response) =>{
//         return response.json()
//     })

//     .then((data) =>{
//         console.log('data:', data)
//     })
    
// };

const likeBtns = document.querySelectorAll('.like');


for(var i = 0; i < likeBtns.length; i++){
    likeBtns[i].addEventListener('click', function(){
        var btnId = this.dataset.id
        var username = user
        console.log('btnId:', btnId, 'User:', username)
        addLike(btnId, username);
        if(location.href == 'http://127.0.0.1:8000/'){
            alert('Movie was add');
        }
        if(location.href == 'http://127.0.0.1:8000/user/'){
            window.location.reload()
            alert('Movie was delete')
        }
        else{
            alert('Movie was add')
        }

    })
}

    



function addLike(btnId, username){
    var url = '/like-movie/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'btnId': btnId, 'username': username})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data:', data)
    })
}