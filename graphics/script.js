const canvas = document.getElementById('supermarket');
const ctxIconCustomer = canvas.getContext('2d');
const ctxIconCollition = canvas.getContext('2d');
const ctxSquare = canvas.getContext("2d");

const img = new Image();
img.src = "img/marker_client.png";

const imgCollition = new Image();
imgCollition.src = "img/red_alert.svg";

const imgPick = new Image();
imgPick.src = "img/grab.png";

const DIM = 40;

let tickets;
let customerColor = new Map();
let customerTickets = new Map();
let locationsShared;
let locationsCollition;
let locationsTotal = [];

let speedText = 1; // es podria multiplicar per 1000, 100, 10 o 1.
let speedValue = 1000;
let cw = canvas.width = container.offsetWidth;
let ch = canvas.height = container.offsetHeight;

document.getElementById('filePicker').addEventListener('change', readFile, false);
document.getElementById('speed_text').innerHTML = "Velocidad Actual: " + speedText;

/**
 * Read CSV file 
 * @param e file content
 */
function readFile(e) {
    tickets = new Map();
    var file = e.target.files[0];
    if (!file) {
        return;
    }
    var reader = new FileReader();
    reader.onload = function (e) {
        var data = e.target.result;
        getDataOfFile(data);
    };
    reader.readAsText(file);
}

// global dictionary count
let ticketsProductListing = {};
let ticketsToRows = {};
let shopOpeningTime;
/**
 * Get content of the CSV file, line by line, splitting it by semicolon.
 * @param contents Content of the file
 */
function getDataOfFile(contents) {
    const dataCSV = [];
    const breakLine = contents.split("\n");
    shopOpeningTime = caculateOpenDate(breakLine);
    let isPicking;
    let productList = 0;

    for (let i = 1; i < breakLine.length; i++) {
        let [customer_id, ticket_id, x, y, picking, x_y_date_time] = breakLine[i].split(';');
        var index = dataCSV.findIndex((element) => element[0] === customer_id);
        if (index === -1) {
            const sec = epochConverter(x_y_date_time, shopOpeningTime)
            if (tickets.has(ticket_id)) {
                const locationsList = tickets.get(ticket_id);
                // if(picking == '1') drawLocationGrab((x-1)*DIM,(y-1)*DIM);
                isPicking = picking == '1';

                // get the current elements to get
                locationsList.push({ x, y, sec, ticket_id, isPicking, customer_id, x_y_date_time });
                if (isPicking && (lastX != x || lastY != y)) {
                    productList++;
                    ticketsProductListing[ticket_id] = productList;
                }
                lastX = x;
                lastY = y;
                tickets.set(ticket_id, locationsList);
            }
            else { tickets.set(ticket_id, [{ x, y, sec, ticket_id, customer_id, x_y_date_time }]); }
            if (ticket_id) locationsTotal.push({ x: x, y: y, s: sec, t: ticket_id });
        }

    }
    getSharedAndCollitionLocations();
    calculateFirstcustomerSec();
}

/**
 * Generates an object with locations and time of the CSV file
 * @param locations customer list of locations points 
 * @return waypoints - object of locations and time
 */
function calcWaypoints(locations) {
    var waypoints = [];
    var time = locations[0].sec;
    for (var i = 0; i < locations.length; i++) {
        var pt = locations[i];
        var dx = (pt.x - 1) * DIM;
        var dy = (pt.y - 1) * DIM;
        waypoints.push({ x: dx, y: dy, s: pt.sec, t: (time + i), isPicking: pt.isPicking, ticket_id: pt.ticket_id });
    }
    return (waypoints);
}

/**
 *Calculates the first second of each ticket.
 */
async function calculateFirstcustomerSec() {
    for (let [key, value] of tickets) {
        const color = generateColor();
        customerTickets.set(color, key)
        customerColor.set(key, color)
        value = sortRouteByTime(value);
        const firstSecond = (+value[0].sec) * speedValue;
        const locations = calcWaypoints(value);
        if(key != undefined) ticketsToRows[key] = insertToTable(3, value[0].customer_id, firstSecond, 0, 0, key, value.length); // FIXME this is not correct
        await drawRouteAfterSeconds(locations, firstSecond, color);
    }
}
/**
 * Execute drawRoute function after first second given by calculateFirstcustomerSec function
 * @param locations customer list of locations points 
 * @param firstSecond customer first second
 * @param color HEX color value
 */
