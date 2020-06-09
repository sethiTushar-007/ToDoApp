var parentElement = document.getElementById('notesID');
function focusMe(inputID) {
    var lastNote = document.getElementById(inputID);
    wantedID = Number(inputID.split('-')[1]);
    lastNote.removeAttribute('onfocus');
    var div_element = document.createElement('div');
    div_element.setAttribute('class', 'my-note');
    div_element.setAttribute('id', 'my-note-' + (wantedID + 1));
    var input_element = document.createElement('input');
    input_element.setAttribute('class', 'my-note-input');
    input_element.setAttribute('id', 'item-' + (wantedID + 1));
    input_element.setAttribute('type', 'email');
    input_element.setAttribute('onfocus', 'focusMe(this.id)')
    input_element.setAttribute('placeholder', 'Add Email');
    input_element.setAttribute('name', 'item' + (wantedID + 1));
    input_element.setAttribute('oninvalid', "this.setCustomValidity('Valid email ID is required')");
    input_element.setAttribute('oninput', "this.setCustomValidity('')");
    var button_element = document.createElement('button')
    button_element.setAttribute('id', 'x-' + (wantedID + 1));
    button_element.setAttribute('type', 'button');
    button_element.setAttribute('class', 'button');
    button_element.setAttribute('onclick', 'removeElement(this.id)');
    button_element.appendChild(document.createTextNode('X'));
    div_element.appendChild(input_element);
    div_element.appendChild(button_element);
    parentElement.appendChild(div_element);
};
function removeElement(buttonID) {
    var allNotes = document.getElementsByClassName('my-note-input');
    i = buttonID.split('-')[1];
    var targetElement = document.getElementById('my-note-' + i);
    var targetNote = document.getElementById('item-' + i);
    if (targetNote.hasAttribute('onfocus')) {
        var lastNote = allNotes[indexOfId(allNotes, targetNote) - 1];
        lastNote.setAttribute('onfocus', 'focusMe(this.id)');
    }
    for (j = Number(i) + 1; j <= allNotes.length; j++) {
        var noteid = document.getElementById('my-note-' + j);
        noteid.setAttribute('id', 'my-note-' + (j - 1));
        var note = document.getElementById('item-' + j);
        var btn = document.getElementById('x-' + j);
        note.setAttribute('id', 'item-' + (j - 1));
        note.setAttribute('name', 'item' + (j - 1));
        btn.setAttribute('id', 'x-' + (j - 1));
    }
    targetElement.remove();
};

function indexOfId(array, id) {
    for (var i = 0; i < array.length; i++) {
        if (array[i] == id) return i;
    }
    return -1;
}