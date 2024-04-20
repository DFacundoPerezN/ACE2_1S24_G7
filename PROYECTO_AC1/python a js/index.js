const exampleString = 'Habitacion1:0,1,0,0;0,0,1,0;1,0,0,0;0,0,0,0'

//Split the string in the : , then split the second part in the ; and then split each of the resulting strings in the ,
//Then with the result of each array at the end search for the 1s and get the index of the 1s
//Write the obtained result like, person found at [0,index] and so on, knowing that when we split in the ;
//This is a new row of a matrix, so the first number is the row and the second is the column

const result = exampleString.split(':')[1].split(';').map((row, rowIndex) => {
    return row.split(',').map((column, columnIndex) => {
        if (column === '1') {
        return `Person found at [${rowIndex},${columnIndex}]`
        }
    })
    }).flat().filter(Boolean)

console.log(result)