function drawRouteAfterSeconds(locations, firstSecond, color) {
    drawPreviousRoute(locations, color);
    setTimeout(() => {
        drawRoute(locations, color);
    }, firstSecond);
}
/**
 * Draw the customers route, with its image, and the color assigned to it. 
 * @param locationRoute customer list of locations points 
 * @param color HEX color value
 */
async function drawRoute(locationRoute, color) {
    const locRoute = locationRoute;
    let collition = false
    // debugger;
    for (let point of locRoute) {
        for (let loc of locationsCollition) {
            const x = ((+loc.split('U')[0]) - 1) * DIM
            const y = ((+loc.split('U')[1]) - 1) * DIM
            const s = ((+loc.split('U')[2]))
            if (point.s == s && point.x == x && point.y == y) {
                drawSquare(point.x, point.y, color);
                await sleep(speedValue);
                drawLocationsCollition(x, y)
                collition = true
                continue
            }
        }
        if (!collition) {
            if (point.s != point.t) {
                clearRoute(locRoute);
                return;
            }
            if (point.isPicking) {
                drawSquare(point.x, point.y, color);
                drawLocationGrab(point.x, point.y);
            }
            else {
                idOfRowToUpdate = ticketsToRows[point.ticket_id];
                statusCell = document.getElementById(idOfRowToUpdate);
                statusCell.innerHTML = '<span class="in-route">● </span>En ruta';

                drawSquare(point.x, point.y, color);
                ctxIconCustomer.drawImage(img, point.x, point.y, DIM, DIM);
            }

            await sleep(speedValue);

            drawSquare(point.x, point.y, color);
            if (point.isPicking) {
                drawLocationGrab(point.x, point.y);
            }

        } collition = false
    }
    await sleep((speedValue / 2));
    clearRoute(locRoute, color);

}

function shadeColor(color, percent) {

    var R = parseInt(color.substring(1, 3), 16);
    var G = parseInt(color.substring(3, 5), 16);
    var B = parseInt(color.substring(5, 7), 16);

    R = parseInt(R * (100 + percent) / 100);
    G = parseInt(G * (100 + percent) / 100);
    B = parseInt(B * (100 + percent) / 100);

    R = (R < 255) ? R : 255;
    G = (G < 255) ? G : 255;
    B = (B < 255) ? B : 255;

    var RR = ((R.toString(16).length == 1) ? "0" + R.toString(16) : R.toString(16));
    var GG = ((G.toString(16).length == 1) ? "0" + G.toString(16) : G.toString(16));
    var BB = ((B.toString(16).length == 1) ? "0" + B.toString(16) : B.toString(16));

    return "#" + RR + GG + BB;
}

// clearRoute(locRoute, orig_color);
let globalColor;

async function drawPreviousRoute(locationRoute, orig_color) {
    debugger;
    color = shadeColor(orig_color, +30);
    let counter = 0;

    const locRoute = locationRoute;
    let collition = false
    // debugger;
    for (let point of locRoute) {
        for (let loc of locationsCollition) {
            const x = ((+loc.split('U')[0]) - 1) * DIM
            const y = ((+loc.split('U')[1]) - 1) * DIM
            const s = ((+loc.split('U')[2]))
            if (point.s == s && point.x == x && point.y == y) {
                drawSquare(point.x, point.y, color);
                drawLocationsCollition(x, y)
                collition = true
                continue
            }
        }
        if (!collition) {
            if (point.s != point.t) {
                clearRoute(locRoute);
                return;
            }
            counter++;
            if (counter > 50) {
                let a = 1;
                counter = 0;
            }
            drawSquare(point.x, point.y, color);
            ctxIconCustomer.drawImage(img, point.x, point.y, DIM, DIM);




            drawSquare(point.x, point.y, color);


        } collition = false
    }
    globalColor = orig_color;
}

/**
 * Deletes the points of the route, when the customer leaves the store 
 * @param locationRoute customer list of locations points 
 * @param color HEX color value
 * @return returns
 */
