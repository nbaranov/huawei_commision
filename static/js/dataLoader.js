fetch("/api-v1/devices/")
    .then((response) => response.json())        
    .then((data) => {
        const devices = []
        for (const device of data.results) {
            devices[device.id] = device.name
        }
        sessionStorage.setItem('devs', JSON.stringify(devices))
    })

fetch("/api-v1/categoryes/")
    .then((response) => response.json())
    .then((data) => {
        const categoryes = []
        for (const categpry of data.results) {
            categoryes[categpry.id] = categpry.name
        }
        sessionStorage.setItem('cat', JSON.stringify(categoryes))
    })
