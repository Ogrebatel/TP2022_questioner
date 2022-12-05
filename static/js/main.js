function like_dislike_resolver(event) {
    var formBody = []
    formBody.push('object_id=' + $(this).data('object_id'))
    formBody.push('object_type=' + $(this).data('object_type'))
    formBody = formBody.join("&");

    const request = new Request(
        event.data.url,
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            },
            body: formBody,

        }
    )

    fetch(request).then(
        responce=> responce.json().then(
            responce => {
                $(this).parent().parent().parent().find("#likes_count")
                    .get("0").innerHTML = responce.likes_count
            }
        )
    );
}

$(".like_btn").on('click', {url: 'http://127.0.0.1:8000/like/'}, like_dislike_resolver)
$(".dislike_btn").on('click', {url: 'http://127.0.0.1:8000/dislike/'}, like_dislike_resolver)