function clearRoute(locationRoute, color) {
    
    for (let point of locationRoute) { ctxSquare.clearRect(point.x, point.y, DIM, DIM); }
    const lastLocation = locationRoute[locationRoute.length - 1]
    const colorTicket = customerTickets.get(color);
    for (let [key, value] of locationsShared) {
        if(color != undefined){
            // if color is set, we've finished the route
            idOfRowToUpdate = ticketsToRows[lastLocation.ticket_id];
            statusCell = document.getElementById(idOfRowToUpdate);
            statusCell.innerHTML = '<span class="finished">● </span>Finalizado';
            
        }
        if (value.length == 0) continue
        value.delete(colorTicket);
        locationsShared.set(key, value);

    }
    for (let [key, value] of locationsShared) {
        for (let ticket of value) {
            if (lastLocation.s > (+key.split('U')[2])) {
                drawSquare(((+key.split('U')[0]) - 1) * DIM, ((+key.split('U')[1]) - 1) * DIM, customerColor.get(ticket));
            }
        }
    }
    for (let loc of locationsCollition) {
        if (lastLocation.s > (+loc.split('U')[2])) {
            drawLocationsCollition(((+loc.split('U')[0]) - 1) * DIM, ((+loc.split('U')[1]) - 1) * DIM);
        }
    }

}


/**
 * Function for draw square with specific color
 * @param x x location 
 * @param y y location
 * @param color HEX color value
 */
function drawSquare(x, y, color) {
    ctxSquare.lineCap = 'square';
    ctxSquare.fillStyle = color;
    ctxSquare.fillRect(x, y, DIM, DIM);
}

/**
 * Generates a new different color.
 * @return randomColor
 */
function generateColor() {
    let maxVal = 0xFFFFFF;
    let randomColor;
    do {
        randomColor = Math.floor(Math.random() * maxVal);
    } while (randomColor === 0xFFFFFF);
    let randColor = randomColor.toString(16).padStart(6, "0");
    return `#${randColor.toUpperCase()}`
}
/**
 * Waits ms seconds
 * @param ms miliseconds
 */
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
/**
 * Function called from html buttons, that modifies the speed of the route. 
 * Also modifies the text shown between the buttons. 
 * @param buttonAction passing add or remove depending on which button is clicked. 
 */
function modifySpeed(buttonAction) {

    if (buttonAction == 'add' && speedText < 4) {
        speedText = speedText + 1;
        speedValue = speedValue / 10;
    } else if (buttonAction == 'remove' && speedText > 1) {
        speedText = speedText - 1;
        speedValue = speedValue * 10;
    }
    document.getElementById('speed_text').innerHTML = "Velocitat Actual: " + speedText;
}


/**
 *Converts date and time from the CSV file to epoctime and returns milliseconds.
 * @param date day and time format like "yyyy-mm-dd hh:mm:ss"
 * @param shopOpeningTime epochtime of the shop open time.
 * @return milliseconds
 */
function epochConverter(date, shopOpeningTime) {
    var epochtime = Date.parse(date);
    return ((epochtime - shopOpeningTime) / 1000);
}

// reverse epochConverter
function epochConverterReverse(seconds, shopOpeningTime) {
    var epochtime = seconds * 1000 + shopOpeningTime;
    return (new Date(epochtime));
}

/**
 * Sort arrayValues by time and returns it.
 * @param arrayValues array of locations and time
 * @return arrayValues
 */
function sortRouteByTime(arrayValues) {
    for (var i = 0; i < arrayValues.length; i++) {
        for (var j = i + 1; j < arrayValues.length; j++) {
            if (arrayValues[i].sec > arrayValues[j].sec) {
                let lineValueAux = arrayValues[i];
                arrayValues[i] = arrayValues[j];
                arrayValues[j] = lineValueAux;
            }
        }
    }
    return (arrayValues);
}

/**
 * Read the date (day) of the breakLine, set the time to 9:00 and returns it in epochtime.
 * @param breakLine line from CSV file
 * @return epochtime of the shop opening time
 */
function caculateOpenDate(breakLine) {
    let [a, b, c, d, e, date] = breakLine[1].split(';');
    let datestr = date.substring(0, 10);
    let timestr = "09:00:00";
    datestr = datestr.concat(" ", timestr);
    return Date.parse(datestr);
}
/**
 * Function that draws all the collitions.
 */
