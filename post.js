function post(user, date, title, body) {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', `/data`, true);
    xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
        console.log(JSON.parse(xhr.responseText)); // Parse JSON data
    }
    };
    xhr.send();
}