let emission = document.getElementById("emitted");
let metadata = document.getElementById("metadata");
let averageData = document.getElementById("averageData");

let data;

document.getElementById("csvForm").addEventListener("submit", function (e) {
  e.preventDefault(); // Prevent form submission

  let file = document.getElementById("csvFile").files[0];
  let reader = new FileReader();

  reader.onload = function (e) {
    let contents = e.target.result;
    data = parseCSV(contents);
    populateProjectDropdown(data);
    generateMetadata(data);
    plotEmissionRate(data);
    plotEnergyComparison(data);
    plotPowerComparison(data);
    displaySum(data);
  };

  reader.readAsText(file);
});


// Parsing CSV Input

function parseCSV(csv) {
  let lines = csv.split(/\r?\n/);
  let delimiter = lines[0].includes(";") ? ";" : ",";
  let headers = lines[0].split(delimiter);
  let data = [];

  for (let i = 1; i < lines.length; i++) {
    let row = lines[i].replace(/"/g, "").split(delimiter);
    let rowData = {};

    for (let j = 0; j < headers.length; j++) {
      let value = row[j] || "";
      rowData[headers[j]] = value.trim();
    }

    if (Object.values(rowData).some((val) => val !== "")) {
      data.push(rowData);
    }
  }

  return data;
}

// Run-id display
function outputRunId(data) {
  const RunId = data[0].run_id; 
  const runIdDiv = document.getElementById("run-id");
  runIdDiv.textContent = `Run ID: ${RunId}`;
}

// Populate the dropdown with unique project names
function populateProjectDropdown(data) {
  const projectDropdown = document.getElementById("projectDropdown");
  const projectNames = new Set(data.map((d) => d.project_name));

  projectDropdown.innerHTML = '<option value="">All Projects</option>';
  for (const projectName of projectNames) {
    const option = document.createElement("option");
    option.value = projectName;
    option.textContent = projectName;
    projectDropdown.appendChild(option);
  }
}

// per Project Display Button
function onRunButtonClick(e) {
  e.preventDefault();

  const selectedProject = document.getElementById("projectDropdown").value;
  const filteredData = selectedProject
    ? data.filter((d) => d.project_name === selectedProject)
    : data;


  generateMetadata(filteredData);
  plotEmissionRate(filteredData);
  plotEnergyComparison(filteredData);
  plotPowerComparison(filteredData);
  displayAverage(filteredData, selectedProject);
  outputRunId(filteredData)
}

document.getElementById("runButton").addEventListener("click", onRunButtonClick);


// Meta-data visualization

function generateMetadata(data) {
  const osVersion = data[0].os;
  const pythonVersion = data[0].python_version;
  const cpuCount = data[0].cpu_count;
  const cpuModel = data[0].cpu_model;
  const gpuCount = data[0].gpu_count;
  const gpuModel = data[0].gpu_model;
  const longitude = data[0].longitude;
  const latitude = data[0].latitude;
  const ramTotalSize = data[0].ram_total_size;
  const trackingMode = data[0].tracking_mode;

  metadata.innerHTML = `
    <div id='container'>
      <h3 id='MetadataHeader'> Metadata: </h3>
      <div><b>OS Version:</b> ${osVersion}</div>
      <div><b>Python Version:</b>  ${pythonVersion}</div>
      <div><b>Number of CPUs:</b>  ${cpuCount}</div>
      <div><b>CPU Model:</b>  ${cpuModel}</div>
      <div><b>Number of GPUs:</b>  ${gpuCount}</div>
      <div><b>GPU Model:</b>  ${gpuModel}</div>
      <div><b>Longitude:</b>  ${longitude}</div>
      <div><b>Latitude:</b>  ${latitude}</div>
      <div><b>RAM Total Size:</b>  ${ramTotalSize} GB</div>
      <div><b>Tracking Mode:</b>  ${trackingMode}</div>
    </div>
  `;

  return metadata;
}

//Emission rate VS Time

function plotEmissionRate(data) {
  const dates = data.map((d) => d.timestamp);
  const emissionRates = data.map((d) => parseFloat(d.emissions_rate));

  const trace = {
    x: dates,
    y: emissionRates,
    mode: 'lines',
    type: 'scatter',
    name: 'Emission Rate',
    marker: {
      color: '#009193',
    },
  };

  const layout = {
    xaxis: {
      title: 'Time',
    },
    yaxis: {
      title: 'Emission Rate',
    },
    font: {
      size: 10,
      color: 'white'
    },
    plot_bgcolor: "#222",
    paper_bgcolor: '#222'
  };

  const plotData = [trace];

  Plotly.newPlot('emissionRateChart', plotData, layout);
}

//RAM energy, GPU energy, CPU energy vs Energy Consumption
function plotEnergyComparison(data) {
  const energyConsumption = data.map((d) => parseFloat(d.energy_consumed));
  const ramEnergy = data.map((d) => parseFloat(d.ram_energy));
  const gpuEnergy = data.map((d) => parseFloat(d.gpu_energy));
  const cpuEnergy = data.map((d) => parseFloat(d.cpu_energy));

  const trace1 = {
    x: energyConsumption,
    y: ramEnergy,
    mode: 'lines',
    type: 'scatter',
    name: 'RAM Energy',
    marker: {
      color: '#1C82AD',
    },
  };

  const trace2 = {
    x: energyConsumption,
    y: gpuEnergy,
    mode: 'lines',
    type: 'scatter',
    name: 'GPU Energy',
    marker: {
      color: '#4E9F3D',
    },
  };

  const trace3 = {
    x: energyConsumption,
    y: cpuEnergy,
    mode: 'lines',
    type: 'scatter',
    name: 'CPU Energy',
    marker: {
      color: '#C147E9',
    },
  };

  const layout = {
    xaxis: {
      title: 'Energy Consumption',
    },
    yaxis: {
      title: 'Energy',
    },
    font: {
      size: 10,
      color: 'white'
    },
    plot_bgcolor: "#222",
    paper_bgcolor: '#222'
  };

  const plotData = [trace1, trace2, trace3];

  Plotly.newPlot('energyComparisonChart', plotData, layout);
}

//RAM power, GPU power, CPU power vs Power Consumption

function plotPowerComparison(data) {
  const powerConsumption = data.map((d) => parseFloat(d.energy_consumed));
  const ramPower = data.map((d) => parseFloat(d.ram_power));
  const gpuPower = data.map((d) => parseFloat(d.gpu_power));
  const cpuPower = data.map((d) => parseFloat(d.cpu_power));

  const trace1 = {
    x: powerConsumption,
    y: [ramPower.reduce((a, b) => a + b, 0)],
    type: 'bar',
    name: 'RAM Power',
    marker: {
      color: '#1C82AD',
    },
  };

  const trace2 = {
    x: powerConsumption,
    y: [gpuPower.reduce((a, b) => a + b, 0)],
    type: 'bar',
    name: 'GPU Power',
    marker: {
      color: '#4E9F3D',
    },
  };

  const trace3 = {
    x: powerConsumption,
    y: [cpuPower.reduce((a, b) => a + b, 0)],
    type: 'bar',
    name: 'CPU Power',
    marker: {
      color: '#C147E9',
    },
  };

  const layout = {
    barmode: 'group',
    xaxis: {
      title: 'Power Consumption',
    },
    yaxis: {
      title: 'Power',
    },
    font: {
      size: 10,
      color: 'white'
    },
    plot_bgcolor: "#222",
    paper_bgcolor: '#222'
  };

  const plotData = [trace1, trace2, trace3];

  Plotly.newPlot('powerComparisonChart', plotData, layout);
}



// Emission by Date

function getDateElement(e) {
  e.preventDefault()

  if(!data){
    alert('Data needed.')
    return
  }


  const inputElement = document.getElementById('date');
  const dateValue = inputElement.value;
  
  const slicedData = data.filter((d) => {
    const dataDate = d.timestamp.split('T')[0];
    return dataDate === dateValue;
  });

  slicedData.sort((a, b) => (a.timestamp < b.timestamp ? 1 : -1));

  // Create the chart with filtered emissions

  populateProjectDropdown(slicedData);

  generateMetadata(slicedData);
  plotEmissionRate(slicedData);
  plotEnergyComparison(slicedData);
  plotPowerComparison(slicedData);
  displayRecent(slicedData);

}

const dateSearch = document.getElementById('dateSearch');
dateSearch.addEventListener('submit', getDateElement);

// Emission by Range

function getRangeElements(e) {
  e.preventDefault()

  if(!data){
    alert('Data needed.')
    return
  }

  const startDateElement = document.getElementById('rangeStart');
  const endDateElement = document.getElementById('rangeEnd');
  
  const startDateValue = startDateElement.value;
  const endDateValue = endDateElement.value;

  if (startDateValue > endDateValue) {
    alert("Invalid date range");
    return;
  }

  const slicedData = data.filter((d) => {
    const dataDate = d.timestamp.split('T')[0];
    return dataDate >= startDateValue && dataDate <= endDateValue;
  });

  slicedData.sort((a, b) => (a.timestamp < b.timestamp ? 1 : -1));

  // Create the chart with filtered emissions

  populateProjectDropdown(slicedData);

  generateMetadata(slicedData);
  plotEmissionRate(slicedData);
  plotEnergyComparison(slicedData);
  plotPowerComparison(slicedData);
  displaySum(slicedData);
  
}


const rangeSearch = document.getElementById('RangeSearch');
rangeSearch.addEventListener('submit', getRangeElements);



//Sum energy consumed, emission produced and duration

function displaySum(data, selectedProject) {
  const filteredData = selectedProject
    ? data.filter((d) => d.project_name === selectedProject)
    : data;

  const energyValues = filteredData.map((d) => parseFloat(d.energy_consumed));
  const emissionValues = filteredData.map((d) => parseFloat(d.emissions));
  const durationValues = filteredData.map((d) => parseFloat(d.duration));

  const sumEnergy = energyValues.reduce((sum, value) => sum + value, 0);
  const sumEmission = emissionValues.reduce((sum, value) => sum + value, 0);
  const sumDuration = durationValues.reduce((sum, value) => sum + value, 0);

  const averageData = document.getElementById("averageData");
  averageData.innerHTML = '';

  averageData.innerHTML = `
    <div id='head'>
      <div id='circle'>
        <div id='dataCircle'><span id='avgNum'>${sumEnergy.toFixed(5)}</span> kwh</div>
        <h3>Energy Consumed</h3>
      </div>
      <div id='circle'>
        <div id='dataCircle'><span id='avgNum'>${sumEmission.toFixed(5)}</span> Kg.Eq.CO2</div>
        <h3>Emissions Produced</h3>
      </div>
      <div id='circle'>
        <div id='dataCircle'><span id='avgNum'>${sumDuration.toFixed(2)}</span> Sec</div>
        <h3>Duration</h3>
      </div>
    </div>
  `;
}


//Average energy consumed, emission produced and duration


function displayAverage(data, selectedProject) {
  const filteredData = selectedProject
    ? data.filter((d) => d.project_name === selectedProject)
    : data;

  const energyValues = filteredData.map((d) => parseFloat(d.energy_consumed));
  const emissionValues = filteredData.map((d) => parseFloat(d.emissions));
  const durationValues = filteredData.map((d) => parseFloat(d.duration));

  const totalEnergy = energyValues.reduce((sum, value) => sum + value, 0);
  const totalEmission = emissionValues.reduce((sum, value) => sum + value, 0);
  const totalDuration = durationValues.reduce((sum, value) => sum + value, 0);

  const averageEnergy = totalEnergy / energyValues.length;
  const averageEmission = totalEmission / emissionValues.length;
  const averageDuration = totalDuration / durationValues.length;

  const averageData = document.getElementById("averageData");
  averageData.innerHTML = '';

  averageData.innerHTML = `
    <div id='head'>
      <div id='circle'>
        <div id='dataCircle'><span id='avgNum'>${averageEnergy.toFixed(5)}</span> kwh</div>
        <h3>Energy Consumed</h3>
      </div>
      <div id='circle'>
        <div id='dataCircle'><span id='avgNum'>${averageEmission.toFixed(5)}</span> Kg.Eq.CO2</div>
        <h3>Emissions Produced</h3>
      </div>
      <div id='circle'>
        <div id='dataCircle'><span id='avgNum'>${averageDuration.toFixed(2)}</span> Sec</div>
        <h3>Duration</h3>
      </div>
    </div>
  `;
}


//Recent energy consumed, emission produced and duration

function displayRecent(data) {
  const energyValues = data.map((d) => parseFloat(d.energy_consumed));
  const emissionValues = data.map((d) => parseFloat(d.emissions));
  const durationValues = data.map((d) => parseFloat(d.duration));

  const averageEnergy = energyValues.reduce((sum, value) => sum + value, 0) ;
  const averageEmission = emissionValues.reduce((sum, value) => sum + value, 0) ;
  const averageDuration = durationValues[0]

  averageData.innerHTML = ''

  averageData.innerHTML = `
    <div id='head'>
      <div id='circle'>
      <div id='dataCircle'><span id='avgNum'>${averageEnergy.toFixed(5)}</span> kwh</div>
      <h3>Energy Consumed</h3>
      </div>
      <div id='circle'>
      <div id='dataCircle'><span id='avgNum'>${averageEmission.toFixed(5)}</span> Kg.Eq.CO2</div>
      <h3>Emissions Produced</h3>
      </div>
      <div id='circle'>
      <div id='dataCircle'><span id='avgNum'>${averageDuration.toFixed(2)}</span> Sec</div>
      <h3>Duration</h3>
      </div>
    </div>
  `;
}

//Run_id with respect to date and daterange
function displayRunIdByDate(date) {
  // Filter the data to find the 'run_id' for the selected date
  let run = data.find((d) => d.timestamp.split('T')[0] === date);
  
  // If a 'run_id' is found, display it
  if (run) {
    document.getElementById('runIdDisplay').textContent = 'Run ID: ' + run.run_id;
  } else {
    document.getElementById('runIdDisplay').textContent = 'No run found for this date';
  }
}

// Add an event listener for the 'dateSearch' form
document.getElementById('dateSearch').addEventListener('submit', function(e) {
  e.preventDefault();

  // Get the selected date
  let date = document.getElementById('date').value;

  // Display the 'run_id' for the selected date
  displayRunIdByDate(date);
});




