const eol = require('eol')
 const docschanged = (diff)=>{
    var str = diff.split("\n");
    //console.log(str)
    const lines = eol.split(diff)
    let count = 0;
    for (var i = 0; i < str.length; i++) {
        if (str[i].startsWith("diff") && (str[i].includes("md")||str[i].includes("txt")||str[i].includes("rst") )){
            count +=1
        }
    }
    return count
}

module.exports = docschanged;