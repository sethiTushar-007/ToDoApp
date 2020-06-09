function check() {
    var checkbox = document.getElementsByClassName('checkboxes');
    count = 0;
    for (var i = 0; i < checkbox.length; i++) {
        var list = document.getElementById('item%' + checkbox[i].getAttribute('id').split('-')[1])
        if (!checkbox[i].checked) {
            list.style.boxShadow = '0px 0px 20px 1px rgba(0,0,0,0.28)';
            count++;
        }
        else {
            list.style.boxShadow = '0px 0px 20px 1px rgba(0,0,0,0.095)';
        }
    }
    if (count === -1){
        count = 0;
    }
    document.getElementById('remaining-items').innerHTML = count;
}

check();

function checkall() {
    var checkbox = document.getElementsByClassName('checkboxes');
    for (var i = 0; i < checkbox.length; i++) {
        if (!checkbox[i].checked) {
            checkbox[i].checked = true;
            var list = document.getElementById('item%' + checkbox[i].getAttribute('id').split('-')[1])
            list.style.boxShadow = '0px 0px 20px 1px rgba(0,0,0,0.095)';
        }
    }
    check();
}
function uncheckall() {
    var checkbox = document.getElementsByClassName('checkboxes');
    for (var i = 0; i < checkbox.length; i++) {
        if (checkbox[i].checked) {
            checkbox[i].checked = false;
            var list = document.getElementById('item%' + checkbox[i].getAttribute('id').split('-')[1])
            list.style.boxShadow = '0px 0px 20px 1px rgba(0,0,0,0.28)';
        }
    }
    check();
}
function clicked(id) {
    var list = document.getElementById(id);
    var checkbox = document.getElementById('item-' + id.split('%')[1]);
    if (checkbox.checked) {
        list.style.boxShadow = '0px 0px 20px 1px rgba(0,0,0,0.095)';
    }
    else {
        list.style.boxShadow = '0px 0px 20px 1px rgba(0, 0, 0, 0.28)';
    }
    check();
}