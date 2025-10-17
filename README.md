# AI Flappy Bird

An AI-powered version of the classic **Flappy Bird** game built with **Python**, **Pygame**, and **NEAT (NeuroEvolution of Augmenting Topologies)**.  
In this project, a population of birds learns to play the game autonomously through **genetic algorithms** — evolving over generations to improve their gameplay!

---

## Features

- Flappy Bird clone built using **Pygame**
- AI agent trained with **NEAT**
- Birds evolve and improve their performance over time
- Visuals for real-time AI performance

---

## Tech Stack

- **Python 3.13.2**
- **Pygame** – Game rendering and physics
- **NEAT-Python** – Evolutionary neural network algorithm
- **OS** – File and path handling

---

## How It Works

The AI doesn’t rely on pre-defined rules — instead, it learns how to play:

1. Each bird has a **neural network** controlling its jump decisions.  
2. Birds receive inputs such as:
   - Birds current height
   - Height difference between the bird and the next top pipe
   - Height difference between the bird and the next bottom pipe
3. The **NEAT algorithm** evaluates their fitness using a fitness function.
