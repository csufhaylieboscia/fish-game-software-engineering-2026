import pygame
import os

Base_Dir = os.path.dirname(os.path.abspath(__file__))
Assets_Dir = os.path.join(Base_Dir, "assets")
FishSprite_Dir = os.path.join(Assets_Dir, "Sprites\FishSprites")

class Fish(pygame.sprite.Sprite):
    def __init__(self, name, imagePath, difficulty):
        super().__init__()

        self.name = name
        self.difficulty = difficulty
        self.imagePath = imagePath

    def displayFish(self, surface, screen_w, screen_h):

        fish_image_path = os.path.join(FishSprite_Dir, self.imagePath)
        self.image = pygame.image.load(fish_image_path).convert_alpha()
        tw, th = self.image.get_size()
        ratio = tw / th
        self.image = pygame.transform.scale(self.image, (150 * ratio, 150))

        self.rect = self.image.get_rect(center=(screen_w // 2, screen_h // 2))
        surface.blit(self.image, self.rect)
        
        #keep scale and ratio in case need to change size for full screen when swim
        #tw, th = self.image.get_size()
        #scale = self.tw / self.th

    def getDifficulty(self):
        return self.difficulty
    
    def getName(self):
        return self.name
    
fishObjectList = [
    Fish("axolotl","axolotl.png", 4),
    Fish("betafish","betafish.png", 3),
    Fish("blackfish","blackfish.png", 2),
    Fish("clownfish","clownfish.png", 3),
    Fish("flatfish","flatfish.png", 2),
    Fish("goldfish","goldfish.png", 1),
    Fish("greenfish","greenfish.png", 1),
    Fish("mossball","mossball.png", 1),
    Fish("octopus","octopus.png", 4),
    Fish("pirahna","pirhana.png", 4),
    Fish("plasticbag","plasticbag.png", 3),
    Fish("sea snail","seasnail.png", 1),
    Fish("Starfish","seastar.png", 4),
    Fish("shell","shell.png", 1),
]