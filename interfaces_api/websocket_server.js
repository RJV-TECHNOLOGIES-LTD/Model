const WebSocket = require("ws");
const grpc = require("@grpc/grpc-js");
const protoLoader = require("@grpc/proto-loader");

// Load gRPC service definition
const PROTO_PATH = __dirname + "/grpc_service.proto";
const packageDefinition = protoLoader.loadSync(PROTO_PATH);
const grpcService = grpc.loadPackageDefinition(packageDefinition).inference;

// Connect to gRPC server
const grpcClient = new grpcService.InferenceService(
  "localhost:50051",
  grpc.credentials.createInsecure()
);

// Start WebSocket server
const wss = new WebSocket.Server({ port: 8080 });

console.log("WebSocket Server running on port 8080");

wss.on("connection", (ws) => {
  console.log("New client connected");

  ws.on("message", (message) => {
    try {
      const requestData = JSON.parse(message);
      if (!requestData.input) {
        ws.send(JSON.stringify({ status: "error", message: "Missing 'input' field" }));
        return;
      }

      grpcClient.RunInference({ input: requestData.input }, (err, response) => {
        if (err) {
          console.error("gRPC Error:", err);
          ws.send(JSON.stringify({ status: "error", message: "Inference failed" }));
        } else {
          ws.send(JSON.stringify({ status: response.status, result: response.result }));
        }
      });
    } catch (error) {
      ws.send(JSON.stringify({ status: "error", message: "Invalid JSON format" }));
    }
  });

  ws.on("close", () => {
    console.log("Client disconnected");
  });
});
