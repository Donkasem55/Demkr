const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

let com = urlParams.get('comm');
console.log(com);
document.getElementById('newpostcomm').value = com;
if (urlParams.has("ref")) {
    window.location.assign(`/s/${com}`);
}

function post() {
    var npc = document.getElementById('newpostcomm').value;
    var npu = document.getElementById('newpostusername').value;
    var npt = document.getElementById('newposttitle').value;
    var npb = document.getElementById('newpostbody').value;

    fetch(window.location.href, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ comm: npc, user: npu, title: npt, body: npb })
    })
    setTimeout(() => {
        window.location.href = `/post?comm=${npc}&ref=true`;
    }, 150);
}