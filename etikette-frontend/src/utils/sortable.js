

function updateMovedObject(moved, reactiveArray) {
    let movedObject = reactiveArray.find(object => object === moved.element)
    movedObject.order = moved.newIndex
    return movedObject
}


function updateAllObjectsOrder(moved, objects, movedObject) {
    // Update the order of all objects in the given array and returns an array of the updated objects.
    let updatedObjectArray = []
    objects.forEach(object => {
        let updatedObject = updateObjectOrder(moved, object, movedObject)
        updatedObjectArray.push(updatedObject)
    })
    return updatedObjectArray
}

function updateObjectOrder(moved, object, movedObject) {
    let [oldPosition, newPosition, highPosition, lowPosition] = getPositions(moved)
    if (!(object == movedObject) && lowPosition <= object.order && object.order <= highPosition) {
        if (object.order === newPosition) { object.order += object.order > oldPosition ? -1 : 1 }
        else {object.order += object.order > newPosition ? 1 : -1}
    }
    return object
}

function getPositions(moved) {
    // Gets all variations of positions from the SortableJS/Vue.Draggable component.
    // Takes in a moved object FROM that component.
    let oldPosition = moved.oldIndex
    let newPosition = moved.newIndex
    let highPosition = Math.max(oldPosition, newPosition)
    let lowPosition = Math.min(oldPosition, newPosition)
    return [oldPosition, newPosition, highPosition, lowPosition]
} 

export {
    updateMovedObject,
    updateAllObjectsOrder,
    updateObjectOrder,
    getPositions
}