function drawLocationsCollition(x, y) {
    ctxIconCollition.drawImage(imgCollition, x, y, DIM, DIM);
}


function drawLocationGrab(x, y) {
    ctxIconCollition.drawImage(imgPick, x, y, DIM, DIM);
}
/**
 * Function to set a Shared locations list 
 * and collition location list.
 */
function getSharedAndCollitionLocations() {
    locationsShared = new Map();
    locationsCollition = [];
    locationsTotal.forEach((element, index) => {
        locationsTotal.forEach((loc, i) => {
            const idList = loc.x.concat('U').concat(loc.y).concat('U').concat(loc.s);
            if (element.x == loc.x && element.y == loc.y && element.s == loc.s && i != index) {
                if (locationsCollition.indexOf(idList) == -1) locationsCollition.push(idList)
            }
            if (element.x == loc.x && element.y == loc.y && element.t != loc.t && i != index) {
                const idList = loc.x.concat('U').concat(loc.y).concat('U').concat(loc.s);
                if (locationsShared.has(idList)) {
                    const newList = locationsShared.get(idList);
                    newList.add(loc.t);
                    locationsShared.set(idList, new Set(newList));
                }
                else { locationsShared.set(idList, new Set([loc.t])); }
            }
        });
    });
}



function insertToTable(status, client_id, entry_time, exit_time, start_time, ticket_id) { // TODO: Add qty_articles_picked so we can do ex: 2/30

    // Define the content of the new row using variables
    if (status == 1) {
        statusClass = 'completed';
        statusText = 'Completado';
    }
    else if (status == 2) {
        statusClass = 'in-route';
        statusText = 'En ruta';
    }
    else if (status == 3) {
        statusClass = 'waiting';
        statusText = 'Esperando';
    }

    // define status class 


    // var statusClass = 'completed'; // Use 'completed', 'in-route', or 'waiting' accordingly
    // var statusText = 'Completado'; // Use 'Completado', 'En ruta', or 'En espera' accordingly
    var clientNumber = client_id;
    var entryTime = tickets.get(ticket_id)[0].x_y_date_time;
    var exitTime = tickets.get(ticket_id)[tickets.get(ticket_id).length - 1].x_y_date_time;
    var duration = epochConverter(exitTime,shopOpeningTime)-epochConverter(entryTime, shopOpeningTime); // this is in secs




    // convert this seconds into h,m,s
    var hours = Math.floor(duration / 3600);
    var minutes = Math.floor((duration - (hours * 3600)) / 60);
    var seconds = duration - (hours * 3600) - (minutes * 60);
    duration = hours + 'h, ' + minutes + 'm, ' + seconds+ 's ';

    
    var ticketNumber = ticket_id;
    var itemCount = ticketsProductListing[ticket_id];

    // Find the table within the 'statuses' div
    var tableBody = document.getElementById('statuses');
    if (!tableBody) {
        console.error('Table body not found inside #statuses');
        return;
    }

    // Create the new row and cells
    var newRow = document.createElement('tr');
    
    // Append the status cell
    var statusCell = document.createElement('td');
    statusCell.id = "id"+ticket_id;
    var statusSpan = document.createElement('span');
    statusSpan.className = statusClass;
    statusSpan.textContent = '● ';
    statusCell.appendChild(statusSpan);
    statusCell.append(statusText);
    newRow.appendChild(statusCell);

    // Append other cells
    var clientCell = document.createElement('td');
    clientCell.textContent = clientNumber;
    newRow.appendChild(clientCell);

    var entryCell = document.createElement('td');
    entryCell.textContent = entryTime;
    newRow.appendChild(entryCell);

    var exitCell = document.createElement('td');
    exitCell.textContent = exitTime;
    newRow.appendChild(exitCell);

    var durationCell = document.createElement('td');
    durationCell.textContent = duration;
    newRow.appendChild(durationCell);

    var ticketCell = document.createElement('td');
    ticketCell.textContent = ticketNumber;
    newRow.appendChild(ticketCell);

    var itemCell = document.createElement('td');
    itemCell.textContent = itemCount;
    newRow.appendChild(itemCell);

    // Append the new row to the table body
    tableBody.appendChild(newRow);

    return "id"+ticket_id;
}

// Call the function to append the row
