from abc import ABC, abstractmethod
from .genetics import GeneticCode
from models.animal_catalog import ANIMAL_CATALOG


class Animal(ABC):
    def __init__(self, species_key: str, age: int, genetic_code: GeneticCode):
        self.__species_key = species_key
        self.__age = age
        self.__genetic_code = genetic_code
        self.__health = 100
        self.__hunger = 0
        self.__happiness = 50
        self.__is_alive = True
        self.__data = ANIMAL_CATALOG.get(species_key, list(ANIMAL_CATALOG.values())[0])
        self.__rarity = self._calculate_rarity()
        self.__income_per_day = self._calculate_income()

    def _calculate_rarity(self) -> str:
        genes = self.__genetic_code.get_all_genes()
        rare_genes = 0
        total_genes = len(genes)

        if total_genes == 0:
            return "Обычное"

        for g in genes.values():
            genotype = g.genotype
            if len(genotype) >= 2 and genotype[0] == genotype[1] and genotype[0].isupper():
                rare_genes += 1

        ratio = rare_genes / total_genes
        if ratio >= 0.8:
            return "Легендарное"
        elif ratio >= 0.6:
            return "Эпическое"
        elif ratio >= 0.4:
            return "Редкое"
        elif ratio >= 0.2:
            return "Необычное"
        else:
            return "Обычное"

    def _calculate_income(self) -> int:
        rarity_income = {
            "Обычное": 100,
            "Необычное": 300,
            "Редкое": 1000,
            "Эпическое": 5000,
            "Легендарное": 25000
        }
        return rarity_income.get(self.__rarity, 100)

    @property
    def name(self) -> str:
        return self.__species_key

    @property
    def age(self) -> int:
        return self.__age

    @property
    def health(self) -> int:
        return self.__health

    @property
    def hunger(self) -> int:
        return self.__hunger

    @property
    def is_alive(self) -> bool:
        return self.__is_alive

    @property
    def genetic_code(self) -> GeneticCode:
        return self.__genetic_code

    @property
    def rarity(self) -> str:
        return self.__rarity

    @property
    def income_per_day(self) -> int:
        return self.__income_per_day

    @abstractmethod
    def make_sound(self) -> str:
        pass

    def get_species(self) -> str:
        return self.__species_key

    @abstractmethod
    def get_space_required(self) -> float:
        pass

    def feed(self, food_amount: int):
        if not self.__is_alive:
            raise ValueError("Нельзя покормить мёртвое животное")
        if food_amount < 0:
            raise ValueError("Количество еды не может быть отрицательным")
        self.__hunger = max(0, self.__hunger - food_amount)
        self.__health = min(100, self.__health + 5)

    def breed(self, other):
        if not self.__is_alive or not other.__is_alive:
            raise ValueError("Мёртвые животные не могут размножаться")
        if type(self) != type(other):
            raise ValueError(f"Нельзя скрестить {self.get_species()} и {other.get_species()}")
        if self.__age < 2 or other.__age < 2:
            raise ValueError("Животные должны быть старше 2 лет")
        offspring_genetics = self.__genetic_code.combine(other.__genetic_code)
        offspring_genetics.mutate_all()
        return self._create_offspring(offspring_genetics)

    @abstractmethod
    def _create_offspring(self, genetics: GeneticCode):
        pass

    def __str__(self):
        status = "жив" if self.__is_alive else "мёртв"
        return f"{self.__species_key} ({self.__age} лет, {status}, {self.__rarity})"


class ZooAnimal(Animal):
    def __init__(self, species_key: str, age: int, genetic_code: GeneticCode):
        super().__init__(species_key, age, genetic_code)

    def make_sound(self) -> str:
        return self._Animal__data.get("sound", "Звук животного")

    def get_space_required(self) -> float:
        return self._Animal__data.get("space", 50.0)

    def _create_offspring(self, genetics: GeneticCode):
        return ZooAnimal(self._Animal__species_key, 0, genetics)