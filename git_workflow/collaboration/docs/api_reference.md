# API Reference

## Inference API

**Endpoint:** `POST /infer`  
**Description:** Executes AI model inference.  

### **Request Format**

{
  "input": [0.1, 0.2, 0.3, 0.4]
}

### **Response Format**

{
  "status": "success",
  "result": [...],
  "message": "Inference completed successfully"
}
```json
