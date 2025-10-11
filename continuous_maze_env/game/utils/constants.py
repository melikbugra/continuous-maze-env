DOWNSCALE = 1

PLAYER_SIZE = 28 // DOWNSCALE
INTERVAL = 1 / 60.0
PLAYER_SPEED = 4000 // DOWNSCALE
WINDOW_WIDTH = 800 // DOWNSCALE
WINDOW_HEIGHT = 600 // DOWNSCALE
GRID_SIZE = 40 // DOWNSCALE
RENDER_SCALE = DOWNSCALE

# Physics safety: maximum pixels the player can move per collision check.
# Higher speed values will be internally subdivided into micro-steps to avoid
# skipping through thin walls (tunneling) when PLAYER_SPEED is large.
PHYSICS_MAX_PIXEL_STEP = max(2, GRID_SIZE // 4)

# Simulation acceleration: how many physics updates to process per env.step call.
# Increasing this will make episodes complete faster (in agent steps and wall-clock),
# while still keeping each physics update small and stable thanks to the micro-steps above.
SIMULATION_UPDATES_PER_STEP = 8
