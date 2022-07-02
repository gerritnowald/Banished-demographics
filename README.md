# Banished demographics

Simulating the demographics of the city builder game Banished

![](https://github.com/gerritnowald/Banished-demographics/blob/main/population.png)

In [Banished](https://www.gog.com/de/game/banished) the player manages a small medieval village. While the beginning of the game heavily focuses on survival elements like food and firewood supply, another threat arises once the basic needs have been met: demographic change. The population ages and the village may die out if the younger generation does not replace the old quickly enough. But growing to fast might deplete the resources, which also leads to the downfall of the village.

Citizens only reproduce if they have homes for themselves. If new houses are built, couples move in and conceive children. If no houses are available, they stay with their parents and don't get children. Thus the growth of the population can be controlled by the amount of houses being built.

A common tip for beginners is to only build 1 house every in-game year in order to grow not too fast, while still maintaining a stable population growth. But at some point this approach is not sufficient anymore, because too many widows and widower are blocking the houses and the supply for new homes does not keep up with demand. Unfortunately the game does not provide a detailed statistic of the population's age distribution.

The aim of this project is to simulate the demographics of the game under the assumption that all needs for resources are met. Just like in the game, each citizen is simulated individually. The rules of the game are applied with the best knowledge of the author, while also trying to keep the logic as simple as possible.
