<div align="center">

# 🐝 SwarmPy

**An educational multi-agent orchestration framework built on OpenAI's Swarm — explore handoffs, routines, and agentic patterns**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat&logo=openai&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

> ⚠️ **Experimental & Educational** — built to explore ergonomic interfaces for multi-agent systems, not for production use.

</div>

---

SwarmPy is an educational framework for exploring multi-agent orchestration patterns. Based on OpenAI's Swarm, it showcases the handoff and routines patterns from the [Orchestrating Agents cookbook](https://cookbook.openai.com/examples/orchestrating_agents) — wrapped in a Streamlit UI for hands-on experimentation.

## ✨ Features

- **Agent handoffs** — transfer control between agents based on context
- **Routines** — define multi-step agent workflows
- **Swarm orchestration** — lightweight, ergonomic multi-agent coordination
- **Streamlit UI** — interactive interface for experimenting with agent flows
- **GPT-4 powered** — built on OpenAI's chat completions API

## 🚀 Quick Start

```bash
git clone https://github.com/RhythrosaLabs/swarmpy.git
cd swarmpy
pip install -r requirements.txt
# Set your OpenAI key
export OPENAI_API_KEY=your_key
streamlit run app.py
```

Or install the Swarm library directly:

```bash
pip install git+https://github.com/openai/swarm.git
```

```python
from swarm import Swarm, Agent

client = Swarm()
agent = Agent(name="Assistant", instructions="You are a helpful assistant.")
response = client.run(agent=agent, messages=[{"role": "user", "content": "Hello!"}])
print(response.messages[-1]["content"])
```

## 🛠️ Tech Stack

- **Python 3.10+** — core language
- **OpenAI / GPT-4** — LLM backbone
- **Swarm** — multi-agent orchestration
- **Streamlit** — interactive UI

## 🤝 Contributing

PRs welcome. Open an issue first for major changes.

## 📄 License

MIT

## 💛 Support

If SwarmPy helps you explore agentic AI patterns, consider supporting development:

👉 [Donate via PayPal](https://paypal.me/noodlebake) — @noodlebake

---
<div align="center">Made with ❤️ by <a href="https://github.com/RhythrosaLabs">RhythrosaLabs</a></div>
