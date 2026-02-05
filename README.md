# MCF Chatbot – Civil Defense Assistant

## 📌 Project Overview
This project is an AI-powered chatbot built using public information from **Myndigheten för civilt försvar (MCF)**.  
The goal is to make civil defense and crisis preparedness information easier to understand and more accessible for the general public.

The chatbot uses **Retrieval-Augmented Generation (RAG)** to answer questions based on real, up-to-date content from MCF’s website.

---

## 🎯 Purpose
- Help users understand civil defense and crisis preparedness
- Provide clear, summarized answers instead of long policy texts
- Practice AI engineering in a real-world scenario using agile teamwork

---

## 🧠 Key Features
- Chat interface for asking questions about civil defense
- Answers based on real MCF content (RAG)
- Source references to original pages

---

## 🏗️ Tech Stack
- **Backend:** Python, FastAPI  
- **Frontend:** Streamlit  
- **AI:** LLM + embeddings (RAG)  
- **Vector Database:** LanceCb
- **Deployment:** Docker & Azure  
- **Version Control:** GitHub (branches, pull requests, Kanban)

---

## 📄 Data & Ethics
- Only publicly available information is used
- `robots.txt` is respected
- No personal data is collected or stored
- Content is summarized, not reproduced verbatim
- This project is for educational purposes only and is not affiliated with MCF

---

## 👥 Team & Workflow
- 3 developers working with agile methodology
- Kanban board with issues and pull requests
- Code reviews before merging to `main`

---

## 🚀🚀 Deployment
The application is containerized with Docker and deployed to Azure.

---

## 📢 Disclaimer
This project is created for educational purposes as part of an AI engineering course.

## 📸 Screenshots and description

**Web scraping and data collection:**
The project begins with a web crawler that scrapes MSB's privatpersoner_hemberedskap web pages. Each page is saved as structured data in JSON format.

<img width="366" height="521" alt="Skärmbild 2026-02-05 101843" src="https://github.com/user-attachments/assets/879c924f-ac16-40b8-a610-79143e7e45e6" />

**Data Ingestion**
We now run the ingestion.py, that takes in the ingestion_raw_content that splits the text into chunks, creates MCFContent-object and saves the data, in the vector database.



<img width="661" height="822" alt="Skärmbild 2026-02-05 105940" src="https://github.com/user-attachments/assets/41651c8b-80d2-47be-af45-3db0c206a807" />



<img width="622" height="584" alt="Skärmbild 2026-02-05 102926" src="https://github.com/user-attachments/assets/9614c91a-0ed4-4d01-8635-464b1155fb28" />



When we decide to take in the LanceModel (MCFContent) the embedding is taken care of with gemini text-embedding004.


<img width="820" height="824" alt="Skärmbild 2026-02-05 105954" src="https://github.com/user-attachments/assets/3839b93f-4a18-4f5a-9c37-1000ebcfdfa2" />


**The knowledge base has been created**
Once the ingetsion.py has doing its work, a knowledge base is created if not existed, with the original data from the web scraper but now transformed and vectorized.
content being split into chunks and embeddings.


<img width="645" height="583" alt="Skärmbild 2026-02-05 103947" src="https://github.com/user-attachments/assets/3944cae4-18b9-4a8c-953a-08a201d4422d" />



<img width="386" height="92" alt="Skärmbild 2026-02-05 105917" src="https://github.com/user-attachments/assets/4960a687-fb07-4742-8edf-e872a8429e7d" />


**The Rag-agent**
Once we have our vectorized/embedded the data we can now tell our rag-agent to search for information in the knowledge base to answer questions from the user.

we use a system prompt to explain what we are requesting from the agent, and how it should work and answering the questions.


<img width="898" height="978" alt="Skärmbild 2026-02-05 110438" src="https://github.com/user-attachments/assets/40900332-fbb2-4853-b627-67c337848c9c" />




**The final product**
Everyting is put togheter in Streamlit UI, an interface where the users can chat with our agent and get an answer back. When a question is being asked a get-request is being sent to our FastAPI, and serves with an answer post-request. 

<img width="818" height="950" alt="Skärmbild 2026-02-05 135521" src="https://github.com/user-attachments/assets/e03cee21-01c6-49dd-8935-3293567d2f19" />


We also have FAQ (frequently asked questions) this questions you see in the picture is default question being hard coded until there is enough questions asked that can replace these questions, with the once most asked.
<img width="2852" height="1555" alt="Skarmbild_2026-02-04_165247" src="https://github.com/user-attachments/assets/c25ea384-13ae-433c-8584-30989bfcf910" />

Here is the FAQ-handler that logs all the questions being asked, and stores them in a json data folder (Dict). We have functions that can get the top questions being asked and countsunique questions, total questions and most common.


<img width="1173" height="989" alt="Skärmbild 2026-02-05 140451" src="https://github.com/user-attachments/assets/91baa4b9-9dff-4394-b733-d8407a25e3fd" />





<img width="1456" height="809" alt="Skärmbild 2026-02-05 140520" src="https://github.com/user-attachments/assets/8399824a-35ab-48e9-8cfb-29a736baaedc" />




We also have a function that makes it possible to see locations of nerby shelters. We have downloaded a gpkg file that mapping out nearby shelters based on lat/lon.


<img width="1391" height="802" alt="Skärmbild 2026-02-05 145416" src="https://github.com/user-attachments/assets/308d7a84-7f85-4ac7-b74e-5e7901a2ca7e" />



<img width="2858" height="1565" alt="Skärmbild 2026-02-05 145519" src="https://github.com/user-attachments/assets/186953f7-fbef-4c6e-a6ea-7010ccd7f028" />



