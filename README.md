# Fun-with-Pathfind

Experiments with pathfinding algorithms

# Commands

Running the tests:

```python
pytest -q tests -vv
```

Running the sample:

```python
python3 src/main.py
```

# Plans

- [ ] Github Actions: format stage, isort stage, tests stage
- [ ] Add more tests to account for large-scale grids
- [ ] Github Actions: linters for Python and Markdown
- [ ] Perhaps generate grids with AI for easier testing
- [ ] Create a UI using the Pygame library or Javascript, where a user could input their own start, end, obstacles and grid size
- [ ] Add more algorithms like LPA* or Dijkstra's as options
- [ ] Add more obstacle and path types, each with different weights, to mimic real-life path search
- [ ] Add "characters" who change the weights for the path types, e.g. a hiker who goes through hills quicker than a generic person
- [ ] Add options for pathfinding for groups of people
- [ ] Add option to snapshot results in the UI
- [ ] Perhaps add character creation option in the UI
- [ ] Add zoom-in option to the UI
