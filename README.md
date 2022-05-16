## Orchestrator
Orchestration service implemented using websockets.

Client example:
```
const socket = new WebSocket('ws://localhost:9090');
 
socket.addEventListener('open', function (event) {
    credentials = { 'pub_key': '%key%' };
    socket.send(JSON.stringify(credentials));
});

socket.addEventListener('message', function (event) {
    console.log(event.data);
});
```