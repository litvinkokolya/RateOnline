const names = document.querySelectorAll('.evaluations-name--referee')
const items = document.querySelectorAll('.evaluations-item--referee')
const sizes =[]
for (const i of names) {
    sizes.push(i.offsetHeight + "px")
}  
const resize = (col) => {
    let iter = 0;
    for (const elem of col) {
        elem.style.height = sizes[iter]
        iter++;
    }
}
resize(names)
resize(items)
