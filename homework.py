"""
Импортирование библиотек.

Из библиотеки typing ипортировались:
- Dict (словари)
- Type (Поддержка выполнения аннотации типов)
- ClassVar (Конструкция специального типа для обозначения переменных класса)

Из библиотеки dataclasses ипортировались:
- dataclass (Декоратор и функции для автоматического
             добавления сгенерированных специальных методов)
- asdict (Преобразует экземпляр класса данных в словарь dict)
"""
from typing import Dict, Type, ClassVar, List
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """
    Класс для создания объектов сообщений.

    Вывод сообщения о тренировки.

    Переменные класса:
    - training_type(Имя класса тренировки)
    - duration (Длительность в часах)
    - distance (Дистанция в километрах)
    - speed (Средняя скорость в км/ч)
    - calories (Израсх. киллокалории)
    """

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message_output: str = ('Тип тренировки: {training_type}; '
                           'Длительность: {duration:.3f} ч.; '
                           'Дистанция: {distance:.3f} км; '
                           'Ср. скорость: {speed:.3f} км/ч; '
                           'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Метод возвращает строку сообщения."""
        return self.message_output.format(**asdict(self))


@dataclass
class Training:
    """
    Базовый класс тренировки.

    Входные перменные:
    - action (Кол-во действий)
    - duration (Длительность в часах)
    - weight (вес спортсмена)

    Константы класса:
    LEN_STEP - Дистанция за один шаг/гребок.
    M_IN_KM - Константа для перевода километров в метры.
    TOTTALLY_MINUTES_IN_HOURS - Константа для перевода минут в часы.
    """

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[float] = 1000
    TOTTALLY_MINUTES_IN_HOURS: ClassVar[float] = 60

    action: int         # Кол-во действий
    duration: float     # Длительность (в часах)
    weight: float       # Вес спортсмена

    def get_distance(self) -> float:
        """Возвращает дистанцию в км, которую преодолел спортсмен."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения спротсмена."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            """Подклассы должны реализовывать
                метод get_spent_calories"""
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_RUN_1: ClassVar[int] = 18
    COEFF_CALORIE_RUN_2: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CALORIE_RUN_1
                 * self.get_mean_speed()
                 - self.COEFF_CALORIE_RUN_2)
                * self.weight
                / self.M_IN_KM
                * self.duration
                * self.TOTTALLY_MINUTES_IN_HOURS)


@dataclass
class SportsWalking(Training):
    """
    Тренировка: спортивная ходьба.

    Входные перменные:
    - action (Кол-во действий)
    - duration (Длительность в часах)
    - weight (вес спортсмена)

    Дополнительая переменная
    - height (рост спортсмена).
    """

    COEFF_CALORIE_WALK_1: ClassVar[float] = 0.035
    COEFF_CALORIE_WALK_2: ClassVar[float] = 0.029
    COEFF_CALORIE_WALK_3: ClassVar[int] = 2

    action: int
    duration: float
    weight: float
    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CALORIE_WALK_1
                 * self.weight
                + (self.get_mean_speed()
                   ** self.COEFF_CALORIE_WALK_3
                   // self.height)
                * self.COEFF_CALORIE_WALK_2
                * self.weight)
                * self.duration
                * self.TOTTALLY_MINUTES_IN_HOURS
                )


@dataclass
class Swimming(Training):
    """
    Тренировка: плавание.

    Входные перменные:
    - action (Кол-во действий)
    - duration (Длительность в часах)
    - weight (вес спортсмена)

    Дополнительные переменные:
    - length_pool (длина бассейна).
    - count_pool (количество переплытий бассейна).

    Переопределенная переменная:
    - LEN_STEP - один гребок

    Переопределенные методы:
    - get_spent_calories() - расчет калорий
    - get_mean_speed() - средняя скорость
    """

    LEN_STEP: ClassVar[float] = 1.38
    COEFF_CALORIE_SWIM_1: ClassVar[float] = 1.1
    COEFF_CALORIE_SWIM_2: ClassVar[int] = 2

    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed()
                 + self.COEFF_CALORIE_SWIM_1)
                * self.COEFF_CALORIE_SWIM_2
                * self.weight)


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_code: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    try:
        return workout_code[workout_type](*data)
    except KeyError:
        return ('Такой тренировки нет!')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
