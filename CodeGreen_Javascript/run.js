const { exec } = require('child_process');

const scriptPath = 'website.bat';  // Specify the path to your batch script

function startWebsite() {
  console.log('Starting website...');
  exec(scriptPath, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing script: ${error}`);
    } else {
      console.log('Website started successfully.');
    }
  });
}


startWebsite();
