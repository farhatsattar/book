const { spawn } = require('child_process');

console.log('Creating Docusaurus project...');

const child = spawn('npx', ['create-docusaurus@latest', 'ai-native-book', 'classic'], {
  stdio: ['pipe', 'pipe', 'pipe'],
  cwd: process.cwd()
});

// Send 'Enter' to select JavaScript (first option)
setTimeout(() => {
  child.stdin.write('\n'); // Press Enter to select JavaScript
  child.stdin.end();
}, 2000);

// Capture and display output
child.stdout.on('data', (data) => {
  console.log(data.toString());
});

child.stderr.on('data', (data) => {
  console.error(data.toString());
});

child.on('close', (code) => {
  console.log(`Child process exited with code ${code}`);
});