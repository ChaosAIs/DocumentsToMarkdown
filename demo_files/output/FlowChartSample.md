<!-- Converted from image: FlowChartSample.png -->
<!-- Conversion method: AI Vision (OpenAI gpt-4o) -->
<!-- Original file: C:\MyWorkplace\DocumentsToMarkdown\DocumentsToMarkdown\demo_files\FlowChartSample.png -->

```
      ┌────────┐
      │  Start │
      └───┬────┘
          ↓
   ┌────────────┐
   │ Upload File│
   └───┬────────┘
       ↓
 ┌───────────────┐
 │ Are you logged│
 │     in?       │
 └───┬─────┬─────┘
     ↓     ↓
   Yes     No
     │     │
     │     ↓
     │ ┌───────────────┐
     │ │ Do you have an│
     │ │   account?    │
     │ └───┬─────┬─────┘
     │     ↓     ↓
     │   Yes     No
     │     │     │
     │     │     ↓
     │     │ ┌───────────────┐
     │     │ │ Create an     │
     │     │ │   account     │
     │     │ └───────────────┘
     │     ↓
     │ ┌─────────────────────┐
     │ │ Enter username and  │
     │ │     password        │
     │ └─────────┬───────────┘
     ↓           ↓
┌───────────────┐
│ Choose file to│
│    upload     │
└──────┬────────┘
       ↓
 ┌───────────────┐
 │ All info.     │
 │ submitted     │
 │ correctly?    │
 └───┬─────┬─────┘
     ↓     ↓
   Yes     No
     │     │
     │     ↓
     │ ┌───────────────┐
     │ │   Try Again   │
     │ └───────────────┘
     ↓
┌─────────────────────┐
│ File uploaded       │
│ successfully        │
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│ Save the file       │
│ on server           │
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│ Save file info      │
│ on database         │
└─────────────────────┘
```