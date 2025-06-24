# Disease Spread Simulation

This is a Python-based Pygame simulation that models how a disease spreads through a population. This is determined based on the random movement of the people ("agents" in the simulation), as well as accounting for the factor of their socioeconomic status (based on data for India).

## Current Features

- The simulation simulates 100 people moving freely and randomly in a 2D space
- Agents can be:
  - **Healthy**
  - **Infected**
  - **Recovered** (immune from the disease)
  - **Dead**
- **30% of individuals are rich**, reducing their infection and death probabilities.
- The simulation also tracks the status of the infection through a visual medium as the colour of the agent
- There are real-time stats while the simulation is going on, and a summary when it is over (i.e. no one has the infection)
- Instructions and a restart option in game

## Controls

- `SPACE` — Start simulation
- `T` — Toggle stats
- Click **Restart** button after simulation ends to run again

## Visual Key

- **White** — Healthy  
- **Red** — Infected  
- **Blue** — Recovered  
- **Grey** — Dead  
- **Gold ring** — Agent is rich  

## Educational Angle

This simulation aligns with the theme _"An Imperfect World"_ by showcasing how health outcomes are influenced by inequality. Rich individuals have better survival odds, showing real-world differences in terms of access to healthcare.

## How to Run

1. Make sure [Python](python.org) 3.8+ is installed.
2. Install [Pygame](pygame.org) through the command prompt if not installed already:
   
   ```bash
   pip install pygame
   ```
3. Clone or download this repository
4. Navigate to the folder with DiseaseSpreadSim.py in your terminal
5. Run the simulation from the command prompt:
   
   ```bash
   python DiseaseSpreadSim.py
   ```

## Credits

**Agent Sprites** - Created with assistance from [ChatGPT](chat.openai.com), recoloured by me (Rishit Choudhary)
**Virus Icon** - By Freepik via [Flaticon](flaticon.com)
**Font** - Roboto from [Google Fonts](fonts.google.com)
**Code** - by me (Rishit Choudhary), partial documentation (adding comments and the like) by [ChatGPT](chat.openai.com)

## License

This project is licensed under the [MIT License](LICENSE)


**Made by Rishit Choudhary**
