# Autonomous Workflow Discovery & Meta-Agent System

## Overview
This system autonomously analyzes raw desktop activity logs to discover high-value repeating workflows and generates specialized AI agents to execute them.

## Prerequisites
- Python 3.11+
- [Optional] Gemini API Key (for Task 1.1 enrichment)

## Installation
1. `pip install -r requirements.txt`
2. `playwright install chromium`

## Execution Pipeline
1. **Task 1: Discovery**
   `python main_discovery.py`
   *Analyzes test_data.db and exports `outputs/discovered_workflows.json`*

2. **Task 2: Meta-Agent Factory**
   `python main_factory.py`
   *Constructs specialized "Brain" configurations in `agent_configs/`*

3. **Demonstration: Workforce Management**
   `python check_workforce.py`
   *Lists the discovered digital workforce.*

4. **Demonstration: Operational Agent Runner**
   `python main_agent_run.py`
   *Executes a discovered agent in simulation mode with full observability.*

## Documentation
Full architectural details and design justifications are available in `docs/SYSTEM_DESIGN_DOCUMENT.pdf`.