

function objectsAreSame(x, y) {
    var objectsAreSame = true;
    for (var propertyName in x) {
        if (x[propertyName] !== y[propertyName]) {
            objectsAreSame = false;
            break
        }
    }
    return objectsAreSame
}


export {
    objectsAreSame,
}