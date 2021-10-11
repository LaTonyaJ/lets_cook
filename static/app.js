

$("[class|='thumb']").on('click', (evt) => {
    console.log(evt.target.id);
    var id = evt.target.id.split('-');
    var fav_id = id[1];
    window.location = `/favorite/${fav_id}`
})

