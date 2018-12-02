
// Helpers
const ord = Function.prototype.call.bind(''.charCodeAt);
const chr = String.fromCharCode;
const str = String;

const source = '¢×&Ê´cÊ¯¬$¶³´}ÍÈ´T©Ð8Í³Í|Ô÷aÈÐÝ&¨þJ'
const codes = Array.from(source).map(c => c.charCodeAt())
const allBytes = Array.from({ length: 256 }, (_, i) => i)


function isValid(s) {
    return /^[0-9a-zA-Z_@!?-]+$/.test(s)
}


function computeKeys(possibilites) {
    let keys = [possibilites[0]]

    for (let i = 1; i < possibilites.length; i++) {
        const possible = possibilites[i]
        const next = []
        
        for (let n of possible) {
            keys.forEach(l => next.push(l.concat(n)))
        }
    
        keys = next
    }

    return keys
}


function findKeys(codes, validator, keySize) {
    const possibilites = []

    for (let offset = 0; offset < keySize; offset++) {
        let group = codes.filter((_, i) => (i % keySize) == offset)

        possibilites.push(allBytes.filter(i => {
            let decoded = group.map(c => chr(c ^ i)).join('')
            return validator(decoded)
        }))
    }

    return computeKeys(possibilites)
}


const keySize = 4
findKeys(codes, isValid, keySize)
    .map(key => codes.map((c, i) => chr(c ^ key[i % 4])).join(''))
    .forEach(key => console.log(key))
