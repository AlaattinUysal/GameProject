import asyncio
import platform
from src.core.settings import screen, clock
from src.core.background import draw_background, update_sun_position
from src.effects.cloud import Cloud
from src.effects.bird import Bird

# Bulutlar listesi
clouds = [
    Cloud(100, 100, 0.4),
    Cloud(300, 180, 0.3),
    Cloud(180, 250, 0.5),
]

# Kuşlar listesi
birds = [
    Bird(100, 80, 0.5),
    Bird(300, 150, 0.6),
    Bird(500, 120, 0.4)
]

FPS = 60

async def main():
    running = True
    while running:
        draw_background(screen)

        for cloud in clouds:
            cloud.move()
            cloud.draw(screen)
        
        for bird in birds:
            bird.move()
            bird.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        update_sun_position()

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
