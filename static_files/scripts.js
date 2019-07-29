const addButton =  document.querySelector("#add");
var classes = [];

function showClasses() {
    var d = document.getElementById("MyClasses");
    var html = '';
    for (var i = 0; i < classes.length; i++) {
        html += '<input type="text" name="classes' + i + '" id="classes' + i + '"><br><br>';
    }
    d.innerHTML = html;
    for (var i = 0; i < classes.length; i++) {
        document.getElementById("classes" + i).value = classes[i];
    }
}

function collectClasses() {
    for (var i = 0; i < classes.length; i++) {
        var value = document.getElementById("classes" + i).value;
        console.log(value);
        classes[i] = value;
    }
}

addButton.addEventListener("click", (event) => {
    collectClasses();
    classes.push('your-class-name');
    showClasses();
});

const removeButton =  document.querySelector("#remove");

removeButton.addEventListener("click", (event) => {
    collectClasses();
    classes.pop();
    showClasses();
});