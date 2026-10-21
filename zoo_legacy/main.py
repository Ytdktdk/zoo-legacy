"""Главный файл приложения - тестирование ООП"""
from models.genetics import Gene, GeneticCode
from models.animal import Lion, Tiger


def main():
    print("=== Тестирование генетической системы ===\n")
    coat_color = Gene("Окрас", "A", "a")
    size = Gene("Размер", "B", "b")
    lion_genetics = GeneticCode()
    lion_genetics.add_gene(coat_color)
    lion_genetics.add_gene(size)
    tiger_genetics = GeneticCode()
    tiger_coat = Gene("Окрас", "A", "a")
    tiger_size = Gene("Размер", "B", "b")
    tiger_genetics.add_gene(tiger_coat)
    tiger_genetics.add_gene(tiger_size)
    simba = Lion("Симба", 5, lion_genetics)
    tigress = Tiger("Тигрица", 3, tiger_genetics)
    print(f"Создано животное: {simba}")
    print(f"Звук: {simba.make_sound()}")
    print(f"Требуемая площадь: {simba.get_space_required()} кв.м")
    print(f"Генетический код: {simba.genetic_code}")
    print(f"\nСоздано животное: {tigress}")
    print(f"Звук: {tigress.make_sound()}")
    print(f"Требуемая площадь: {tigress.get_space_required()} кв.м")
    print("\n=== Тестирование кормления ===")
    simba.feed(50)
    print(f"Здоровье {simba.name}: {simba.health}%")
    print(f"Голод {simba.name}: {simba.hunger}%")
    print("\n=== Тестирование скрещивания ===")
    try:
        nala_genetics = GeneticCode()
        nala_coat = Gene("Окрас", "A", "a")
        nala_size = Gene("Размер", "B", "b")
        nala_genetics.add_gene(nala_coat)
        nala_genetics.add_gene(nala_size)
        nala = Lion("Нала", 4, nala_genetics)
        cub = simba.breed(nala)
        print(f"Потомство получено: {cub}")
        print(f"Генетический код потомка: {cub.genetic_code}")
    except ValueError as e:
        print(f"Ошибка скрещивания: {e}")
    print("\n=== Тестирование ошибки скрещивания ===")
    try:
        simba.breed(tigress)
    except ValueError as e:
        print(f"Правильно поймана ошибка: {e}")


if __name__ == "__main__":
    main()
