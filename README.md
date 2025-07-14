<p align="center">
  <img src="https://www.novalad.ai/logo.svg" alt="Novalad Logo" width="500"/>
</p>

**Novalad** is an AI-powered platform that transforms chaotic, unstructured files—such as PDFs and PowerPoints—into beautifully organized, machine-readable data 💡. Designed for developers, data teams, and enterprises, Novalad efficiently handles complex layouts, tables, graphs, and multi-format data using a multi-model, map-reduce approach 🧩.

[View Novalad Extraction Result](https://www.novalad.ai/comparision.html)


---
[![Google Colab](https://img.shields.io/badge/Colab-Notebook-F9AB00?logo=google-colab&logoColor=white)](https://colab.research.google.com/gist/connectaman/92cbb44bcb17a474e32ce9c194effb97/novalad-demo.ipynb)
[![PyPI version](https://img.shields.io/pypi/v/novalad)](https://pypi.org/project/novalad/)
[![Python Version](https://img.shields.io/pypi/pyversions/novalad)](https://pypi.org/project/novalad/)
[![GitHub](https://img.shields.io/badge/GitHub-Repo-181717?logo=github&logoColor=white)](https://github.com/novaladai/novalad)
[![Website](https://img.shields.io/badge/Website-live-blue)](https://www.novalad.ai/)
[![Docs](https://img.shields.io/badge/Documentation-Online-brightgreen)](https://docs.novalad.ai)
[![API Docs](https://img.shields.io/badge/API-Reference-informational)](https://novalad.apidog.io/)
[![YouTube](https://img.shields.io/badge/Watch-Video-red?logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=aoiZqHQ4Um4)
[![License Apache](https://img.shields.io/badge/License-Apache%202.0-blue)](https://www.apache.org/licenses/LICENSE-2.0)
---

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [Importing and Initializing the Client](#importing-and-initializing-the-client)
  - [Uploading a File from Your Local System](#uploading-a-file-from-your-local-system)
  - [Processing a Document Directly from a URL](#processing-a-document-directly-from-a-url)
  - [Checking Job Status](#checking-job-status)
  - [Retrieving and Rendering Outputs](#retrieving-and-rendering-outputs)
    - [JSON Output](#json-output)
    - [Markdown Output](#markdown-output)
    - [LangChain Document Format Output](#langchain-document-format-output)
    - [Knowledge Graph Output](#knowledge-graph-output)
    - [Rendering the Outputs (Notebooks Only)](#rendering-the-outputs-notebooks-only)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Support](#support)

---

## Installation 🚀

Install the Novalad package using pip:

```bash
pip install novalad
```

---

## Usage 📚

1. **Generate API Key**:  
   Log in to [Novalad](https://app.novalad.ai) (https://app.novalad.ai) and generate your API key. Copy the key and keep it handy.

2. **Importing and Initializing the Client**  
   Begin by importing `NovaladClient` from the package and initializing it with your API key:
   You can set `NOVALAD_API_KEY` in env variable or pass it to Client

   ```python
   from novalad import NovaladClient

   # Initialize client with your API key
   client = NovaladClient(api_key="YOUR_API_KEY") # or set env NOVALAD_API_KEY 
   ```

### Uploading a File from Your Local System

If you have a file stored locally (e.g., a PDF document), specify its file path and use the `upload` method to send the file for processing.  
*Note: Only run this code if you are processing a local file. If your file is hosted online (via URL or cloud storage), skip this step.*

```python
# Define the path to your document
path = r"C:\path\to\your\document.pdf"

# Upload the file
client.upload(file_path=path)
```

After uploading your file, trigger the processing job using the `run` method:

```python
# Start processing the uploaded file
client.run()
```

<p align="center">OR</p>

### Processing a Document Directly from a URL

If your document is hosted online (such as in cloud storage or via a public URL), you can process it directly by passing its URL to the `run` method. This approach avoids the local upload step.

```python
# Process document directly by passing the file URL
client.run(
    url="https://d2uars7xkdmztq.cloudfront.net/app_resources/8049/documentation/91320_en.pdf"
)
```

Supported URL Types:
- HTTPS URLs
- AWS S3 pre-signed URLs
- GCP Storage Signed URLs
- Azure Blob HTTPS public URLs

### Checking Job Status

Monitor the status of your processing job by calling the `status` method. The job continues until the status is either `"success"` or `"failed"`:

```python
import time

while True:
    status = client.status()
    if status["status"] in ["success", "failed"]:
        break
    time.sleep(60)  # Check every 30 seconds
    print(".", end="")
print("\n", status)
```

### Retrieving and Rendering Outputs

After the job is complete, you can retrieve and render the results in various formats:

| Format                 | Description                                                                              |
|------------------------|------------------------------------------------------------------------------------------|
| **JSON** 🧾            | Raw layout and structured element data (ideal for developers)                            |
| **Markdown** 📘        | Clean, human-readable content for documentation and wikis                                |
| **Knowledge Graph** 🕸️ | Visual representation of semantic relations and entities                                 |
| **LangChain Docs** 🔗  | Plug-and-play format optimized for LLM pipelines                                           |

#### JSON Output

Retrieve the raw JSON response containing structured data, metadata, and extracted text:

```python
json_response = client.output(format="json")
print(json_response)
```

#### Markdown Output

Get a Markdown version of the output and render it using the `render_markdown` helper:

```python
markdown_output = client.output(format="markdown")
print(markdown_output)
```

#### LangChain Document Format Output

Retrieve the output as a structured document object for further processing:

```python
documents = client.output(format="document")
print(documents)
```

#### Knowledge Graph Output

Retrieve the relationships and entities within the document as a knowledge graph:

```python
kg_output = client.output(format="graph")
print(kg_output)
```

#### Rendering the Outputs (NOTEBOOK ONLY!!!)

IF YOU ARE USING JUPYTER NOTEBOOK/COLLAB/KAGGLE, YOU CAN RENDER OR VIEW THE OUTPUT FORMATS DIRECTLY IN YOUR NOTEBOOK CELLS


**Render JSON Output**:  
This code renders images displaying the PDF document page-wise with elements and layouts highlighted.  
*Note: You can also save the rendered images to a local directory by passing `save_dir=r"C:\path\to\save\visualization"` to the `render_elements` function.*

```python
from novalad import render_elements

render_elements(path, json_response)
# To save images locally:
# render_elements(path, json_response, save_dir=r"C:\path\to\save\visualization")
```
![Knowledge Graph](static/images/extraction_hightlight.png)


**Render Markdown Output**:

```python
from novalad import render_markdown

render_markdown(markdown_output)
```
![Knowledge Graph](static/images/extraction_markdown.png)

**Render Knowledge Graph**:

```python
from novalad import render_knowledge_graph

render_knowledge_graph(kg_output)
```
![Knowledge Graph](static/images/extraction_kg.png)


---



## Troubleshooting 🛠️

- **Job Failure**: Verify that your API key is correct and the file path is accessible. Review the status output for error messages.
- **File Path Issues**: Ensure the file path is correctly formatted (use raw strings for Windows paths).
- **URL Issues**: Confirm that the document URL is correct and publicly accessible.
- **API Key Problems**: Verify that your API key is active and valid. If authentication issues persist, please contact support.

for any issue please mail us at info@novalad.ai

---

## License 📄

This project is licensed under the [Apache License](LICENSE).

---


## Support 🙋‍♂️🙋‍♀️

For additional help or to report issues, please refer to the official documentation or contact support at [info@novalad.ai](mailto:info@novalad.ai)

---

<p align="center">Thank you for choosing Novalad! 🚀</p>

